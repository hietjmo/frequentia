
import os
import csv

def csv_file (typo,csvfile):
  basename = os.path.basename(csvfile)
  base = os.path.splitext(basename)[0]
  return f"csv/{typo}-{base}.csv"

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

ltrs = []
amount = []

lit_file = csv_file ("lit","total")
partes_file = csv_file ("lit","partes")
tex_file = tex_file ("lit","partes")


with open (lit_file) as f:
  reader = csv.reader (f,delimiter='\t')
  for row in reader:
    ltrs.append (row [0].upper())
    amount.append (int (row [1]))

total = sum (amount)
ratios = [n / total for n in amount]
lit_rows = [[k, v] for (k,v) in zip (ltrs,ratios)]
with open (partes_file, 'w') as f:
  writer = csv.writer (f,delimiter='\t')
  writer.writerows (lit_rows)
print ("Scribeva:", partes_file)

def in_toto ():
 x = f"{total:_}".replace("_", " ")
 return f"In toto **{x}** litteras.\\\n"

litordine = " ".join (chunks ("".join (ltrs),5))

ordinefile = "litteras-in-ordine.txt"
with open (ordinefile, 'w') as g:
  g.write ("".join (ltrs))
print ("Scribeva", "".join (ltrs), "to:", ordinefile)

columns = split (lit_rows,6)
with open (tex_file, 'w') as f:
  f.write (in_toto ())
  f.write (f"In ordine: {litordine}.\n\n")
  f.write ("\\setlength{\\tabcolsep}{5pt}\n") # default = 6pt
  f.write ("\\begin{center}")
  for col in columns:
    f.write ("\\begin{tabular}[t]{ c l }\n")
    for a,b in col:
      f.write (f"{a} & {b:.4f} \\\\\n")
    f.write ("\end{tabular}\n")
  f.write ("\\end{center}")
print ("Scribeva:", tex_file)



