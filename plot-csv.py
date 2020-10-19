
import os
import csv
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.ticker as mtick
import numpy as np

font = 'tex gyre heros'  # an open type font
# font = "Liberation Sans"  # alternative to arial
# font = "Latin Modern Sans"
mpl.rcParams['font.sans-serif'] = font
mpl.rc('mathtext', fontset='custom', it=font + ':italic')
mpl.rc('font', size=9)  # change font size from default 10

# csvfile = "freq-collection-1.csv"

def csv_file (typo,csvfile):
  basename = os.path.basename(csvfile)
  base = os.path.splitext(basename)[0]
  return f"csv/{typo}-{base}.csv"

def pdf_file (typo,csvfile):
  basename = os.path.basename(csvfile)
  base = os.path.splitext(basename)[0]
  return f"figures/{typo}-{base}.pdf"

ltrs = []
amount = []

lit_file = csv_file ("lit","total")
pdffile = pdf_file ("lit","total")

with open (lit_file) as f:
  reader = csv.reader (f,delimiter='\t')
  for row in reader:
    ltrs.append (row [0].upper())
    amount.append (int (row [1]))

total = sum (amount)
ratios = [n / total for n in amount]

f = plt.figure (figsize=(5.66,2.5))

bars = plt.bar (
  x=ltrs, height=ratios, color=(1,1,1,1), linewidth=1.0, 
  edgecolor='black')

bottom, top = plt.ylim ()
plt.ylim (top=top + 0.01)
plt.yticks(np.arange(0,0.16,0.03))
for rect, label in zip (bars, ltrs):
  height = rect.get_height()
  x = rect.get_x () + rect.get_width () / 2
  y = height + 0.0015
  plt.text (x, y, label, ha='center', va='bottom')

plt.tick_params (bottom=False,labelbottom=False)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['top'].set_visible(False)
plt.gca().yaxis.set_major_formatter(mtick.FormatStrFormatter('%.2f'))
f.savefig (pdffile, bbox_inches='tight')
print ("Scribeva:", pdffile)
plt.show ()



