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

## 🛠 Installation
```bash
git clone https://github.com/DerLinke/findeb.git
cd findeb
chmod +x findeb
./findeb --setup
```

## ⌨️ Usage
```bash
# Search & Install
findeb <query>

# Update System (Brücke zum Ultimate Debian Updater)
findeb -u

# Configure Sources
findeb --setup
```

## 📝 TODO
- [ ] **Fuzzy Matching:** Tolerance for typos during search.
- [ ] **Exclusion Criteria:** Option to hide specific packages.
- [ ] **Caching:** Improve speed for frequent queries.

---
*Developed with ❤️ by Dan & Gemini CLI.*
