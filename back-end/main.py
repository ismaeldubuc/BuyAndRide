# main.py
import os
from s3_handler import list_files_in_s3, download_file_from_s3
from pdf_handler import extract_text_from_files_in_folder
from ollama_handler import ask_ollama

def main():
    # Configuration
    bucket_name = "groupe4mmotors"
    local_folder = "s3_downloads"  # Dossier temporaire pour stocker les fichiers

    # Créer le dossier s'il n'existe pas
    os.makedirs(local_folder, exist_ok=True)

    # 1️⃣ Lister tous les fichiers du bucket
    file_keys = list_files_in_s3(bucket_name)

    # 2️⃣ Télécharger tous les fichiers du bucket
    for file_key in file_keys:
        local_file_path = os.path.join(local_folder, os.path.basename(file_key))
        download_file_from_s3(bucket_name, file_key, local_file_path)

    # 3️⃣ Extraire le texte de tous les fichiers PDF dans le dossier
    all_text = extract_text_from_files_in_folder(local_folder)

    print("Bienvenue dans l'assistant IA de Buy and Ride !")
    print("Je peux répondre à vos questions sur les véhicules disponibles.")
    
    while True:
        question = input("\nPosez une question (ou tapez 'exit' pour quitter) : ")
        
        if question.lower() == 'exit':
            print("Au revoir !")
            break
            
        response = ask_ollama(question)
        print("\nRéponse :", response)

if __name__ == "__main__":
    main()
