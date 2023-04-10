#!/bin/bash -e
mkdir ./itmon/usr/lib/itmon
cp ../../*.py ./itmon/usr/lib/itmon/
mv ./itmon/usr/lib/itmon/main.py ./itmon/usr/lib/itmon/itmon.reporter.py

cp ../../itmon.config.json ./itmon/usr/lib/itmon/itmon.config.json
dpkg-deb --build itmon
if [ ! -d "../builds" ]; then
  mkdir "../builds"
fi
mv itmon.deb ../builds