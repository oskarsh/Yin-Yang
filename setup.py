from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
  name='yin-yang',
  version='3.3.0',
  url='https://github.com/oskarsh/Yin-Yang',
  description='Auto Nightmode for KDE, Gnome, Budgie, VSCode, Atom and more',
  long_description=long_description,
  long_description_content_type="text/markdown",
  packages=find_packages(),
  classifiers=[
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
  ],
  python_requires='>=3.10',
  install_requires=[
    'psutil==5.9.5',
    'PySide6==6.6.1',
    'PySide6-Addons==6.6.1',
    'suntime==1.2.5',
    'systemd-python==235',
    'requests~=2.28.2'
  ]
)
