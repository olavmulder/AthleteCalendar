from pageHandling import*
from csvHandling import *
'''
keep tracking of indexes:
   1. table
   2. event
total reload every time 
'''

#MyAthletes = OpenFile('athletes.csv')
clubName = "AV Hylas"
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
      lenEventTables = len(eventTables)
      events = GetEventsFromTable(browser, eventTables, eventTablesIndex)
   lenEvents = len(events)
   return events

def IsClickable(browser, events, indexEvents):
   try:
      wait = WebDriverWait(browser, 10)  # Maximum wait time of 10 seconds
      wait.until(EC.element_to_be_clickable(events[indexEvents]))
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
         #partition because "(out of competition)" after name  
         #if(coloms[NameID].text.partition(" (")[0] == names[indexName] or
         #   coloms[NameID].text                   == names[indexName]): 
         if(coloms[clubID].text == clubName):
            print("naam: ", coloms[NameID].text, "; club: ", coloms[clubID].text)
            competitors.append([eventData, eventName, coloms[NameID].text])
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

 
if __name__ == '__main__':
   #test()
   
   browser = Init()
   url = 'https://www.atletiek.nu/wedstrijden/'
   PageLooping(browser, url)   
   #for all the tables with events
   logging.error(f"lenEventTables: {lenEventTables}")
   logging.error(f"lenEvents: {lenEvents}")
   myAthletesCompetingList = []
   for eventTablesIndex in range(0, lenEventTables):
      #reset the data, because dropping data by the library     
      for eventsIndex in range (0, lenEvents):
         
         PageLooping(browser, url)
         
         if IsClickable(browser,events, eventsIndex) == True:
            print(events[eventsIndex].text)
            #if name exits
            '''try:
               eventnaam = events[eventsIndex].find_element(By.CLASS_NAME, "eventnaam")
               eventdatumCol = events[eventsIndex].find_element(By.CLASS_NAME, "datumCol")
            except:
               eventnaam = None

            if(eventnaam != None):
               if CheckNoAtletes(events[eventsIndex]) != 0:
                  #print("name;" ,eventnaam.text)
                  eventName = eventnaam.text
                  eventDate = eventdatumCol.text
                  #scroll to event
                  browser.execute_script("arguments[0].scrollIntoView();", events[eventsIndex])
                  action = ActionChains(browser)
                  #click on event
                  action.move_to_element(events[eventsIndex]).click().perform()
                  
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
            '''
         else:
            logging.debug("not clickable")
   try:      
      ShowAthletes(myAthletesCompetingList)
      WriteToFile('wedstrijddeelname_overzicht.csv', myAthletesCompetingList )
      logging.info("saved, done, return 0")
   except:
      logging.info(f"saving went from, data was: {myAthletesCompetingList}")
   browser.quit()
