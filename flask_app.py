from flask import Flask, request, jsonify
import os
from textblob import TextBlob

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Perform sentiment analysis
    with open(file_path, 'r') as f:
        text = f.read()
        sentiment = analyze_sentiment(text)

    return jsonify({'filename': file.filename, 'sentiment': sentiment})

def analyze_sentiment(text):
    tb = TextBlob(text)
    polarity = round(tb.polarity, 2)
    subjectivity = round(tb.subjectivity, 2)
    sentiment = 'Positive' if polarity > 0.05 else 'Neutral' if polarity <= 0.05 and polarity >=-0.05 else 'Negative'
    return {
        'polarity': polarity,
        'subjectivity': subjectivity,
        'sentiment': sentiment
    }

if __name__ == '__main__':
    app.run(debug=True)
