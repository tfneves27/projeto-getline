[app]
title = Getline
package.name = getlineapp
package.domain = org.getline
source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,json,txt
version = 0.1

requirements = python3,kivy==2.2.1,https://github.com/kivymd/KivyMD/archive/master.zip,httpx,httpcore,h11,sniffio,anyio,urllib3,pillow,openssl,certifi

orientation = portrait
fullscreen = 0
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1