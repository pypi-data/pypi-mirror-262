from weasyprint import HTML, CSS
import json
from .extract_consultants import DossierCompetence
from jinja2 import Template
import markdown


def get_content(source: str) -> str:
    """read le fichier selon la source"""
    with open(source, "r") as content:
        content_str = content.read()
    return content_str


class CV:
    """class pour manipuler un contenu du cv

    :example :
    >>> cv = CV("name='Bob Pipo'
                 poste='Data Scientist'
                sections=[
                    Section(titre='Compétences1', file='### A '),
                    Section(titre='Diplôme1', file='### Diplômes')
                ]")

    """

    def __init__(
        self,
        dossier_competence: DossierCompetence,
        template_path="src/templates/temp_cv.html",
        file_anomyme="src/config/anonyme.json",
        asset_path="src/assets/",
    ) -> None:
        """initialise le contenu du cv"""
        html_template = template_path
        html_content = get_content(html_template)
        self.dossier_competence = dossier_competence
        self.template = Template(html_content)
        self.file_anomyme = file_anomyme

    def to_html_content(self, asset_path):
        """transformer le format md en html"""
        for section in self.dossier_competence.sections:
            section.file = markdown.markdown(section.file)
        html = self.template.render(
            name=self.dossier_competence.name,
            poste=self.dossier_competence.poste,
            sections=self.dossier_competence.sections,
            asset_path=asset_path,
        )
        return html

    def anonimize(self, cv: str) -> str:
        """anonimiser le contenu du cv"""
        with open(self.file_anomyme, "r") as anonimize_file:
            dict_anonimizd = json.loads(anonimize_file.read())
        for key in dict_anonimizd:
            cv = cv.replace(key, dict_anonimizd[key])
        return cv

    def to_html_file(self, output_html_file, anonimize: bool, asset_path):
        """transformer le format md en html et sorti la fichier.html"""
        html_content = self.to_html_content(f"../../../{asset_path}")
        if anonimize:
            html_content = self.anonimize(html_content)
        output_html_file = output_html_file + ".html"
        with open(output_html_file, "w", encoding="utf-8") as html_file:
            html_file.write(html_content)

    def to_pdf_file(self, output_pdf_file, anonimize: bool, asset_path):
        """transformer le format html en pdf et sorti la fichier.pdf"""
        html_content = self.to_html_content(asset_path)
        if anonimize:
            html_content = self.anonimize(html_content)
        html = HTML(string=html_content, base_url="")
        output_pdf_file = output_pdf_file + ".pdf"
        with open(f"{asset_path}/test.css", "rb") as f:
            css = f.read()
        html.write_pdf(
            output_pdf_file,
            stylesheets=[CSS(string=css)],
            presentational_hints=True,
        )
