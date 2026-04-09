import subprocess

class SnapSource:
    def __init__(self):
        self.name = "snap"

    def search(self, query):
        results = []
        try:
            # Snap find Suche
            cmd = ["snap", "find", query]
            output = subprocess.check_output(cmd, text=True)
            
            lines = output.splitlines()
            if len(lines) > 1: # Erste Zeile ist Header
                for line in lines[1:]:
                    parts = line.split()
                    if len(parts) >= 3:
                        name = parts[0]
                        version = parts[1]
                        desc = " ".join(parts[3:]) # Publisher steht meist bei index 2
                        
                        results.append({
                            "name": name,
                            "version": version,
                            "source": self.name,
                            "description": desc,
                            "score": 40 if query.lower() in name.lower() else 20,
                            "install_cmd": ["snap", "install", name]
                        })
        except Exception:
            pass
            
        return results
