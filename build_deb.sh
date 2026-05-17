#!/bin/bash

# findeb .deb Build Script
# Erstellt eine Standalone-Binärdatei mit PyInstaller und verpackt diese als .deb

set -e

VERSION="1.0.0"
MAINTAINER="Daniel Frey <https://github.com/DerLinke>"
HOMEPAGE="https://github.com/DerLinke/FinDeb"
DESCRIPTION="The Universal Package Manager Wrapper"
APP_NAME="findeb"

# Architektur ermitteln
ARCH=$(dpkg --print-architecture)
DEB_NAME="${APP_NAME}_${VERSION}_${ARCH}"
BUILD_DIR="dist/build_deb_temp"

echo "󰚌 Starte Build für $DEB_NAME..."

# 1. Aufräumen
rm -rf build dist "$APP_NAME.spec" "$BUILD_DIR"

# 2. PyInstaller ausführen
echo "󰚌 Kompiliere mit PyInstaller..."

# Dynamisch alle Module in sources/ finden
HIDDEN_IMPORTS=""
for f in sources/*.py; do
    module=$(basename "$f" .py)
    if [ "$module" != "__init__" ]; then
        HIDDEN_IMPORTS="$HIDDEN_IMPORTS --hidden-import sources.$module"
    fi
done

# Zusätzliche Hidden-Imports für die Hauptlogik
HIDDEN_IMPORTS="$HIDDEN_IMPORTS --hidden-import maintenance --hidden-import installer_appimage"

.venv/bin/pyinstaller --onefile $HIDDEN_IMPORTS "$APP_NAME"

# 3. .deb Struktur aufbauen
echo "󰚌 Erstelle Debian-Struktur..."
mkdir -p "$BUILD_DIR/DEBIAN"
mkdir -p "$BUILD_DIR/usr/bin"

# control Datei erstellen
cat <<EOF > "$BUILD_DIR/DEBIAN/control"
Package: $APP_NAME
Version: $VERSION
Section: utils
Priority: optional
Architecture: $ARCH
Maintainer: $MAINTAINER
Homepage: $HOMEPAGE
Description: $DESCRIPTION
EOF

# Binärdatei kopieren
cp dist/"$APP_NAME" "$BUILD_DIR/usr/bin/"
chmod 755 "$BUILD_DIR/usr/bin/$APP_NAME"

# 4. Paket bauen
echo "󰚌 Baue .deb Paket..."
dpkg-deb --root-owner-group --build "$BUILD_DIR" "${DEB_NAME}.deb"

# 5. Finales Aufräumen
rm -rf "$BUILD_DIR"

echo "✅ Fertig! Paket erstellt: ${DEB_NAME}.deb"
