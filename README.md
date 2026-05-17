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

### Der einfachste Weg (.deb Paket)
Da `findeb` als eigenständiges Paket gebaut wird, sind keine Python-Abhängigkeiten auf deinem System nötig. Das Paket wurde auf **Debian Trixie** (Testing) gebaut und ist kompatibel mit modernen Debian-basierten Systemen (Ubuntu, Pop!_OS, etc.).

1. Lade die neueste `.deb`-Datei von der [Releases-Seite](https://github.com/DerLinke/FinDeb/releases) herunter.
2. Installiere sie via Terminal:
   ```bash
   sudo apt install ./findeb_1.0.0_amd64.deb
   ```

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
*Developed with ❤️ by Daniel Frey & Gemini CLI.*
