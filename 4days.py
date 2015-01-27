import Tkinter
from Tkconstants import *
import datetime
import requests
import json
import smtplib
import string 

class fourdays:

     def __init__(self) :
        self.mw = Tkinter.Tk()
        self.mw.title('4 days')

        self.mw.option_add("*font", ("Calibri", 11, "normal"))
        self.mw.geometry("450x300")

        self.frame1 = Tkinter.Frame(self.mw, borderwidth = 3, relief = GROOVE)
        self.frame1.pack(side = LEFT, expand = 1, fill = BOTH)

        Tkinter.Label(self.frame1, text="Today's matches", bg="green").pack()

        self.vartodaymatches = Tkinter.Variable()

        self.lab1 = Tkinter.Label(self.frame1 , textvariable = self.vartodaymatches)
        self.lab1.pack(side = TOP)
        
        self.vartodaymatches.set(self.todaymatches())
        self.lab1 = self.vartodaymatches.get()

        self.frame2 = Tkinter.Frame(self.mw, borderwidth = 3, relief = GROOVE)
        self.frame2.pack(side = RIGHT, expand = 1, fill = BOTH)

        Tkinter.Label(self.frame2, text="Matches in 4 days", bg="green").pack()

        self.varfourdaymatches = Tkinter.Variable()

        self.lab2 = Tkinter.Label(self.frame2 , textvariable = self.varfourdaymatches)
        self.lab2.pack(side = TOP)

        self.varfourdaymatches.set(self.fourdaymatches())
        self.lab2 = self.varfourdaymatches.get()

        self.frame3 = Tkinter.Frame(self.frame2, borderwidth = 3 , relief = GROOVE)
        self.frame3.pack(side = BOTTOM , expand = 1 ,fill = BOTH)

        self.emailsent = Tkinter.Variable()

        self.lab3 = Tkinter.Label(self.frame3 , textvariable = self.emailsent , fg="green")
        self.lab3.pack(side = BOTTOM)

        self.button = Tkinter.Button(self.frame2 , text="Email" , command=self.sendemail)
        self.button.pack(side = BOTTOM, expand = 0 , fill = NONE, ipadx = 20 , padx = 10 , pady = 10)

        self.mw.mainloop()

     def todaymatches(self):
         
         self.i = datetime.datetime.now()
         self.today = self.i.isoformat()[0:10]
        
         self.fixtures = {}
        
         self.r = requests.get("http://api.statsfc.com/fixtures.json?key=LWvKUlG9gd1L9LMJ304f62QUf8eDbQAbMJO5MhXc&competition=premier-league&from="+self.today+"&to="+self.today)
         self.fixtures = json.loads(self.r.text)
            
         if dict(self.fixtures)["error"]:
              self.msg = "There are no fixtures today"
              return self.msg
                
         else :
              self.new_fixtures = []
              for e in self.fixtures:
                   self.match = ""
                   self.match = e["home"].encode('utf-8') + " v. " + e["away"].encode('utf-8')
                   self.new_fixtures.append(self.match)
              for fixture in self.new_fixtures:
                   return self.new_fixtures

     def fourdaymatches(self):
         self.today = datetime.date.today()
         self.seven_days = datetime.timedelta(days = 7) #take time to understand timedelta fully 
         self.seven = self.today + self.seven_days
         self.seven_days_isoformat = self.seven.isoformat()
        
         self.fixtures = {}
        
         self.r = requests.get("http://api.statsfc.com/fixtures.json?key=LWvKUlG9gd1L9LMJ304f62QUf8eDbQAbMJO5MhXc&competition=premier-league&from="+self.seven_days_isoformat+"&to="+self.seven_days_isoformat)
         self.fixtures = json.loads(self.r.text)

         if dict(self.fixtures)["error"]:
             self.msg = "There will be no fixtures in seven days"
             return self.msg

         else :
             self.new_fixtures = []
             for e in self.fixtures:
                  self.match = ""
                  self.match = e["home"].encode('utf-8') + " v. " + e["away"].encode('utf-8')
                  self.new_fixtures.append(self.match)
             self.joined_string = string.join(self.new_fixtures, '\n')
             return self.joined_string

     def sendemail(self):
         self.sender = 'corji12@alastudents.org'
         self.receivers = ['oukaire12@alastudents.org']
         self.message = """Subject: Send Ms Wolter email

         These are the matches in seven days:
         """ + self.fourdaymatches()

         self.smtpObj = smtplib.SMTP('mail.alastudents.org' , 25)
         self.smtpObj.sendmail(self.sender, self.receivers, self.message)
         
         self.emailsent.set("Email has been sent successfully!")
         self.lab3 = self.emailsent.get()
         return

if __name__ == "__main__":
    app = fourdays()
