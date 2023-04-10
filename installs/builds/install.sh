#!/bin/bash

get_pkg=""
# Check for curl
if [ -x "$(command -v curl)" ]; then
  get_pkg="curl"
  echo "curl is installed"
  echo "Example usage: curl https://example.com"
fi

# Check for wget
if [ -x "$(command -v wget)" ]; then
  get_pkg="wget"
  echo "wget is installed"
  echo "Example usage: wget https://example.com"
fi

# Check if both curl and wget are missing
if [ -z "$get_pkg" ]; then
  echo "Either curl or wget must be installed"
  exit
fi

# todo: check if token is unused

# Check if apt-get (Debian package manager) is installed
if [ -x "$(command -v apt-get)" ]; then
  echo "Debian-based distribution detected"

  if [ -f "itmon.deb" ]; then
    rm itmon.deb
  fi

  apt-get update
  apt-get install build-essential python3-dev -y

  $get_pkg https://agents.server-watchdog.com/itmon.deb
  dpkg -i itmon.deb
  apt-get -f install -y
  dpkg -i itmon.deb

# Check if yum (RPM package manager) is installed
elif [ -x "$(command -v yum)" ]; then
  echo "RPM-based distribution detected"
  # Install the package using yum
  yum install mypackage
else
  echo "Unsupported distribution detected"
  exit 1
fi

echo "{\"token\": \"$1\",\"interval\": 20, \"apiUrl\": \"https://api.server-watchdog.com/v1\"}" >/usr/lib/itmon/itmon.config.json
