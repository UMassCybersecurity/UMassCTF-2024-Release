import logging
import requests
import os
import json
import metadata
from concurrent import futures
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("URL")
TOKEN = os.getenv('TOKEN')
BUCKET_NAME = os.getenv('BUCKET_NAME')


AUTH_HEADER = {'Content-Type': 'application/json', 'Authorization': f"Token {TOKEN}"}
LOGGER = logging.getLogger("upload")

uploaded_data = {}
# Add challenges if in file
if os.path.isfile("./uploaded.json"):
    with open("./uploaded.json") as f:
        uploaded_data = json.load(f)

def __add_upload_data(name: str, key: str, val) -> None:
    if not name in uploaded_data:
        uploaded_data[name] = {}
    uploaded_data[name][key] = val
    with open("./uploaded.json", 'w') as f:
        json.dump(uploaded_data, f)


def __add_upload_data_dict(name: str, key1: str, key2: str, val: str) -> None:
    if not name in uploaded_data:
        uploaded_data[name] = {}
    uploaded_data[name][key1][key2] = val
    with open("./uploaded.json", 'w') as f:
        json.dump(uploaded_data, f)

########
# Temp #
########

# def list_challenges() -> None | list[object]:
#     response = requests.get(BASE_URL + "/api/v1/challenges",
#                             headers=AUTH_HEADER, params={'name':'test upload'})
    
#     response_json = response.json()
#     print(response.text)
#     print(response_json)
    
#     if response.status_code != 200 or response_json['success'] == False:
#         LOGGER.error(f"Unable to get challenges from CTFd. Server responded with code {response.status_code} and errors {response_json['errors']}")
#         return None

#     return response_json['data']

##############
# Challenges #
##############
def get_formated_challenge_data(data : dict) -> dict:
    description = data['description']
    if 'static' in data:
        description += "\n\nFiles:\n* " + "\n* ".join([f"[{file_name}](https://storage.googleapis.com/{BUCKET_NAME}/{data['path']}/static/{file_name})" for file_name in data['static']])
    
    output = {
        'name': data['name'],
        'category':data['category'],
        'description': description,
        'type': 'dynamic',
        'initial': data['points']['initial'],
        'function': data['points']['function'],
        'decay': data['points']['decay'],
        'minimum': data['points']['minimum'],
        'state': data['state'],
    }

    if 'requirements' in data:
        requirement_data = data['requirements']
        output['requirements'] = {
            'anonymize': requirement_data['anonymize'] if 'anonymize' in requirement_data else False,
            'prerequisites': [uploaded_data[name]['challenge_id'] for name in requirement_data['prerequisites']] if 'prerequisites' in requirement_data else []
        }
    
    if 'challenge' in data:
        connection_data = data['challenge']
        match connection_data['type']:
            case 'TCP':
                output['connection_info'] = f"nc {connection_data['url']} {connection_data['port']}"
            case 'HTTP':
                output['connection_info'] = f"http://{connection_data['url']}"
            case _:
                LOGGER.warning(f"Can not add connection details for {data['name']}. Unknown protocol on port {connection_data['port']}.")

    return output

def post_challenge(data : dict, quiet : bool = False) -> bool:
    if 'ignore' in data and data['ignore']:
        return False

    if data['name'] in uploaded_data:
        if not quiet:
            LOGGER.error(f"Can not post challenge {data['name']} because it has already been uploaded. Try patch_challenge")
        return False
    
    response = requests.post(BASE_URL + "/api/v1/challenges",
                                headers=AUTH_HEADER,
                                json=get_formated_challenge_data(data))
    
    response_json = response.json()
    
    if response.status_code != 200 or response_json['success'] == False:
        LOGGER.error(f"Failed to upload challenge {data['name']}. Server responded with code {response.status_code} and errors {response_json['errors']}")
        return False

    __add_upload_data(data['name'], "challenge_id", response_json['data']['id'])

    return True

def patch_challenge(data: dict, id: int|None = None) -> bool:
    if 'ignore' in data and data['ignore']:
        return False

    if not data['name'] in uploaded_data and not id:
        LOGGER.error(f"Can not patch challenge {data['name']} because it has not been uploaded or ID has not been supplied. Try post_challenge")
        return False
    
    response = requests.patch(BASE_URL + f"/api/v1/challenges/{id if id else uploaded_data[data['name']]['challenge_id']}",
                                headers=AUTH_HEADER,
                                json=get_formated_challenge_data(data))

    response_json = response.json()
    
    if response.status_code != 200 or response_json['success'] == False:
        LOGGER.error(f"Failed to patch challenge {data['name']}. Server responded with code {response.status_code} and errors {response_json['errors']}")
        return False

    return True

def update_challenge(data: dict) -> None:
    if not post_challenge(data, True):
        patch_challenge(data)

#########
# Flags #
#########
def get_formated_flag_data(data: dict) -> dict:
    return {
        "challenge_id": uploaded_data[data['name']]['challenge_id'],
        "content": data['flag'],
        "type": "static",
        "data": ""
    }

