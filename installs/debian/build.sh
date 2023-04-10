#!/bin/bash -e
if [ ! -d "./itmon/usr/lib/itmon" ]; then
  mkdir ./itmon/usr/lib/itmon
fi
cp ../../*.py ./itmon/usr/lib/itmon/
mv ./itmon/usr/lib/itmon/main.py ./itmon/usr/lib/itmon/itmon.reporter.py

cp ../../itmon.config.json ./itmon/usr/lib/itmon/itmon.config.json

chmod 0555 ./itmon/DEBIAN/prerm
dpkg-deb -Znone --build itmon
if [ ! -d "../builds" ]; then
  mkdir "../builds"
fi
mv itmon.deb ../builds
