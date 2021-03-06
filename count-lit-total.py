import csv
import os.path
from collections import Counter

filelist = "file-list.txt"

def csv_file (typo,csvfile):
  basename = os.path.basename(csvfile)
  base = os.path.splitext(basename)[0]
  return f"csv/{typo}-{base}.csv"

ltrs = []
amount = []

def one_result (csvfile):
  with open (csvfile) as f:
    reader = csv.reader (f,delimiter='\t')
    ltrs = []
    amount = []
    for row in reader:
      ltrs.append (row [0].upper())
      amount.append (int (row [1]))
  return Counter (dict (zip (ltrs,amount)))

ffre = []

with open (filelist) as f:
  reader = csv.reader (f,delimiter='\t')
  cnt = Counter()
  for row in reader:
    txtfile = row [0]
    lit_file = csv_file ("lit",txtfile)
    onre = one_result (lit_file)
    cnt = cnt + onre
    basename = os.path.basename(txtfile)
    base = os.path.splitext(basename)[0]
    ffre.append ([base,sum (onre.values())])
  print (cnt.most_common())
  print ("Total:", sum(cnt.values())) 
  lit_cnt = cnt
  lit_mc = lit_cnt.most_common()
  lit_total = sum ([x [1] for x in lit_mc])
  lit_rows = [[k, v] for (k,v) in lit_mc]
  lit_file = csv_file ("lit","total")
  with open (lit_file, 'w') as f:
    writer = csv.writer (f,delimiter='\t')
    writer.writerows (lit_rows)
  print ("Scribeva:", lit_file)

fontesfile = "csv/lit-fontes.csv"
with open (fontesfile, 'w') as ff:
  writer = csv.writer (ff,delimiter='\t')
  writer.writerows (ffre)
  #print (ffre)
  print ("Scribeva:", fontesfile)

