from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
'''
keep tracking of indexes:
   1. table
   2. event
total reload every time 
'''

MyAtlets = [
            ["Jolande Brasser", "AV Trias"]
]

def UsePupilFilter(browser):
   pupils = ["U12 Mannen", "U12 Vrouwen", "U10 Mannen", "U10 Vrouwen", "U9 Mannen", "U9 Vrouwen"]
   
   wait = WebDriverWait(browser, 10)
   wait.until(EC.visibility_of_element_located((By.ID,"advancedsearchoptions")))
   dropDown = browser.find_element(By.ID,"advancedsearchoptions")
   button = dropDown.find_elements(By.TAG_NAME, "button")
   
   for b in button:
      if b.text == "All categories":
         print("found alle cat:")
         b.click()
         wait = WebDriverWait(browser, 10)
         wait.until(EC.visibility_of_element_located((By.TAG_NAME, "li")))
         list = dropDown.find_elements(By.TAG_NAME, "li")
         listNL = list.find_elements(By.CLASS_NAME, "countryspecific country_NL")
         for l in listNL:
            for p in pupils:
               if(l.text == p):
                  l.click()
       

def GetEventPage(browser):
   
   try:
      return browser.find_element(By.ID, "events")
   except:
      wait = WebDriverWait(browser, 10)
      wait.until(EC.visibility_of_element_located((By.ID, "events")))
      return  browser.find_element(By.ID, "events")
   #return eventPage

def GetEventTables(browser, eventPage):

   wait = WebDriverWait(browser, 10)
   wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "table-content")))
   eventTable =  eventPage.find_elements(By.CLASS_NAME, "table-content")   
   return eventTable

def IsClickable(browser, events, indexEvents):
   try:
      wait = WebDriverWait(browser, 10)  # Maximum wait time of 10 seconds
      wait.until(EC.element_to_be_clickable(events[indexEvents]))
      return True
   except:
      print(f"Element is not clickable.")
      return False

def GetEventsFromTable(browser, eventTables, eventTablesIndex):
   #first get all nececarry variables
   try:
      return eventTables[eventTablesIndex].find_elements(By.TAG_NAME, "tr")
   except:
      #if eventTable is missing get it again
      wait = WebDriverWait(browser, 10)
      wait.until(EC.visibility_of_element_located((By.TAG_NAME, "tr")))
      return eventTables[eventTablesIndex].find_elements(By.TAG_NAME, "tr")
   
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
   names = [name[0] for name in MyAtlets]
   clubs = [club[1] for club in MyAtlets]
   comp = [[4]]
   list = None
   
   try:
      browser.find_element(By.ID, "adminAtleten")
      print("no registrated atletes")
   except:
      try:
         wait = WebDriverWait(browser, 10)
         wait.until(EC.visibility_of_element_located((By.ID, "deelnemers_1")))
         list = browser.find_element(By.ID, "deelnemers_1")
      except:
         list = None
   
   if(list != None):
      added = False
      atletes = list.find_elements(By.TAG_NAME, "tr")
      for index,atlete in enumerate(atletes):
         if index != 1:
            coloms = atlete.find_elements(By.TAG_NAME, "td")
            if len(coloms) >= 3:
               for index, n in enumerate(names):
                  #coloms[1] = name, coloms[2] = club
                  if(coloms[1].text == n):
                     if(clubs[index] == coloms[2].text):
                        print("naam: ", coloms[1].text, "; club: ", coloms[2].text)
                        comp.append([eventData, eventName, coloms[1].text, coloms[2].text])
                        added = True
      if added:
         return comp
      else:
         return False
   else:
      #print("list of atletes is none")
      return False

def ShowAthletes(athletes):
   
   for at in athletes:
      print(at)

def main():
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


   eventTablesIndex = 0
   lenEventTables = 0 

   indexEvents = 0
   lenEvents = 0

   UsePupilFilter(browser)
   
   eventPage = GetEventPage(browser)
   eventTables = GetEventTables(browser,eventPage)
   lenEventTables = len(eventTables)

   #for all the tables with events
   print("lenEventTables", lenEventTables)
   myAtltesCompetingList = [[4]]
   for eventTablesIndex in range(0, lenEventTables):
      #reset the data, because dropping data by the library
      UsePupilFilter(browser)

      eventPage = GetEventPage(browser)
      if(eventPage != None):
         eventTables = GetEventTables(browser, eventPage)
         if(eventTables != None):
            events = GetEventsFromTable(browser, eventTables, eventTablesIndex)
            if(events != None):
               lenEvents = len(events)
               print(f"lenEvents: {lenEvents}")
            else:
               print("events = None")
               return -1
         else:
            print("eventTables = None")
            return -1
      else:
         print("eventPage = None")
         return -1
      #need to change to 0
      for indexEvents in range (15, lenEvents):
         #reset all variables
         print(f"indexEvents: {indexEvents}, eventTableIndex: {eventTablesIndex}")
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
                        myAtltesCompetingList.append(listRet)
                     else:
                        print("my atletes don't compete here")
                     browser.get("https://www.atletiek.nu/wedstrijden/")
                  else:
                     print("no competition button found")
               else:
                  print("no competitors")
            else:
               print("no eventname")
         else:
            print("not clickable")
         
         
         indexEvents +=1
      
      
      eventTablesIndex += 1
      indexEvents = 0
   ShowAthletes(myAtltesCompetingList)

   browser.quit()
main()