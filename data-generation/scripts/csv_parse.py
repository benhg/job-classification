import csv
for i in ["ExampleMailingList"]:
    fh = open('{}.csv'.format(i))
    fh2 = open('{}_fixed.csv'.format(i), 'w')
    reader = csv.reader(fh)
    writer = csv.writer(fh2)
    for row in reader:
        list = row
        row[1] = "https://en.wikipedia.org/wiki/User_talk:" + row[0]
        writer.writerow(row)
