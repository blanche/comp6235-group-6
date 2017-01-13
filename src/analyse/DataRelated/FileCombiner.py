import glob, os
os.chdir("C:\Users\Ut\Desktop\Foundations\ScrappedData_CSV")
fileList = []
for file in glob.glob("*.csv"):
    fileList.append(file)


with open('C:\Users\Ut\Desktop\Foundations\Gathered.csv', 'w') as outfile:
    for fname in fileList:
        print(fname)
        with open(fname) as infile:
            for line in infile:
                if "No Comment" not in line:#Only get reviews having comment
                    line = line.replace('"','')
                    line = line.replace('\"','')
                    line = line.replace('\'','')
                    outfile.write(line)

#mongoimport -d textDB -c gatheredTexts --type csv --headerline C:\Users\Ut\Desktop\Foundations\Gathered.csv
"""
db.gatheredTexts.update({}, {$unset: {urlExtention:1}} , {multi: true});
db.gatheredTexts.update({}, {$unset: {restUrl:1}} , {multi: true});
db.gatheredTexts.update({}, {$unset: {restAdress:1}} , {multi: true});
db.gatheredTexts.update({}, {$unset: {po1:1}} , {multi: true});
db.gatheredTexts.update({}, {$unset: {po2:1}} , {multi: true});
db.gatheredTexts.update({}, {$unset: {po3:1}} , {multi: true});
db.gatheredTexts.update({}, {$unset: {po4:1}} , {multi: true});
db.gatheredTexts.update({}, {$unset: {totRew:1}} , {multi: true});
"""