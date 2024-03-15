from pathlib import Path
import click
from .consultant import get_consultants, add_consultant, check_consultant
from .export import write_exports
from .extract_consultants import get_cvs
from .init_src import copy_file, creer_dossier

BASE_PATH = "sources_exemple"
# DESTINATION_PATH = "src"
OUTPUT_PATH = "outputs"
asset_path = "assets"


@click.group()
def main():
    pass


@main.command()
def init():
    list_dossier = ["assets", "templates", "config", "consultants"]
    for dossier in list_dossier:
        creer_dossier(f"{dossier}/")
    code_path = Path(__file__).parent
    copy_file(code_path / "assets", "assets", "logo_pied.png")  # noqa
    copy_file(
        code_path / "assets",
        "assets",
        "Datalyo_logo_rvb.png",  # noqa
    )
    copy_file(code_path / "assets", "assets", "test.css")
    copy_file(code_path / "templates", "templates", "temp_cv.html")  # noqa
    copy_file(code_path / "config", "config", "anonyme.json")  # noqa
    print("fichiers prêt")


@main.group()
def consultant():
    pass


@consultant.command()
@click.argument("consultant")
def export(consultant):
    consultants_path = "consultants"
    cvs = get_cvs(consultant, consultants_path)
    write_exports(cvs, OUTPUT_PATH, consultant, asset_path)


@consultant.command()
def list():
    get_consultants()


@consultant.command()
@click.argument("consultant")
def new(consultant):
    add_consultant(consultant)


@consultant.command()
@click.argument("consultant")
def check(consultant):
    check_consultant(consultant)


if __name__ == "__main__":
    main()
