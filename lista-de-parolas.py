import csv
import os.path
import itertools

par_file = "csv/par-total.csv"

par = []
amount = []

with open (par_file) as f:
  reader = csv.reader (f,delimiter='\t')
  for row in reader:
    n = int (row [1])
    if n >= 5:
      par.append (row [0])
      amount.append (n)

total = sum (amount)
unic = len (par)


def chunks (lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range (0, len (lst), n):
        yield lst [i:i + n]

def split (a, n):
  k, m = divmod (len (a), n)
  return (a [i * k + min (i, m):(i + 1) * k + min (i + 1, m)] 
    for i in range (n))

cols_fst = 29
cols_rest = 49

def formulate (m):
  if not m:
    return ""
  else:
    goal = 23
    # print ("m = ", m)
    mw,i,a,b = m
    b = " " + str (b)
    d1 = str (i+1)
    d2 = (mw-len (d1)) * " " + d1 + " "
    g = len (b) + len (d2)
    return d2 + a [:goal-g] + (goal - (g + len(a))) * " " + b

def maxwidth (c):
  return max ([len (str (i)) for (i,(a,b)) in c])

def transpose (lst):
  # return map (list, zip (*matrix))
  return [
    list(t) for t in itertools.zip_longest(*lst, fillvalue="")]

tex_file = "md/lista-de-parolas.md"

outfile = open (tex_file,"w")
wds = list (enumerate (zip (par,amount)))
outfile.write (f"\n# Frequentia de parolas\n\n")
pages = [wds [:3*cols_fst]] + list (
  chunks (wds [3*cols_fst:],3*cols_rest))
# print ("pages =", pages)
for nro,pg in enumerate (pages):
  if nro == 0:
    # columns = list (chunks (pg,cols_fst))
    columns = list (split (pg,3))
  else:
    # columns = list (chunks (pg,cols_rest))
    columns = list (split (pg,3))
  # print ("pg =", pg)
  outfile.write (
   "\\begin{Verbatim}[fontsize=\\small,baselinestretch=0.85,"
   + "commandchars=\\\\\\{\\}]\n")
  # print (columns)
  columns = [[(maxwidth(c),i,a,b) for (i,(a,b)) in c] 
             for c in columns]
  rows = transpose (columns)
  for m in rows:
    out = " ".join (map (formulate, m))
    outfile.write (f"{out}\n")
  outfile.write ("\\end{Verbatim} \n")
print ("Scribeva:", tex_file)

