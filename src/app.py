#!/bin/env python
import sqlite3
from sensibo_client import SensiboClientAPI
import secrets
from tenacity import retry, wait_fixed, stop_after_attempt

DEVICENAME = "Living Room"
DBPATH = "../data/sensibodata.sqlite"
TBLNAME = f"housedata"


@retry(wait=wait_fixed(2), stop=stop_after_attempt(10))
def get_client():
    return SensiboClientAPI(secrets.APIKEY)


@retry(wait=wait_fixed(2), stop=stop_after_attempt(10))
def get_uid(client):
    return client.devices()[DEVICENAME]


@retry(wait=wait_fixed(2), stop=stop_after_attempt(10))
def get_ac_state(client, uid):
    return client.pod_ac_state(uid)


@retry(wait=wait_fixed(2), stop=stop_after_attempt(10))
def get_measurements(client, uid):
    return client.pod_measurement(uid)


client = get_client()
uid = get_uid(client)
ac_state = get_ac_state(client, uid)
measurements = get_measurements(client, uid)

# Convert fields as necessary
ts = ac_state["timestamp"]["time"].split(".")[0].replace("T", " ") + "+00:00"
power = 1 if ac_state["on"] is True else 0

data = dict(
    date=ts,
    power=power,
    mode=ac_state["mode"],
    settemp=ac_state["targetTemperature"],
    fanlevel=ac_state["fanLevel"],
    vswing=ac_state["swing"],
    hswing=ac_state["horizontalSwing"],
    meastemp=f"{measurements[0]['temperature'] * 9 / 5 + 32:.1f}",
    meashumidity=measurements[0]["humidity"],
)

placeholders = ",".join(["?"] * len(data))

sql = f"""INSERT INTO {TBLNAME} VALUES ({placeholders})"""

with sqlite3.connect(DBPATH) as conn:
    cur = conn.cursor()
    cur.execute(sql, list(data.values()))
    conn.commit()

conn.close()
