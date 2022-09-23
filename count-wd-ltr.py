
import re
import csv
import sys
import os.path
import time
from collections import Counter

filelist = "file-list.txt"

p = re.compile (r'[a-zA-ZÀ-ÖØ-öø-ÿ]+')

def csv_file (typo,csvfile):
  basename = os.path.basename(csvfile)
  base = os.path.splitext(basename)[0]
  return f"csv/{typo}-{base}.csv"

def mc (filename):
  f = open (filename)
  try:
    text = f.read ()
  except: return []
  parolas = [wd.lower() for wd in p.findall (text)]
  cnt = Counter (parolas)
  return cnt.most_common ()

def count_frequency (txtfile):
  print ("Legeva:", txtfile)
  with open (txtfile) as f:
    content = f.read()
  contentlower = content.lower()
  contentlower = contentlower.replace ("\n"," ")
  ltrs = [c for c in contentlower if "a" <= c <= "z"]
  lit_cnt = Counter (ltrs)
  lit_mc = lit_cnt.most_common()
  lit_total = sum ([x [1] for x in lit_mc])
  lit_rows = [[k, v] for (k,v) in lit_mc]
  lit_file = csv_file ("lit",txtfile)

  with open (lit_file, 'w') as f:
    writer = csv.writer (f,delimiter='\t')
    writer.writerows (lit_rows)
  print ("Scribeva:", lit_file)

  parolas = [wd.lower() for wd in p.findall (content)]
  par_cnt = Counter (parolas)
  par_mc = par_cnt.most_common()
  par_total = sum ([x [1] for x in par_mc])
  par_rows = [[k, v] for (k,v) in par_mc]
  par_file = csv_file ("par",txtfile)

  with open (par_file, 'w') as f:
    writer = csv.writer (f,delimiter='\t')
    writer.writerows (par_rows)
  print ("Scribeva:", par_file)

  grammas = [a+b for a,b in zip (contentlower,contentlower[1:]) 
    if "a" <= a <= "z" and "a" <= b <= "z"]
  gr_cnt = Counter (grammas)
  gr_mc = gr_cnt.most_common()
  gr_total = sum ([x [1] for x in gr_mc])
  gr_rows = [[k, v] for (k,v) in gr_mc]
  gr_file = csv_file ("gr",txtfile)

  with open (gr_file, 'w') as f:
    writer = csv.writer (f,delimiter='\t')
    writer.writerows (gr_rows)
  print ("Scribeva:", gr_file)


def mod_date (filename):
  try:
    modTimesinceEpoc = os.path.getmtime (filename)
    modificationTime = time.strftime ('%Y-%m-%d %H:%M:%S', 
      time.localtime(modTimesinceEpoc))
    result = modificationTime
  except FileNotFoundError:
    result = ""
  return result

force = len (sys.argv) > 0 and "-f" in sys.argv

def check_mod (txtfile):
  lit_file = csv_file ("lit",txtfile)
  par_file = csv_file ("par",txtfile)
  gr_file = csv_file ("gr",txtfile)

  txt_mod = mod_date (txtfile)
  lit_mod = mod_date (lit_file)
  par_mod = mod_date (par_file)
  gr_mod = mod_date (gr_file)
  if lit_mod < txt_mod or par_mod < txt_mod or gr_mod < txt_mod or force: 
    count_frequency (txtfile)

with open (filelist) as f:
  reader = csv.reader (f,delimiter='\t')
  for row in reader:
    txtfile = row [0]
    if os.path.isfile (txtfile):
      check_mod (txtfile)
    else:
      print (f"Le file \"{txtfile}\" non existe.\n"
             f"Controla le lista de files \"{filelist}\"!")

