// Get access to the camera
async function initCamera() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'user' } });
        const video = document.getElementById('video');
        video.srcObject = stream;
    } catch (err) {
        console.error('Error accessing the camera: ', err);
    }
}

// Capture the current frame from the camera and send it to the endpoint
async function captureAndSend() {
    const canvas = document.createElement('canvas');
    const video = document.getElementById('video');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Convert the canvas content to a Blob
    canvas.toBlob(async function(blob) {
        const formData = new FormData();
        formData.append('image', blob, 'image.jpg'); // Append the Blob as 'image.jpg'

        try {
            const response = await fetch('https://7f84-42-60-104-146.ngrok-free.app/analyze', {
                method: 'POST',
                body: formData
            });
            if (response.ok) {
                const data = await response.json();
                console.log('Image sent successfully!')
                console.log('Data received:', data)
                if (data.person_detected) {
                    if (data.posture_description == true) {
                        document.getElementById("message").innerHTML = "Good posture, keep it up!"
                        document.body.style.backgroundColor = "greenyellow"
                    }
                    else {
                        document.getElementById("message").innerHTML = "Please sit upright!"
                        document.body.style.backgroundColor = "red"
                    }
                }
                else {
                    document.getElementById("message").innerHTML = "No person detected"
                    document.body.style.backgroundColor = "orange"
                }

                
                // alert('Image sent successfully! Posture: ' + data.posture_description);
            } else {
                alert('Failed to send image.');
            }
        } catch (err) {
            console.error('Error sending image: ', err);
            document.getElementById("message").innerHTML = "Error sending image: " + err

        }
    }, 'image/jpeg');
}


let timer;

function startDetection () {
    timer = setInterval(captureAndSend, 5000);
    document.getElementById("message").innerHTML = "Starting Detection"
    document.getElementById("start").setAttribute("hidden", true)
    document.getElementById("stop").removeAttribute("hidden")
    document.body.style.backgroundColor = "greenyellow"
}

function stopDetection () {
    clearInterval(timer)
    document.getElementById("message").innerHTML = "Detection Stopped"
    document.getElementById("stop").setAttribute("hidden", true)
    document.getElementById("start").removeAttribute("hidden")
    document.body.style.backgroundColor = "#fff"
}

// Initialize the camera when the page loads
window.onload = function () {
    initCamera();
};