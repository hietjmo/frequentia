
import os
import sys
import csv
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.ticker as mtick
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
import scipy.interpolate as spy
import numpy as np

# font = "Liberation Sans"  # alternative to arial
# font = "NimbusSansL"
font = 'tex gyre heros'  # an open type font

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
cum = [(0,0)]
cumsum = 0

par_file = csv_file ("par","total")
pdffile1 = pdf_file ("par","longitudes")
pdffile2 = pdf_file ("par","longitudes-unic")
pdffile3 = pdf_file ("par","cumulative")

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

longor_s = dict (sorted (longor.items ()))
unic_s = dict (sorted (unic.items ()))
totalP = sum (longor.values())
ratiosP = {str (k):n / totalP for (k,n) in longor_s.items()}
totalU = sum (unic.values())
ratiosU = {str (k):n / totalU for (k,n) in unic_s.items()}

# Figure 1:

def figure1 ():
  f = plt.figure (figsize=(5.66,2.5))
  
  bars = plt.bar (
    x=ratiosP.keys(), height=ratiosP.values(), color=(1,1,1,1), linewidth=1.0, 
    edgecolor='black')
  
  bottom, top = plt.ylim ()
  plt.ylim (top=top + 0.01)
  plt.yticks(np.arange(0,0.30,0.05))
  for rect, label in zip (bars, ratiosP.keys()):
    height = rect.get_height()
    x = rect.get_x () + rect.get_width () / 2
    y = height + 0.0015
    plt.text (x, y, label, ha='center', va='bottom')
  
  plt.tick_params (bottom=False,labelbottom=False)
  plt.gca().spines['right'].set_visible(False)
  plt.gca().spines['top'].set_visible(False)
  plt.gca().yaxis.set_major_formatter(mtick.FormatStrFormatter('%.2f'))
  f.savefig (pdffile1, bbox_inches='tight')
  print ("Scribeva:", pdffile1)

  plt.show ()

# Figure 2:
def figure2 ():
  f = plt.figure (figsize=(5.66,2.5))
  
  bars = plt.bar (
    x=ratiosU.keys(), height=ratiosU.values(), color=(1,1,1,1), linewidth=1.0, 
    edgecolor='black')
  
  bottom, top = plt.ylim ()
  plt.ylim (top=top + 0.01)
  plt.yticks(np.arange(0,0.17,0.05))
  for rect, label in zip (bars, ratiosP.keys()):
    height = rect.get_height()
    x = rect.get_x () + rect.get_width () / 2
    y = height + 0.0015
    plt.text (x, y, label, ha='center', va='bottom')
  
  plt.tick_params (bottom=False,labelbottom=False)
  plt.gca().spines['right'].set_visible(False)
  plt.gca().spines['top'].set_visible(False)
  plt.gca().yaxis.set_major_formatter(mtick.FormatStrFormatter('%.2f'))
  f.savefig (pdffile2, bbox_inches='tight')
  print ("Scribeva:", pdffile2)
  plt.show ()

# Figure 3:
def figure3 ():
  xs = [a for a,b in cum]
  ys = [b / totalP for a,b in cum]
  xs_new = np.linspace (min(xs), max(xs), 300)
  ys_smooth = spy.make_interp_spline (xs,ys)
  ys_new = ys_smooth (xs_new)
  f = plt.figure (figsize=(5,5))
  plt.gca().spines['right'].set_visible(False)
  plt.gca().spines['top'].set_visible(False)

  plt.plot (xs_new, ys_new, 'k')
  f.savefig (pdffile3, bbox_inches='tight')
  print ("Scribeva:", pdffile3)
  plt.show ()

# Figure 4:
def figure4 ():
  xs = [a for a,b in cum]
  ys = [b / totalP for a,b in cum]
  xs_new = np.linspace (min(xs), max(xs), 300)
  ys_smooth = spy.make_interp_spline (xs,ys)
  ys_new = ys_smooth (xs_new)
  fig, ax = plt.subplots(figsize=[5, 4])
  ax.tick_params(bottom=False, top=True, labelbottom=False, labeltop=True)
  # f = plt.figure (figsize=(5,5))
  plt.gca().spines['right'].set_visible(False)
  plt.gca().spines['bottom'].set_visible(False)
  plt.plot (xs_new, ys_new, 'k')

  #axins = inset_axes(ax, 1,1 , loc=2, bbox_to_anchor=(200, 220))
  axins = ax.inset_axes([0.4, 0.0, 0.60, 0.8])
  #axins = inset_axes(ax, 1,1 , loc=2, bbox_to_anchor=(0.35, 0.35))
  axins.set_xlim(0, 10000) 
  axins.set_ylim(0.65, 0.95) 
  axins.yaxis.tick_right()
  axins.grid (True)
  mark_inset(ax, axins, loc1=1, loc2=3, fc="none", ec="0.5")
  axins.plot(xs_new, ys_new, 'k')
  fig.savefig (pdffile3, bbox_inches='tight')
  print ("Scribeva:", pdffile3)
  plt.show ()

def figure5 ():
  fig, ax = plt.subplots()
  ax.plot(range(10))
  #axin1 = ax.inset_axes([0.8, 0.1, 0.15, 0.15])
  axin1 = ax.inset_axes([0.2, 0.1, 0.65, 0.45])
  axin2 = ax.inset_axes(
          [5, 7, 2.3, 2.3], transform=ax.transData)
  axin1.plot ()
  plt.show ()

if "1" in sys.argv: figure1 ()
if "2" in sys.argv: figure2 ()
if "3" in sys.argv: figure3 ()
if "4" in sys.argv: figure4 ()
if "5" in sys.argv: figure5 ()
