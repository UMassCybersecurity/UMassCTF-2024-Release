import yaml
import logging
import os
from dotenv import load_dotenv

os.chdir(os.path.dirname(__file__))

load_dotenv()

BASE_PATH = os.getenv("BASE_PATH")
CATEGORIES = os.getenv("CATEGORIES").split(",")

LOGGER = logging.getLogger("metadata")

def __get_metadata_from_challenge(base_path: str, category: str, challenge: str):
    path = os.path.join(base_path, category, challenge)
    metadata_path = os.path.join(path, "metadata.yaml")
    if not os.path.isfile(metadata_path):
        LOGGER.warning(f"Challenge at {path} does not have any metadata.")
        return
    
    with open(metadata_path) as f:
        data : dict[str,str] = yaml.safe_load(f)
    
    # Add path
    data['path'] = os.path.join(category, challenge)
    
    # Add category
    if not 'category' in data:
        data['category'] = category

    # Add static resources
    static_path = os.path.join(path, "static")
    if os.path.isdir(static_path):
        data['static'] = []
        with os.scandir(static_path) as scan:
            for entry in scan:
                if entry.is_file():
                    data['static'].append(entry.name)
    
    # Add challenge
    challenge_path = os.path.join(path, "challenge.yaml")
    if os.path.isfile(challenge_path):
        with open(challenge_path) as f:
            challenge_data = next(yaml.safe_load_all(f))
        port = challenge_data['spec']['network']['ports'][0]['port']
        data['challenge'] = {'url':f"{challenge_data['metadata']['name']}.ctf.umasscybersec.org", 'port':port, 'type': "TCP" if port == 1337 else "HTTP" if port == 80 else "Unknown"}

    # Add point data
    if not 'points' in data:
        data['points'] = {
            'initial': 500,
            'function': 'logarithmic',
            'decay': 100,
            'minimum': 100
        }

    # Add wave data
    if not 'wave' in data:
        data['wave'] = 0

    # Add state data
    if not 'state' in data:
        data['state'] = 'visible'

    return data    

def get_metadata(path : str = BASE_PATH, categories : str = CATEGORIES) -> dict[str, object]:
    """
    Gets all avalible metadata.yaml files starting from the specified path and returns a dictionary by challenge name
    """

    output = {}

    for category in categories:
        category_path = os.path.join(path, category)
        if not os.path.isdir(category_path):
            LOGGER.error(f"Unable to find folder for {category}.")
            continue

        with os.scandir(category_path) as scan:
            for challenge in scan:
                if challenge.is_dir():
                    data = __get_metadata_from_challenge(path, category, challenge.name)
                    if not data:
                        continue
                    if data['name'] in output:
                        LOGGER.error(f"Two challenges share the name {data['name']}. Ignoring all metadata except first.")
                        continue
                    output[data['name']] = data
    
    return output

# TODO add validation code
def validate_challenges(challenges : dict[str, object]) -> None:
    for name, challenge in challenges.items():
        try:
            with open(os.path.join(challenge['path'], 'README.md')) as f:
                readme = f.read()
        except(FileNotFoundError):
            LOGGER.warning(f"No README at {challenge['path']} to validate {name} against. Can only check name against path")
    

if __name__ == "__main__":
    import json

    print(f"Search categories: {', '.join(CATEGORIES)}")

    with open('metadata.json', 'w') as f:
        json.dump(get_metadata(), f)

    print("Generating metadata.json...")
    print("Done!")