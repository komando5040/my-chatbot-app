[app]
title = My ChatGPT
package.name = mychatbot
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy==2.1.0
orientation = portrait
osx.python_version = 3
osx.kivy_version = 2.1.0
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1

android.accept_sdk_license = True
android.ndk = 25.2.9519653
android.sdk = 34
android.build_tools = 34.0.0
android.minapi = 21
android.api = 34
android.arch = arm64-v8a
