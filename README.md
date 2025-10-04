# Exoplanet AI Hunter 🔭

An AI-powered web application to detect potential exoplanets from transit survey data. This project, developed for the NASA Space Apps Challenge, uses a machine learning model trained on NASA's open-source Kepler dataset to classify celestial objects as exoplanet candidates or false positives through a user-friendly interface.

---

## ✨ Features

* **AI-Powered Predictions:** Utilizes a highly accurate Gradient Boosting model trained on thousands of data points from the Kepler mission.
* **Interactive Web Interface:** A clean UI built with React to input stellar and planetary parameters for real-time classification.
* **FastAPI Backend:** A high-performance, asynchronous backend server to handle predictions efficiently.
* **Modular & Scalable:** A well-organized project structure that's easy to understand and extend.
* **Easy to Run:** A straightforward setup process to get the application running locally.

---

## 🛠️ Tech Stack

* **Backend:** 🐍 Python, 🚀 FastAPI
* **Machine Learning:** 🧠 Scikit-learn, Pandas, Joblib
* **Frontend:** ⚛️ React.js (using Vite)
* **Server:** 🦄 Uvicorn

---

## 📂 Project Structure

The project is organized into a clean and modular structure:

exoplanet-hackathon/
│
├── backend/
│   ├── app/            # Main FastAPI application source
│   ├── models/         # Saved .pkl files for the ML model and scaler
│   └── requirements.txt  # Python dependencies
│
├── frontend/
│   ├── src/            # React application source
│   └── package.json    # Frontend dependencies
│
├── data/
│   └── kepler.csv      # The dataset used for training
│
├── train_model.py      # Script to train the ML model
└── README.md           # You are here!


---

## 🚀 Getting Started

Follow these instructions to get the project set up and running on your local machine.

### **Prerequisites**

* **Python** (3.8 or newer)
* **Node.js** and **npm** (v16 or newer)

### **Installation & Setup**

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd exoplanet-hackathon
    ```

2.  **Set up the Backend:**
    ```bash
    cd backend
    pip install -r requirements.txt
    ```

3.  **Set up the Frontend:**
    ```bash
    cd ../frontend
    npm install
    ```

---

## 🏃‍♀️ How to Run the Application

The application requires three main steps to run: training the model, starting the backend server, and starting the frontend server.

### **1. Train the Machine Learning Model**

First, you need to run the training script. This will process the data from the `data/` folder and save the trained model files (`.pkl`) to the `backend/models/` directory.

* From the **root directory** (`exoplanet-hackathon/`), run:
    ```bash
    python train_model.py
    ```

### **2. Start the Backend API Server**

Once the model is trained, start the FastAPI server.

* Navigate to the **backend directory** and run Uvicorn:
    ```bash
    cd backend
    uvicorn app.main:app --reload
    ```
* The API will be live at `http://127.0.0.1:8000`. You can see the interactive API documentation at `http://127.0.0.1:8000/docs`.

### **3. Start the Frontend Development Server**

Finally, in a **new terminal window**, start the React application.

* Navigate to the **frontend directory** and run the dev server:
    ```bash
    cd frontend
    npm run dev
    ```
* The application will be available in your browser at `http://localhost:5173` (or another port if 5173 is busy).

---

## 🧪 API Usage

You can interact with the API directly using tools like `curl` or the auto-generated docs.

### **Endpoint: `/predict`**

* **Method:** `POST`
* **Description:** Predicts if a celestial object is an exoplanet candidate.
* **Request Body:** A JSON object with the following keys.

    ```json
    {
      "koi_period": 84.6,
      "koi_duration": 4.5,
      "koi_depth": 87.5,
      "koi_prad": 2.7,
      "koi_teq": 350,
      "koi_insol": 9.4,
      "koi_steff": 5800
    }
    ```

* **Success Response:**

    ```json
    {
      "prediction": "Exoplanet Candidate"
    }
    ```

### **Example `curl` Request**

```bash
curl -X 'POST' \
  '[http://127.0.0.1:8000/predict](http://127.0.0.1:8000/predict)' \
  -H 'Content-Type: application/json' \
  -d '{
        "koi_period": 84.6,
        "koi_duration": 4.5,
        "koi_depth": 87.5,
        "koi_prad": 2.7,
        "koi_teq": 350,
        "koi_insol": 9.4,
        "koi_steff": 5800
      }'

🙏 Acknowledgments

    This project utilizes open-source data provided by the NASA Exoplanet Archive.

    Built for the NASA International Space Apps Challenge 2025.