import requests
from pdf_handler import extract_text_from_files_in_folder

def ask_ollama(question):
    """ Envoie la question à Ollama et retourne la réponse. """
    url = "http://localhost:11434/api/generate"
    
    # Récupérer le contexte des fichiers PDF
    folder_path = "s3_downloads"
    context = extract_text_from_files_in_folder(folder_path)
    
    prompt = f"""
    Tu es une IA spécialisée en extraction d'informations depuis des documents.
    Voici le contenu des devis extraits depuis S3 :
    
    {context}
    
    En te basant uniquement sur ce texte, réponds précisément à la question suivante :
    
    {question}
    
    Si l'information n'est pas présente dans le document, réponds : "Je ne peux pas répondre avec les informations fournies."
    """
    
    payload = {
        "model": "mistral",
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json().get("response", "Pas de réponse.")
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête à Ollama : {e}")
        return "Je suis désolé, je ne peux pas répondre pour le moment. Veuillez réessayer plus tard."
