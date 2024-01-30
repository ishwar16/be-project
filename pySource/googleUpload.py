from googleapiclient.http import MediaFileUpload
from Google import CreateService

CLIENT_SECRET_FILE = 'client secret GoogleCloudDemo.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ["https://www.googleapis.com/auth/drive"]

service = CreateService(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

folder_id = '126070_IMIZNUSEW9Gc6irtTNsKmZV--L'
file_names = ['masked.jpg']
mime_types = ['image/jpeg']

for file_name, mime_type in zip(file_names, mime_types):
    file_metadata = {
        "name": file_name,
        "parents": [folder_id]
    }
    media = MediaFileUpload('./Random Files/{}'.format(file_name), mimetype=mime_type)
    service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id"
    ).execute()