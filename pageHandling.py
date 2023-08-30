from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import logging

timeout = 10

def Reload(browser, url):
   browser.get(url)
   try:
      element_present = EC.presence_of_element_located((By.ID,"advancedsearchoptions"))
      WebDriverWait(browser, timeout).until(element_present)
   except:
      logging.error('Timed out while waiting for page to load')
      return -1
   return 0

def UsePupilFilter(browser):
   pupils = ["U12 Mannen", "U12 Vrouwen", "U10 Mannen", "U10 Vrouwen", "U9 Mannen", "U9 Vrouwen"]
   try:
      element_present = EC.presence_of_element_located((By.ID,"advancedsearchoptions"))
      WebDriverWait(browser, timeout).until(element_present)
   except:
      logging.error('Timed out while waiting for page to load advancedsearchoptions')
      return -1

   dropDown = browser.find_element(By.ID,"advancedsearchoptions")

   try:
      element_present = EC.presence_of_element_located((By.TAG_NAME,"button"))
      WebDriverWait(browser, timeout).until(element_present)
   except:
      logging.error('Timed out while waiting for page to load button')
      return -1
   button = dropDown.find_elements(By.TAG_NAME, "button")
   
   for b in button:
      if b.text == "All categories":
         try:
            element_present = (EC.element_to_be_clickable(b))
            WebDriverWait(browser, timeout).until(element_present)
         except:
            logging.error('Timed out while waiting for page to click on all categories')
            return -1
         b.click()
         try:
            element_present = (EC.visibility_of_element_located((By.TAG_NAME, "li")))
            WebDriverWait(browser, timeout).until(element_present)
         except:
            logging.error('Timed out while waiting for page to find li')
            return -1
         
         list = dropDown.find_elements(By.CLASS_NAME, "country_NL")
         for p in pupils:
            for l in list:
               if l.text == p:
                  try:
                     element_present = (EC.element_to_be_clickable(l))
                     WebDriverWait(browser, timeout).until(element_present)
                  except:
                     logging.error(f'cant click on {l.text}')
                     return -1
                  l.click()
                  break
   #print('successful executed UsePupilFilter')
   logging.warning('successful executed UsePupilFilter')
   return 0                         
                  

def GetEventPage(browser):
   try:
      element_present = EC.presence_of_element_located((By.ID, "events"))
      WebDriverWait(browser, timeout).until(element_present)
   except:
      logging.error('Time out while waiting for events load')
      return -1
   eventPage = browser.find_elements(By.ID, "events")
   if len(eventPage) > 0:
      logging.warning("successful got event page")
      return  eventPage
   else:
      logging.error("didn't get event page")
      return -1

def GetEventTables(browser, eventPage):

   try:
      element_present = EC.presence_of_element_located((By.CLASS_NAME, "table-content"))
      WebDriverWait(browser, timeout).until(element_present)
   except:
      logging.error("can't get event-table")
      return -1
   
   eventTable =  eventPage.find_elements(By.CLASS_NAME, "table-content")
   if len(eventTable) > 0:
      logging.warning('successfull got eventTable')
      return eventTable
   else:
      logging.error("can't get event-table")
      return -1

def GetEventsFromTable(browser, eventTables, eventTablesIndex):
   #first get all nececarry variables
   try:
      element_present = EC.presence_of_element_located((By.CLASS_NAME, "calendarTable"))
      WebDriverWait(browser, timeout).until(element_present)
   except:
      logging.error("can't get calendarTable")
      return -1
   cal = eventTables[eventTablesIndex].find_elements(By.CLASS_NAME, "calendarTable")
   if len(cal) > 0:
      table = cal[0].find_elements(By.TAG_NAME, "tbody")
      if(len(table) > 0):
         events = table[0].find_elements(By.TAG_NAME, "tr")
         if(len(events) > 0):
            logging.warning("successfull got events")
            return events
         else:
            logging.warning("no events in table")
      else:
         logging.warning("no table can be found ")
   else:
      logging.error("len calendar table = 0")
   #no events
   return -2