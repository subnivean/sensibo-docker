#!/bin/env python
import sqlite3
from sensibo_client import SensiboClientAPI
import secrets

DEVICENAME = 'Living Room'
DBPATH = "../data/sensibodata.sqlite"
TBLNAME = f"housedata"

client = SensiboClientAPI(secrets.APIKEY)
uid = client.devices()[DEVICENAME]

ac_state = client.pod_ac_state(uid)
measurements = client.pod_measurement(uid)

# Convert fields as necessary
ts = ac_state['timestamp']['time'].split('.')[0].replace('T', ' ') + "+00:00"
power = 1 if ac_state['on'] is True else 0

data = dict(
        date=ts,
        power=power,
        mode=ac_state['mode'],
        settemp=ac_state['targetTemperature'],
        fanlevel=ac_state['fanLevel'],
        vswing=ac_state['swing'],
        hswing=ac_state['horizontalSwing'],
        meastemp=f"{measurements[0]['temperature'] * 9 / 5 + 32:.1f}",
        meashumidity=measurements[0]['humidity'],
        )

placeholders = ",".join(['?'] * len(data))

sql = f"""INSERT INTO {TBLNAME} VALUES ({placeholders})"""

with sqlite3.connect(DBPATH) as conn:
    cur = conn.cursor()
    cur.execute(sql, list(data.values()))
    conn.commit()

conn.close()