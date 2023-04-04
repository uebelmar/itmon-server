cp ../../main.py ./itmon/usr/lib/itmon.reporter.py
cp ../../itmon.config.json ./itmon/usr/lib/itmon.config.json
dpkg-deb --build itmon
dpkg -i itmon.deb