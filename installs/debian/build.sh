cp ../../main.py ./itmon/usr/lib/itmon.reporter.py
cp ../../config.json ./itmon/usr/lib/config.json
dpkg-deb --build itmon
dpkg -i itmon.deb