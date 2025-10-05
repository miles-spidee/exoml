const express = require('express');
const cors = require('cors');
const fs = require('fs').promises;
const { exec } = require('child_process');
const path = require('path');

const app = express();
const PORT = 3001;

app.use(cors());
app.use(express.json());

app.post('/api/analyze', async (req, res) => {
  try {
    const inputData = req.body;
    console.log('Received data for analysis:', inputData);

    // 1. Write input data to input.json
    const inputPath = path.join(__dirname, 'input.json');
    await fs.writeFile(inputPath, JSON.stringify(inputData, null, 2));
    console.log('Data written to input.json');

    // 2. Execute the curl command
    const curlCommand = `curl -X 'POST' 'http://127.0.0.1:8000/predict' -H 'Content-Type: application/json' -d '@input.json' > formatted_result.json`;
    
    await new Promise((resolve, reject) => {
      exec(curlCommand, { cwd: __dirname }, (error, stdout, stderr) => {
        if (error) {
          console.error('Error executing curl command:', error);
          reject(error);
          return;
        }
        console.log('Curl command executed successfully');
        resolve();
      });
    });

    // 3. Read the result from formatted_result.json
    const resultPath = path.join(__dirname, 'formatted_result.json');
    
    // Wait a moment for the file to be written
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    const resultData = await fs.readFile(resultPath, 'utf8');
    const parsedResult = JSON.parse(resultData);

    console.log('Analysis completed, sending results');
    res.json({
      success: true,
      result: parsedResult,
      message: 'Analysis completed successfully'
    });

  } catch (error) {
    console.error('Error in analysis workflow:', error);
    res.status(500).json({
      success: false,
      error: error.message,
      message: 'Error during analysis'
    });
  }
});

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'Backend server is running' });
});

app.listen(PORT, () => {
  console.log(`Backend server running on http://localhost:${PORT}`);
});