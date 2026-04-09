import subprocess

class PkconSource:
    def __init__(self):
        self.name = "pkcon"

    def search(self, query):
        results = []
        try:
            # pkcon search name <query> sucht via PackageKit
            cmd = ["pkcon", "search", "name", query]
            output = subprocess.check_output(cmd, text=True)
            
            # Die Ausgabe von pkcon ist oft sehr strukturiert
            for line in output.splitlines():
                if "\t" in line:
                    parts = line.split("\t")
                    if len(parts) >= 2:
                        status = parts[0].strip()
                        pkg_info = parts[1].strip()
                        desc = parts[2].strip() if len(parts) > 2 else ""
                        
                        # pkg_info ist oft name;version;arch;repo
                        if ";" in pkg_info:
                            name = pkg_info.split(";")[0]
                            version = pkg_info.split(";")[1]
                            
                            results.append({
                                "name": name,
                                "version": version,
                                "source": self.name,
                                "description": desc,
                                "install_cmd": ["pkcon", "install", "-y", name]
                            })
        except Exception:
            pass
            
        return results
