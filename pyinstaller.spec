# myscript.spec

# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['main.py'],
              pathex=['C:/Users/admin/OneDrive/Documents/GitHub/itmon-server'],
             binaries=[],
             datas=[],
             hiddenimports=['requests','netifaces', 'psutil','cpuinfo'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='server-watchdog-agent',
          debug=True,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )