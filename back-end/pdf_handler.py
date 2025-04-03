import pdfplumber
import os

def extract_text_from_pdf(pdf_path):
    """ Extrait le texte d'un fichier PDF. """
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

def extract_text_from_files_in_folder(folder_path):
    """ Extrait le texte de tous les fichiers PDF dans un dossier donné. """
    all_text = ""
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if filename.lower().endswith(".pdf"):
            all_text += extract_text_from_pdf(file_path) + "\n\n"
    return all_text
