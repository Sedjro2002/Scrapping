import requests
from pathlib import Path
import json
import pandas as pd


def main():
    url_autorites = "https://api.marches-publics.bj/v2/api/portail/plandepassations/autorites?page=0&size=1000&search=&column=denomination&asc=true"
    nbre_de_page_autorites = requests.get(url_autorites).json()["totalPages"]
    print("le nombre de page pour les autorites:", nbre_de_page_autorites)
    liste_autorites = []
    donnees_brutes = []
    donnees_utiles = []
    marches = []
    nbre_autorites = 0
    nbre_marches = 0
    for page in range(nbre_de_page_autorites):
        url_autorites = "https://api.marches-publics.bj/v2/api/portail/plandepassations/autorites?page={}&size=1000&search=&column=denomination&asc=true".format(
            page
        )
        autorites = requests.get(url_autorites).json()["content"]
        nbre_autorites += len(autorites)

        for autorite in autorites:
            liste_autorites.append(autorite)
            id_autorite = (
                autorite["sigle"].replace("/", "__") + "-" + str(autorite["id"])
            )
            url_marches = "https://api.marches-publics.bj/v2/api/portail/plandepassations/{}?page=0&size=1000&search=&annee=2023".format(
                id_autorite
            )
            nbre_de_page_marches = requests.get(url_marches).json()["realisations"][
                "totalPages"
            ]

            for page in range(nbre_de_page_marches):
                url_marches = "https://api.marches-publics.bj/v2/api/portail/plandepassations/{}?page={}&size=1000&search=&annee=2023".format(
                    id_autorite, page
                )
                marches_brutes = requests.get(url_marches).json()
                donnees_brutes.append(marches_brutes)
                for m in marches_brutes["realisations"]["content"]:
                    nbre_marches += 1

                    donnees_utiles.append(
                        {
                            "id_autorite": marches_brutes["autorite"]["id"],
                            "denomination_autorite": marches_brutes["autorite"][
                                "denomination"
                            ],
                            "email_autorite": marches_brutes["autorite"]["email"],
                            "telephone_autorite": marches_brutes["autorite"][
                                "telephone"
                            ],
                            "sigle_autorite": marches_brutes["autorite"]["sigle"],
                            "responsable_autorite": marches_brutes["autorite"][
                                "responsable"
                            ],
                            "annee": marches_brutes["autorite"]["annee"],
                            "urlsiteweb_autorite": marches_brutes["autorite"][
                                "urlsiteweb"
                            ],
                            "datedemarrage": m["datedemarrage"],
                            "datelancement": m["datelancement"],
                            "annee_plan": m["plan"]["annee"],
                            "motif_plan": m["plan"]["motif"],
                            "status_plan": m["plan"]["status"],
                            "libelle": m["libelle"],
                            "id_modepassation": m["modepassation_ID"]["id"],
                            "code_modepassation": m["modepassation_ID"]["code"],
                            "libelle_modepassation": m["modepassation_ID"]["libelle"],
                            "montantEstime": m["montantEstime"],
                            "reference": m["reference"],
                            "sourcefinancement": m["sourcefinancement"],
                            "id_typeMarche": m["typeMarche"]["id"],
                            "code_typeMarche": m["typeMarche"]["code"],
                            "libelle_typeMarche": m["typeMarche"]["libelle"],
                            "typeMarcheName": m["typeMarcheName"],
                            "id_plan": m["id_plan"],
                        }
                    )
                    marches.append(m)

            print(f"marches de l'autorite {id_autorite} recuperees avec succes")

        print(f"autorités recuperees avec succes sur la page {page+1}")

    print("nombre total d'autorites:", nbre_autorites)
    print("nombre total de marches:", nbre_marches)

    # Path("autorites.json").write_text(
    #     str(json.dumps(liste_autorites, ensure_ascii=False, indent=4))
    # )
    # print(" fichier autorites.json cree")
    # Path("donnees_brutes.json").write_text(
    #     str(json.dumps(donnees_brutes, ensure_ascii=False, indent=4))
    # )
    # print(" fichier donnees_brutes.json cree")
    # Path("marches.json").write_text(
    #     str(json.dumps(marches, ensure_ascii=False, indent=4))
    # )
    # print(" fichier marches.json cree")
    # Path("donnees_utiles.json").write_text(
    #     str(json.dumps(donnees_utiles, ensure_ascii=False, indent=4))
    # )
    # print(" fichier donnees_utiles.json cree")

    print("debut de la conversion en dataframe...")

    df = pd.DataFrame(donnees_utiles)
    print("donnees converties en dataframe")

    print("debut de la conversion en excel...")
    df.to_excel("data.xlsx")
    print("fin de la conversion")
    print("fichier excel data.xlsx cree avec succes")
    print("fin du script")


if __name__ == "__main__":
    main()
