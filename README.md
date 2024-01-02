# FileUploader 🚀
A cli based tool with a gui that allows quick uploads to catbox. Responds with url of the uploaded file


https://github.com/MG-Osman/FileUploader/assets/58115228/c1e6073f-77e6-4e69-9ba6-0c8aa030cbec

*DEMO*


## Usage

To use the tool, simply run it from your command line, providing the path to the file you wish to upload:

python catbox_uploader.py <file_path>
Optional Arguments
--userhash - Your Catbox user hash if you have one (optional):

python catbox_uploader.py <file_path> --userhash YOUR_USER_HASH
Functionality
The tool has a simple function upload_to_catbox which takes the following arguments:

file_path: The path to the file you want to upload.
user_hash: Your Catbox user hash (optional).
Upon successful upload, the tool prints the URL of the uploaded file. If the upload fails, it prints an error message with the status code or exception details.

The GUI is intuitive so these are CLI based instructions
