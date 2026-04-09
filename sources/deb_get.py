import subprocess

class DebGetSource:
    def __init__(self):
        self.name = "deb-get"

    def search(self, query):
        results = []
        try:
            # deb-get search zeigt nur Paketnamen
            cmd = ["deb-get", "search", query]
            output = subprocess.check_output(cmd, text=True)
            
            for line in output.splitlines():
                if ":" in line:
                    pkg_name, desc = line.split(":", 1)
                    pkg_name = pkg_name.strip()
                    results.append({
                        "name": pkg_name,
                        "version": "Latest",
                        "source": self.name,
                        "description": desc.strip(),
                        "install_cmd": ["deb-get", "install", pkg_name]
                    })
        except Exception as e:
            # print(f"Deb-get error: {e}")
            pass
            
        return results
