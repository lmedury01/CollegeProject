import mysql.connector

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.recycleview import RecycleView
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput

mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="password",
    database="college"
)

mycursor=mydb.cursor()


class MainWindow(Screen,Widget):
    uname=ObjectProperty(None)
    passw=ObjectProperty(None)

    def validate(self):
        var_uname=self.uname.text.strip()
        var_passw=self.passw.text.strip()
        sqlFormula="""SELECT password From registrations WHERE username=%s"""
        mycursor.execute(sqlFormula,(var_uname,))
        result = mycursor.fetchone()
        sqlFormula = """SELECT htno From registrations WHERE username=%s"""
        mycursor.execute(sqlFormula, (var_uname,))
        htno = mycursor.fetchone()

        if result[0] == var_passw:
            Profile.current=self.uname.text
            Profile.no=htno[0]
            RegularFee.no=htno[0]
            SupplementaryFee.no=htno[0]
            ChangePassword.currentPassword=result[0]
            ChangePassword.username=var_uname
            PendingTasks.current=self.uname.text
            Include.current=self.uname.text
            self.uname.text=""
            self.passw.text=""
            sm.current="home"
        else:
            pop = Popup(title='Invalid Form',
                        content=Label(text='Invalid Credentials.\nRe-enter your username and password'),
                        size_hint=(None, None), size=(400, 400))

            pop.open()
            self.uname.text=""
            self.passw.text=""


class SecondWindow(Screen, Widget):
    pass

class NewUser(Screen):
    name1=ObjectProperty(None)
    uname=ObjectProperty(None)
    password=ObjectProperty(None)
    age = ObjectProperty(None)

    def save(self):
        var_name=self.name1.text
        var_uname=self.uname.text
        var_password=self.password.text
        var_age = (self.age.text)

        sqlFormula= "INSERT INTO users (name, uname,password,age) VALUES(%s , %s , %s, %s)"
        detail = (var_name, var_uname, var_password, var_age)
        mycursor.execute(sqlFormula, detail)
        mydb.commit()
        sm.current= "main"


class LoginSuccess(Screen):
    pass

class Include(Screen,Widget):
    task=ObjectProperty(None)
    deadline=ObjectProperty(None)
    current=""
    def set(self):
        var_task=self.task.text
        var_deadline=self.deadline.text
        var_user=self.current
        sqlFormula = """SELECT uid From users WHERE uname=%s"""
        mycursor.execute(sqlFormula, (var_user,))
        thisID = mycursor.fetchone()
        Profile.currentID=thisID[0]
        sqlFormula="INSERT INTO list(uid,task,deadline) VALUES (%s,%s,%s)"
        detail=(thisID[0],var_task,var_deadline)
        mycursor.execute(sqlFormula,detail)
        mydb.commit()

        pop = Popup(title='Task included',
                    content=Label(text='The task has been successfully included'),
                    size_hint=(None, None), size=(400, 400))

        pop.open()
        self.task.text = ""
        self.deadline.text = ""
        sm.current="home"

class AMeetUp(Screen, BoxLayout):
        #Starting Here
    pass
        #Ending Here

class Query(Screen):
    pass

class AQuery(Screen):
    pass

class Profile(Screen):
    name1=ObjectProperty(None)
    htno=ObjectProperty(None)
    cgpa=ObjectProperty(None)
    current=""
    currentID=""
    no=""
    def on_enter(self, *args):
        var_user=self.no
        sqlFormula = """SELECT name From students WHERE htno=%s"""
        mycursor.execute(sqlFormula,(var_user,))
        thisName=mycursor.fetchone()
        sqlFormula = """SELECT cgpa From cgpa WHERE htno=%s"""
        mycursor.execute(sqlFormula, (var_user,))
        thisCgpa = mycursor.fetchone()
        self.htno.text = "Hall Ticket No: " +var_user
        self.name1.text = "Name : " + thisName[0]
        self.cgpa.text= "CGPA: " + str(thisCgpa[0])

class ChangePassword(Screen):
    existing=ObjectProperty(None)
    password=ObjectProperty(None)
    repeatPassword=ObjectProperty(None)
    currentPassword=""
    username=""
    def modify(self):
        var_existing=self.existing.text
        var_password=self.password.text
        var_repeatPassword=self.repeatPassword.text
        if var_existing == self.currentPassword:
            if var_password == var_repeatPassword:
                sqlFormula = "UPDATE registrations set password=%s WHERE username=%s "
                detail = (var_password,self.username)
                mycursor.execute(sqlFormula, detail)
                mydb.commit()
                sm.current = "main"
                pop = Popup(title='Passwords Change Successful',
                            content=Label(text='Password has been changed successfully'),
                            size_hint=(None, None), size=(400, 400))

                pop.open()
                self.existing.text = ""
                self.password.text = ""
                self.repeatPassword.text = ""
            else:
                pop = Popup(title='Passwords do not match',
                            content=Label(text='Passwords do not match.\nRe-enter your new password'),
                            size_hint=(None, None), size=(400, 400))

                pop.open()
                self.existing.text = ""
                self.password.text = ""
                self.repeatPassword.text=""
        else:
            pop = Popup(title='Wrong existing password',
                        content=Label(text='The password you have entered is wrong.\nRe-enter your password'),
                        size_hint=(None, None), size=(400, 400))

            pop.open()
            self.existing.text = ""
            self.password.text = ""
            self.repeatPassword.text = ""


