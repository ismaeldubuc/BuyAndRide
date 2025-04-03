import requests

def ask_ollama(question, context):
    """ Envoie la question et le contexte à Ollama et retourne la réponse. """
    url = "http://localhost:11434/api/generate"
    
    # Préparer le prompt avec le texte extrait des PDF
    prompt = f"""
    Tu es une IA spécialisée en extraction d'informations depuis des documents.
    Voici le contenu d'un fichier PDF extrait depuis S3 :
    
    {context}
    
    En te basant uniquement sur ce texte, réponds précisément à la question suivante :
    
    {question}
    
    Si l'information n'est pas présente dans le document, réponds : "Je ne peux pas répondre avec les informations fournies."
    """
    
    payload = {
        "model": "mistral",  # Essaie avec llama2, gemma ou autre si nécessaire
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json().get("response", "Pas de réponse.")
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête à Ollama : {e}")
        return "Erreur de connexion à Ollama."
