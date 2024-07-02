# FileUploader 🚀
A cli based tool with a gui that allows quick uploads to catbox from a given url or local file. Responds with catbox url of the uploaded file



![image](https://github.com/MG-Osman/FileUploader/assets/58115228/853daffb-29c7-45e2-b15d-b9118fab8208)


## Usage

### GUI: paste your url('s) in the top box and click 'process url'. one line per url. the log box will below will return the catbox url where the file was uploaded. Click 'Upload File' to browse for a file to uplload or alternatively, drag and drop the file.


### CLI: To use the tool with CLI, simply run it from your command line, providing the path to the file you wish to upload:

### python catbox_uploader.py <file_path> [Optional Arguments]

 --userhash - Your Catbox user hash if you have one (optional):

 Example: python catbox_uploader.py <file_path> --userhash YOUR_USER_HASH


## Functionality
The tool has a simple function upload_to_catbox which takes the following arguments:

file_path: The path to the file you want to upload.

user_hash: Your Catbox user hash (optional).

Upon successful upload, the tool prints the URL of the uploaded file. If the upload fails, it prints an error message with the status code or exception details.

The GUI is intuitive so these are CLI based instructions
