const express = require('express');
const cors = require('cors');
const fs = require('fs').promises;
const { exec } = require('child_process');
const path = require('path');
const util = require('util');
const http = require('http');

const app = express();
const PORT = 3001;
const execAsync = util.promisify(exec);

// Middleware
app.use(cors());
app.use(express.json());

// New: request logger and CORS preflight handling
app.use((req, res, next) => {
  console.log(`[${new Date().toISOString()}] ${req.method} ${req.originalUrl} from ${req.ip}`);
  // limit header logging size to avoid huge outputs
  try { console.log('Headers:', JSON.stringify(req.headers)); } catch(e) { console.log('Headers: <unserializable>'); }
  next();
});
app.options('*', cors());

// --- NEW: very early, permissive probes to avoid 404s ---
// Accept any HTTP method and always return JSON (and plain text) for common probes.
// Placed early so probes won't hit other middleware/routes that could 404.
app.all(['/health', '/api/health'], (req, res) => {
  console.log(`PROBE ${req.method} ${req.originalUrl} from ${req.ip}`);
  const payload = {
    status: 'OK',
    message: 'Backend health check',
    path: req.originalUrl,
    method: req.method,
    timestamp: new Date().toISOString()
  };
  // Always return JSON and also a short plain-text for curl/browser quick-checks
  if (req.headers.accept && req.headers.accept.includes('text/plain')) {
    res.type('text').send(`OK - ${payload.path}`);
  } else {
    res.json(payload);
  }
});

// Provide a simple routes probe that always responds (any method)
app.all('/api/routes', (req, res) => {
  try {
    const routeList = [];
    app._router.stack.forEach((middleware) => {
      if (middleware.route) {
        const methods = Object.keys(middleware.route.methods).map(m => m.toUpperCase()).join(',');
        routeList.push({ methods, path: middleware.route.path });
      } else if (middleware.name === 'router' && middleware.handle && middleware.handle.stack) {
        middleware.handle.stack.forEach((handler) => {
          if (handler.route) {
            const methods = Object.keys(handler.route.methods).map(m => m.toUpperCase()).join(',');
            routeList.push({ methods, path: handler.route.path });
          }
        });
      }
    });
    res.json({ success: true, routes: routeList });
  } catch (err) {
    res.status(500).json({ success: false, error: 'Could not enumerate routes', details: err.message });
  }
});

// Health check endpoint
app.all('/api/health', (req, res) => {
  console.log('ANY /api/health requested from', req.ip, 'method:', req.method);
  res.json({ status: 'OK', message: 'Backend health check', timestamp: new Date().toISOString(), method: req.method });
});

// Model health check endpoint
app.get('/api/model-health', async (req, res) => {
  try {
    console.log('Testing ML model connectivity...');
    
    // Test basic connectivity
    const testCommand = 'curl -s -o /dev/null -w "%{http_code}" --connect-timeout 5 http://127.0.0.1:8000/';
    const { stdout, stderr } = await execAsync(testCommand);
    
    console.log('ML model connectivity test - HTTP code:', stdout);
    console.log('ML model connectivity test - stderr:', stderr);
    
    if (stdout.trim() === '200') {
      res.json({ 
        status: 'OK', 
        message: 'ML model server is accessible',
        httpCode: stdout.trim()
      });
    } else {
      res.status(503).json({ 
        status: 'ERROR', 
        message: 'ML model server not accessible',
        httpCode: stdout.trim(),
        stderr: stderr
      });
    }
  } catch (error) {
    console.error('ML model health check failed:', error);
    res.status(503).json({
      status: 'ERROR',
      message: 'Cannot connect to ML model server',
      error: error.message
    });
  }
});

