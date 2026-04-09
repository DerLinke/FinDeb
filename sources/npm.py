import subprocess
import json

class NpmSource:
    def __init__(self):
        self.name = "npm"

    def search(self, query):
        results = []
        try:
            # npm search --json ist sehr präzise
            cmd = ["npm", "search", "--json", query]
            output = subprocess.check_output(cmd, text=True)
            
            if not output.strip():
                return []
                
            data = json.loads(output)
            
            # Wir nehmen die Top 10 Treffer zur Übersichtlichkeit
            for item in data[:10]:
                pkg_name = item.get('name', '')
                version = item.get('version', 'Latest')
                desc = item.get('description', '')
                
                score = 30
                if query.lower() in pkg_name.lower(): score += 30
                
                results.append({
                    "name": pkg_name,
                    "version": version,
                    "source": self.name,
                    "description": desc,
                    "score": score,
                    "install_cmd": ["npm", "install", "-g", pkg_name]
                })
        except Exception:
            pass
            
        return results
