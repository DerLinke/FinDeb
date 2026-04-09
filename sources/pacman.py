import subprocess

class PacmanSource:
    def __init__(self):
        self.name = "pacman"

    def search(self, query):
        results = []
        try:
            # pacman -Ss sucht in den Repos
            cmd = ["pacman", "-Ss", query]
            output = subprocess.check_output(cmd, text=True)
            
            lines = output.splitlines()
            for i in range(0, len(lines), 2):
                if i+1 < len(lines):
                    # pacman gibt Name/Version in Zeile 1 und Beschreibung in Zeile 2 aus
                    info_line = lines[i]
                    desc_line = lines[i+1]
                    
                    if "/" in info_line:
                        repo_pkg = info_line.split(" ", 1)[0]
                        repo, pkg_name = repo_pkg.split("/", 1)
                        version = info_line.split(" ", 2)[1]
                        
                        results.append({
                            "name": pkg_name,
                            "version": version,
                            "source": self.name,
                            "description": desc_line.strip(),
                            "install_cmd": ["pacman", "-S", "--noconfirm", pkg_name]
                        })
        except Exception:
            pass
            
        return results
