import glob, os
os.chdir("C:\Users\Ut\Desktop\Foundations\ScrappedData")
fileList = []
for file in glob.glob("*.csv"):
    fileList.append(file)

#os.remove("C:\Users\Ut\Desktop\Foundations of DS\ScrappedData\Summary.csv")
f2 = open ('Summary.csv','w')
for fname in fileList:
    f1 = open(fname, 'r')
    fileList = []
    print fname
    for line in f1:
        cityIndex = line.index(',')
        city = line[:cityIndex]
        line = line[cityIndex+1:]

        websiteIndex = line.index(',')
        website = "just-eat.co.uk" + line[:websiteIndex]
        line = line[websiteIndex+1:]

        restIdIndex = line.index(',')
        restId = line[:restIdIndex]
        line = line[restIdIndex+1:]
        
        if restId not in fileList:
            fileList.append (restId)
            
            iterator = line.index(',')
            line = line[iterator+1:]

            restNameIndex = line.index(',')
            restName = line[:restNameIndex]
            line = line[restNameIndex+1:]

            adressIndex = line.index(',')
            adress = line[:adressIndex]
            line = line[adressIndex+1:]

            avgRatingIndex = line.index(',')
            avgRating = line[:avgRatingIndex]
            line = line[avgRatingIndex+1:]

            foodQualIndex = line.index(',')
            foodQuality = line[:foodQualIndex]
            line = line[foodQualIndex+1:]

            deliveryIndex = line.index(',')
            deliveryStar = line[:deliveryIndex]
            line = line[deliveryIndex+1:]

            serviceIndex = line.index(',')
            serviceStar = line[:serviceIndex]
            line = line[serviceIndex+1:]

            revCountIndex = line.index(',')
            revCount = line[:revCountIndex]
            line = line[revCountIndex+1:]

            f2.write(city+',')
            f2.write(website+',')
            f2.write(restId+',')
            f2.write(restName+',')
            f2.write(adress+',')
            f2.write(avgRating+',')
            f2.write(foodQuality+',')
            f2.write(deliveryStar+',')
            f2.write(serviceStar+',')
            f2.write(revCount+',')
            f2.write('\n')
f2.close()
