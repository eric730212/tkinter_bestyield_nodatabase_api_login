# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['bestyield_system_flip_barcodeenter.py'],
             pathex=['C:\\Users\\GOD\\PycharmProjects\\tkinter_bestyield_nodatabase_api_login'],
             binaries=[],
             datas=[],
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
          name='bestyield_system_flip_barcodeenter',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False , icon='C:\\Users\\GOD\\PycharmProjects\\tkinter_bestyield_nodatabase_api_login\\dist\\bestyield1.ico')
