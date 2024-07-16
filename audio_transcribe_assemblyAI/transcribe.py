import requests
from environs import Env

env = Env()
env.read_env()  # read .env file, if it exists
# required variables
API_TOKEN = env.str("API_TOKEN")
base_url = "https://api.assemblyai.com/v2"


def get_url(token, data):
    '''
    Parameter:
    token: The API key
    data : The File Object to upload
    Return Value:
    url : Url to uploaded file
    '''
    headers = {
        'authorization': token
    }
    response = requests.post(base_url + "/upload",
                             headers=headers,
                             data=data)
    url = response.json()["upload_url"]
    print("uploaded file and got temporary url to the file")
    return url


def get_transcribe_id(token, url):
    '''
    Parameter:
    token: The API key
    url : Url to uploaded file
    Return Value:
    id : The transcribe id of the file
    '''
    endpoint = base_url + "/transcript"
    data = {
        "audio_url": url
    }
    headers = {
        "authorization": token,
        "content_type": "application/json"
    }
    response = requests.post(endpoint, json=data, headers=headers)
    id = response.json()['id']
    print("mad request  and file is currently queued")
    return id


def get_text(token, transcribe_id):
    '''
    Parameter:
    token: The API key
    transcribe_id: The ID of the file which is being
    Return Value:
    result : The response object
    '''
    endpoint = base_url + f"/transcript/{transcribe_id}"
    headers = {
        "authorization": token
    }
    result = requests.get(endpoint, headers=headers).json()
    return result


def upload_file(fileObj):
    '''
    Parameter:
    fileObj: The File Object to transcribe
    Return Value:
    token : The API key
    transcribe_id: The ID of the file which is being transcribed
    '''
    file_url = get_url(API_TOKEN, fileObj)
    transcribe_id = get_transcribe_id(API_TOKEN, file_url)
    return API_TOKEN, transcribe_id
