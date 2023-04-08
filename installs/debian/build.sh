#!/bin/bash -e

cp ../../main.py ./itmon/usr/lib/itmon.reporter.py
cp ../../itmon.config.json ./itmon/usr/lib/itmon.config.json
dpkg-deb --build itmon
if [ ! -d "../builds" ]; then
  mkdir "../builds"
fi
mv itmon.deb ../builds