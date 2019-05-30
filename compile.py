import subprocess
subprocess.call(['pyinstaller', 'clusterid.py', '-y', '--onefile', \
                '--icon=cluster.ico', '--paths', 'C:\\Python34\\Lib\\site-packages\\PyQt5\\'])
