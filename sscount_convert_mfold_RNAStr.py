import os
import csv
import fileinput
import pandas as pd
from pathlib import Path
print("/n"*5)
undscr = "->"*30
print(undscr)
print("/n"+"WARNING: Previous files will be overwritten!  Save them in a "+"/n"+"different location than the current file, or rename them to "+"/n")
print(undscr)




filein = input("Enter the ct file path and name: ")
userpath = os.path.dirname(filein)
fname=Path(filein).stem
with open(filein,'r') as firstfile, open(userpath+'\\'+fname+'_new_input.txt','w') as ct_file:
    # read content from first file
    for line in firstfile:
             # append content to second file
             ct_file.write(line)

ct_file = userpath+'\\'+fname+'_new_input.txt'
strct = 0
with open(ct_file, 'r') as infile:
    for row in infile:
        if "ENERGY" in row:
            strct += 1
    #print (strct)
for lines in fileinput.FileInput(ct_file, inplace=1):
   lines2 = ",".join(lines.split())
   if lines == '': continue
   print (lines2)

with open(ct_file, 'r') as infile2, open(userpath+'\\'+fname+'_base_file.csv', 'w') as csv_file:
    reader = csv.reader(infile2)
    writer = csv.writer(csv_file, delimiter = ',', lineterminator = '/n')
    writer.writerow(["baseno","base","bs_bf", "bs_aft", "bs_bind", "base2"])
    for row in reader:
        if "ENERGY" not in row:
            writer.writerow(row)
            csv_file.flush() # whenever you want

mb_pick = pd.read_csv(userpath+'\\'+fname+'_base_file.csv', sep=',', usecols=[0,1,4], dtype=object)
mb_pick.to_csv(userpath+'\\'+fname+'_three_col.csv', index=False)

with open (userpath+'\\'+fname+'_three_col.csv', 'r') as infile3, open(userpath+'\\'+fname+'_sscount1.csv', 'w') as outfile3:
    cls = [[],[],[]]
    reader = csv.reader(infile3)
    for row in reader:
       for col in range (3):
           cls[col].append(row[col])
       base_nol = cls[0]
       basel = cls[1]
       sscntl = cls[2]

       sscntl = [1 if x == '0' else 0 for x in sscntl]

    writer = csv.writer(outfile3)
    rows = zip(base_nol, sscntl, basel )
    for row in rows:
        writer.writerow(row)

df = pd.read_csv(userpath+'\\'+fname+'_sscount1.csv')

df_grouped = df.groupby(['baseno', 'base'], as_index = False).sum()

a = pd.DataFrame(df_grouped)
a.to_csv(userpath+'\\'+fname+'_base_grouped.csv', index=False)

with open (userpath+'\\'+fname+'_base_grouped.csv', 'r') as infile4, open(userpath+'\\'+fname+'_sscount.txt', 'w') as outfile4:

    cls = [[],[],[]]
    reader = csv.reader(infile4)
    next(infile4)
    for row in reader:
        if "ENERGY" not in row:
            for col in range (3):
                cls[col].append(row[col])
                base_nol = cls[0]
                basel2 = cls[1]
                basel = [sub.replace('T', 'U') for sub in basel2]
                sscntl = cls[2]

    writer = csv.writer(outfile4, delimiter = ' ')
    writer.writerow([int(strct), ""])
    rows = zip(base_nol, sscntl, basel )
    for row in rows:
        writer.writerow(row)

os.remove(userpath+'\\'+fname+'_new_input.txt')
os.remove(userpath+'\\'+fname+'_base_file.csv')
os.remove(userpath+'\\'+fname+'_three_col.csv')
os.remove(userpath+'\\'+fname+'_sscount1.csv')
os.remove(userpath+'\\'+fname+'_base_grouped.csv')
