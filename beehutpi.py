# Author: Mitch @ BeeHutPi (support@beehutpi.com)
# For more info, check out
# http://beehutpi.com/beehutpi-raspberrypi-cctv-controller-project/

import os
from flask import Flask, render_template, request, redirect, url_for
from utils import *
from collections import OrderedDict
app = Flask(__name__)

DEBUG = False
SECURE = True
BHP_PATH = "/home/pi/beehutpi/"
LOGGEDIN = BHP_PATH + "loggedin.conf"
BHP_CONF = BHP_PATH + "bhp.conf"
WIFI_CONF = BHP_PATH + "wifimode.conf"
DBOX_CONF = BHP_PATH + "dboxsync.conf"
mybeehutpi={ 'AVIPATH' : '',
             'DBOXURL' : '',
             'MYHOMEIP' : '',
             'MYREMOTEIP' : '',
             'MYPORT' : '' }

def btn_browse():
    dprint("button pressed with value={}".format('browse'), DEBUG)

def btn_configure():
    dprint("button pressed with value={}".format('configure'), DEBUG)

def btn_config_basic():
    dprint("button pressed with value={}".format('basic'), DEBUG)

def btn_config_advanced():
    dprint("button pressed with value={}".format('advanced'), DEBUG)

def btn_config_back():
    dprint("button pressed with value={}".format('back'), DEBUG)

def btn_help():
    dprint("button pressed with value={}".format('help'), DEBUG)

def btn_stop():
    dprint("button pressed with value={}".format('stop'), DEBUG)
    syscall("sudo systemctl stop motion", DEBUG)

def btn_start():
    dprint("button pressed with value={}".format('start'), DEBUG)
    syscall("sudo systemctl start motion", DEBUG)

def btn_restart():
    dprint("button pressed with value={}".format('restart'), DEBUG)
    syscall("sudo systemctl restart motion", DEBUG)

def btn_check():
    dprint("button pressed with value={}".format('check'), DEBUG)

def btn_reboot():
    dprint("button pressed with value={}".format('reboot'), DEBUG)
    syscall("sudo systemctl reboot", DEBUG)

def btn_shutdown():
    dprint("button pressed with value={}".format('shutdown'), DEBUG)
    syscall("sudo shutdown -h now", DEBUG)

def check_logged():
    """0 means logged in, 1 otherwise"""
    with open(LOGGEDIN, 'r') as f:
        for line in f:
            l = line.rstrip("\n")
            logged = True if l.endswith('0') else False
        f.close()
    return logged

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if SECURE and not check_logged():
        return redirect(url_for('login'))
    setting = read_wifi_mode()
    fname = 'dashboard.html' if setting == 'remote' else 'dashboardhome.html'
    return redirect(url_for('static', filename=fname))

