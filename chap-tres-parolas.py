import csv
import os.path


par_file = "csv/par-total.csv"

par = []
amount = []

with open (par_file) as f:
  reader = csv.reader (f,delimiter='\t')
  for row in reader:
    par.append (row [0])
    amount.append (int (row [1]))

total = sum (amount)
unic = len (par)

def in_toto ():
 x = f"{total:_}".replace("_", " ")
 y = f"{unic:_}".replace("_", " ")
 return f"In toto **{x}** parolas, ex illes **{y}** parolas differente.\\\n\n"

tex_file = "md/chap-tres-parolas.md"

with open (tex_file, 'w') as f:
  f.write (in_toto())
  print ("Scribeva:", tex_file)


"""
fontesfile = "csv/fontes-lit-par.csv"
with open (fontesfile, 'w') as ff:
  writer = csv.writer (ff,delimiter='\t')
  writer.writerows (ffre)
  #print (ffre)
  print ("Scribeva:", fontesfile)
"""

