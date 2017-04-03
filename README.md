## Author

Mitch aka MrGramps @ BeeHutPi (support@beehutpi.com)

## About the BeeHutPi Project

The BeeHutPi RPI CCTV Controller project is a software suite based on flask python framework where it provides remote control of the open source software Motion via a web application. That means you can remotely stream and control your RPI-based CCTV thru your internet-connected smartphone, tablet, or laptop from anywhere in the world. CCTV recordings are also synced to your Dropbox account.

## How-To

Detailed instructions on how to use this project can be found in http://beehutpi.com/beehutpi-raspberrypi-cctv-controller-project/

## Quick Guide

If you have followed thru the instructions in the link above, BeeHutPi
application is automatically ran in the background when Raspberry Pi is
started. If you want to change this, that is, to manually run it, 
terminate background process first:

pi@beehutpi:~ $ ps ax | grep beehutpi | grep -v grep | awk {' print $1 '} | xargs -I out sudo kill -9 out

How to manually run BeeHutPi Raspberry Pi CCTV Controller:

1. go to project directory
$ cd /home/pi/beehutpi/

2. activate virtual environment
$ source venv/bin/activate

3. run server (You should see the welcome message.)
python beehutpi.py

4. when done, deactivate virtual environment
deactivate

## License

GNU GPLv3
For more details, read LICENSE file.


