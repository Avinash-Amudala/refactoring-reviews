from chatgpt_integration import analyze_code_with_chatgpt

import re

def extract_features_from_snippet(code_snippet):
    # Hypothetical features - replace with actual features used in your model
    features = []

    # Example features based on the content of the code snippet
    features.append(len(code_snippet))  # Total length of the snippet
    features.append(code_snippet.count('\n'))  # Number of line breaks
    features.append(code_snippet.count(' '))  # Number of spaces
    features.append(len(code_snippet.split()))  # Number of words
    features.append(code_snippet.count('if'))  # Number of 'if' statements
    features.append(code_snippet.count('for'))  # Number of 'for' loops
    features.append(code_snippet.count('while'))  # Number of 'while' loops
    features.append(code_snippet.count('def'))  # Number of function definitions
    features.append(code_snippet.count('class'))  # Number of class definitions
    features.append(code_snippet.count('import'))  # Number of imports
    features.append(len(re.findall(r'\bprint\b', code_snippet)))  # Number of 'print' statements
    features.append(len(re.findall(r'#[^!]', code_snippet)))  # Number of comments (excluding shebang)
    features.append(len(re.findall(r'def ', code_snippet)))  # Number of function definitions (alternative method)
    features.append(len(re.findall(r'\breturn\b', code_snippet)))  # Number of 'return' keywords
    features.append(len(re.findall(r'\bTrue\b|\bFalse\b', code_snippet)))  # Number of boolean literals
    features.append(len(re.findall(r'\bNone\b', code_snippet)))  # Number of 'None' literals
    features.append(len(re.findall(r'\bexcept\b', code_snippet)))  # Number of 'except' keywords
    features.append(len(re.findall(r'\btry\b', code_snippet)))  # Number of 'try' keywords
    features.append(len(re.findall(r'\bwith\b', code_snippet)))  # Number of 'with' keywords
    features.append(len(re.findall(r'\bas\b', code_snippet)))  # Number of 'as' keywords
    features.append(len(re.findall(r'\bfrom\b', code_snippet)))  # Number of 'from' keywords
    features.append(len(re.findall(r'\bimport\b', code_snippet)))  # Number of 'import' keywords
    features.append(len(re.findall(r'\bglobal\b', code_snippet)))  # Number of 'global' keywords
    features.append(len(re.findall(r'\bnonlocal\b', code_snippet)))  # Number of 'nonlocal' keywords
    features.append(len(re.findall(r'\blambda\b', code_snippet)))  # Number of 'lambda' expressions
    features.append(len(re.findall(r'\basync\b', code_snippet)))  # Number of 'async' keywords
    features.append(len(re.findall(r'\bawait\b', code_snippet)))  # Number of 'await' keywords
    features.append(len(re.findall(r'\braise\b', code_snippet)))  # Number of 'raise' keywords
    features.append(len(re.findall(r'\byield\b', code_snippet)))  # Number of 'yield' keywords
    features.append(len(re.findall(r'\bpass\b', code_snippet)))  # Number of 'pass' keywords
    features.append(len(re.findall(r'\bbreak\b', code_snippet)))  # Number of 'break' keywords
    features.append(len(re.findall(r'\bcontinue\b', code_snippet)))  # Number of 'continue' keywords
    features.append(len(re.findall(r'\bdel\b', code_snippet)))  # Number of 'del' keywords
    features.append(len(re.findall(r'\bin\b', code_snippet)))  # Number of 'in' keywords
    features.append(len(re.findall(r'\bis\b', code_snippet)))  # Number of 'is' keywords
    features.append(len(re.findall(r'\bnot\b', code_snippet)))  # Number of 'not' keywords
    features.append(len(re.findall(r'\band\b', code_snippet)))  # Number of 'and' keywords
    features.append(len(re.findall(r'\bor\b', code_snippet)))  # Number of 'or' keywords
    features.append(len(re.findall(r'\bif\b', code_snippet)))  # Number of 'if' keywords
    features.append(len(re.findall(r'\belse\b', code_snippet)))  # Number of 'else' keywords
    features.append(len(re.findall(r'\belif\b', code_snippet)))  # Number of 'elif' keywords
    features.append(len(re.findall(r'\bassert\b', code_snippet)))  # Number of 'assert' keywords
    features.append(len(re.findall(r'\bimport\b', code_snippet)))  # Number of 'import' keywords
    features.append(len(re.findall(r'\bfrom\b', code_snippet)))  # Number of 'from' keywords
    features.append(len(re.findall(r'\bclass\b', code_snippet)))  # Number of 'class' keywords
    features.append(len(re.findall(r'\bdef\b', code_snippet)))  # Number of 'def' keywords
    features.append(len(re.findall(r'\bself\b', code_snippet)))  # Number of 'self' references

    # You can add additional features based on your specific requirements
    while len(features) < 49:
        features.append(0)  # Adding dummy features to match the expected count

    return features

def combined_analysis(code_snippet, model, scaler, api_key):
    # Extract features for the model
    model_features = extract_features_from_snippet(code_snippet)

    # Check if the number of features is correct
    if len(model_features) != 49:
        raise ValueError(f"Expected 49 features, but got {len(model_features)} features")

    # Scale features
    scaled_features = scaler.transform([model_features])

    # Get model's prediction
    model_prediction = model.predict(scaled_features)

    # Get ChatGPT's analysis
    chatgpt_analysis = analyze_code_with_chatgpt(code_snippet, api_key)

    # Extract ChatGPT feedback from the response
    chatgpt_feedback = chatgpt_analysis.get('choices', [{}])[0].get('message', {}).get('content', 'Analysis not available.')

    # Combine results
    combined_result = {
        "model_prediction": model_prediction[0],
        "chatgpt_feedback": chatgpt_feedback
    }

    return combined_result


