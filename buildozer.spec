[app]
title = الخفاش
package.name = bat_app
package.domain = com.alrufaaey
source.dir = src
source.include_exts = py,png,jpg,kv,txt,ttf
version = 1.0
requirements = python3,kivy==2.1.0,kivymd==1.1.1,requests
orientation = portrait
fullscreen = 0
presplash.filename = assets/presplash.png
icon.filename = assets/ico.png

[android]
android.permissions = INTERNET,ACCESS_NETWORK_STATE
android.api = 31
android.minapi = 21
android.sdk = 31
android.ndk = 25b
android.private_storage = True
android.accept_sdk_license = True
android.archs = arm64-v8a
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
