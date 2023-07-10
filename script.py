import csv
import os
from openpyxl import load_workbook

cd = os.getcwd()
files = os.listdir(cd)
excelFile = []
for file in files:
    ext = os.path.splitext(file)[1]
    if ext == '.txt':
        textFile = file
    if ext == '.xlsx':
        excelFile.append(file)

rtxtf = open(textFile, 'r')
csvFile = 'output.csv'
with open(csvFile, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Column 1', 'Keyword 1', 'AND', 'Column 2', 'Keyword 2', 'AND', 'Column 3', 'Keyword 3', 'AND NOT', 'Column 4', 'Keyword 4', 'Then'])
    line = rtxtf.readline()
    hashset = set()
    while line:
        if not line.startswith("if") and not line.startswith("else"):
            line = rtxtf.readline()
            continue
        else:
            if line.startswith("if"):
                line = "else " + line
            if (line.lower() in hashset):
                line = rtxtf.readline()
                line = rtxtf.readline()
            else:
                hashset.add(line.lower())
                col4 = ""
                kw4 = ""
                if (line.find("and not") != -1):
                    notline = line[line.find("and not"):]
                    col4 = notline[notline.find("#\"")+2:notline.find("\"]")]
                    kw4 = notline[notline.find("\"]")+5:notline.find("\")")]
                    line = line[:line.find("and not")]
                col1 = line[line.find("#\"")+2:line.find("\"]")]
                kw1 = line[line.find("\"]")+5:line.find("\")")]
                line = line[line.find("\")")+3:None]
                col2 = line[line.find("#\"")+2:line.find("\"]")]
                kw2 = line[line.find("\"]")+5:line.find("\")")]
                line = line[line.find("\")")+3:None]
                col3 = line[line.find("#\"")+2:line.find("\"]")]
                kw3 = line[line.find("\"]")+5:line.find("\")")]

                line = rtxtf.readline()
                line = line[line.find("\"")+1:None]
                then = line[:line.find("\"")]

                writer.writerow([col1, kw1, '', col2, kw2, '', col3, kw3, '', col4, kw4, then])
                line = rtxtf.readline()
try:
    for f in excelFile:
        wb = load_workbook(f)
except:
    pass
sheet = wb['Sheet1']
with open(csvFile, 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        sheet.append(row)
wb.save(f)