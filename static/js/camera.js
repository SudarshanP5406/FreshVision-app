const captureTab = document.getElementById('captureTab');
const uploadTab = document.getElementById('uploadTab');
const cameraSection = document.getElementById('cameraSection');
const video = document.getElementById('video');
const snapBtn = document.getElementById('snap');
const fileInput = document.getElementById('fileInput');
const previewImg = document.getElementById('previewImg');
let stream;

// Switch to Camera mode
captureTab.addEventListener('click', () => {
  fileInput.value = '';               // clear any previous file
  previewImg.classList.add('hidden');
  cameraSection.classList.remove('hidden');
  startCamera();
});

// Switch to Upload mode
uploadTab.addEventListener('click', () => {
  stopCamera();
  cameraSection.classList.add('hidden');
  previewImg.classList.add('hidden');
  fileInput.click();                  // open file picker
});

// Start webcam
function startCamera() {
  navigator.mediaDevices.getUserMedia({ video: true })
    .then(s => {
      stream = s;
      video.srcObject = s;
      video.play();
    })
    .catch(console.error);
}

// Stop webcam
function stopCamera() {
  if (stream) stream.getTracks().forEach(t => t.stop());
}

// Capture from webcam
snapBtn.addEventListener('click', () => {
  const canvas = document.createElement('canvas');
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  canvas.getContext('2d').drawImage(video, 0, 0);
  canvas.toBlob(blob => {
    const file = new File([blob], 'capture.jpg', { type: 'image/jpeg' });
    const dt = new DataTransfer();
    dt.items.add(file);
    fileInput.files = dt.files;
    updatePreview(URL.createObjectURL(file));
    stopCamera();
  }, 'image/jpeg');
});

// Show preview when a file is selected
fileInput.addEventListener('change', () => {
  if (fileInput.files.length) {
    updatePreview(URL.createObjectURL(fileInput.files[0]));
  }
});

function updatePreview(src) {
  previewImg.src = src;
  previewImg.classList.remove('hidden');
}
