import requests
def fetch_content_not_found(platform_name):
    """Récupère les contenus non trouvés pour une plateforme donnée."""
    api_url = f"http://127.0.0.1:8000/api/read/contents_not_found/{platform_name}"
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erreur lors de la récupération des données depuis l'API: {response.status_code}")
        return []