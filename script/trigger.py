#!/usr/bin/env python3

import argparse
import os
import time

last_log = f'/home/sks/software/trig-control/last.log'

NumOfRegion2 = 6
BeamDetectors = ['BH1', 'T0', 'UpVeto', 'HTOF', 'Other1', 'Other2']
ScatDetectors = ['BEAM', 'AC', 'eeVeto', 'TOF-unused',
                 'TOF', 'Clock1kHz', 'M2D1', 'M2D2',
                 'M3D', 'BGO', 'CFT']

#______________________________________________________________________________
def is_updated(path, threshold):
  if not os.path.exists(path):
    return 0
  mtime = os.path.getmtime(path)
  current_time = time.time()
  if current_time - mtime <= threshold:
    return mtime
  else:
    return 0

#______________________________________________________________________________
def remove_escape(arg):
  arg = arg.replace(gray, '')
  arg = arg.replace(green, '')
  arg = arg.replace(magenta, '')
  arg = arg.replace(red, '')
  arg = arg.replace(cyan, '')
  arg = arg.replace(default, '')
  return arg

#______________________________________________________________________________
def bps(ctrl, coin):
  if ctrl == 0:
    return 'OFF'
  if coin == 0:
    return 'VETO'
  return 'ON'

#______________________________________________________________________________
def beam_bps(ctrl, coin):
  buf = ''
  for i, d in enumerate(BeamDetectors):
    b = bps((ctrl>>(len(BeamDetectors)-1-i))&1,
            (coin>>(len(BeamDetectors)-1-i))&1)
    if 'OFF' in b:
      continue
    elif 'VETO' in b:
      buf += cyan + '/'
    buf += d + default + 'x'
  if buf[-1:] == 'x':
    buf = buf[:-1]
  return buf

#______________________________________________________________________________
def scat_bps(ctrl, coin, beam):
  buf = ''
  for i, d in enumerate(ScatDetectors):
    b = bps((ctrl>>(len(ScatDetectors)-1-i))&1,
            (coin>>(len(ScatDetectors)-1-i))&1)
    if 'OFF' in b:
      continue
    elif 'VETO' in b:
      buf += cyan + '/'
    if i == 0:
      buf += beam + default + 'x'
    else:
      buf += d + default + 'x'
  if buf[-1:] == 'x':
    buf = buf[:-1]
  if len(buf) == 0:
    buf = red + 'N/A' + default
  return buf


#______________________________________________________________________________
def gate(val):
  if val == 0:
    return '-'
  elif val == 1:
    return 'on'
  elif val == 2:
    return 'off'
  elif val == 3:
    return 'on/off'
  else:
    return '-'

#______________________________________________________________________________
def onoff(val, char=False):
  on = '!' if char else 'ON '
  off = '.' if char else 'OFF'
  if val == 0:
    return f'{gray}{off}{default}'
  elif val == 1:
    return f'{green}{on}{default}'
  else:
    return ''

#______________________________________________________________________________
if __name__ == '__main__':
  mtime = is_updated(last_log, threshold=19)
  if mtime > 0:
    param = {}
    with open(last_log, 'r') as f:
      for line in f.readlines():
        line = line.split()
        if len(line) == 1 and line[0][0] != '#':
          param['param_file'] = line[0]
        if len(line) == 2 and line[0][0] != '#':
          param[line[0]] = int(line[1])
    if len(param) > 0:
      print('trigger ', end='')
      for key, val in param.items():
        print(f'{key}={val}', end=(f' {int(mtime*1e9)}\n' if key == 'RGN4::GATE' else ','))
