import csv
import os.path

filelist = "file-list.txt"

par_file = "csv/par-fontes.csv"
lit_file = "csv/lit-fontes.csv"

def csv_file (typo,csvfile):
  basename = os.path.basename(csvfile)
  base = os.path.splitext(basename)[0]
  return f"csv/{typo}-{base}.csv"

def one_result (csvfile):
  with open (csvfile) as f:
    reader = csv.reader (f,delimiter='\t')
    k = []
    v = []
    for row in reader:
      k.append (row [0])
      v.append (int (row [1]))
  return dict (zip (k,v))

onre_lit = one_result (lit_file)
onre_par = one_result (par_file)

table1 = [(d,onre_lit [d],onre_par [d]) for d in onre_lit]
table1.sort(key = lambda x: x[1],reverse=True)
table = [(str (i+1), a,str (b),str (c),f"{(b/c):.2f}") 
  for i,(a,b,c) in enumerate (table1)]
print (table)

tex_file = "fulltext/fontes.txt"

with open (tex_file, 'w') as f:
  for a,b,c,d,e in table:
    f.write (f"{a}. {b}: {d} parolas. \n")
  print ("Scribeva:", tex_file)

"""
fontesfile = "csv/fontes-lit-par.csv"
with open (fontesfile, 'w') as ff:
  writer = csv.writer (ff,delimiter='\t')
  writer.writerows (ffre)
  #print (ffre)
  print ("Scribeva:", fontesfile)
"""

