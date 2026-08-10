[app]
title = DifApp
package.name = diffapp
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy,pypdf==5.1.0,python-docx==1.0.1,openpyxl==3.0.10,python-pptx==0.6.23,requests
orientation = portrait
fullscreen = 0
icon.filename = %(source.dir)s/data/icon.png

[buildozer]
log_level = 2
warn_on_root = 1
