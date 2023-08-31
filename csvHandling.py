import csv
from datetime import datetime, timedelta
'''
open file and return array with all my athletes
'''
def OpenFile(fileName):
   atletes =[]
   with open(fileName, newline='') as csvFile:
      reader = csv.DictReader(csvFile)
      for row in reader:
         atletes.append([row['naam'], "AV Hylas"])
   return atletes

def IsDateNextDate(dateLast, dateNow):
   if(dateNow-timedelta(days=1) == dateLast):
      return True
   return False


def RemoveRow(fileName, array):
   with open(fileName, "r", newline="") as file:
      csvReader = csv.reader(file)
      rows = list(csvReader)
      for i in array:
         if i < len(rows):
            print("remove", i)
            rows.pop(i)
            
   with open(fileName, "w", newline="") as file:
      csv_writer = csv.writer(file)
      csv_writer.writerows(rows)

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
         #print(f"row: {row}")
         dateNow = datetime.strptime(row['Datum'], dateInputFormat)
         eventName = row['Wedstrijd']
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
               print(f"{row['Wedstrijd']} was also yesterday")
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
   RemoveRow(fileName, array)

def WriteToFile(fileName, array):
   '''array[0] date
      array[1] eventname
      array[2] competitor name
      array[3] club of competitor
   '''
   with open(fileName, 'w', newline='') as csvFile:
      fieldNames = ['Datum', 'Wedstrijd', 'Naam', 'Categorie']
      writer = csv.DictWriter(csvFile, fieldnames=fieldNames)
      writer.writeheader()
      print(f"len array is {len(array)}")
      for match in array:
         print(f"len match is {len(match)}")
         for competitor in match:
            writer.writerow({fieldNames[0]: competitor[0],
                             fieldNames[1]: competitor[1], 
                             fieldNames[2]: competitor[2],
                             fieldNames[3]: competitor[3]})
   RemoveDoubleEvent(fileName)
      
