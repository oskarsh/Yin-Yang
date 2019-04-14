# -*- mode: python -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['/home/daeh/Application/Yin-Yang-Build'],
             binaries=[],
             datas=[
		("assets/yin-yang.svg", "assets"),
		("assets/dark.wav", "assets"),
		("assets/light.wav", "assets"),
		("assets/change_wallpaper.sh", "assets")	
			],
             hiddenimports=[],
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
          name='yin-yang',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
