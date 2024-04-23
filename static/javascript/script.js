function redirectToOpenCamera() {
	window.location.href = "/camera_capture";
}

function openFilePicker_one() {
	const fileInput = document.createElement('input');
	fileInput.type = 'file';
	fileInput.accept = 'image/*';
	fileInput.style.display = 'none';

	fileInput.addEventListener('change', function() {
	  const file = this.files[0];
	  uploadFile(file);
	
	});
	document.body.appendChild(fileInput);
	fileInput.click();
}

function uploadFile(file) {
	const formData = new FormData();
	formData.append('file', file);
	
	fetch('/upload', {
		method: 'POST',
		body: formData
	})
	.then(response => {
		if (response.ok) {
			console.log('File uploaded successfully.');
			window.location.href = "/one_prediction_result";
		} else {
			console.error('Error uploading file.');
		}
	})
	.catch(error => {
		console.error('Error:', error);
	});
}

function openFilePicker_batch() {
	const fileInput = document.createElement('input');
	fileInput.type = 'file';
	fileInput.accept = 'image/*';
	fileInput.multiple = true;
	fileInput.style.display = 'none';

	fileInput.addEventListener('change', function() {
	  const files = this.files;
	  if (files.length <= 10) {
		uploadFiles(files);
	  } else {
		alert('You can upload a maximum of 10 files.');
	  }
	});

	document.body.appendChild(fileInput);
	fileInput.click();
}

function uploadFiles(files) {
	const formData = new FormData();

	for (let i = 0; i < files.length; i++) {
	  const file = files[i];
	  formData.append('files[]', file);
	}
	
	fetch('/upload_batch', {
	method: 'POST',
	body: formData
	})
	.then(response => {
	if (response.ok) {
		console.log('Files uploaded successfully.');
		window.location.href = "/batch_prediction_result"; 
	} else {
		console.error('Error uploading files.');
	}
	})
	.catch(error => {
		console.error('Error:', error);
	});
}