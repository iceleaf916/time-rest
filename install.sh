#!/bin/bash

cd `dirname $0`

rm -f /usr/bin/time-rest
echo "Remove /usr/bin/time-rest."

chmod +x `pwd`/time-rest.py
ln -s `pwd`/time-rest.py /usr/bin/time-rest
echo "Build symbol link for time-rest.py."

rm -f /etc/xdg/autostart/time-rest.desktop
cp `pwd`/time-rest.desktop /etc/xdg/autostart/time-rest.desktop
echo "Copy desktop file to autostart folder."
