import subprocess

class AptSource:
    def __init__(self):
        self.name = "apt"

    def search(self, query):
        results = []
        try:
            # Suche nach Paketen
            cmd = ["apt-cache", "search", query]
            output = subprocess.check_output(cmd, text=True)
            
            for line in output.splitlines():
                if " - " in line:
                    pkg_name, desc = line.split(" - ", 1)
                    pkg_name = pkg_name.strip()
                    
                    # Score berechnen für besseres Sorting
                    score = 0
                    if pkg_name == query:
                        score = 100 # Exakter Treffer
                    elif pkg_name.startswith(query):
                        score = 50 # Beginnt mit Query
                    elif query in pkg_name:
                        score = 25 # Query irgendwo im Namen
                    
                    # Sprachpakete erkennen (Malus-Punkte)
                    is_lang_pack = "-l10n-" in pkg_name or "-i18n-" in pkg_name or pkg_name.endswith("-de") or pkg_name.endswith("-en")
                    if is_lang_pack:
                        score -= 20

                    results.append({
                        "name": pkg_name,
                        "version": "Repo",
                        "source": self.name,
                        "description": desc.strip(),
                        "score": score,
                        "is_lang_pack": is_lang_pack,
                        "install_cmd": ["apt", "install", "-y", pkg_name]
                    })
        except Exception:
            pass
            
        return results
