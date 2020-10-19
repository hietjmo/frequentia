
f = open ("input2.txt")
ys = f.readlines ()
xs = [x.rstrip() for x in ys]

d = 3

for x in xs:
  print (f"file 'png/{x}'")
  print (f"duration {d}")
print (f"file 'png/{xs[-1]}'")

