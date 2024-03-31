import urllib
from google.cloud import storage
import os
import urllib.request
import urllib.error
import vertexai
from vertexai.generative_models import GenerativeModel, Part
from google.api_core.client_options import ClientOptions
from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech
from google.cloud import texttospeech
from pydub import AudioSegment
import base64
from io import BytesIO

def query_image(question:str ,image_bucket_url: str, project_id: str, location: str) -> None:
    # Initialize Vertex AI
    vertexai.init(project=project_id, location=location)

    # Load the model
    model = GenerativeModel(model_name="gemini-pro-vision")

    image_content = Part.from_uri(image_bucket_url, "image/jpeg")

    # Query the model
    response = model.generate_content([image_content, question])
    print(response)

    return response.text


def transcribe_chirp(
    project_id: str,
    audio_blob: bytes,
):
    """Transcribe an audio file using Chirp."""
    # Instantiates a client
   
    client = SpeechClient(
        client_options=ClientOptions(
            api_endpoint="us-central1-speech.googleapis.com",
        )
    )

    # Reads a file as bytes
    # with open(audio_file, "rb") as f:
    #     content = f.read()

    config = cloud_speech.RecognitionConfig(
        auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
        language_codes=["en-US"],
        model="chirp",
    )

    audio = cloud_speech.RecognitionAudio(content=audio_blob)

    request = cloud_speech.RecognizeRequest(
        recognizer=f"projects/{project_id}/locations/us-central1/recognizers/_",
        config=config,
        audio=audio
        # content=content,
    )


    # Transcribes the audio into text
    response = client.recognize(request=request)
  

    for result in response.results:
        print(f"Transcript: {result.alternatives[0].transcript}")

    return response

def synthesize_speech(text, output_filename):

    # Create a Text-to-Speech client

    client = texttospeech.TextToSpeechClient()

    # Set the text input
    input_text = texttospeech.SynthesisInput(text=text)

    # Configure the voice settings
    voice = texttospeech.VoiceSelectionParams(
    language_code="en-US",
    ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    )
    # Set the audio configuration
    audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request
    response = client.synthesize_speech(
    input=input_text, voice=voice, audio_config=audio_config
    )

    # Save the audio to a file
    with open("output.mp3", 'wb') as out:
        out.write(response.audio_content)
        print(f"Audio content written to '{output_filename}'")
    

def convert_blob_to_mp3(audio_blob):
    # Convert the WAV audio blob to AudioSegment
    audio_segment = AudioSegment.from_wav(io.BytesIO(audio_blob))

    # Export the AudioSegment to MP3 format
    mp3_data = io.BytesIO()
    audio_segment.export(mp3_data, format='mp3')

    # Get the MP3 data as bytes
    mp3_bytes = mp3_data.getvalue()
    return mp3_bytes