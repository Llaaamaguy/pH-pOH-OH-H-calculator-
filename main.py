from math import log10
from parser import eval_expr
import signal
from timeout import TimeOutException
from utils import *
from sigfig import round

sigfigs = 4

def main(sigfigs):
  defstr = f"FORMAT: (value) (from) (to)\nEx: 2.75 pH pOH\nEx2: (8.34*10**-5) H pH\n\n(Only put a value in parentheses if it is an equation such as 1*10**-3)\n\nCONSOLE COMMANDS:\nclear : Clears console\nsigfig (digits) : Set number of sigfigs to your value\n\nKEY:\n* = Multiplication\n** Denotes exponent\n/ = Division\n+ = Addition\n- = Subtraction\n\nSigFigs: {sigfigs}\n"
  print(defstr)
  
  valid = ["H", "pH", "pOH", "OH"]
  
  while True:
    v = True
    r = []
    problem = input("Enter problem: ")
    parsed = problem.split(" ")

    if problem == "clear":
      clear()
      print(defstr)
    elif parsed[0] == "sigfig":
      sigfigs = int(parsed[1])
      clear()
      defstr = f"FORMAT: (value) (from) (to)\nEx: 2.75 pH pOH\nEx2: (8.34*10**-5) H pH\n\n(Only put a value in parentheses if it is an equation such as 1*10**-3)\n\nCONSOLE COMMANDS:\nclear : Clears console\nsigfig (digits) : Set number of sigfigs to your value\n\nKEY:\n* = Multiplication\n** Denotes exponent\n/ = Division\n+ = Addition\n- = Subtraction\n\nSigFigs: {sigfigs}\n"
      print(defstr)
  
    else:
      if len(parsed) == 3:
        if parsed[0][0] != "(":
          try:
            float(parsed[0])
          except ValueError:
            v = False
            r.append("Problem with value")
          if parsed[1] == parsed[2]:
            v = False
            r.append("Args (from) and (to) cannot be the same")
        else:
          if parsed[1] not in valid:
            v = False
            r.append("Invalid (from)")
          elif parsed[2] not in valid:
            v = False
            r.append("Invalid (to)")
          else:
            signal.signal(signal.SIGALRM, alarm_handler)
            signal.alarm(3)
            try:
              exp = eval_expr(parsed[0][1:-1])
              log10(exp)
            except (TimeOutException, ZeroDivisionError, SyntaxError, ValueError) as exc:
              v = False
              exc = exc.__class__
              if exc == TimeOutException:
                r.append("Value is too large/computationally expensive")
              elif exc == ZeroDivisionError:
                r.append("Cannot divide by zero")
              elif exc == SyntaxError:
                r.append("Syntax Error")
              elif exc == ValueError:
                r.append("Probelm with value")
            signal.alarm(0)
      else:
        v = False
        r.append("Not enough/too many arguments passed")
    
      if v:
        if parsed[0][0] == "(":
          parsed[0] = exp
        else:
          parsed[0] = float(parsed[0])
      
        val = parsed[0]
        frm = parsed[1]
        to = parsed[2]
        ans = None
        
        if not isTwoStep(frm, to):
          if to == "H":
            ans = H(frm, val)
          elif to == "pH":
            ans = pH(frm, val)
          elif to == "pOH":
            ans = pOH(frm, val)
          elif to == "OH":
            ans = OH(frm, val)
        else:
          if to == "H":
            pHval = pH(frm, val)
            ans = H("pH", pHval)
          elif to == "pH":
            Hval = H(frm, val)
            ans = pH("H", Hval)
          elif to == "pOH":
            pHval = pH(frm, val)
            ans = pOH("pH", pHval)
          elif to == "OH":
            pOHval = pOH(frm, val)
            ans = OH("pOH", pOHval)
      
        if ans:
          print(f"Answer: {round(ans, sigfigs=sigfigs)}\n")
      else:
        print("INVALID PROBLEM:")
        for x in r:
          print(x)
        print("\n")

if __name__ == "__main__":
  main(sigfigs)
