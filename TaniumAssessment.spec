# -*- mode: python -*-

block_cipher = None


a = Analysis(['TaniumAssessment.py'],
             pathex=['c:\\Python27\\Lib', 'D:\\GIT\\HygieneAssessment', 'D:\\GIT\\HygieneAssessment\\lib'],
             binaries=None,
             datas=[('*.py', '.' ), ('lib', 'lib' ), ('PPTXTEMPLATES', 'PPTXTEMPLATES')],
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
          name='TaniumAssessment',
          debug=False,
          strip=False,
          upx=True,
          console=True )
