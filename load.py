# -*- coding: utf-8 -*-

import os
import Tkinter as tk
import sys
import threading
import requests
from config import config
import time
import re

this = sys.modules[__name__]	# For holding module globals

this.version = "0.0.1"
this.new_version = version
this.kill_count = 0
this.bond_count = 0

def debug(msg):
    pass

def plugin_start():
    last_version_check = float(config.get("firedamage.vcheck") or "0")
    now = time.time()
    if now > last_version_check + 24 * 3600:
        debug("Checking for a new version")
        config.set("firedamage.vcheck", str(now))
        src = requests.get("https://raw.githubusercontent.com/factabulous/fire-damage/master/load.py").text
        for line in src.split("\n"):
            if line.startswith("version = "):
                debug("Found a line <" + line + ">")
                res = re.match(r'^version\s*=\s*"(\d+\.\d+\.\d+)"', line)
                if res:
                    this.new_version = res.group(1)
                    debug("New version = {}".format(this.new_version))
                break
        
    return "FireDamage"

def plugin_stop():
    pass

def plugin_app(parent):
    """
    Returns a frame containing the status fields we want to display to the 
    app in the main window
    """
    this.status_frame = tk.Frame(parent)
 
    # Current Action being recommended 
    this.status = tk.StringVar() 
    if this.new_version != this.version:
        this.status.set("New version of the fire-damage plugin available")
        debug("Reported new version to GUI")
    tk.Label(this.status_frame, textvariable=this.status).grid(row=0, column = 0,sticky=tk.W)

    return this.status_frame

def matches(d, field, value):
   return field in d and value == d[field]

class Reporter(threading.Thread):
    def __init__(self, payload):
        threading.Thread.__init__(self)
        self.payload = payload.copy()

    def run(self):
        try:
            requests.post("https://docs.google.com/forms/d/e/1FAIpQLSdP0eoGf2Cq8uEze6ujmdmZGOiRZ2m2sU7eJe4lXEJzPLj32w/formResponse", data = self.payload)
            debug("[fire-damage] After post")
        except:
            print("[fire-damage] Issue posting message " + str(sys.exc_info()[0]))
      
def report(**fields):
    
    payload = {}

    if 'system' in fields:
        payload['entry.132486708'] = fields['system']
    if 'ship' in fields:
        payload['entry.1003893312'] = fields['ship']
        debug('[fire-damage] ship : ' + fields['ship'])
    if 'ship_count' in fields: # Confirmed
        payload['entry.1351220981'] = fields['ship_count']
        this.kill_count = this.kill_count + fields['ship_count']
    if 'bonds' in fields:
        payload['entry.1086192416'] = fields['bonds']
        this.bond_count = this.bond_count + fields['bonds']
    this.status.set("{} kills, {} CR bonds redeemed this session".format(this.kill_count, this.bond_count))
    payload['submit'] = 'Submit'
    debug("[fire-damage] Reporting a Thargoid state {}".format(payload))
    # Async update to avoid GUI jamming
    Reporter(payload).start()


def rewardToShip(reward):
    bonds = { "Scout": 10000, "Cyclops": 2000000, "Basilisk": 6000000, "Medusa": 10000000 }
    for k in bonds:
        if bonds[k] == reward:
            return k
    print("[fire-damage] Unrecognised reward level {}".format(reward))
    return "Unknown {}".format(reward)

def reportKill(cmdr, system, reward):
    return report( system = system, ship = rewardToShip(reward), ship_count = 1 )

def reportBond(cmdr, system, reward):
    return report( system = system, bonds = reward )

def journal_entry(cmdr, is_beta, system, station, entry, state):
    if is_beta:
        return
    if entry['event'] == "FactionKillBond":
        debug("[fire-damage] Bond")
        if matches(entry, 'VictimFaction', '$faction_Thargoid;') and 'Reward' in entry:
            reportKill(cmdr, system, entry['Reward'])

    if entry['event'] == 'RedeemVoucher':
        debug("[fire-damage] RedeemBond")
        if matches(entry, 'Faction', 'PilotsFederation') and matches(entry, 'Type', 'CombatBond'):
            
            reportBond(cmdr, system, entry['Amount'])

