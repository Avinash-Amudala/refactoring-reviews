import sqlite3

import requests

import openai
import logging

def analyze_code_with_chatgpt(code_snippet, api_key):
    """
    Send a code snippet to ChatGPT for analysis using the chat endpoint.

    Parameters:
    code_snippet (str): The code snippet to analyze.
    api_key (str): Your OpenAI API key.

    Returns:
    dict: The response from ChatGPT.
    """
    openai.api_key = api_key
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-1106-preview",
            messages=[
                {
                    "role": "system",
                    "content": f"Review this code for refactoring opportunities:\n```\n{code_snippet}\n```"
                },
                {
                    "role": "user",
                    "content": "Please provide feedback on the code snippet above."
                }
            ],
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        chatgpt_feedback = response['choices'][0]['message']['content']
        return chatgpt_feedback
    except Exception as e:
        logging.error(f"Error in ChatGPT API call: {e}")
        return 'Analysis failed due to an error'

def extract_snippets_from_db(db_path):
    """
    Extract code snippets from an SQLite database.

    Parameters:
    db_path (str): Path to the SQLite database file.

    Returns:
    list: A list of code snippets.
    """
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute("SELECT snippet FROM snippets")
    snippets = [row[0] for row in cursor.fetchall()]
    connection.close()
    return snippets

