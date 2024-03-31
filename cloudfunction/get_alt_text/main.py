import functions_framework
from flask import Request, jsonify
from cloudfunction.get_alt_text.utils import *

@functions_framework.http
def generate_alt_text(request: Request):
    """HTTP Cloud Function to generate alt text for images.
    Args:
        request (flask.Request): The request object.
    Returns:
        A JSON response containing alt texts for the images.
    """
    request_json = request.get_json(silent=True)

    if request.method == 'OPTIONS':
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }

        return ('', 204, headers)
    
    if not request_json or 'image_url' not in request_json:
        return 'Error: No image URLs provided in JSON payload', 400

    
    
    image_url = request_json['image_url']

    # Generate alt texts for the images
    alt_text = generate_alt_text_for_image(image_url)

    # Return JSON response with alt texts
    response = jsonify({'alt_text': alt_text})
    headers = {"Access-Control-Allow-Origin": "*"}
    return (response, 200, headers)

def generate_alt_text_for_image(image_url: str) -> str:
    """Generate alt text for a single image URL."""
    # Replace this function with your logic to generate alt text for the image
    # For demonstration purposes, let's assume alt text is just the image URL
    bucket_image_url = "gs://accesibility-image-bucket/image.jpg"
    # download_image_from_url(image_url)
    # store_in_cloud()
    # project_id = 'accesibilityimagereader'
    # location = 'us-central1'
    # text = generate_text(bucket_image_url, project_id, location)
    return image_url