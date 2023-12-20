import argparse
import requests

def upload_to_catbox(file_path, user_hash=None):
    """Uploads a file to Catbox and returns the URL."""
    data = {'reqtype': 'fileupload'}
    if user_hash:
        data['userhash'] = user_hash

    files = {'fileToUpload': open(file_path, 'rb')}

    try:
        response = requests.post('https://catbox.moe/user/api.php', data=data, files=files)
        files['fileToUpload'].close()  # Make sure to close the file after uploading

        if response.status_code == 200:
            return 'Upload successful. URL: ' + response.text.strip()
        else:
            return f'Upload failed. Status Code: {response.status_code}'
    except Exception as e:
        return f'An error occurred: {e}'

def main():
    parser = argparse.ArgumentParser(description="Upload files to Catbox via CLI.")
    parser.add_argument('file', type=str, help="The path to the file you want to upload.")
    parser.add_argument('--userhash', type=str, default=None, help="Your Catbox user hash (optional).")

    args = parser.parse_args()

    # Call the upload function
    result = upload_to_catbox(args.file, args.userhash)
    print(result)

if __name__ == "__main__":
    main()
