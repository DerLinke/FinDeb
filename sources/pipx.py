import subprocess
import json
import urllib.request

class PipxSource:
    def __init__(self):
        self.name = "pipx"

    def search(self, query):
        results = []
        try:
            # Suche via PyPI JSON API (wir suchen nach Paketen)
            url = f"https://pypi.org/pypi/{query}/json"
            # Da PyPI keine echte 'search' API für JSON hat, die einfach ist,
            # nutzen wir hier einen kleinen Trick oder suchen nach exakten Treffern.
            # Für eine echte Suche müssten wir XML-RPC nutzen, was komplexer ist.
            # Alternativ suchen wir via 'pip search' falls der Server es erlaubt (oft deaktiviert).
            
            # Einfachheitshalber prüfen wir hier erst mal auf den exakten Namen:
            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'findeb-cli')
            
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())
                info = data.get('info', {})
                results.append({
                    "name": info.get('name', query),
                    "version": info.get('version', 'Latest'),
                    "source": self.name,
                    "description": info.get('summary', 'Python CLI Application'),
                    "score": 100,
                    "install_cmd": ["pipx", "install", info.get('name', query)]
                })
        except Exception:
            # Wenn kein exakter Treffer, versuchen wir zumindest den Namen als Option anzubieten
            pass
            
        return results
