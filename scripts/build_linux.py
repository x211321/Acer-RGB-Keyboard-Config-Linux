#!/usr/bin/env python3

import os
import sys
import shutil
from zipfile import ZipFile

sys.path.append("../")

from version import VERSION

BUILD_DIR  = "build"
BUNDLE_DIR = "RGB_Config_acer-gkbbl-0_" + str(VERSION) + "_script"
DEBPKG_DIR = "RGB_Config_acer-gkbbl-0_" + str(VERSION) + "_deb"

# Find directory that contains this script
baseDir = os.path.abspath(os.path.dirname(__file__))

# cd to base dir
os.chdir(baseDir)

# Create build directory
if os.path.exists(BUILD_DIR):
    shutil.rmtree(BUILD_DIR)

os.makedirs(BUILD_DIR)

# cd to build dir
os.chdir(BUILD_DIR)

# Create bundle dir
os.makedirs(BUNDLE_DIR)

# Copy files to bundle dir
shutil.copy("../../rgb_config_acer_gkbbl_0.py"   , os.path.join(BUNDLE_DIR, "rgb_config_acer_gkbbl_0.py"))
shutil.copy("../../rgb_config_acer_gkbbl_0_wx.py", os.path.join(BUNDLE_DIR, "rgb_config_acer_gkbbl_0_wx.py"))
shutil.copy("../../version.py"                    , os.path.join(BUNDLE_DIR, "version.py"))
shutil.copy("../../icon.png"                      , os.path.join(BUNDLE_DIR, "icon.png"))
shutil.copy("../../LICENSE"                       , os.path.join(BUNDLE_DIR, "LICENSE"))
shutil.copy("../../README.md"                     , os.path.join(BUNDLE_DIR, "README.md"))
shutil.copytree("../../preview_gif/"              , os.path.join(BUNDLE_DIR, "preview_gif/"))

# Zip bundle
zip = ZipFile(BUNDLE_DIR + ".zip", "w")

for root, dirs, files in os.walk(BUNDLE_DIR):
    for f in files:
        zip.write(os.path.join(root, f))

zip.close()


# Create .deb file

os.makedirs(os.path.join(DEBPKG_DIR, "usr/local/bin"))
os.makedirs(os.path.join(DEBPKG_DIR, "usr/share/applications"))
os.makedirs(os.path.join(DEBPKG_DIR, "DEBIAN"))

# Copy previously bundled files to .deb structure lib
shutil.copytree(BUNDLE_DIR + "/", os.path.join(DEBPKG_DIR, "usr/local/lib/rgb_config_acer_gkbbl_0/"))

# Copy start script to .deb structure bin
shutil.copy("../rgb_config_acer_gkbbl_0", os.path.join(DEBPKG_DIR, "usr/local/bin/rgb_config_acer_gkbbl_0"))

# Copy .desktop application file to .deb structure
shutil.copy("../rgb_config_acer_gkbbl_0.desktop", os.path.join(DEBPKG_DIR, "usr/share/applications/rgb_config_acer_gkbbl_0.desktop"))

# Write metadata
metaData =  "Package: rgb-config-acer-gkbbl-0\n" \
            "Version: " + str(VERSION) + "\n" \
            "Section: base\n" \
            "Priority: optional\n" \
            "Architecture: amd64\n" \
            "Depends: python3-wxgtk4.0\n" \
            "Maintainer: x211321\n" \
            "Description: A simple GUI for controlling the RGB settings of the acer-gkbbl-0 kernel module\n" \
            "Homepage: https://github.com/x211321/Acer-RGB-Keyboard-Config-Linux\n"

file = open (os.path.join(DEBPKG_DIR, "DEBIAN/control"), "w", encoding="utf-8")
file.write(metaData)
file.close()

os.system("dpkg-deb --build " + DEBPKG_DIR)