@app.route('/', methods=['GET', 'POST'])
def control():
    if SECURE and not check_logged():
        return redirect(url_for('login'))

    if request.method == 'POST':
        if request.form['submit'] == 'DROPBOX':
            btn_browse()
            return redirect(url_for('browse'))
        if request.form['submit'] == 'CONFIGURE':
            btn_configure()
            return redirect(url_for('configure'))
        if request.form['submit'] == 'BACK TO DASHBOARD':
            sel = request.form.get('field')
            dprint("selected wifi mode=<{}>".format(sel), DEBUG)
            with open(WIFI_CONF, 'w') as f:
                f.write(sel)
                f.close()
            ip = mybeehutpi['MYHOMEIP'] if sel=='home' else mybeehutpi['MYREMOTEIP']
            homepage="http://" + ip + ':' + mybeehutpi['MYPORT'] + '/dashboard'
            return redirect(homepage, code=302)
        if request.form['submit'] == 'HELP':
            btn_help()
        if request.form['submit'] == 'STOP CCTV':
            btn_stop()
        if request.form['submit'] == 'START CCTV':
            btn_start()
        if request.form['submit'] == 'RESTART CCTV':
            btn_restart()
        if request.form['submit'] == 'CHECK':
            btn_check()
        if request.form['submit'] == 'REBOOT RPI':
            btn_reboot()
        if request.form['submit'] == 'SHUTDOWN RPI':
            btn_shutdown()

    dashboard_type={'remote':'unchecked','home':'unchecked'}
    dashboard_type[read_wifi_mode()] = 'checked'
    data = {}
    data['desc'] = "BeeHutPi RPI CCTV Controller"
    data['fields'] = dashboard_type

    return render_template('control.html',
        data=data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Route for handling the login page logic."""
    with open(LOGGEDIN, 'w') as f:
        error = None
        f.write('BHP_Logged:')
        if request.method == 'POST':
            # NOTE:IT IS IMPORTANT THAT YOU CHANGE THE USERNAME AND PASSWORD HERE
            if request.form['username'] != 'admin' or request.form['password'] != 'admin':
                error = 'Invalid Credentials. Please try again.'
                f.write('1')
                f.close()
            else:
                f.write('0')
                f.close()
                return redirect(url_for('dashboard'))
    return render_template('login.html', error=error)
 
def read_wifi_mode():
    setting = None
    with open(WIFI_CONF, 'r') as f:
        setting = f.readlines()[0]
        dprint("reading wifi mode setting=<{}>".format(setting), DEBUG)
    return setting

def read_dbox_conf():
    dbox = None
    with open(DBOX_CONF, 'r') as f:
        dbox = f.readlines()[0]
        dprint("reading dbox sync configuration=<{}>".format(dbox), DEBUG)
    return dbox

def get_filesize(f):
    st = os.stat(f)
    return st.st_size

@app.route('/browse', methods=['GET', 'POST'])
def browse():
    if SECURE and not check_logged():
        return redirect(url_for('login'))

    if request.method == 'POST':
        if request.form['submit'] == 'BACK':
            btn_config_back()
            # enable/disable dropbox sync, read thru checkbox
            val = request.form.getlist('check')
            dbox_conf = 'disable' if val == [] else 'enable'
            with open(DBOX_CONF, 'w') as f:
                f.write(dbox_conf)
                f.close()
            return redirect(url_for('control'))

    avi_dir = mybeehutpi['AVIPATH']
    avi_files = []
    i = 0
    for f in os.listdir(avi_dir):
        if f.endswith('.avi'):
            s = get_filesize(mybeehutpi['AVIPATH']+f)
            ss = round((s/1000), 2)
            dbox = mybeehutpi['DBOXURL'] + '?preview=' +f
            avi_files.append([f, str(ss)+ ' KB', dbox])
    avi_files_number = len(avi_files)
    sorted_avi_files = sorted(avi_files)
    return render_template("browse.html",
        title = 'BeeHutPi RPI CCTV Controller - Dropbox Viewer',
        dbox_setting = 'checked' if (read_dbox_conf() == 'enable') else '',
        avi_files_number = avi_files_number,
        avi_files = sorted_avi_files)

def readconf():
    try:
        with open(BHP_CONF, 'r') as f:
            for line in f.readlines():
                if not line.startswith('#') and '=' in line:
                    l = line.strip('\r\n')
                    ll = l.split('=')
                    mybeehutpi[ll[0]] = ll[1]
    except:
        print("Error reading configuration file. Refer to beehutpi.com for details")

def init():
    with open(LOGGEDIN, 'w') as f:
        f.write('BHP_Logged:')
        f.close()
    with open(WIFI_CONF, 'w') as f:
        f.write('remote')
        f.close()
    with open(DBOX_CONF, 'w') as f:
        f.write('enable')
        f.close()
    print("=== Welcome to BeeHutPi RPI CCTV Controller. Checkout beehutpi.com for more info. ===")

if __name__ == "__main__":
    init()
    readconf()
    app.run(host="0.0.0.0", port=int(mybeehutpi['MYPORT']))
