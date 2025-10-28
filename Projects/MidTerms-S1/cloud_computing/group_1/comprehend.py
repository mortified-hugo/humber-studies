from flask import Flask, render_template, request
import os
import boto3

app = Flask(__name__)

# Initialize AWS Comprehend client
comprehend = boto3.client('comprehend', region_name='us-east-1')

def do_analysis(text, analysis_type):
    """Analyze text using Amazon Comprehend"""
    try:
        # Detect language first
        lang_response = comprehend.detect_dominant_language(Text=text)
        language_code = lang_response['Languages'][0]['LanguageCode']
        
        if analysis_type == 'sentiment':
            response = comprehend.detect_sentiment(Text=text, LanguageCode=language_code)
            return f"{response['Sentiment']} (Positive: {response['SentimentScore']['Positive']:.2f}, Negative: {response['SentimentScore']['Negative']:.2f})"
        
        elif analysis_type == 'entities':
            response = comprehend.detect_entities(Text=text, LanguageCode=language_code)
            entities = [f"{e['Text']} ({e['Type']})" for e in response['Entities'][:5]]
            return ', '.join(entities) if entities else 'No entities found'
        
        elif analysis_type == 'keyphrases':
            response = comprehend.detect_key_phrases(Text=text, LanguageCode=language_code)
            phrases = [p['Text'] for p in response['KeyPhrases'][:5]]
            return ', '.join(phrases) if phrases else 'No key phrases found'
        
        else:
            return 'Invalid analysis type'
            
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/', methods=['GET', 'POST'])
def main():
    input_text = ''
    analysis_type = ''
    result = ''
    
    if request.method == 'POST':
        input_text = request.form.get("input_text", '')
        analysis_type = request.form.get("analysis_type", '')
        
        if input_text and analysis_type:
            result = do_analysis(input_text, analysis_type)
    
    return render_template("index.html", input=input_text, analysis_type=analysis_type, result=result)

# Run the app
if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8081)), debug=True)
