from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import logging
from csvHandling import *
'''
keep tracking of indexes:
   1. table
   2. event
total reload every time 
'''

MyAthletes = OpenFile('athletes.csv')

def DebugInit():
   logging.basicConfig(filename="main.log", filemode="w", format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

def UsePupilFilter(browser):
   pupils = ["U12 Mannen", "U12 Vrouwen", "U10 Mannen", "U10 Vrouwen", "U9 Mannen", "U9 Vrouwen"]
   
   wait = WebDriverWait(browser, 10)
   wait.until(EC.visibility_of_element_located((By.ID,"advancedsearchoptions")))
   dropDown = browser.find_element(By.ID,"advancedsearchoptions")
   button = dropDown.find_elements(By.TAG_NAME, "button")
   
   for b in button:
      if b.text == "All categories":
         wait = WebDriverWait(browser, 10)
         wait.until(EC.element_to_be_clickable(b))
         b.click()
         wait = WebDriverWait(browser, 10)
         wait.until(EC.visibility_of_element_located((By.TAG_NAME, "li")))
         list = dropDown.find_elements(By.CLASS_NAME, "country_NL")
         for p in pupils:
            for l in list:
               if l.text == p:
                  try:
                     wait = WebDriverWait(browser, 10)
                     wait.until(EC.element_to_be_clickable(l))
                     l.click()
                     break
                  except:
                     logging.debug("cant click", l.text)
                     
   time.sleep(1)        
                  

def GetEventPage(browser):
   wait = WebDriverWait(browser, 10)
   wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "calendarTable")))
   return  browser.find_element(By.ID, "events")

def GetEventTables(browser, eventPage):

   
   wait = WebDriverWait(browser, 10)
   wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "calendarTable")))
   eventTable =  eventPage.find_elements(By.CLASS_NAME, "table-content")   
   return eventTable

def IsClickable(browser, events, indexEvents):
   try:
      wait = WebDriverWait(browser, 10)  # Maximum wait time of 10 seconds
      wait.until(EC.element_to_be_clickable(events[indexEvents]))
      return True
   except:
      logging.debug(f"Element is not clickable.")
      return False

def GetEventsFromTable(browser, eventTables, eventTablesIndex):
   #first get all nececarry variables
   wait = WebDriverWait(browser, 10)
   wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "calendarTable")))
   cal = eventTables[eventTablesIndex].find_element(By.CLASS_NAME, "calendarTable")
   table = cal.find_element(By.TAG_NAME, "tbody")
   return table.find_elements(By.TAG_NAME, "tr")
   
def CheckNoAtletes(event):
   compData = event.find_elements(By.TAG_NAME, "td")
   for cd in compData:
      if cd.text == "0":
         return 0
   return 1

def GoToCompetitors(browser):
   #find link to "inschrijving"
   wait = WebDriverWait(browser, 10)
   wait.until(EC.visibility_of_element_located((By.ID, "menu")))
   menu = browser.find_element(By.ID, "menu")
   ul = menu.find_element(By.ID, "topmenuHolder")
   list_items = ul.find_elements(By.TAG_NAME, "li")
   for item in list_items:
      if( item.text == "Competitors"):
         action = ActionChains(browser)
         action.move_to_element(item).click().perform()
         return True     
   return False

def FindAtletes(browser, eventName, eventData):
   names = [name[0] for name in MyAthletes]
   clubs = [club[1] for club in MyAthletes]
   competitors = []
   list = None
   
   try:
      wait = WebDriverWait(browser, 10)
      wait.until(EC.visibility_of_element_located((By.ID, "deelnemers_1")))
      list = browser.find_element(By.ID, "deelnemers_1")
     
   except:
      try:
         browser.find_element(By.ID, "adminAtleten")
         logging.debug("no registrated atletes")
      except:
         list = None
   
   if(list != None):
      added = False

      tableHead = list.find_element(By.TAG_NAME, "thead")
      tableHeadTh = tableHead.find_elements(By.TAG_NAME, "th")
      clubID = -1
      NameID = -1
      for i,headernames in enumerate(tableHeadTh):
         if headernames.text == "Club":
            clubID = i
         if headernames.text == "Name":
            NameID = i
      logging.debug(f"name id;{NameID}, club id;{clubID}")

      tableBody = list.find_element(By.TAG_NAME, "tbody")
      tableBodyTr = tableBody.find_elements(By.TAG_NAME, "tr")

      for atlete in tableBodyTr:
         coloms = atlete.find_elements(By.TAG_NAME, "td")
         for indexName in range(0, len(names)):
            #partition because "(out of competition)" after name  
            if(coloms[NameID].text.partition(" (")[0] == names[indexName] or
               coloms[NameID].text                   == names[indexName]): 
               
               if(coloms[clubID].text == clubs[indexName]):
                  print("naam: ", coloms[NameID].text, "; club: ", coloms[clubID].text)
                  competitors.append([eventData, eventName, names[indexName], clubs[indexName] ])
                  added = True
      if added:
         return competitors
      else:
         return False
   else:
      return False

