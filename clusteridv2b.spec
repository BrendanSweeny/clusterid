# -*- mode: python -*-

block_cipher = None


a = Analysis(['clusteridv2b.py'],
             pathex=['C:\\Python34\\Lib\\site-packages\\PyQt5', 'C:\\Users\\Brendan\\Desktop\\clusterid'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='clusteridv2b',
          debug=False,
          strip=False,
          upx=True,
          console=True , icon='cluster.ico')
