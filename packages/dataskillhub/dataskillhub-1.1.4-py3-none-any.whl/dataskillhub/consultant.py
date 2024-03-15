from pathlib import Path


DESTINATION_PATH = "src"
consultants_path = f"{DESTINATION_PATH}/consultants/"


def get_consultants():
    path = Path(consultants_path)
    for i in path.iterdir():
        print(i.name)


def add_consultant(consultant: str):
    folder_path = Path(f"{consultants_path}/{consultant}")
    folder_path.mkdir(parents=True, exist_ok=True)


def check_consultant(consultant: str):
    file_miss = False
    file_list = [
        "export.yaml",
        "valeur_ajoutee.md",
        "competences_cle.md",
        "diplome.md",
        "langue.md",
        "formations_suivies.md",
        "experiences_significatives.md",
        "experiences_formateurs.md",
    ]
    for f in file_list:
        path = Path(f"{consultants_path}/{consultant}/{f}")
        if not path.exists():
            file_miss = True
            print(f"{f} is missing.")
    if not file_miss:
        print("All files exist.")
