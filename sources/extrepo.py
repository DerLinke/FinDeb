import subprocess

class ExtRepoSource:
    def __init__(self):
        self.name = "extrepo"

    def search(self, query):
        results = []
        try:
            # Extrepo Suche nach Repositories
            cmd = ["extrepo", "search", query]
            output = subprocess.check_output(cmd, text=True)
            
            current_repo = None
            for line in output.splitlines():
                line = line.strip()
                if not line:
                    continue
                
                # Wenn eine Zeile mit "Found" beginnt, ist das oft der Start eines neuen Eintrags
                if line.startswith("Found"):
                    parts = line.split()
                    if len(parts) >= 2:
                        current_repo = parts[1]
                        # Wir fügen das Repo direkt hinzu, wenn wir es finden
                        results.append({
                            "name": current_repo,
                            "version": "External",
                            "source": self.name,
                            "description": f"Repository: {current_repo}",
                            "repo_id": current_repo,
                            "install_cmd": ["extrepo", "enable", current_repo]
                        })
                
                # Falls die Ausgabe anders strukturiert ist (Name am Zeilenanfang vor einem Doppelpunkt)
                elif ":" in line and not current_repo:
                    repo_id = line.split(":")[0].strip()
                    # Filter: Wir ignorieren typische Metadaten-Felder
                    if repo_id.lower() not in ["description", "url", "suites", "components", "architectures", "types", "uris", "gpg-key-checksum", "gpg-key-file", "source", "policy", "sha256"]:
                        current_repo = repo_id
                        results.append({
                            "name": current_repo,
                            "version": "External",
                            "source": self.name,
                            "description": f"Repository: {current_repo}",
                            "repo_id": current_repo,
                            "install_cmd": ["extrepo", "enable", current_repo]
                        })
            
            # Deduplizierung der Repos
            seen = set()
            unique_results = []
            for r in results:
                if r["name"] not in seen:
                    unique_results.append(r)
                    seen.add(r["name"])
            return unique_results

        except Exception:
            pass
            
        return results
