from flask import Flask, render_template, request, jsonify, send_file
import boto3
from botocore.exceptions import BotoCoreError, ClientError
import os
from datetime import datetime
import io

app = Flask(__name__)

# Initialize AWS Polly client
polly_client = boto3.client('polly', region_name='us-east-1')

# Create a directory for audio files if it doesn't exist
AUDIO_DIR = 'audio_files'
if not os.path.exists(AUDIO_DIR):
    os.makedirs(AUDIO_DIR)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/synthesize', methods=['POST'])
def synthesize_speech():
    try:
        # Get text from request
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Optional parameters
        voice_id = data.get('voice', 'Joanna')  # Default voice
        output_format = data.get('format', 'mp3')
        
        # Call AWS Polly
        response = polly_client.synthesize_speech(
            Text=text,
            OutputFormat=output_format,
            VoiceId=voice_id,
            Engine='neural'  # Use neural engine for better quality
        )
        
        # Get audio stream
        if "AudioStream" in response:
            # Read the audio stream
            audio_stream = response['AudioStream'].read()
            
            # Save to file with timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'speech_{timestamp}.{output_format}'
            filepath = os.path.join(AUDIO_DIR, filename)
            
            with open(filepath, 'wb') as file:
                file.write(audio_stream)
            
            return jsonify({
                'success': True,
                'message': 'Speech synthesized successfully',
                'audio_url': f'/audio/{filename}'
            })
        else:
            return jsonify({'error': 'No audio stream in response'}), 500
            
    except (BotoCoreError, ClientError) as error:
        return jsonify({'error': f'AWS Error: {str(error)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Server Error: {str(e)}'}), 500

@app.route('/audio/<filename>')
def serve_audio(filename):
    try:
        filepath = os.path.join(AUDIO_DIR, filename)
        return send_file(filepath, mimetype='audio/mpeg')
    except Exception as e:
        return jsonify({'error': f'File not found: {str(e)}'}), 404

@app.route('/voices', methods=['GET'])
def get_voices():
    """Get list of available voices from Polly"""
    try:
        response = polly_client.describe_voices()
        voices = [
            {
                'id': voice['Id'],
                'name': voice['Name'],
                'language': voice['LanguageCode'],
                'gender': voice['Gender']
            }
            for voice in response['Voices']
        ]
        return jsonify({'voices': voices})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Run on all interfaces for Cloud9 accessibility
    app.run(host='0.0.0.0', port=8080, debug=True)
