# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['findeb'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['sources.appimage', 'sources.apt', 'sources.deb_get', 'sources.extrepo', 'sources.flatpak', 'sources.npm', 'sources.pacman', 'sources.pipx', 'sources.pkcon', 'sources.snap', 'maintenance', 'installer_github'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='findeb',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
