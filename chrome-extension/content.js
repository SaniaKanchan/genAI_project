import {MediaRecorder, register} from 'extendable-media-recorder';
import {connect as connectEncoder} from 'extendable-media-recorder-wav-encoder';

let mediaRecorder = null;
let audioBlobs = [];
let capturedStream = null;
let isRecording = false;
let imageUrl = null;

async function connectToEncoder() {
    await register(await connectEncoder());
}
connectToEncoder();

// Register the extendable-media-recorder-wav-encoder

// Starts recording audio
function startRecording() {

  return navigator.mediaDevices.getUserMedia({
    audio: {
      echoCancellation: true,
    }
  }).then(stream => {
      audioBlobs = [];
      capturedStream = stream;

      // Use the extended MediaRecorder library
      mediaRecorder = new MediaRecorder(stream, {
        mimeType: 'audio/wav'
      });

      // Add audio blobs while recording 
      mediaRecorder.addEventListener('dataavailable', event => {
        audioBlobs.push(event.data);
      });

      mediaRecorder.start();
      isRecording = true;

  }).catch((e) => {
    console.error(e);
  });
}
function sendBlob(audioBlob) {
    if (audioBlob) {
        console.log("AudioBLOBBBB", audioBlob)
        fetch('https://us-central1-accesibilityimagereader.cloudfunctions.net/audio_processing', {
            method: 'POST',
            headers: {
                'Content-Type': 'audio/wav', // Set appropriate Content-Type header
            },
            body: audioBlob,
        })
        .then(response => response.json())
        .then(data => {
            // Set alt attribute to the received alt text
            console.log(data.alt_text);
            // image.alt = data.alt_text || "No alt text available";
            // // Remove the event listener to prevent further generation
            // image.removeEventListener('mouseenter', altTextGenerationHandler);
            mediaRecorder.stop();
        })
        .catch(error => {
            console.error('Error fetching alt text:', error);
        });
    }
} 
function stopRecording() {
    return new Promise(resolve => {
        if (!mediaRecorder) {
          resolve(null);
          return;
        }
        
        mediaRecorder.addEventListener('stop', () => {
          const mimeType = mediaRecorder.mimeType;
          const audioBlob = new Blob(audioBlobs, { type: mimeType });
    
          if (capturedStream) {
            capturedStream.getTracks().forEach(track => track.stop());
          }
    
          resolve(audioBlob);
        });
        
        mediaRecorder.stop();
        isRecording = false;
      });
  }


function handleKeyEvents(event) {
    if (event.key === 'a') {
        if (!isRecording) {
            console.log("Start recording");
            console.log(imageUrl)
            startRecording()
            }
        else {
            console.log("Stop recording");
            stopRecording().then(sendBlob);
        }
    }
}
document.addEventListener('mouseover', function(event) {
    // Check if the mouseover event target is an image element and the specific key has been pressed
    if (event.target.tagName.toLowerCase() === 'img') {
        // Retrieve information about the image element
        imageUrl = event.target.src;
        // Display image information to the user (replace with your preferred method)
        console.log('Image URL:', imageUrl);
    }
});

document.addEventListener('keydown', handleKeyEvents);

function handleAltTextGeneration(image) {
    // Set alt attribute to "hello"
    fetch('https://us-central1-accesibilityimagereader.cloudfunctions.net/get_alt_text', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            image_url: image.src // Use image_url key
        })
    })
    .then(response => response.json())
    .then(data => {
        // Set alt attribute to the received alt text
        image.alt = data.alt_text || "No alt text available";
        // Remove the event listener to prevent further generation
        image.removeEventListener('mouseenter', altTextGenerationHandler);
    })
    .catch(error => {
        console.error('Error fetching alt text:', error);
    });
}

// Event handler for alt text generation
function altTextGenerationHandler(event) {
    const image = event.target;
    // Check if alt attribute is already set
    if (!image.alt) {
        handleAltTextGeneration(image);
    }
}

// Attach event listener to each image
var images = document.getElementsByTagName('img');
for (var i = 0, l = images.length; i < l; i++) {
    images[i].addEventListener('mouseenter', altTextGenerationHandler);
}
