DEFVER=1
ARCHS_SUPPORTED="amd64"
get_github_releases "DerLinke/FinDeb" "latest"
if [ "${ACTION}" != "prettylist" ]; then
    # Sucht nach der passenden .deb Datei im GitHub Release für amd64
    URL="$(grep -m 1 "browser_download_url.*_${HOST_ARCH}\.deb\"" "${CACHE_FILE}" | cut -d '"' -f 4)"
    # Extrahiert die Versionsnummer aus dem Dateinamen (zwischen _ und _)
    VERSION_PUBLISHED=$(cut -d '_' -f 2 <<< "${URL//v/}" ) # uses current derivation from current filename 
    #VERSION_PUBLISHED=$(cut -d '/' -f 8 <<< "${URL//v/}" ) # if release tag is in format v1.2.3 or 4.5.6
fi
PRETTY_NAME="FinDeb"
WEBSITE="https://github.com/DerLinke/FinDeb"
SUMMARY="The Universal Package Manager Wrapper"

