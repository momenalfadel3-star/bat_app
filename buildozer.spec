[app]

# معلومات التطبيق
title = الخفاش
package.name = bat_app
package.domain = com.alrufaaey

# مسار المصادر
source.dir = ./src
source.include_exts = py,png,jpg,kv,txt,ttf

# إصدار التطبيق
version = 1.0

# المتطلبات
requirements = 
    python3,
    kivy==2.1.0,
    kivymd==1.1.1,
    pyjnius==1.4.2,
    openssl,
    requests

# واجهة المستخدم
presplash.filename = ./assets/presplash.png
icon.filename = ./assets/ico.png
orientation = portrait
fullscreen = 0

# إعدادات Android
[android]

# أذونات النظام
android.permissions = 
    INTERNET,
    ACCESS_NETWORK_STATE,
    FOREGROUND_SERVICE,
    POST_NOTIFICATIONS,
    VIBRATE

# إصدارات API
android.api = 31
android.minapi = 21
android.sdk = 24
android.ndk = 23b
android.ndk_api = 21

# اسم الحزمة
android.package = com.alrufaaey.bat_app

# إعدادات التنفيذ
android.private_storage = True
android.wakelock = True
android.accept_sdk_license = True

# إعدادات الترجمة
android.arch = arm64-v8a

[buildozer]

# مستوى السجلات
log_level = 2
warn_on_root = 1
