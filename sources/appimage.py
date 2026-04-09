import subprocess
import json
import urllib.request

class AppImageSource:
    def __init__(self):
        self.name = "appimage"

    def search(self, query):
        results = []
        try:
            # Wir nutzen die GitHub API (ohne Token, mit Rate-Limit)
            # Suche nach Repositories, die das Topic 'appimage' haben
            url = f"https://api.github.com/search/repositories?q={query}+topic:appimage"
            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'findeb-cli')
            
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())
                
                for item in data.get('items', [])[:5]: # Top 5 Treffer
                    results.append({
                        "name": item['name'],
                        "version": "Latest",
                        "source": self.name,
                        "description": item['description'] or "AppImage von GitHub",
                        "score": 35,
                        "url": item['html_url'],
                        "install_cmd": ["echo", f"Lade AppImage von {item['html_url']} herunter... (WIP)"]
                    })
        except Exception:
            pass
            
        return results
