import subprocess
import os
import shutil

def run_maintenance(enabled_sources):
    from rich.console import Console
    from rich.panel import Panel
    
    console = Console()
    
    # Pfad zu deinem spezialisierten Updater
    updater_path = os.path.expanduser("~/Projekte/Ultimate-Debian-Updater/update.sh")
    
    if os.path.exists(updater_path):
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
            console_print("\n[yellow]Tipp: Installiere den Ultimate Debian Updater in ~/Projekte/ für volle Power![/yellow]")
