import glob, os
os.chdir("C:\Users\Ut\Desktop\Foundations\ScrappedData")
fileList = []
for file in glob.glob("*.txt"):
    fileList.append(file)

for fileName in fileList:
    cityName = fileName.replace('.txt', '')
    f1 = open("C:\\Users\\Ut\\Desktop\\Foundations\\ScrappedData\\"+cityName+'.txt', 'r')
    f2 = open("C:\\Users\\Ut\\Desktop\\Foundations\\ScrappedData\\"+cityName+'_Clean.csv', 'w')
    cnt = 0
    for line in f1:
        cnt = cnt+1
        if line[:len(cityName)] == cityName:
            lineStr = line.replace(',', ';')
            f2.write(lineStr.replace('|', ','))
    f1.close()
    f2.close()
