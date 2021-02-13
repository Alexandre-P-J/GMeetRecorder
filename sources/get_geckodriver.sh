#!/bin/bash

url=$(curl -s https://api.github.com/repos/mozilla/geckodriver/releases/latest | python -c "import sys, json; print(next(item['browser_download_url'] for item in json.load(sys.stdin)['assets'] if 'linux32' in item.get('browser_download_url', '')))")
curl -s -L "$url" | tar -xz
chmod +x geckodriver
mv geckodriver /usr/local/bin/