class Payments(Screen):
    pass
class CollegeFee(Screen):
    pass
class SupplementaryFee(Screen):
    pass
class RegularFee(Screen):
    htno=ObjectProperty(None)
    name1=ObjectProperty(None)
    fee=ObjectProperty(None)
    Status = ObjectProperty(None)
    no=""
    def on_enter(self, *args):
        var_user = self.no
        sqlFormula = """SELECT name From students WHERE htno=%s"""
        mycursor.execute(sqlFormula, (var_user,))
        thisName = mycursor.fetchone()
        self.htno.text = "Hall Ticket No: " + var_user
        self.name1.text = "Name : " + thisName[0]
        self.fee.text="Fee: "+"1200"
        sqlFormula = """SELECT status From regularfee WHERE htno=%s"""
        mycursor.execute(sqlFormula, (var_user,))
        thisStatus = mycursor.fetchone()
        self.status.text="Status: "+thisStatus[0]

    def pay(self):
        sqlFormula = """SELECT status From regularfee WHERE htno=%s"""
        mycursor.execute(sqlFormula, (self.no,))
        thisStatus = mycursor.fetchone()
        if thisStatus[0] == "Not Paid Yet":
            sqlFormula = "UPDATE regularfee set status=%s WHERE htno=%s "
            detail = ("Paid", self.no)
            mycursor.execute(sqlFormula, detail)
            mydb.commit()
            sm.current = "main"
            pop = Popup(title='Payment Done',
                        content=Label(text='Payment has been processed succesfully'),
                        size_hint=(None, None), size=(400, 400))

            pop.open()

        else:
            pop = Popup(title='Payment Already Done',
                        content=Label(text='No fee due'),
                        size_hint=(None, None), size=(400, 400))

            pop.open()

class SupplementaryFee(Screen):
    htno = ObjectProperty(None)
    name1 = ObjectProperty(None)
    fee = ObjectProperty(None)
    Status = ObjectProperty(None)
    no = ""

    def on_enter(self, *args):
        var_user = self.no
        sqlFormula = """SELECT name From students WHERE htno=%s"""
        mycursor.execute(sqlFormula, (var_user,))
        thisName = mycursor.fetchone()
        sqlFormula = """SELECT subjects From supplementaryfee WHERE htno=%s"""
        mycursor.execute(sqlFormula, (var_user,))
        thisSubjects = mycursor.fetchone()
        self.htno.text = "Hall Ticket No: " + var_user
        self.name1.text = "Name : " + thisName[0]
        self.subjects.text="Subjects Due: "+str(thisSubjects[0])
        sqlFormula = """SELECT fee From supplementaryfee WHERE htno=%s"""
        mycursor.execute(sqlFormula, (var_user,))
        thisFee = mycursor.fetchone()
        self.fee.text = "Fee: " + str(thisFee[0])
        sqlFormula = """SELECT status From supplementaryfee WHERE htno=%s"""
        mycursor.execute(sqlFormula, (var_user,))
        thisStatus = mycursor.fetchone()
        self.status.text="Status: "+thisStatus[0]

    def pay(self):
        sqlFormula = """SELECT status From supplementaryfee WHERE htno=%s"""
        mycursor.execute(sqlFormula, (self.no,))
        thisStatus = mycursor.fetchone()
        if thisStatus[0] == "Not Paid Yet":
            sqlFormula = "UPDATE supplementaryfee set status=%s,fee=0 WHERE htno=%s "
            detail = ("Paid", self.no)
            mycursor.execute(sqlFormula, detail)
            mydb.commit()
            sm.current = "main"
            pop = Popup(title='Payment Done',
                        content=Label(text='Payment has been processed succesfully'),
                        size_hint=(None, None), size=(400, 400))

            pop.open()

        else:
            pop = Popup(title='Payment Already Done',
                        content=Label(text='No fee due'),
                        size_hint=(None, None), size=(400, 400))

            pop.open()
class PendingTasks(RecycleView,Screen):
    pass

class WindowManager(ScreenManager):
    pass

kv= Builder.load_file("/home/lmedury/PycharmProjects/DoList/my.kv")
sm=WindowManager()
screens = [MainWindow(name="main"), LoginSuccess(name="home"), NewUser(name="register"), Profile(name="profile"), Include(name="include"), PendingTasks(name="pending"), ChangePassword(name="change"),
           Payments(name="payments"), CollegeFee(name="collegefee"), RegularFee(name="regularfee"), SupplementaryFee(name="supplementaryfee")]
for screen in screens:
    sm.add_widget(screen)

class NavigationApp(App):
    title="DoList"
    def build(self):
        return sm

if __name__ == "__main__":
    NavigationApp().run()