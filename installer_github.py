import subprocess
import os
import urllib.request
import shutil
import json

def get_home_dir():
    # Ermittelt das echte Home-Verzeichnis, auch wenn der Befehl mit sudo ausgeführt wird
    real_user = os.environ.get("SUDO_USER", os.environ.get("USER", "root"))
    if real_user == "root":
        return "/root"
    return os.path.expanduser(f"~{real_user}")

def install_github(pkg):
    from rich.console import Console
    console = Console()
    
    repo_url = pkg["url"].replace("https://github.com/", "https://api.github.com/repos/") + "/releases/latest"
    console.print(f"[cyan]󰇚 Analysiere GitHub Release für {pkg['name']}...[/cyan]")
    
    try:
        req = urllib.request.Request(repo_url)
        req.add_header('User-Agent', 'findeb-cli')
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            assets = data.get("assets", [])
            
            # Filtere Assets nach passendem Betriebssystem/Architektur (Linux amd64 bevorzugt)
            valid_assets = []
            for asset in assets:
                name_lower = asset["name"].lower()
                # Schließe falsche Betriebssysteme und Architekturen aus
                if any(x in name_lower for x in ["macos", "darwin", "windows", "win32", "win64", ".exe", ".dmg"]):
                    continue
                if any(x in name_lower for x in ["arm64", "aarch64", "armv7"]):
                    continue
                valid_assets.append(asset)
            
            # Fallback, falls der Filter zu strikt war
            if not valid_assets:
                valid_assets = assets
            
            # Priorität der Installation: 1. deb, 2. appimage, 3. archive
            target_asset = None
            asset_type = None
            
            for ext in [".deb", ".appimage", ".tar.gz", ".tar.xz", ".zip"]:
                for asset in valid_assets:
                    if asset["name"].lower().endswith(ext):
                        target_asset = asset
                        asset_type = ext
                        break
                if target_asset:
                    break
                    
            if not target_asset:
                console.print("[yellow]Dieses Repository bietet keine direkt unterstützten Installationsdateien (AppImage, .deb, Archiv) für Linux amd64 im Release an.[/yellow]")
                console.print(f"Es handelt sich vermutlich um Source-Code. Bitte besuche: {pkg['url']}")
                return

            download_url = target_asset["browser_download_url"]
            filename = target_asset["name"]
            home_dir = get_home_dir()
            
            if asset_type == ".deb":
                dest_path = os.path.join("/tmp", filename)
                console.print(f"[green]󰇚 Lade {filename} nach /tmp herunter...[/green]")
                subprocess.run(["wget", "-q", "--show-progress", "-O", dest_path, download_url], check=True)
                console.print("[cyan]Installiere .deb Paket...[/cyan]")
                subprocess.run(["sudo", "apt", "install", "-y", dest_path], check=True)
                console.print(f"\n[bold green]✅ {pkg['name']} wurde erfolgreich installiert![/bold green]")
                try: os.remove(dest_path)
                except: pass
                
            elif asset_type == ".appimage":
                # Check libfuse2
                if not shutil.which("fusermount") and not os.path.exists("/usr/lib/x86_64-linux-gnu/libfuse.so.2"):
                    console.print("[bold red]⚠ libfuse2 fehlt (wird für AppImages benötigt).[/bold red]")
                    confirm = input("Soll libfuse2 installiert werden? (j/n): ").lower()
                    if confirm in ["j", "y", "ja"]:
                        subprocess.run(["sudo", "apt", "update"], check=True)
                        subprocess.run(["sudo", "apt", "install", "-y", "libfuse2"], check=True)

                app_dir = os.path.join(home_dir, "Applications")
                os.makedirs(app_dir, exist_ok=True)
                dest_path = os.path.join(app_dir, filename)
                
                console.print(f"[green]󰇚 Lade {filename} nach {app_dir} herunter...[/green]")
                subprocess.run(["wget", "-q", "--show-progress", "-O", dest_path, download_url], check=True)
                os.chmod(dest_path, 0o755)
                
                # Besitzer auf den eigentlichen Nutzer setzen
                if os.environ.get("SUDO_USER"):
                    subprocess.run(["chown", f"{os.environ.get('SUDO_USER')}:{os.environ.get('SUDO_USER')}", dest_path])
                    subprocess.run(["chown", "-R", f"{os.environ.get('SUDO_USER')}:{os.environ.get('SUDO_USER')}", app_dir])
                    
                create_desktop_entry(pkg['name'], dest_path, home_dir)
                console.print(f"\n[bold green]✅ {pkg['name']} wurde erfolgreich in {app_dir} installiert und zum Menü hinzugefügt![/bold green]")

            elif asset_type in [".tar.gz", ".tar.xz", ".zip"]:
                dl_dir = "/tmp"
                dest_path = os.path.join(dl_dir, filename)
                console.print(f"[green]󰇚 Lade Archiv {filename} nach {dl_dir} herunter...[/green]")
                subprocess.run(["wget", "-q", "--show-progress", "-O", dest_path, download_url], check=True)
                
                app_dir = os.path.join(home_dir, "Applications", pkg['name'])
                os.makedirs(app_dir, exist_ok=True)
                console.print(f"[cyan]Entpacke Archiv nach {app_dir}...[/cyan]")
                
                if asset_type == ".zip":
                    subprocess.run(["unzip", "-q", "-o", dest_path, "-d", app_dir], check=True)
                else:
                    subprocess.run(["tar", "-xf", dest_path, "-C", app_dir], check=True)
                
                # Besitzer auf den eigentlichen Nutzer setzen
                if os.environ.get("SUDO_USER"):
                    subprocess.run(["chown", "-R", f"{os.environ.get('SUDO_USER')}:{os.environ.get('SUDO_USER')}", app_dir])
                    
                console.print(f"\n[bold green]✅ {pkg['name']} wurde in {app_dir} entpackt![/bold green]")
                console.print(f"[yellow]Hinweis: Da es sich um ein Archiv handelt, findest du die ausführbaren Dateien im Ordner: {app_dir}[/yellow]")
                try: os.remove(dest_path)
                except: pass

    except urllib.error.HTTPError as e:
        if e.code == 404:
            console.print("[yellow]Kein Release für dieses Repository auf GitHub gefunden (nur Source-Code).[/yellow]")
            console.print(f"Besuche das Repository für Installationsanweisungen: {pkg['url']}")
        else:
            console.print(f"[red]HTTP-Fehler beim Abrufen der Release-Informationen: {e.code} {e.reason}[/red]")
    except Exception as e:
        console.print(f"[red]Ein unerwarteter Fehler ist aufgetreten: {e}[/red]")

def create_desktop_entry(name, exec_path, home_dir):
    desktop_dir = os.path.join(home_dir, ".local", "share", "applications")
    if not os.path.exists(desktop_dir):
        os.makedirs(desktop_dir, exist_ok=True)
        if os.environ.get("SUDO_USER"):
            subprocess.run(["chown", "-R", f"{os.environ.get('SUDO_USER')}:{os.environ.get('SUDO_USER')}", os.path.join(home_dir, ".local")])
            
    entry_path = os.path.join(desktop_dir, f"findeb-{name.lower()}.desktop")
    content = f"""[Desktop Entry]
Type=Application
Name={name}
Exec={exec_path}
Icon=utilities-terminal
Terminal=false
Categories=Utility;
Comment=Installiert via findeb
"""
    with open(entry_path, "w") as f:
        f.write(content)
        
    if os.environ.get("SUDO_USER"):
        subprocess.run(["chown", f"{os.environ.get('SUDO_USER')}:{os.environ.get('SUDO_USER')}", entry_path])
