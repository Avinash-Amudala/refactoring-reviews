import os
import json
import logging
from time import time
from flask import Flask, render_template, jsonify, request, redirect, url_for
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from celery import Celery
from joblib import dump, load

# Import custom modules
from combined_analysis import combined_analysis
from data_preprocessing import load_data, preprocess_data
from model_training import train_model, evaluate_model
from chatgpt_integration import analyze_code_with_chatgpt, extract_snippets_from_db
from plot_service import generate_confusion_matrix_plot

# Global variable for start time
start_time_of_analysis = None

# Setup basic logging
logging.basicConfig(level=logging.INFO)
app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_analysis', methods=['GET', 'POST'])
def start_analysis():
    global start_time_of_analysis

    if request.method == 'POST':
        start_time_of_analysis = time()  # Set start time when analysis begins

        combined_df = pd.concat([load_data('OnlyNonTrivial_dt.csv'), load_data('OnlyTrivial_dt.csv')])
        y = combined_df['refactoring']
        X = combined_df.drop('refactoring', axis=1).select_dtypes(include=[np.number])
        X_preprocessed = preprocess_data(X)

        X_train, X_test, y_train, y_test = train_test_split(X_preprocessed, y, test_size=0.2, random_state=42)

        scaler = StandardScaler()
        scaler.fit(X_train)
        X_train_scaled = scaler.transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        model = train_model(X_train_scaled, y_train)
        evaluate_model(model, X_test_scaled, y_test)

        model_filename = 'trained_model.joblib'
        scaler_filename = 'scaler.joblib'
        dump(model, model_filename)
        dump(scaler, scaler_filename)

        analyze_and_plot.delay(X_test_scaled.tolist(), model_filename, scaler_filename)

        return redirect(url_for('results'))

    return render_template('index.html')

@app.route('/results')
def results():
    return render_template('results.html')

@app.route('/analysis_results')
def analysis_results():
    analysis_complete = check_analysis_complete()
    results_data = get_analysis_results() if analysis_complete else {}

    # Adjust the graph path to be relative to the static directory
    graph_path = url_for('static', filename='confusion_matrix.png') if analysis_complete else ''

    return jsonify({
        'status': 'complete' if analysis_complete else 'in progress',
        'results': results_data.get('html_results', ''),
        'graph_path': graph_path
    })

@celery.task
def analyze_and_plot(X_test_scaled_list, model_filename, scaler_filename):
    X_test_scaled = np.array(X_test_scaled_list)
    model = load(model_filename)
    scaler = load(scaler_filename)

    api_key = "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"
    db_path = "snippets-dev.db"
    code_snippets = extract_snippets_from_db(db_path)

    combined_results = pd.DataFrame(columns=['Snippet', 'ModelPrediction', 'ChatGPTFeedback'])

    for index, code_snippet in enumerate(code_snippets[:10]):
        if index < len(X_test_scaled):
            try:
                if not code_snippet.strip():  # Skip empty snippets
                    continue
                model_prediction = model.predict([X_test_scaled[index]])[0]
                chatgpt_feedback = analyze_code_with_chatgpt(code_snippet, api_key)
                combined_results.loc[index] = [code_snippet, model_prediction, chatgpt_feedback]
            except Exception as e:
                logging.error(f"Error processing snippet at index {index}: {e}")

    combined_results['ChatGPTLabel'] = combined_results['ChatGPTFeedback'].apply(process_chatgpt_response)

    graph_path = generate_confusion_matrix_plot(combined_results['ModelPrediction'], combined_results['ChatGPTLabel'])
    save_analysis_results(combined_results, graph_path)

def process_chatgpt_response(response):
    keywords_indicating_refactoring = [
        'improve', 'refactor', 'restructure', 'optimize', 'enhance',
        'clean up', 'modify', 'change', 'revise', 'adjust'
    ]
    return 1 if any(keyword in response.lower() for keyword in keywords_indicating_refactoring) else 0

def check_analysis_complete():
    global start_time_of_analysis
    return os.path.exists('analysis_complete.txt') and os.path.getmtime('analysis_complete.txt') > start_time_of_analysis

def get_analysis_results():
    if os.path.exists('analysis_results.json'):
        with open('analysis_results.json', 'r') as file:
            return json.load(file)
    return {}

def save_analysis_results(combined_results, graph_path):
    results_data = {
        'html_results': combined_results.to_html(classes='data', header="true"),
        'graph_path': graph_path
    }
    with open('analysis_results.json', 'w') as file:
        json.dump(results_data, file)
    # Create a file to indicate analysis completion
    with open('analysis_complete.txt', 'w') as file:
        file.write('complete')

if __name__ == "__main__":
    app.run(debug=False)

