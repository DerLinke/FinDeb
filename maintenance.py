import subprocess
import os
import shutil

def run_maintenance(enabled_sources):
    from rich.console import Console
    from rich.panel import Panel
    
    console = Console()
    
    # Suche nach dem Updater an verschiedenen Orten für maximale Portabilität
    possible_paths = [
        # 1. Relativ zum aktuellen Skript (z.B. wenn beide Projekte im gleichen Ordner liegen)
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Ultimate-Debian-Updater", "update.sh"),
        # 2. Klassischer Pfad im Home-Verzeichnis
        os.path.expanduser("~/Projekte/Ultimate-Debian-Updater/update.sh"),
        # 3. Falls der Nutzer es direkt in ~/bin oder ähnliches verlinkt hat
        shutil.which("ultimate-debian-updater")
    ]
    
    updater_path = None
    for path in possible_paths:
        if path and os.path.exists(path):
            updater_path = path
            break
    
    if updater_path:
        console.print(f"[bold green]󰚌 Ultimate Debian Updater gefunden![/bold green]")
        console.print(f"[dim]Starte externe Wartung: {updater_path}[/dim]\n")
        # Wir führen dein Original-Script aus
        try:
            subprocess.run(["bash", updater_path], check=True)
        except subprocess.CalledProcessError:
            console.print("\n[red]❌ Der Updater wurde mit einem Fehler beendet.[/red]")
    else:
        # Fallback für Nutzer ohne dein Script
        console.print(Panel("[bold yellow]Ultimate Debian Updater nicht gefunden[/bold yellow]\n"
                            "Möchtest du eine einfache Basis-Wartung (APT/Flatpak) durchführen?", expand=False))
        
        confirm = input("Basis-Wartung starten? (j/n): ").lower()
        if confirm in ["j", "y", "ja"]:
            console.print("\n[bold cyan]󰚌 Starte Basis-Update (APT)...[/bold cyan]")
            subprocess.run(["sudo", "apt", "update"])
            subprocess.run(["sudo", "apt", "upgrade", "-y"])
            
            if "flatpak" in enabled_sources and shutil.which("flatpak"):
                console.print("\n[bold cyan]󰚌 Aktualisiere Flatpaks...[/bold cyan]")
                subprocess.run(["flatpak", "update", "-y"])
            
            console.print("\n[bold green]✅ Basis-Wartung abgeschlossen.[/bold green]")
        else:
            console.print("\n[yellow]Tipp: Installiere den Ultimate Debian Updater in ~/Projekte/ für volle Power![/yellow]")
