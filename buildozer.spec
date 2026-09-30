[app]
title = Sikandar AI Agent
package.name = sikandaraiagent
package.domain = org.sikandar
source.dir = .
source.exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy==2.3.0,cython==3.0.8,requests
orientation = portrait
fullscreen = 0
android.archs = arm64-v8a
android.api = 33
android.minapi = 21
android.sdk = 30
android.ndk = 25b
android.private_storage = True

[buildozer]
log_level = 2
warn_on_root = 1
