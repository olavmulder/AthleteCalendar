import csv
from datetime import datetime, timedelta
<<<<<<< HEAD
=======

fieldNames = ['Datum', 'Wedstrijd', 'Naam', 'Categorie', 'Link']
>>>>>>> release/v1.0

def IsDateNextDate(dateLast, dateNow):
   if(dateNow-timedelta(days=1) == dateLast):
      return True
   return False


def RemoveRows(fileName, array):
<<<<<<< HEAD
   filterRows = []
   with open(fileName, "r", newline="") as file:
      csvReader = csv.DictReader(file)
      for rowNum, row in enumerate(csvReader, start = 2):
         if rowNum not in array:
            filterRows.append(row)
   with open(fileName, "w", newline="") as file:
      fieldNames = ['Datum', 'Wedstrijd', 'Naam', 'Categorie']
      csvWriter = csv.DictWriter(file, fieldnames=fieldNames)
      csvWriter.writeheader()
      csvWriter.writerows(filterRows)
=======
   filtered = []
   with open(fileName, "r", newline="") as file:
      csvReader = csv.DictReader(file)
      for rowNumber, row in enumerate(csvReader, start=2):
         if rowNumber not in array:
            filtered.append(row)
   with open(fileName, "w", newline="") as file:
      csvWriter = csv.DictWriter(file, fieldnames=fieldNames)
      csvWriter.writeheader()
      csvWriter.writerows(filtered)
>>>>>>> release/v1.0

def DetectDoubleEvent(fileName):
   dateInputFormat = "%a %d %b %Y"
   delete = False
   lastDate = None
   lastEventName = ""
   arrayToRemove = []
   with open(fileName, 'r', newline='') as csvFile:
      reader = csv.DictReader(csvFile)
      rNum = 0
      for rNum,row in enumerate(reader, start=1):
<<<<<<< HEAD
         #print(f"row: {row}")
         dateNow = datetime.strptime(row['Datum'], dateInputFormat)
         eventName = row['Wedstrijd']
=======
         dateNow = datetime.strptime(row[fieldNames[0]], dateInputFormat)
         eventName = row[fieldNames[1]]
>>>>>>> release/v1.0
         if delete:
            if(dateNow == lastDate and
               eventName == lastEventName):
               arrayToRemove.append(rNum)
            else:
               arrayToRemove.append(rNum)
               delete = False
         else:
            if(IsDateNextDate(lastDate, dateNow) and
               eventName == lastEventName):
<<<<<<< HEAD
               print(f"{row['Wedstrijd']} was also yesterday")
=======
               print(f"{row[fieldNames[1]]} was also yesterday")
>>>>>>> release/v1.0
               delete = True
         lastDate = dateNow
         lastEventName = eventName
         
      #add also the last one
      if (delete):
         arrayToRemove.append(rNum+1)

   return arrayToRemove

def RemoveDoubleEvent(fileName):

   array = DetectDoubleEvent(fileName)
   print("array to delete: ", array)
   RemoveRows(fileName, array)

def WriteToFile(fileName, array):
   '''array[0] date
      array[1] eventname
      array[2] competitor name
      array[3] club of competitor
      array[4] link of competition
   '''
   with open(fileName, 'w', newline='') as csvFile:
<<<<<<< HEAD
      fieldNames = ['Datum', 'Wedstrijd', 'Naam', 'Categorie']
=======
>>>>>>> release/v1.0
      writer = csv.DictWriter(csvFile, fieldnames=fieldNames)
      writer.writeheader()
      print(f"len array is {len(array)}")
      for match in array:
         print(f"len match is {len(match)}")
         for competitor in match:
            writer.writerow({fieldNames[0]: competitor[0],
                             fieldNames[1]: competitor[1], 
                             fieldNames[2]: competitor[2],
                             fieldNames[3]: competitor[3],
                             fieldNames[4]: competitor[4]})
   RemoveDoubleEvent(fileName)
      
