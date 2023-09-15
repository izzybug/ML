const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const classifyBtn = document.getElementById('classify_btn');
const clearBtn = document.getElementById('clear_btn');
const saveBtn = document.getElementById('save_btn');
const predictionDiv = document.getElementById('prediction');

let isDrawing = false;

canvas.addEventListener('mousedown', startDrawing);
canvas.addEventListener('mousemove', draw);
canvas.addEventListener('mouseup', stopDrawing);
canvas.addEventListener('mouseout', stopDrawing);

classifyBtn.addEventListener('click', classifyHandwriting);
clearBtn.addEventListener('click', clearCanvas);
saveBtn.addEventListener('click', saveCanvasImage);

function startDrawing(event) {
    isDrawing = true;
    draw(event);
}

function draw(event) {
    if (!isDrawing) return;

    const x = event.clientX - canvas.offsetLeft;
    const y = event.clientY - canvas.offsetTop;

    ctx.lineWidth = 20;
    ctx.lineCap = 'round';
    ctx.strokeStyle = 'black';

    ctx.lineTo(x, y);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(x, y);
}

function stopDrawing() {
    isDrawing = false;
    ctx.beginPath();
}

function clearCanvas() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    predictionDiv.innerHTML = '';
}

function classifyHandwriting() {
    const imageData = canvas.toDataURL('image/png');

    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ image: imageData })
    })
    .then(response => response.json())
    .then(data => {
        const digit = data.digit;
        const confidence = data.confidence;

        predictionDiv.innerHTML = `Prediction: ${digit}, Confidence: ${confidence}%`;

        // Save the image on the server
        saveImage(imageData);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function saveImage(imageData) {
    // Convert base64 image data to a Blob
    const byteCharacters = atob(imageData.split(',')[1]);
    const arrayBuffer = new ArrayBuffer(byteCharacters.length);
    const uint8Array = new Uint8Array(arrayBuffer);
    for (let i = 0; i < byteCharacters.length; i++) {
        uint8Array[i] = byteCharacters.charCodeAt(i);
    }
    const blob = new Blob([arrayBuffer], { type: 'image/png' });

    // Create a FormData object and append the Blob
    const formData = new FormData();
    formData.append('image', blob, 'canvas_image.png');

    // Send a POST request to save the image on the server
    fetch('/save_image', {
        method: 'POST',
        body: formData
    })
    .then(response => response.text())
    .then(data => {
        console.log('Image saved:', data);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}