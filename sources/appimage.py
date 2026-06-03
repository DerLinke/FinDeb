import subprocess
import json
import urllib.request

class AppImageSource:
    def __init__(self):
        self.name = "github"

    def search(self, query):
        results = []
        try:
            # Wir nutzen die GitHub API (ohne Token, mit Rate-Limit)
            # Generelle Suche ohne Topic-Zwang
            url = f"https://api.github.com/search/repositories?q={query}"
            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'findeb-cli')
            
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())
                
                for item in data.get('items', [])[:5]: # Top 5 Treffer
                    repo_full_name = item['full_name']
                    release_url = f"https://api.github.com/repos/{repo_full_name}/releases/latest"
                    release_req = urllib.request.Request(release_url)
                    release_req.add_header('User-Agent', 'findeb-cli')
                    
                    version = "Latest"
                    has_binary = False
                    formats = set()
                    try:
                        # Versuche das neueste Release und dessen Assets abzufragen
                        with urllib.request.urlopen(release_req) as rel_response:
                            rel_data = json.loads(rel_response.read().decode())
                            version = rel_data.get('tag_name', 'Latest').lstrip('v')
                            assets = rel_data.get('assets', [])
                            for asset in assets:
                                asset_name = asset['name'].lower()
                                if asset_name.endswith('.appimage'):
                                    has_binary = True
                                    formats.add("AppImage")
                                elif asset_name.endswith('.deb'):
                                    has_binary = True
                                    formats.add(".deb")
                                elif asset_name.endswith('.flatpak'):
                                    has_binary = True
                                    formats.add("Flatpak")
                                elif asset_name.endswith('.tar.xz') or asset_name.endswith('.tar.gz') or asset_name.endswith('.zip'):
                                    has_binary = True
                                    formats.add("Archiv")
                    except Exception:
                        pass # Kein Release gefunden oder Rate-Limit
                    
                    format_str = "/".join(sorted(formats)) if formats else "Source"

                    results.append({
                        "name": item['name'],
                        "version": version,
                        "source": self.name,
                        "format": format_str,
                        "description": item['description'] or "GitHub Repository",
                        "score": 45 if has_binary else 20,
                        "url": item['html_url'],
                        "install_cmd": ["echo", f"Lade Binärdatei von {item['html_url']}/releases herunter... (WIP)"]
                    })
        except Exception:
            pass
            
        return results
