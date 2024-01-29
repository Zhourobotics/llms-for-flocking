import yaml

with open('./secrets.yml', 'r') as secret_file:
    secret = yaml.safe_load(secret_file)

api_keys = secret.get('api_keys', {})
coolest_key = 0

if len(api_keys) == 0:
    exit("Error: api_keys could not be found in secrets.yml")


# returns the first api key in the list
def get_first_key():
    return api_keys[0]


# returns a key such that all keys are used equally
def get_key():
    global coolest_key
    key = api_keys[coolest_key]
    coolest_key = (coolest_key + 1) % len(api_keys)
    return key
