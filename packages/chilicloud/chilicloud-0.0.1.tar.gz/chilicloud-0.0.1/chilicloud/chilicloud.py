import requests
import os
import dotenv

dotenv.load_dotenv()
env_username = os.getenv("username")
env_password = os.getenv("password")

global cookies
cookies = {'X-Apigw-Session': os.getenv("X-Apigw-Session")}

def updateApiToken(username=os.getenv("username"), password=os.getenv("password")):
    json_data = {
        'username': username,
        'password': password,
    }
    response = requests.post('https://portal.chiliprotect.com/api/1/login', json=json_data)
    response = requests.get(
        'https://portal.chiliprotect.com/fc/access',
        cookies=response.cookies,
    )
    response_key = response.cookies.get('X-Apigw-Session')
    dotenv.set_key('.env', 'X-Apigw-Session', response_key)
    global cookies
    cookies = {'X-Apigw-Session': response_key}
    return response_key

def downloadFile(file_id, file_path):
    response = requests.get(
        'https://portal.chiliprotect.com/fc/api/v1/sync_and_share_nodes/'+file_id+'/download',
        cookies=cookies,
    )
    
    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            file.write(response.content)
        return response
    else:
        return "Failed to download file. Status code:", response.status_code

def deleteFile(file_id):
    response = requests.delete(
        'https://portal.chiliprotect.com/fc/api/v1/sync_and_share_nodes/'+file_id,
        cookies=cookies,
    )

    if response.status_code == 204:
        return response
    else:
        return "Failed to delete file. Status code:", response.status_code

def uploadFile(file_path):
    file_size = os.path.getsize(file_path)
    file_name = os.path.basename(file_path)
    params = {
        'filename': file_name,
        'size': file_size,
    }
    # Open the file in binary mode and read its content
    with open(file_path, 'rb') as file:
        file_content = file.read()

    response = requests.post(
        'https://portal.chiliprotect.com/fc/api/v1/sync_and_share_nodes/0/upload',
        params=params,
        cookies=cookies,
        data=file_content,
    )
    if response.status_code == 201:
        return response.json()["uuid"]
    else:
        if response.json()["error"]["code"] == 4:
            updateApiToken()
            return "Invalid API Token, getting a new one..."
        return "Failed to upload file. Status code:", response.text