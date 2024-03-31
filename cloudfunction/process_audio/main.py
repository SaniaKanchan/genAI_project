import functions_framework
from flask import Request, jsonify
from google.cloud import speech_v1p1beta1 as speech
import base64
from utils import *

@functions_framework.http
def process_audio(request: Request):
    """HTTP Cloud Function to process audio input.
    Args:
        request (flask.Request): The request object containing audio data.
    Returns:
        A JSON response containing the processed MP3 audio data.
    """
    if request.method == 'OPTIONS':
        # Handle preflight requests
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return '', 204, headers

    # Get the audio data from the request
    if request.is_json:
        request_json = request.get_json()
        audio_blob_base64 = request_json.get('audio_blob', '')
    else:
        audio_blob_base64 = request.data.decode('utf-8')

    if not audio_blob_base64:
        return 'Error: No audio data provided', 400
    
    response=""
    try:
        # Decode the base64-encoded audio data
       
        audio_blob = base64.b64decode(audio_blob_base64)
    
        # Convert audio Blob to an AudioSegment (assuming it's in WAV format)
        audio_segment = AudioSegment.from_wav(audio_blob)
        # Export the AudioSegment to an MP3 file
        mp3_data = audio_segment.export(format='mp3')
        mp3_data = convert_blob_to_mp3(request.data)
        # Encode the MP3 data as base64 for transmission
        alt_text = final(request.data)
        # Return the processed MP3 audio data as a JSON response
        response = jsonify({'alt_text': alt_text})
        headers = {"Access-Control-Allow-Origin": "*"}
        return response, 200, headers
    except Exception as e:
        print(response)
        return response, 480


def final(audio):
  project_id = 'accesibilityimagereader'
  location = 'us-central1'

  speech2text = transcribe_chirp(project_id, audio)

  transcript = speech2text.results[0].alternatives[0].transcript

  response = query_image(transcript,bucket_image_url, project_id, location)

  return synthesize_speech(response, "output.mp3"), 400
  # return response 