def post_flag(data: dict, quiet: bool = False) -> bool:
    if 'ignore' in data and data['ignore']:
        return False
    
    if not data['name'] in uploaded_data:
        LOGGER.error(f"Can not post flag of challenge {data['name']} because challenge has not been uploaded. Try post_challenge")
        return False

    if 'flag_id' in uploaded_data[data['name']]:
        if not quiet:
            LOGGER.error(f"Can not set flag of challenge {data['name']} because flag already exists. Try patch_flag")
        return False

    response = requests.post(BASE_URL + "/api/v1/flags",
                                headers=AUTH_HEADER,
                                json=get_formated_flag_data(data))
    
    response_json = response.json()
    
    if response.status_code != 200 or response_json['success'] == False:
        LOGGER.error(f"Failed to post challenge flag {data['name']}. Server responded with code {response.status_code} and errors {response_json['errors']}")
        return False
    
    __add_upload_data(data['name'], "flag_id", response_json['data']['id'])

    return True
    
def patch_flag(data: dict) -> bool:
    if 'ignore' in data and data['ignore']:
        return False

    if not data['name'] in uploaded_data:
        LOGGER.error(f"Can not post flag of challenge {data['name']} because challenge has not been uploaded. Try post_challenge")
        return False

    if not 'flag_id' in uploaded_data[data['name']]:
        LOGGER.error(f"Can not patch flag of challenge {data['name']} because flag does not exist. Try post_flag")
        return False

    response = requests.patch(BASE_URL + f"/api/v1/flags/{uploaded_data[data['name']]['flag_id']}",
                                headers=AUTH_HEADER,
                                json=get_formated_flag_data(data))
    
    response_json = response.json()
    
    if response.status_code != 200 or response_json['success'] == False:
        LOGGER.error(f"Failed to patch challenge flag {data['name']}. Server responded with code {response.status_code} and errors {response_json['errors']}")
        return False
    
    return True

def update_flag(data: dict) -> None:
    if not post_flag(data, True):
        patch_flag(data)


########
# Tags #
########
def post_tag(data: dict, index: int, quiet: bool = False) -> bool:
    if 'ignore' in data and data['ignore']:
        return False
    
    if not data['name'] in uploaded_data:
        LOGGER.error(f"Can not post tag to challenge {data['name']} because it has not been uploaded. Try post_challenge")
        return False

    if not 'tags' in uploaded_data[data['name']]:
        uploaded_data[data['name']]['tags'] = {}
    elif data['tags'][index] in uploaded_data[data['name']]['tags']:
        if not quiet:
            LOGGER.error(f"Can not post tag {data['tags'][index]} of challenge {data['name']} because tag has already been uploaded.")
        return False
    
    response = requests.post(BASE_URL + "/api/v1/tags",
                             headers=AUTH_HEADER, 
                             json= {
                                "challenge": uploaded_data[data['name']]['challenge_id'],
                                "value": data['tags'][index]
                            }
    )

    response_json = response.json()
    
    if response.status_code != 200 or response_json['success'] == False:
        LOGGER.error(f"Failed to post tag for challenge {data['name']}. Server responded with code {response.status_code} and errors {response_json['errors']}")
        return False
    
    __add_upload_data_dict(data['name'], "tags", response_json['data']['value'], response_json['data']['id'])

    return True
    
# def patch_tag(data: dict, index: int) -> bool:
#     if 'ignore' in data and data['ignore']:
#         return False
    
#     if not data['name'] in uploaded_data:
#         LOGGER.error(f"Can not post tag to challenge {data['name']} because it has not been uploaded. Try post_challenge")
#         return False

#     if not 'tags' in uploaded_data[data['name']] or not data['tags'][index] in uploaded_data[data['name']]['tags']:
#         LOGGER.error(f"Can not patch tag {data['tags'][index]} of challenge {data['name']} because tag has not been uploaded. try post_tag")
#         return False
    
#     response = requests.post(BASE_URL + "/api/v1/tags/" + uploaded_data[data['name']]['tags'][data['tags'][index]],
#                              headers=AUTH_HEADER, 
#                              json= {
#                                 "value": data['tags'][index]
#                             }
#     )

#     response_json = response.json()
    
#     if response.status_code != 200 or response_json['success'] == False:
#         LOGGER.error(f"Failed to patch tag for challenge {data['name']}. Server responded with code {response.status_code} and errors {response_json['errors']}")
#         return False

#     return True

def update_tag(data: dict, index: int) -> bool:
    if not post_tag(data, index, True):
        # return patch_tag(data, index)
        pass
    return True

def update_tags(data: dict) -> None:
    if not 'tags' in data:
        return
    
    for i in range(len(data['tags'])):
        update_tag(data, i)

def update_all(data: dict) -> None:
    update_challenge(data)
    update_flag(data)
    update_tags(data)

if __name__ == "__main__":
    print("Getting metadata")
    challenges = metadata.get_metadata().values()
    
    print("Uploading challenges...")
    with futures.ThreadPoolExecutor(10) as executor:
        for challenge in challenges:
            executor.submit(update_all, challenge)
    
    print("Done!")