import csv
import os.path
from collections import Counter

filelist = "file-list.txt"

def csv_file (typo,csvfile):
  basename = os.path.basename(csvfile)
  base = os.path.splitext(basename)[0]
  return f"csv/{typo}-{base}.csv"

def one_result (csvfile):
  with open (csvfile) as f:
    reader = csv.reader (f,delimiter='\t')
    parolas = []
    amount = []
    for row in reader:
      parolas.append (row [0])
      amount.append (int (row [1]))
  return Counter (dict (zip (parolas,amount)))

ffre = []

with open (filelist) as f:
  reader = csv.reader (f,delimiter='\t')
  cnt = Counter()
  for row in reader:
    txtfile = row [0]
    par_file = csv_file ("par",txtfile)
    onre = one_result (par_file)
    cnt = cnt + onre
    basename = os.path.basename(txtfile)
    base = os.path.splitext(basename)[0]
    ffre.append ([base,sum (onre.values())])
  print (cnt.most_common (30))
  print ("Total:", sum(cnt.values())) 
  par_cnt = cnt
  par_mc = par_cnt.most_common()
  par_total = sum ([x [1] for x in par_mc])
  par_rows = [[k, v] for (k,v) in par_mc]
  par_file = csv_file ("par","total")
  with open (par_file, 'w') as f:
    writer = csv.writer (f,delimiter='\t')
    writer.writerows (par_rows)
  print ("Scribeva:", par_file)

fontesfile = "csv/par-fontes.csv"
with open (fontesfile, 'w') as ff:
  writer = csv.writer (ff,delimiter='\t')
  writer.writerows (ffre)
  #print (ffre)
  print ("Scribeva:", fontesfile)

