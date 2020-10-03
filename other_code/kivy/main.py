from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen


class LoginWindow(Screen):
    username = ObjectProperty()
    passord = ObjectProperty()

    def loginBtn(self):
        if len(self.username.text) and len(self.passord.text):
            a = login(self.username.text, self.passord.text)
            if a:
                sm.current = 'main'
            elif a is False:
                login1()
                self.passord.text = ''
            elif a is None:
                login2()
                self.passord.text = ''
                self.username.text = ''
            else:
                print('Error with database')
        else:
            login3()

    def registrerBtn(self):
        pass


class UserRegistrationWindow(Screen):
    pass


class MainWindow(Screen):

    def bytteBtn(self):
        sm.current = 'swap'

    def proveBtn(self):
        sm.current = 'testing'

    def salgBtn(self):
        pass

    def registrerBtn(self):
        sm.current = 'varereg'


class BytteWindow(Screen):
    firma = ObjectProperty()
    blomst = ObjectProperty()
    retur = ObjectProperty()
    notat = ObjectProperty()

    def tilbakeBtn(self):
        sm.current = 'main'

    def submitBtn(self):
        if self.firma.text or self.blomst.text or self.retur.text or self.notat.text:
            if bytte(self.firma.text, self.blomst.text, self.retur.text, self.notat.text):
                self.reset()
                registered_action()
            else:
                print('Error with database')
        else:
            failed_action()

    def reset(self):
        self.firma.text = ''
        self.blomst.text = ''
        self.retur.text = ''
        self.notat.text = ''


class LeveranseWindow(Screen):

    def bytteBtn(self):
        sm.current = 'swap'

    def trialBtn(self):
        pass

    def tilbakeBtn(self):
        sm.current = 'main'


class SalgWindow(Screen):
    pass


class VareregWindow(Screen, BoxLayout):

    def checkbox(self, instance, value):
        a = SampBoxLayout()
        a.checkbox_clicked(value)

    def tilbakeBtn(self):
        sm.current = 'main'


class WindowManager(ScreenManager):
    pass


class SampBoxLayout(CheckBox):
    checkbox_is_active = ObjectProperty(False)

    def checkbox_clicked(self, value):
        if value is True:
            print('clicked checkbox')
        else:
            print('checkbox unchecked')

    def tilbakeBtn(self):
        sm.current = 'main'


class TestWindow(Screen):

    def tilbakeBtn(self):
        sm.current = 'main'

    def test(self):
        print('clicked')


def registered_action():
    pop = Popup(title='Vellykket!',
                content=Label(text='Registrert til databasen.'),
                size_hint=(None, None), size=(400, 400))
    pop.open()


def failed_action():
    pop = Popup(title='Mislykket.',
                content=Label(text='Sjekk at all informasjon er riktig.'),
                size_hint=(None, None), size=(500, 500))
    pop.open()


def login1():
    pop = Popup(title='Mislykket',
                content=Label(text='Feil passord.'),
                size_hint=(None, None), size=(400, 400))
    pop.open()


def login2():
    pop = Popup(title='Mislykket!',
                content=Label(text='Denne brukeren er ikke registrert'),
                size_hint=(None, None), size=(400, 400))
    pop.open()


def login3():
    pop = Popup(title='Lol',
                content=Label(text='Du mÃ¥ legge inn brukernavn og passord.'),
                size_hint=(None, None), size=(400, 400))
    pop.open()


kv = Builder.load_file('my.kv')
sm = WindowManager()

screens = [LoginWindow(name='login'), MainWindow(name='main'), BytteWindow(name='swap'),
           LeveranseWindow(name='leveranse'), VareregWindow(name='varereg'),
           TestWindow(name='testing')]

for screen in screens:
    sm.add_widget(screen)

sm.current = 'main'


class MyMainApp(App):
    def build(self):
        Window.clearcolor = (.5, .5, .5, .5)
        return sm


if __name__ == '__main__':
    MyMainApp().run()
