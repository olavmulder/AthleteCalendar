import csv

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

def WriteToFile(fileName, array):
   '''array[0] date
   array[1] eventname
   array[2] competitor name
   array[3] club of competitor
   '''
   with open(fileName, 'w', newline='') as csvFile:
      fieldNames = ['datum', 'wedstrijd naam', 'naam', 'club']
      writer = csv.DictWriter(csvFile, fieldnames=fieldNames)
      writer.writeheader()
      for i in array:
            writer.writerow({fieldNames[0]: i[0],
                             fieldNames[1]: i[1],
                             fieldNames[2]: i[2],
                             fieldNames[3]: i[3]})
      
