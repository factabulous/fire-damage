# -*- coding: utf-8 -*-

import mats
import events
import os
import Tkinter as tk
import myNotebook as nb
from config import config
import sys
import Queue
import watcher
import visited
import plug
import heading
import requests
from sys import platform
from util import GridHelper

this = sys.modules[__name__]	# For holding module globals

window=tk.Tk()
window.withdraw()

bonds = { "marauder": 10000, "cyclops": 2000000, "basilisk": 6000000, "medusa": 10000000 }

def local_file(name):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), name)

def plugin_start():
    #this._IMG_CLIPBOARD = tk.PhotoImage(file = local_file('clipboard.gif'))
    return "FireDamage"

def plugin_stop():
    window.destroy()



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

def reportKill(cmdr, system, reward):
    pass

def reportBond(cmdr, system, reward):
    pass
   

def journal_entry(cmdr, is_beta, system, station, entry, state):
    if is_beta:
        return
    if entry['event'] == "FactionKillBond":
        if matches(entry, 'VictimFaction', '$faction_Thargoid') and 'Reward' in entry:
            reportKill(cmdr, system, entry['Reward')

    if entry['event'] == 'RedeemVoucher':
        if matches(entry, 'Faction', 'PilotsFederation') and matches(entry, 'Type', 'CombatBond'):
            
            reportBond(cmdr, system, entry['Amount'])

