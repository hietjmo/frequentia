import csv
import os.path
from math import floor
from collections import Counter

filelist = "file-list.txt"

def csv_file (typo,csvfile):
  basename = os.path.basename(csvfile)
  base = os.path.splitext(basename)[0]
  return f"csv/{typo}-{base}.csv"

def one_result (csvfile):
  with open (csvfile) as f:
    reader = csv.reader (f,delimiter='\t')
    grammas = []
    amount = []
    for row in reader:
      grammas.append (row [0])
      amount.append (int (row [1]))
  return Counter (dict (zip (grammas,amount)))

ffre = []

with open (filelist) as f:
  reader = csv.reader (f,delimiter='\t')
  cnt = Counter()
  for row in reader:
    txtfile = row [0]
    gr_file = csv_file ("gr",txtfile)
    onre = one_result (gr_file)
    cnt = cnt + onre
    basename = os.path.basename(txtfile)
    base = os.path.splitext(basename)[0]
    ffre.append ([base,sum (onre.values())])
  print (cnt.most_common (30))
  print ("Total:", sum(cnt.values())) 
  gr_cnt = cnt
  gr_mc = gr_cnt.most_common()
  gr_total = sum ([x [1] for x in gr_mc])
  gr_rows = [[k, floor (1_000_000 * v / gr_total)] for (k,v) in gr_mc]
  gr_file = "csv/gr-total-ppm.csv"
  with open (gr_file, 'w') as f:
    writer = csv.writer (f,delimiter='\t')
    writer.writerows (gr_rows)
  print ("Scribeva:", gr_file)

fontesfile = "csv/gr-fontes.csv"
with open (fontesfile, 'w') as ff:
  writer = csv.writer (ff,delimiter='\t')
  writer.writerows (ffre)
  #print (ffre)
  print ("Scribeva:", fontesfile)

