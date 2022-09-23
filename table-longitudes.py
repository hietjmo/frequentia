
import os
import csv
import sys
import numpy as np

csvfile = "freq-collection-1.csv"

def csv_file (typo,csvfile):
  basename = os.path.basename(csvfile)
  base = os.path.splitext(basename)[0]
  return f"csv/{typo}-{base}.csv"

def pdf_file (typo,csvfile):
  basename = os.path.basename(csvfile)
  base = os.path.splitext(basename)[0]
  return f"figures/{typo}-{base}.pdf"

def tex_file (typo,csvfile):
  basename = os.path.basename(csvfile)
  base = os.path.splitext(basename)[0]
  return f"md/{typo}-{base}.md"

def chunks (lst, n):
  "Yield successive n-sized chunks from lst."
  for i in range (0, len (lst), n):
    yield lst [i:i + n]

def split (a, n):
  k, m = divmod (len (a), n)
  return (a [i * k + min (i, m):(i + 1) * k + min (i + 1, m)] 
    for i in range (n))

longor = {}
unic = {}
monstros = [(0,"")]
cum = [(0,0)]
cumsum = 0


par_file = csv_file ("par","total")
tex_file1 = tex_file ("par","longitudes")
tex_file2 = tex_file ("par","longitudes-unic")
tex_file3 = tex_file ("par","cumultable")

with open (par_file) as f:
  reader = csv.reader (f,delimiter='\t')
  for i,row in enumerate (reader):
    k = len (row [0])
    v = int (row [1])
    cumsum += v
    cum.append ((i+1,cumsum))
    if k in longor:
      longor [k] += v
      unic [k] += 1
    else:
      longor [k] = v
      unic [k] = 1
    if k > monstros[0][0]:
      monstros.append ((k,row[0]))
      monstros.sort ()
      monstros = monstros [-30:]

print ("monstros =")
for i,j in monstros:
  print (f"{i:5} {j}")

longor_s = dict (sorted (longor.items ()))
unic_s = dict (sorted (unic.items ()))
totalP = sum (longor.values())
ratiosP = {str (k):n / totalP for (k,n) in longor_s.items()}
totalU = sum (unic.values())
ratiosU = {str (k):n / totalU for (k,n) in unic_s.items()}

# Table 1:

def table1 ():
  lon_rows = [(k, v) for (k,v) in ratiosP.items()]
  columns = split (lon_rows,5)
  with open (tex_file1, 'w') as f:
    f.write ("\\setlength{\\tabcolsep}{5pt}\n") # default = 6pt
    f.write ("\\begin{center}")
    for col in columns:
      f.write ("\\begin{tabular}[t]{ c l }\n")
      for a,b in col:
        f.write (f"{a} & {b:.4f} \\\\\n")
      f.write ("\end{tabular}\n")
    f.write ("\\end{center}")
  print ("Scribeva:", tex_file1)


# Table 2:

def table2 ():
  lon_rows = [(k, v) for (k,v) in ratiosU.items()]
  columns = split (lon_rows,5)
  with open (tex_file2, 'w') as f:
    f.write ("\\setlength{\\tabcolsep}{5pt}\n") # default = 6pt
    f.write ("\\begin{center}")
    for col in columns:
      f.write ("\\begin{tabular}[t]{ c l }\n")
      for a,b in col:
        f.write (f"{a} & {b:.4f} \\\\\n")
      f.write ("\end{tabular}\n")
    f.write ("\\end{center}")
  print ("Scribeva:", tex_file2)


# Table 3:

def table3 ():
  cumpart = [(a,b / totalP) for a,b in cum]
  old = -0.00001
  r = np.arange(0.0, 1.01, 0.05)
  s = set ()
  for i,j in cumpart:
    for k in r:
      if old <= k <= j: s.add ((i,j))
    old = j
  xs = list(s)
  xs.sort()
  columns = split (xs,5)
  with open (tex_file3, 'w') as f:
    f.write ("\\setlength{\\tabcolsep}{5pt}\n") # default = 6pt
    f.write ("\\begin{center}")
    for col in columns:
      f.write ("\\begin{tabular}[t]{ c l }\n")
      for a,b in col:
        f.write (f"{a} & {b:.2f} \\\\\n")
      f.write ("\end{tabular}\n")
    f.write ("\\end{center}")
  print ("Scribeva:", tex_file3)

if "1" in sys.argv: table1 ()
if "2" in sys.argv: table2 ()
if "3" in sys.argv: table3 ()



