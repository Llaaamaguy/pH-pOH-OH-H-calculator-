from math import log10
from timeout import TimeOutException
import os

def alarm_handler(signum, frame):
  raise TimeOutException()

def H(frm, val):
  if frm == "OH":
     return (1*(10**-14))/val
  elif frm == "pH":
      return 10**(-val)

def pH(frm, val):
  if frm == "H":
    return -1*(log10(val))
  elif frm == "pOH":
    return 14-val

def pOH(frm, val):
  if frm == "pH":
    return 14-val
  elif frm == "OH":
    return -1*(log10(val))

def OH(frm, val):
  if frm == "pOH":
    return 10**(-1*val)
  elif frm == "H":
    return (1*(10**-14))/val

def isTwoStep(frm, to):
  if frm == "H":
    if to == "pOH":
      return True
  elif frm == "pH":
    if to == "OH":
      return True
  elif frm == "pOH":
    if to == "H":
      return True
  elif frm == "OH":
    if to == "pH":
      return True
  return False

clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')