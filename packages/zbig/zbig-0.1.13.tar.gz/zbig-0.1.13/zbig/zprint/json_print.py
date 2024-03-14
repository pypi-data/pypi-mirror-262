import json


# Print JSON data with indentation
def json_print(data, indent=4):
    print(json.dumps(data, indent=indent))