def ShowAthletes(athletes):
   print("show athletes:")
   for at in athletes:
      print(at)

def Init():
   opts = Options()
   #opts.headless = True
   #assert opts.headless  # Operating in headless mode
   browser = Firefox(options=opts)
   browser.get('https://www.atletiek.nu/wedstrijden')

   #accpet cookies
   # Find the button by its id
   button = None
   while(button == None):
      try:
         button = browser.find_element(By.ID, "cmpbntyestxt")
      except:
         button = None
   # Click the button
   button.click()
   return browser

def main():
   DebugInit()
   browser = Init()

   eventTablesIndex = 0
   lenEventTables = 0 

   indexEvents = 0
   lenEvents = 0

   UsePupilFilter(browser)
   
   eventPage = GetEventPage(browser)
   eventTables = GetEventTables(browser,eventPage)
   lenEventTables = len(eventTables)

   #for all the tables with events
   logging.debug("lenEventTables", lenEventTables)
   myAthletesCompetingList = []
   for eventTablesIndex in range(0, lenEventTables):
      #reset the data, because dropping data by the library
      UsePupilFilter(browser)
      
      eventPage = GetEventPage(browser)
      eventTables = GetEventTables(browser, eventPage)
      events = GetEventsFromTable(browser, eventTables, eventTablesIndex)
      lenEvents = len(events)
      
      for indexEvents in range (0, lenEvents):
         #reset all variables
         #print(f"indexEvents: {indexEvents}, eventTableIndex: {eventTablesIndex}")
         if(browser.current_url != "https://www.atletiek.nu/wedstrijden/"):
            browser.get("https://www.atletiek.nu/wedstrijden/")
         
        
         
         eventPage = None
         eventTables = None
         events = None
         UsePupilFilter(browser) 
         eventPage   = GetEventPage(browser)
         eventTables = GetEventTables(browser, eventPage) 
         events      = GetEventsFromTable(browser, eventTables, eventTablesIndex)
         
         if IsClickable(browser,events, indexEvents) == True:
            #print(events[indexEvents].text)
            #if name exits
            try:
               eventnaam = events[indexEvents].find_element(By.CLASS_NAME, "eventnaam")
               eventdatumCol = events[indexEvents].find_element(By.CLASS_NAME, "datumCol")
            except:
               eventnaam = None

            if(eventnaam != None):
               if CheckNoAtletes(events[indexEvents]) != 0:
                  #print("name;" ,eventnaam.text)
                  eventName = eventnaam.text
                  eventDate = eventdatumCol.text
                  #scroll to event
                  browser.execute_script("arguments[0].scrollIntoView();", events[indexEvents])
                  action = ActionChains(browser)
                  #click on event
                  action.move_to_element(events[indexEvents]).click().perform()
                  
                  #go to event & and the competitors over there
                  if GoToCompetitors(browser) == True:
                     #print("atletes here")
                     listRet = FindAtletes(browser, eventName, eventDate)
                     if(listRet != False):
                        myAthletesCompetingList.append(listRet)
                     browser.get("https://www.atletiek.nu/wedstrijden/")
                  else:
                     logging.debug("no competition button found")
               else:
                  logging.debug("no competitors")
            else:
               logging.debug("no eventname")
         else:
            logging.debug("not clickable")
         
   ShowAthletes(myAthletesCompetingList)
   browser.quit()
def test():
   athletes = []
   browser = Init()
   browser.get('https://www.atletiek.nu/wedstrijd/atleten/39444/')

   ret = FindAtletes(browser, "test", "testData")
   if ret != False:
      athletes.append(ret)
   
   browser.get('https://www.atletiek.nu/wedstrijd/atleten/39703/')
   
   ret = FindAtletes(browser, "test", "testData")
   if ret != False:
      athletes.append(ret)
   
   #ShowAthletes(athletes)
   print("athletes: ", athletes)
   WriteToFile('wedstrijddeelname_overzicht.csv', athletes)
   browser.quit()
   
#test()
main()