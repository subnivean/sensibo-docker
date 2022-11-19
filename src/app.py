#!/bin/env python
import os
import sys
from pathlib import Path
from sensibo_client import SensiboClientAPI

import secrets

DEVICENAME = 'Living Room'

OUTFILE = Path('../data/sensibo_readings.log')
 
client = SensiboClientAPI(secrets.APIKEY)
uid = client.devices()[DEVICENAME]

ac_state = client.pod_ac_state(uid)
measurements = client.pod_measurement(uid)

ts = ac_state['timestamp']['time'].split('.')[0].replace('T', ' ') + "+00:00"

data = dict(
        date=ts,
        on=ac_state['on'],
        mode=ac_state['mode'],
        settemp=ac_state['targetTemperature'],
        fanlevel=ac_state['fanLevel'],
        vswing=ac_state['swing'],
        hswing=ac_state['horizontalSwing'],
        meastemp=f"{measurements[0]['temperature'] * 9 / 5 + 32:.1f}",
        meashumidity=measurements[0]['humidity'],
        )

if not OUTFILE.is_file():
    OUTFILE.write_text(','.join(list(data.keys())) + '\n')

if os.isatty(sys.stdin.fileno()):  # ie not running under cron
    #print(list(data.values()))
    print(",".join(str(e) for e in data.values()))
else:
    #print("Hello, CRON!")
    pass

with OUTFILE.open('a') as fh:
    fh.write(",".join(str(e) for e in data.values()) + '\n')
