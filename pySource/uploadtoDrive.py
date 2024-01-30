import json
import requests

def uploadMasked(name):
    uploadIMG(name, "path", "1--kTZviKHJ7uLIWvakkgGQqa41WMIxhN")

def uploadIMG(name, path, parent):
    headers = {
        "Authorization": "Bearer ya29.a0AVvZVspkQ18dcJ_VEthcUqOwXhZ76v68BPpwY9UGjTzqf5PehAvwG30yRkyM90FOmQLX4hoLejvA_wwGKENNZwX_jWItbggIjLhxUMGukcdwoDsmBvZA3IlNAYwf4KPtY5amBahM1Fpc4YaHSnfrmLbSI9v4aCgYKAVESARMSFQGbdwaIySVG23XJMmFO0ISc9N0tpg0163"
    }

    para = {
        "name": name,
        "parents": [parent]

    }

    files = {
        'data': ('metadata', json.dumps(para), 'application/json;charset=UTF-8'),
        'file': open('./'+name, 'rb')
    }

    r = requests.post("https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
                      headers=headers,
                      files=files
                      )

    if r.status_code == 200:
        print('The file was uploaded successfully to Google Drive')
    else:
        print('An error occurred: {r.text}')
