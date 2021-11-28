#!/usr/bin/python3
##coding=utf-8
# ------------------------------------------------------
#
# Zimbra Exporter
#
# Script by : Jason Cheng
# Website : www.jason.tools / blog.jason.tools
# Version : 1.0
# Date : 2021/11/28
#
# ------------------------------------------------------

import requests
import prometheus_client
import os
import psutil
import time
import datetime
from prometheus_client.core import CollectorRegistry
from prometheus_client import Gauge
from prometheus_client import Counter
from flask import Response,Flask

# ------
# define
# ------

PORT_EXPORTER = 9093

MAILSERVER = 'mail.zimbra.domain'
EXCLUDE_DOMAIN = '' # If you want to filter out a specific domain, please add it here.

PORT_SMTP = '25'
PORT_IMAP = '143'
PORT_IMAPS = '993'
PORT_POP3 = '110'
PORT_POP3S = '995'
PORT_WEBCLIENT = '443'

# ------


# -----
# test

# print(test)

# -----



# --------------
# get info function
def getcheck():

# try:

    REGISTRY = CollectorRegistry(auto_describe=False)


    # -----


    # get stats

    get_st = os.popen('/opt/zimbra_pflogsumm.pl /var/log/zimbra.log | grep -v Redundent').read().splitlines()
    st = Gauge("zimbra_stats","Zimbra Stats:",["name"],registry=REGISTRY)
    for i in range(len(get_st)):

      st_name = get_st[i].split(' ')[1].strip().split('=')[0]
      st_value = int(get_st[i].split('=')[1].strip())

      st.labels(st_name).set(st_value)


    # -----


    # get top usage

    if (EXCLUDE_DOMAIN ==''):
      get_qu_cmd = '/bin/su - zimbra -c "zmprov getQuotaUsage ' + MAILSERVER + '| grep -v \"spam.\" | grep -v \"virus-quarantine.\" | head -n 6"'
    else:
      get_qu_cmd = '/bin/su - zimbra -c "zmprov getQuotaUsage ' + MAILSERVER + '| grep -v \"' + EXCLUDE_DOMAIN + '\" | grep -v \"spam.\" | grep -v \"virus-quarantine.\" | head -n 6"'

    get_qu = os.popen(get_qu_cmd).read().splitlines()
    qu = Gauge("zimbra_quota_usage","Zimbra User Quota Usage:",["name","usage"],registry=REGISTRY)
    for i in range(len(get_qu)):

      qu_name = get_qu[i].split(' ')[0].strip()
      qu_usage = int(get_qu[i].split(' ')[2].strip())
      qu_quota = int(get_qu[i].split(' ')[1].strip())
      qu_value = 0
      if (qu_quota != 0 and qu_usage != 0):
        qu_value = qu_usage / qu_quota

      qu.labels(qu_name,qu_usage).set(qu_value)


    # -----


    # get port litsen
    pt = Gauge("zimbra_port","Zimbra Listen Ports:",["name","status"],registry=REGISTRY)

    get_pt = os.popen('netstat -tnpl | grep ":' + PORT_SMTP + '"').read().strip()
    pt.labels("SMTP","LISTEN").set(1)

    get_pt = os.popen('netstat -tnpl | grep nginx | cut -d ":" -f2 | cut -d " " -f1 | grep "' + PORT_POP3 + '"').read().strip()
    pt.labels("POP3","LISTEN").set(1)

    get_pt = os.popen('netstat -tnpl | grep nginx | cut -d ":" -f2 | cut -d " " -f1 | grep "' + PORT_IMAP + '"').read().strip()
    pt.labels("IMAP","LISTEN").set(1)

    get_pt = os.popen('netstat -tnpl | grep nginx | cut -d ":" -f2 | cut -d " " -f1 | grep "' + PORT_WEBCLIENT + '"').read().strip()
    pt.labels("WEBCLIENT","LISTEN").set(1)

    get_pt = os.popen('netstat -tnpl | grep nginx | cut -d ":" -f2 | cut -d " " -f1 | grep "' + PORT_IMAPS + '"').read().strip()
    pt.labels("IMAPS","LISTEN").set(1)

    get_pt = os.popen('netstat -tnpl | grep nginx | cut -d ":" -f2 | cut -d " " -f1 | grep "' + PORT_POP3S + '"').read().strip()
    pt.labels("POP3S","LISTEN").set(1)


    # -----


    # get cpu, mem, iowait, uptime, df
    Gauge("zimbra_cpu_usage","CPU Usage:",registry=REGISTRY).set(psutil.cpu_percent())
    Gauge("zimbra_mem_usage","MEM Usage:",registry=REGISTRY).set(psutil.virtual_memory().percent)
    Gauge("zimbra_iowait","IO_Wait:",registry=REGISTRY).set(str(psutil.cpu_times_percent()).split(",")[4].split("=")[1].strip())
    Gauge("zimbra_uptime","Up Time:",registry=REGISTRY).set((time.time()-psutil.boot_time())/60/60/24)

    get_df = os.popen('df -h / | cut -d \" \" -f12').read().strip().replace("%","")
    zv = Gauge("zimbra_disk_usage","Disk Usage:",registry=REGISTRY).set(get_df)


    # get zimbra version
    get_zv = os.popen('/bin/su - zimbra -c "/opt/zimbra/bin/zmcontrol -v"').read().split(' ')[6].strip()[:-1].replace("_"," ")
    zv = Gauge("zimbra_version","Zimbra Version:",["version"],registry=REGISTRY)
    zv.labels(get_zv).set(0)


    # -----


    # get all accounts
    acc = Gauge("zimbra_account_status_total","Zimbra Account Status Total",["name"],registry=REGISTRY)
    os.popen('/bin/su - zimbra -c "/opt/zimbra/bin/zmaccts | grep -v \"spam.\" | grep -v \"virus-quarantine.\" | grep -v total > /tmp/zm_ex_accts.txt"')

    # active accounts
    get_acc = os.popen('cat /tmp/zm_ex_accts.txt | grep -v total | grep active | grep "@" | wc -l').read().strip()
    acc.labels("active").set(get_acc)

    # locked accounts
    get_acc = os.popen('cat /tmp/zm_ex_accts.txt | grep -v total | grep locked | grep "@" | wc -l').read().strip()
    acc.labels("locked").set(get_acc)

    # closed accounts
    get_acc = os.popen('cat /tmp/zm_ex_accts.txt | grep -v total | grep closed | grep "@" | wc -l').read().strip()
    acc.labels("closed").set(get_acc)

    # maintenance accounts
    get_acc = os.popen('cat /tmp/zm_ex_accts.txt | grep -v total | grep maintenance | grep "@" | wc -l').read().strip()
    acc.labels("maintenance").set(get_acc)

    # admin accounts
    get_acc = os.popen('/bin/su - zimbra -c "/opt/zimbra/bin/zmprov gaaa | wc -l"').read().strip()
    acc.labels("admin").set(get_acc)


    # -----


    # get zimbra service
    get_sv = os.popen('/bin/su - zimbra -c "/opt/zimbra/bin/zmcontrol status"').read().splitlines()
    sv = Gauge("zimbra_service_status","Zimbra Service Status",["name","status"],registry=REGISTRY)
    for i in range(len(get_sv)):

      sv_value = 0
      sv_name = get_sv[i][0:24].strip()
      sv_status = get_sv[i][25:].strip()

      if (get_sv[i][0:4].strip() != 'Host'):
        if (sv_status == 'Running'):
          sv_value = 1
        else:
          if (get_sv[i].find("Stopped") > 0):
            sv_name = get_sv[i][0:24].strip()
            sv_status = "Stopped"
          elif (get_sv[i].find("is not running") > 0):
            continue

        sv.labels(sv_name, sv_status).set(sv_value)


    # -----


    # get queue
    get_zmq = os.popen('/opt/zimbra/libexec/zmqstat').read().splitlines()
    zmq = Gauge("zimbra_queue","-",["name"],registry=REGISTRY)
    for i in range(len(get_zmq)):
      zmq.labels(get_zmq[i].split('=')[0].strip()).set(get_zmq[i].split('=')[1].strip())


    # -----


    return prometheus_client.generate_latest(REGISTRY)


    # -----


# metric route
app = Flask(__name__)
@app.route("/metrics")
def ApiResponse():
    return Response(getcheck(),mimetype="text/plain")

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=PORT_EXPORTER)