// Prediction endpoint
app.post('/api/predict', async (req, res) => {
  try {
    console.log('=== PREDICTION REQUEST START ===');
    console.log('Request body:', JSON.stringify(req.body, null, 2));
    console.log('Request headers:', req.headers);
    
    // Validate input data
    const requiredFields = ['koi_period', 'koi_duration', 'koi_depth', 'koi_prad', 'koi_teq', 'koi_insol', 'koi_steff'];
    for (const field of requiredFields) {
      if (!(field in req.body) || isNaN(req.body[field])) {
        return res.status(400).json({ success: false, error: `Invalid or missing field: ${field}` });
      }
    }

    // 1. Write input data to input.json in the exoplanet directory
    const inputPath = path.join(__dirname, '..', 'exoplanet', 'input.json');
    console.log('Writing input to:', inputPath);
    
    const bodyString = JSON.stringify(req.body, null, 2);
    await fs.writeFile(inputPath, bodyString);
    console.log('✓ Input data written successfully');

    // 2. Send request to ML model using Node http to avoid shell/curl issues
    console.log('Sending request to ML model at http://127.0.0.1:8000/predict');

    const requestToModel = () => new Promise((resolve, reject) => {
      const options = {
        hostname: '127.0.0.1',
        port: 8000,
        path: '/predict',
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Content-Length': Buffer.byteLength(bodyString)
        },
        timeout: 60000
      };

      const reqModel = http.request(options, (resModel) => {
        let data = '';
        resModel.on('data', chunk => data += chunk);
        resModel.on('end', () => {
          resolve({ statusCode: resModel.statusCode, body: data });
        });
      });

      reqModel.on('error', (err) => {
        reject(err);
      });

      reqModel.on('timeout', () => {
        reqModel.destroy(new Error('Model request timed out'));
      });

      reqModel.write(bodyString);
      reqModel.end();
    });

    let modelResponse;
    try {
      modelResponse = await requestToModel();
    } catch (modelErr) {
      console.error('Error contacting ML model:', modelErr);
      return res.status(502).json({
        success: false,
        error: 'Cannot contact ML model server on 127.0.0.1:8000',
        details: modelErr.message
      });
    }

    console.log('Model response statusCode:', modelResponse.statusCode);
    console.log('Model response length:', (modelResponse.body || '').length);
    console.log('Model response preview:', (modelResponse.body || '').substring(0, 500));

    if (modelResponse.statusCode !== 200) {
      // save raw response for debugging
      const debugPath = path.join(__dirname, 'debug_response.txt');
      await fs.writeFile(debugPath, modelResponse.body || '');
      return res.status(502).json({
        success: false,
        error: `ML model returned HTTP ${modelResponse.statusCode}`,
        raw: (modelResponse.body || '').substring(0, 200),
        debugPath
      });
    }

    // 3. Parse the model response (must be JSON)
    let parsedResult;
    try {
      parsedResult = JSON.parse(modelResponse.body);
    } catch (parseError) {
      const resultPath = path.join(__dirname, '..', 'exoplanet', 'formatted_result.json');
      await fs.writeFile(resultPath, modelResponse.body || '');
      console.error('Error parsing model JSON:', parseError);
      return res.status(502).json({
        success: false,
        error: 'ML model returned invalid JSON',
        parseError: parseError.message,
        resultPreview: (modelResponse.body || '').substring(0, 200),
        resultPath
      });
    }

    // 4. Save formatted result
    const resultPath = path.join(__dirname, '..', 'exoplanet', 'formatted_result.json');
    await fs.writeFile(resultPath, JSON.stringify(parsedResult, null, 2));
    console.log('✓ Formatted result saved to:', resultPath);

    console.log('=== PREDICTION REQUEST COMPLETE ===');
    return res.json({
      success: true,
      input: req.body,
      result: parsedResult,
      debug: {
        inputPath,
        resultPath,
        responseLength: (modelResponse.body || '').length
      }
    });

  } catch (error) {
    console.error('=== PREDICTION ERROR ===');
    console.error('Error message:', error.message);
    console.error('Error stack:', error.stack);
    console.error('=== END ERROR ===');
    
    return res.status(500).json({
      success: false,
      error: error.message,
      details: error.stack,
      timestamp: new Date().toISOString()
    });
  }
});

// Ensure a simple root endpoint (useful for probes)
app.get('/', (req, res) => {
  console.log('GET / requested from', req.ip, 'headers:', req.headers);
  res.json({ status: 'OK', message: 'Backend root - server is running', timestamp: new Date().toISOString() });
});

// Also support legacy /health path probes
app.get('/health', (req, res) => {
  console.log('GET /health requested from', req.ip);
  res.json({ status: 'OK', message: 'Backend health check', timestamp: new Date().toISOString() });
});

// Add diagnostic endpoint to list registered routes at runtime
app.get('/api/routes', (req, res) => {
  try {
    const routeList = [];
    app._router.stack.forEach((middleware) => {
      if (middleware.route) {
        const methods = Object.keys(middleware.route.methods).map(m => m.toUpperCase()).join(',');
        routeList.push({ methods, path: middleware.route.path });
      } else if (middleware.name === 'router' && middleware.handle && middleware.handle.stack) {
        middleware.handle.stack.forEach((handler) => {
          if (handler.route) {
            const methods = Object.keys(handler.route.methods).map(m => m.toUpperCase()).join(',');
            routeList.push({ methods, path: handler.route.path });
          }
        });
      }
    });
    res.json({ success: true, routes: routeList });
  } catch (err) {
    res.status(500).json({ success: false, error: 'Could not enumerate routes', details: err.message });
  }
});

// Catch-all: always return JSON on unknown routes to avoid HTML/plain 404 responses
app.use((req, res) => {
  console.warn(`Unhandled route requested: ${req.method} ${req.originalUrl} from ${req.ip}`);
  res.status(404).json({
    success: false,
    error: 'Not Found',
    path: req.originalUrl,
    method: req.method,
    timestamp: new Date().toISOString()
  });
});

// New: global error handler to return JSON for uncaught errors
app.use((err, req, res, next) => {
  console.error('Unhandled error:', err && err.stack ? err.stack : err);
  if (res.headersSent) return next(err);
  res.status(500).json({
    success: false,
    error: err && err.message ? err.message : 'Internal Server Error',
    timestamp: new Date().toISOString()
  });
});

app.listen(PORT, () => {
  console.log(`Backend server running on http://localhost:${PORT}`);
  console.log('Available endpoints:');
  console.log('  GET  /api/health - Backend health check');
  console.log('  GET  /api/model-health - ML model connectivity test');
  console.log('  POST /api/predict - Make predictions');

  // New: list registered routes for verification
  try {
    const routeList = [];
    app._router.stack.forEach((middleware) => {
      if (middleware.route) {
        // routes registered directly on the app
        const methods = Object.keys(middleware.route.methods).map(m => m.toUpperCase()).join(',');
        routeList.push(`${methods} ${middleware.route.path}`);
      } else if (middleware.name === 'router' && middleware.handle && middleware.handle.stack) {
        // router middleware 
        middleware.handle.stack.forEach((handler) => {
          if (handler.route) {
            const methods = Object.keys(handler.route.methods).map(m => m.toUpperCase()).join(',');
            routeList.push(`${methods} ${handler.route.path}`);
          }
        });
      }
    });
    console.log('Registered routes:\n' + routeList.join('\n'));
  } catch (err) {
    console.warn('Could not enumerate routes:', err);
  }

  console.log('Process PID:', process.pid);
});
