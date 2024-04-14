// custom_script.js

$(document).on('submit', '#post-form', function (e) {
    e.preventDefault();

    // Get the message input value
    var message = $('#message').val().trim();

    // Check if the message is empty
    if (!message) {
        alert('Please enter a message before sending.');
        return; // Stop further execution
    }

    var formData = new FormData(this);
    var sentMessage = formData.get('message');

    // Display the "text-end" message
    $('#result-message').append('<p class="text-end m-3 fw-bold p-3 mb-2 bg-success text-white" style= "border-radius: 10px;"> {user}: <span >' + sentMessage + '</span></p>').show();
    $('#result-message').append('<p class="Hello text-start m-3 fw-bold p-3 mb-2 bg-warning text-dark placeholder-glow " style= "border-radius: 10px;"> VedaGPT <span class="placeholder col-11"><br></span> <span class="placeholder col-11"><br></span></p>').show();
    $('#message').val('');
    
    $.ajax({
        type: 'POST',
        url: 'send',
        data: formData,
        processData: false,
        contentType: false,
        
        success: function (data) {
                $('#result-message .Hello').remove();
                $('#result-message').append('<p class="text-start m-3 fw-bold p-3 mb-2 bg-warning text-dark" style= "border-radius: 10px;"> VedaGPT: ' + data.reply + '</p>').show();  
                // Clear the message and file inputs after submission
               
         }
    });

    window.scrollTo(0, document.body.scrollHeight);
});



// FOR FILE Input
// Get the input element
var input = document.getElementById('file-upload');
var infoArea = document.getElementById('file-upload-filename');

input.addEventListener('change', showFileName);

function showFileName(event) {
    // the change event gives us the input it occurred in 
    var input = event.srcElement;
    
    // the input has an array of files in the `files` property, each one has a name that you can use. We're just using the name here.
    var fileName = input.files[0].name;
    
    // use fileName however fits your app best, i.e. add it into a div
    infoArea.textContent = 'File name: ' + fileName;

    // Disable the file input to prevent further uploads
    input.disabled = true;
}

// Prevent form submission if no file is selected
document.getElementById('upload-form').addEventListener('submit', function(event) {
    // Check if a file is selected
    if (input.files.length === 0) {
        // Prevent form submission
        event.preventDefault();
        alert("Please select a file to upload.");
    }
});
