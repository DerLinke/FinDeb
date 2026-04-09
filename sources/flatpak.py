import subprocess

class FlatpakSource:
    def __init__(self):
        self.name = "flatpak"

    def search(self, query):
        results = []
        try:
            # Wir fügen die 'name' Spalte hinzu für den lesbaren Namen
            cmd = ["flatpak", "search", "--columns=name,application,version,description", query]
            output = subprocess.check_output(cmd, text=True)
            
            lines = output.splitlines()
            for line in lines:
                parts = line.split("\t")
                if len(parts) >= 4:
                    friendly_name = parts[0].strip()
                    app_id = parts[1].strip()
                    version = parts[2].strip()
                    desc = parts[3].strip()
                    
                    # Wir zeigen den lesbaren Namen an, behalten aber die App-ID für die Installation
                    display_name = f"{friendly_name} ({app_id})"
                    
                    score = 40
                    if query.lower() in friendly_name.lower(): score += 30
                    if query.lower() in app_id.lower(): score += 10
                    
                    results.append({
                        "name": display_name,
                        "real_name": app_id, # Die ID brauchen wir für den Befehl
                        "version": version or "Flathub",
                        "source": self.name,
                        "description": desc,
                        "score": score,
                        "install_cmd": ["flatpak", "install", "-y", "flathub", app_id]
                    })
        except Exception:
            pass
            
        return results
