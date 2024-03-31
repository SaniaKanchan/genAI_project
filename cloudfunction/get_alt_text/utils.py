import urllib
from google.cloud import storage
import os
import urllib.request
import urllib.error
import vertexai
from vertexai.generative_models import GenerativeModel, Part

def generate_text(image_bucket_url: str, project_id: str, location: str) -> None:
    # Initialize Vertex AI
    vertexai.init(project=project_id, location=location)

    # Load the model
    model = GenerativeModel(model_name="gemini-pro-vision")

    # Load example image
    #image_url = "gs://accesibility-image-bucket/im2text.jpg"
    image_content = Part.from_uri(image_bucket_url, "image/jpeg")

    # Query the model
    response = model.generate_content([image_content, "what is this image?"])
    print(response)

    return response.text


def download_image_from_url(image_url: str):
    pic2_path='pic2.jpg'
    if os.path.exists(pic2_path):
       os.remove(pic2_path)
       print("Deleted previous image")
    # pic_url = "https://www.maggi.in/sites/default/files/maggi_logo_png_0.png"
    pic_url = image_url
    # Add a user-agent header to mimic a regular web browser request
    req = urllib.request.Request(pic_url, headers={'User-Agent': 'Mozilla/5.0'})

    try:
        with urllib.request.urlopen(req) as response:
            if response.status != 200:
                print("Error:", response.status, response.reason)
            else:
                with open('pic2.jpg', 'wb') as handle:
                    while True:
                        block = response.read(1024)
                        if not block:
                            break
                        handle.write(block)
        print("Image downloaded successfully!")
    except urllib.error.HTTPError as e:
        print("HTTP Error:", e.code, e.reason)
    except urllib.error.URLError as e:
        print("URL Error:", e.reason)


def store_in_cloud():
    # Initialize a Cloud Storage client
    client = storage.Client()

    # Define the bucket name and image file name in Cloud Storage
    bucket_name = 'accesibility-image-bucket'  # Replace 'your-bucket-name' with your actual bucket name
    image_file_name = 'image.jpg'  # Replace 'image.jpg' with the name you want to give to your image in GCS

    # Get the bucket where you want to store the image
    bucket = client.bucket(bucket_name)
    
    # Specify the local path to the image file you want to upload
    local_image_path = 'pic2.jpg'  # Replace 'path/to/your/local/image.jpg' with the actual path
    
    # Upload the image file to Cloud Storage
    blob = bucket.blob(image_file_name)
    if blob.exists():
        blob.delete()
    
    blob.upload_from_filename(local_image_path)

    print(f"Image {image_file_name} uploaded to bucket {bucket_name}.")

