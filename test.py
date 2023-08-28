import requests
from pathlib import Path
import json


def main():
    url_autorites = "https://api.marches-publics.bj/v2/api/portail/plandepassations/autorites?page=0&size=5&search=&column=denomination&asc=true"
    data = requests.get(url_autorites).json()
    print(data)
    print(
        "---------------------------------------------------------------------------------"
    )
    # data_json = json.JSONEncoder()
    data_json = json.dumps(data)
    print(data_json)
    # decoder = json.JSONDecoder()
    # decoder.strict = False
    # data = decoder.decode(str(response.content, "utf-8"))
    # data = json.loads(response.content)
    # data = requests.get(url_autorites).json()
    # print(data["content"])

    # Convertit les doublequotes en singlequotes
    # data_json = json.loads(data, object_hook=doublequote_to_singlequote)

    Path("test_data.json").write_text(str(data_json))


def doublequote_to_singlequote(obj):
    if isinstance(obj, str):
        return obj.replace('"', "'")
    return obj


if __name__ == "__main__":
    main()
