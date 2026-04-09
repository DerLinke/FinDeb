import subprocess
import os
import urllib.request
import shutil

def install_appimage(pkg):
    from rich.console import Console
    console = Console()
    
    # 1. Abhängigkeiten prüfen (libfuse2 ist essenziell für AppImages)
    console.print("[yellow]󰒓 Prüfe System-Abhängigkeiten für AppImage...[/yellow]")
    if not shutil.which("fusermount") and not os.path.exists("/usr/lib/x86_64-linux-gnu/libfuse.so.2"):
        console.print("[bold red]⚠ libfuse2 fehlt (wird für AppImages benötigt).[/bold red]")
        confirm = input("Soll libfuse2 installiert werden? (j/n): ").lower()
        if confirm in ["j", "y", "ja"]:
            subprocess.run(["sudo", "apt", "update"], check=True)
            subprocess.run(["sudo", "apt", "install", "-y", "libfuse2"], check=True)

    # 2. Zielverzeichnis erstellen
    app_dir = os.path.expanduser("~/Applications")
    if not os.path.exists(app_dir):
        os.makedirs(app_dir)
    
    # 3. GitHub API nutzen um den Download-Link zu finden
    repo_url = pkg["url"].replace("https://github.com/", "https://api.github.com/repos/") + "/releases/latest"
    console.print(f"[cyan]󰇚 Suche nach .AppImage in {pkg['name']} Releases...[/cyan]")
    
    try:
        req = urllib.request.Request(repo_url)
        req.add_header('User-Agent', 'findeb-cli')
        with urllib.request.urlopen(req) as response:
            import json
            data = json.loads(response.read().decode())
            assets = data.get("assets", [])
            download_url = None
            for asset in assets:
                if asset["name"].lower().endswith(".appimage"):
                    download_url = asset["browser_download_url"]
                    filename = asset["name"]
                    break
            
            if not download_url:
                console.print("[red]Keine .AppImage Datei im neuesten Release gefunden.[/red]")
                return

            dest_path = os.path.join(app_dir, filename)
            console.print(f"[green]󰇚 Lade herunter:[/green] {filename}...")
            
            # Download mit wget (Fortschrittsanzeige)
            subprocess.run(["wget", "-q", "--show-progress", "-O", dest_path, download_url], check=True)
            
            # Ausführbar machen
            os.chmod(dest_path, 0o755)
            
            # 4. .desktop Datei erstellen
            create_desktop_entry(pkg['name'], dest_path)
            
            console.print(f"\n[bold green]✅ {pkg['name']} wurde erfolgreich in {app_dir} installiert und zum Menü hinzugefügt![/bold green]")

    except Exception as e:
        console.print(f"[red]Fehler beim Download: {e}[/red]")

def create_desktop_entry(name, exec_path):
    desktop_dir = os.path.expanduser("~/.local/share/applications")
    if not os.path.exists(desktop_dir):
        os.makedirs(desktop_dir)
    
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
