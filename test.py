import AtleticCalendar as AC
import csvHandling 
def test_reload():
   print("test reload")
   url = "https://www.atletiek.nu/wedstrijden/"
   browser = AC.Init()
   
   for i in range (0, 100):
      res = AC.Reload(browser, url)
      while(res == -1):
         res = AC.Reload(browser, url)
      print(res)

def test_filter():
   url = "https://www.atletiek.nu/wedstrijden/"
   browser = AC.Init()
   for i in range (0, 100):
      while(AC.Reload(browser, url) != 0):
         continue
      while(AC.UsePupilFilter(browser) != 0):
         continue
      print(i)

def test_eventpage():
   url = "https://www.atletiek.nu/wedstrijden/"
   browser = AC.Init()
   
   for i in range (0, 100):
      events = -1
      while events == -1:
         while(AC.Reload(browser, url) != 0):
            continue
         while(AC.UsePupilFilter(browser) != 0):
            continue
         events = AC.GetEventPage(browser)
      print(i)

def test_get_events():
   url = "https://www.atletiek.nu/wedstrijden/"
   browser = AC.Init()
   #all the events I guess
   #amount pages, normaly 1
   eventPageIndex = 0
   #amount tables, 1 or 2(i case of 'today')
   eventTablesIndex = 0
   for eventIndex in range (0, 15):
      events = -2
      eventTables = -1
      eventPage = -1
      while (events == -2): #-2 == no events
         while(eventTables == -1):
            while (eventPage == -1):
               while(AC.Reload(browser, url) != 0):
                  continue
               while(AC.UsePupilFilter(browser) != 0):
                  continue
               eventPage = AC.GetEventPage(browser)
            eventTables = AC.GetEventTables(browser, eventPage[eventPageIndex])
         events = AC.GetEventsFromTable(browser, eventTables, eventTablesIndex)
      print(eventIndex)


def test_clickable():
   url = "https://www.atletiek.nu/wedstrijden/"
   browser = AC.Init()
   #all the events I guess
   #amount pages, normaly 1
   eventPageIndex = 0
   #amount tables, 1 or 2(i case of 'today')
   eventTablesIndex = 0
   for eventIndex in range (0, 15):
      events = -2
      eventTables = -1
      eventPage = -1
      while (events == -2): #-2 == no events
         while(eventTables == -1):
            while (eventPage == -1):
               while(AC.Reload(browser, url) != 0):
                  continue
               while(AC.UsePupilFilter(browser) != 0):
                  continue
               eventPage = AC.GetEventPage(browser)
            eventTables = AC.GetEventTables(browser, eventPage[eventPageIndex])
         events = AC.GetEventsFromTable(browser, eventTables, eventTablesIndex)
      ret = AC.IsClickable(browser, events, eventIndex)
      print(ret)

def test_find_atletes():
   url = "https://www.atletiek.nu/wedstrijd/atleten/39710/"
   browser = AC.Init()
   browser.get(url)
   array = []
   res = AC.FindAtletes(browser, "test", "test")
   if res != False:
      AC.ShowAthletes(res)
      array.append(res)
      AC.WriteToFile('temp.csv', array)
     
def test_csv():
   csvHandling.RemoveDoubleEvent("wedstrijddeelname_overzicht.csv")
      
def test_main():

   print("test main")
   #test_reload()
   #test_filter()
   #test_eventpage()
   #test_get_events()
   #test_clickable()
   #test_find_atletes()
   test_csv()
if __name__ == '__main__':
   AC.logging.basicConfig(filename='main.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=AC.logging.WARNING)
   test_main()