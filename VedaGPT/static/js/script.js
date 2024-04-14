// Get the input element
var input = document.getElementById('file-uploaded');

// Add event listener to the input element
input.addEventListener('change', showFileName);

// Function to handle the change event and display the file name
function showFileName(event) {
    // Get the input element
    var input = event.srcElement;

    // Get the file name
    var fileName = input.files[0].name;

    // Display the file name
    var infoArea = document.getElementById('file-upload-filename');
    infoArea.textContent = 'File name: ' + fileName;
}
