import requests
from pathlib import Path
import json


def main():
    url_autorites = "https://api.marches-publics.bj/v2/api/portail/plandepassations/autorites?page=0&size=1000&search=&column=denomination&asc=true"
    nbre_de_page_autorites = requests.get(url_autorites).json()["totalPages"]
    print("le nombre de page pour les autorites:", nbre_de_page_autorites)
    liste_autorites = []
    donnees_brutes = []
    marches = []
    nbre_autorites = 0
    nbre_marches = 0
    for page in range(nbre_de_page_autorites):
        url_autorites = "https://api.marches-publics.bj/v2/api/portail/plandepassations/autorites?page={}&size=1000&search=&column=denomination&asc=true".format(
            page
        )
        autorites = requests.get(url_autorites).json()["content"]
        nbre_autorites += len(autorites)

        for autorite in autorites[:1]:
            liste_autorites.append(json.dumps(autorite))
            id_autorite = (
                autorite["sigle"].replace("/", "__") + "-" + str(autorite["id"])
            )
            # print('id autorite:',id_autorite)
            url_marches = "https://api.marches-publics.bj/v2/api/portail/plandepassations/{}?page=0&size=1000&search=&annee=2023".format(
                id_autorite
            )
            nbre_de_page_marches = requests.get(url_marches).json()["realisations"][
                "totalPages"
            ]
            # print(requests.get(url_marches).json())

            for page in range(nbre_de_page_marches):
                url_marches = "https://api.marches-publics.bj/v2/api/portail/plandepassations/{}?page={}&size=1000&search=&annee=2023".format(
                    id_autorite, page
                )
                marches_brutes = requests.get(url_marches).json()
                # donnees_brutes.append(correctSingleQuoteJSON(marches_brutes))
                donnees_brutes.append(json.dumps(marches_brutes))
                # donnees_brutes.append(marches_brutes.replace("\'", "\""))
                for m in marches_brutes["realisations"]["content"]:
                    nbre_marches += 1
                    # marches.append(correctSingleQuoteJSON(m))
                    # marches.append(m.replace("\'", "\""))
                    marches.append(json.dumps(m))

            print(f"marches de l'autorite {id_autorite} recuperees avec succes")

        print(f"autorités recuperees avec succes sur la page {page+1}")

    print("nombre total d'autorites:", nbre_autorites)
    print("nombre total de marches:", nbre_marches)

    Path("autorites2.json").write_text(str(liste_autorites))
    print(" fichier autorites.json cree")
    Path("donnees_brutes2.json").write_text(str(donnees_brutes))
    print(" fichier donnees_brutes.json cree")
    Path("marches2.json").write_text(str(marches))
    print(" fichier marches.json cree")


# def correctSingleQuoteJSON(s):
#     rstr = ""
#     escaped = False

#     for c in s:
#         if c == "'" and not escaped:
#             c = '"'  # replace single with double quote

#         elif c == "'" and escaped:
#             rstr = rstr[:-1]  # remove escape character before single quotes

#         elif c == '"':
#             c = "\\" + c  # escape existing double quotes

#         escaped = c == "\\"  # check for an escape character
#         rstr += c  # append the correct json

#     return rstr


if __name__ == "__main__":
    main()
