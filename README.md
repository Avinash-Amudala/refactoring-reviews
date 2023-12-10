
# Refactoring Tool User Guide

## Introduction
This guide provides instructions on how to set up and use the refactoring tool developed as part of the SWEN.777 - Software Quality Assurance project. The tool leverages the ChatGPT API and a Random Forest classifier to enhance code quality in refactoring changes.

## Prerequisites
- Python 3.x
- Pip (Python package manager)
- Redis server
- Joblib 
- Sklearn 
- Pandas 
- Numpy 
- Matplotlib & Seaborn (for plotting)
- Internet connection for ChatGPT API

## Setting Up the Dataset
Before running the application, you need to set up the dataset used for analysis. This project utilizes a specific dataset named OnlyNonTrivial_dt.csv, which is essential for the functionality of the system.

1. **Download the Dataset:**
Visit the Kaggle dataset page at https://www.kaggle.com/datasets/amalsalilan/code-metrics-dataset-softwareprojectstructure/
Download the OnlyNonTrivial_dt.csv file.
2. **Place the Dataset in the Project:**
Once downloaded, place the OnlyNonTrivial_dt.csv file in the root directory of the project. This is important as the application expects the dataset to be located here.
In main.py, The code snippet combined_df = pd.concat([load_data('OnlyNonTrivial_dt.csv')]) in the project scripts will read this dataset for processing. Ensuring the file is in the correct location is crucial for the proper execution of the application.
3. **Kaggle Dataset:**
      Since the database file is too large for GitHub, download the test DB snippets from https://www.kaggle.com/datasets/simiotic/github-code-snippets-development-sample/data.

## Setup Instructions

1. **Clone the Repository**
   Clone the project repository to your local machine using Git:
   ```
   git clone [Repository URL]
   ```

2. **Install Dependencies**
   Navigate to the project directory and install the required Python packages:
   ```
   cd [Project Directory]
   pip install -r requirements.txt
   ```

3. **Redis Server**
   Ensure that you have Redis server installed and running on your machine. If not, download and install Redis from [https://redis.io/download](https://redis.io/download).
   Start the Redis server:
   ```
   redis-server
   ```

4. **API Key Configuration**
   In the `main.py` file, replace the placeholder for the API key with your actual ChatGPT API key:
   ```python
   api_key = "YOUR_API_KEY_HERE"
   ```
   Ensure that the key is valid to allow the tool to interact with ChatGPT.

5. **Running the Application**
   Start the Flask application:
   ```
   python main.py
   ```
6. Celery Worker:
   In a separate terminal, run to start the Celery worker.
   ```
   celery -A main.celery worker
   ```
6. **Accessing the Tool**
   Once the application is running, open a web browser and navigate to `http://localhost:5000` to access the refactoring tool.

## Using the Tool

1. **Uploading Code Snippets**
   - Use the web interface to upload code snippets.
   - You can also use the provided sample dataset from Kaggle for testing: [Kaggle Dataset](https://www.kaggle.com/datasets/simiotic/github-code-snippets-development-sample/data).

2. **Review Process**
   - The tool will use the Random Forest classifier and ChatGPT API to analyze the refactoring quality of the code snippets.
   - Wait for the analysis to complete.

3. **Viewing Results**
   - The tool will display the results, including any recommendations for refactoring and insights from ChatGPT.

## Troubleshooting

- If you encounter any issues with the Redis server, ensure it's properly installed and running.
- Check your API key if the ChatGPT integration fails.

## Conclusion
This tool aims to streamline the code refactoring process by providing an automated way to assess and improve code quality. Your feedback and contributions are welcome to enhance its capabilities further.
