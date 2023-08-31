from pageHandling import*
from csvHandling import *
import sys
import time
'''
keep tracking of indexes:
   1. table
   2. event
total reload every time 
'''

clubName = ""
categoryList  =[]
#global variables
events = -2
 
#table variables
eventTablesIndex = 0
lenEventTables = 0
#event variables
eventsIndex = 0
lenEvents = 0
#end gloabl variables
def PageLooping(browser, url):
   global lenEventTables
   global lenEvents
   global eventTablesIndex
   global eventsIndex
   
   events = -2
   eventTables = -1
   eventPage = -1

   while (events == -2): #-2 == no events
      while(eventTables == -1):
         while (eventPage == -1):
            while(Reload(browser, url) != 0):
               continue
            while(UsePupilFilter(browser) != 0):
               continue

            eventPage = GetEventPage(browser)
         eventTables = GetEventTables(browser, eventPage[0])
         if(eventTables == -1):
            eventPage = -1
      lenEventTables = len(eventTables)
      events = GetEventsFromTable(browser, eventTables, eventTablesIndex)
      if(events == -2):
         eventTables = -1
         eventPage = -1
         #if eventTables is smaller than index reset everything
         if(lenEventTables <= eventTablesIndex):
            eventTablesIndex = 0
            eventsIndex = 0
   lenEvents = len(events)
   return events

def IsClickable(browser, events, indexEvents):
   try:
      element_present = EC.element_to_be_clickable((events[indexEvents]))
      WebDriverWait(browser, timeout).until(element_present)
      return True
   except:
      logging.debug(f"Element is not clickable.")
      return False

def CheckNoAtletes(event):
   compData = event.find_elements(By.TAG_NAME, "td")
   for cd in compData:
      if cd.text == "0":
         return 0
   return 1

def GoToCompetitors(browser):
   #find link to "inschrijving"
   try:
      element_present = EC.visibility_of_element_located((By.ID, "menu"))
      WebDriverWait(browser, timeout).until(element_present)
      menu = browser.find_element(By.ID, "menu")
      ul = menu.find_element(By.ID, "topmenuHolder")
      list_items = ul.find_elements(By.TAG_NAME, "li")
   except:
      logging.error("cant get menu")
      return -1

   for item in list_items:
      if( item.text == "Competitors"):
         try:
            element_present = EC.element_to_be_clickable(item)
            WebDriverWait(browser, timeout).until(element_present)
            action = ActionChains(browser)
            action.move_to_element(item).click().perform()
            return True     
         except:
            logging.error("cant click on competitors")
            return False

def FindAtletes(browser, eventName, eventData):
   #names = [name[0] for name in MyAthletes]
   #clubs = [club[1] for club in MyAthletes]
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
      catID = -1
      nameID = -1
      for i,headernames in enumerate(tableHeadTh):
         if headernames.text == "Club":
            clubID = i
         if headernames.text == "Category":
            catID = i
         if headernames.text == "Name":
            nameID = i
      logging.debug(f"cat id;{catID}, club id;{clubID}")

      tableBody = list.find_element(By.TAG_NAME, "tbody")
      tableBodyTr = tableBody.find_elements(By.TAG_NAME, "tr")

      for atlete in tableBodyTr:
         coloms = atlete.find_elements(By.TAG_NAME, "td")
         #partition because "(out of competition)" after name  
         #if(coloms[NameID].text.partition(" (")[0] == names[indexName] or
         #   coloms[NameID].text                   == names[indexName]): 
         if(coloms[clubID].text == clubName):
            for c in categoryList:
               if(coloms[catID].text.partition(" ")[0] == c):
                  print("naam: ", coloms[nameID].text, "; cat: ", coloms[catID].text)
                  competitors.append([eventData, eventName, coloms[nameID].text, coloms[catID].text])
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

def GetEventData(browser):
   try:
      element_present = EC.presence_of_element_located((By.CLASS_NAME, "eventnaam"))
      WebDriverWait(browser, timeout).until(element_present)
      element_present = EC.presence_of_element_located((By.CLASS_NAME, "datumCol"))
      WebDriverWait(browser, timeout).until(element_present)
      
      eventnaam = events[eventsIndex].find_element(By.CLASS_NAME, "eventnaam")
      eventdatumCol = events[eventsIndex].find_element(By.CLASS_NAME, "datumCol")
   except:
      eventnaam = None
      eventdatumCol = None
      logging.error(f"no event name or event data at eventIndex {eventsIndex}")
   return eventnaam,eventdatumCol
if __name__ == '__main__':
   if len(sys.argv) < 4:
      print("not enough arguments")
      exit(-1)
   clubName = sys.argv[1]
   print(len(sys.argv))
   for i in range (2,len(sys.argv)):
      categoryList.append(sys.argv[i])
   print(f"club name is: {clubName}")
   print(f"category list: {categoryList}")
   logging.basicConfig(filename='main.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.WARNING)
   browser = Init()
   url = 'https://www.atletiek.nu/wedstrijden/'
   
   #for all the tables with events
   logging.error(f"before: lenEventTables: {lenEventTables}")
   logging.error(f"lenEvents: {lenEvents}")

   events = PageLooping(browser, url)   
   lenEvents =  len(events)
   time.sleep(2)
   events = PageLooping(browser, url)   
   lenEvents =  len(events)
   iters = 0
   #for all the tables with events
   logging.error(f"after: lenEventTables: {lenEventTables}")
   logging.error(f"lenEvents: {lenEvents}")
   myAthletesCompetingList = []
   for eventTablesIndex in range(0, lenEventTables):
      #reset the data, because dropping data by the library     
      for eventsIndex in range (0, lenEvents):
         print(iters)
         iters+=1
         events = PageLooping(browser, url)
         
         if IsClickable(browser,events, eventsIndex) == True:
            #print(events[eventsIndex].text)
            
            eventnaam,eventdatumCol = GetEventData(browser)
            #if name exits
            if(eventnaam != None and eventdatumCol != None):
               if CheckNoAtletes(events[eventsIndex]) != 0:
                  #get string of event data
                  eventName = eventnaam.text
                  eventDate = eventdatumCol.text
                  #scroll to event
                  try:
                     browser.execute_script("arguments[0].scrollIntoView();", events[eventsIndex])
                     action = ActionChains(browser)
                     #click on event
                     action.move_to_element(events[eventsIndex]).click().perform()
                  except:
                     logging.error(f"cant scroll to element {events[eventsIndex].text}")
                  
                  #go to event & and the competitors over there
                  if GoToCompetitors(browser) == True:
                     #print("atletes here")
                     listRet = FindAtletes(browser, eventName, eventDate)
                     if(listRet != False):
                        myAthletesCompetingList.append(listRet)
                  else:
                     logging.error("no competition button found")
               else:
                  logging.warning("no competitors")
            else:
               logging.warning("no eventname")
         else:
            logging.error(f"eventIndex: {eventsIndex} is not clickable")
   try:      
      ShowAthletes(myAthletesCompetingList)
      WriteToFile('wedstrijddeelname_overzicht.csv', myAthletesCompetingList )
      logging.warning("saved, done")
   except:
      logging.error(f"saving went from, data was: {myAthletesCompetingList}")
   browser.quit()
