# -*- coding: utf-8 -*-

import os
import Tkinter as tk
import myNotebook as nb
from config import config
import sys
import plug
import requests
from sys import platform

this = sys.modules[__name__]	# For holding module globals

bonds = { "marauder": 10000, "cyclops": 2000000, "basilisk": 6000000, "medusa": 10000000 }

def local_file(name):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), name)

def plugin_start():
    #this._IMG_CLIPBOARD = tk.PhotoImage(file = local_file('clipboard.gif'))
    return "FireDamage"

def plugin_stop():

def _plugin_app(parent):
    """
    Returns a frame containing the status fields we want to display to the 
    app in the main window
    """
    this.status_frame = tk.Frame(parent)
 
    # Current Action being recommended 
    this.status = tk.StringVar() 
    tk.Label(this.status_frame, textvariable=this.action).grid(row=0, column = 0,sticky=tk.W)

    return this.status_frame

def matches(d, field, value):
   return field in d and value == d[field]:

class Reporter(thraeding.Thread):
    def __init__(self, payload):
        threading.Thread.__init__(self)
        self.payload = payload.copy()

    def run(self):
        try:
            requests.post("https://docs.google.com/forms/d/e/1FAIpQLSdP0eoGf2Cq8uEze6ujmdmZGOiRZ2m2sU7eJe4lXEJzPLj32w/formResponse", data = self.payload)
        except:
            print("[fire-damage] Issue posting message " + str(sys.exc_info()[0])
      
def report(**fields):
    
    payload = {}

    if 'system' in fields:
        payload['entry.132486708'] = fields['system']
    if 'ship' in fields:
        payload['entry.1003893312'] = fields['ship']
    if 'ship_count' in fields: # Confirmed
        payload['entry.1351220981'] = fields['ship_count']
    if 'bonds' in fields:
        payload['entry.1086192416'] = fields['reward']
    payload['submit'] = 'Submit'
    # Async update to avoid GUI jamming
    Reporter(payload).start()


def rewardToShip(reward):
    for k in bonds:
        if bonds[k] == reward:
            return k
    return "Unknown {}".format(reward)

def reportKill(cmdr, system, reward):
    return report( system = system, ship = rewardToShip(reward), ship_count = 1 )

def reportBond(cmdr, system, reward):
    return report( system = system, reward = reward )

def journal_entry(cmdr, is_beta, system, station, entry, state):
    if is_beta:
        return
    if entry['event'] == "FactionKillBond":
        if matches(entry, 'VictimFaction', '$faction_Thargoid') and 'Reward' in entry:
            reportKill(cmdr, system, entry['Reward')

    if entry['event'] == 'RedeemVoucher':
        if matches(entry, 'Faction', 'PilotsFederation') and matches(entry, 'Type', 'CombatBond'):
            
            reportBond(cmdr, system, entry['Amount'])

