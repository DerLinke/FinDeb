# `findeb` – The Universal Package Manager Wrapper

**`findeb`** (alias **`find-deb`**) is an intelligent package searcher and installer for Debian-based systems. It bridges the gap between traditional repositories and modern distribution methods like Flatpak, Snap, AppImage, and GitHub Releases.

## 🚀 Features
- **Unified Search:** Search across `apt`, `extrepo`, `deb-get`, `flatpak`, `snap`, `pipx`, `npm`, and `GitHub Releases` simultaneously.
- **Smart Grouping:** Automatically groups identical packages from different sources and sorts them by version.
- **Auto-Setup:** Missing package managers can be installed automatically via `findeb --setup`.
- **Maintenance Integration:** Seamlessly works with the [Ultimate Debian Updater](https://github.com/DerLinke/Ultimate-Debian-Updater) for system-wide updates (`findeb -u`).
- **AppImage Automation:** Downloads, makes executable, and creates menu entries for AppImages automatically.

## 📦 Supported Sources
- ✅ **APT** (Official Repos)
- ✅ **ExtRepo** (Third-party PPAs)
- ✅ **deb-get** (Direct .deb from vendors)
- ✅ **Flatpak** (Flathub)
- ✅ **Snap** (Snapcraft)
- ✅ **AppImage** (GitHub Releases)
- ✅ **pipx** (Python CLI Tools)
- ✅ **npm** (Node.js Tools)
- ✅ **pkcon** (PackageKit/KDE)

## 📦 Installation

### Der schnellste Weg (APT Repository)
Da `findeb` Teil des zentralen **DerLinke Repositories** ist, kannst du es einfach so installieren:

1. Repository hinzufügen (falls noch nicht geschehen):
   ```bash
   curl -s https://derlinke.github.io/derlinke-repo.gpg.key | gpg --dearmor | sudo tee /usr/share/keyrings/derlinke-repo.gpg > /dev/null
   echo "deb [signed-by=/usr/share/keyrings/derlinke-repo.gpg] https://derlinke.github.io/ stable main" | sudo tee /etc/apt/sources.list.d/derlinke.list
   ```

2. Installieren:
   ```bash
   sudo apt update
   sudo apt install findeb
   ```

### Manuelle Installation (.deb Paket)

### Für Entwickler (Source-Installation)
```bash
git clone https://github.com/DerLinke/FinDeb.git
cd FinDeb
chmod +x findeb
./findeb --setup
```

## 🛠 System-Abhängigkeiten
`findeb` fungiert als Wrapper. Für die volle Funktionalität sollten folgende Tools auf deinem System vorhanden sein (viele können via `findeb --setup` nachinstalliert werden):
- `apt` & `dpkg` (Standard auf Debian/Ubuntu)
- `extrepo` (für Drittanbieter-Quellen)
- `deb-get` (für GitHub-Releases)
- `flatpak` & `snapd` (optional)
- `pipx` & `npm` (für CLI-Tools)

## 🤝 Mitwirken / Contributing
Dieses Projekt lebt vom Austausch! Wir wollen die Brücke zwischen klassischen Repositories und modernen Distributionen so nahtlos wie möglich machen. 
- **Bugs gefunden?** Erstelle gerne ein Issue.
- **Neue Quelle gewünscht?** Schau dir die Module in `sources/` an – es ist sehr einfach, neue Paketquellen hinzuzufügen.
- **Pull Requests** sind immer willkommen!

---
<p align="center">
  <img src="https://derlinke.github.io/logo.svg" width="300" alt="Logo"><br>
  <strong>DerLinke Software Zentrale</strong><br>
  <a href="https://derlinke.github.io/">Offizielle Webseite</a> | <a href="https://github.com/DerLinke/FinDeb">GitHub Repository</a>
</p>
