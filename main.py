import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.clock import Clock

import time
import random

kivy.require('1.9.0')

#f = open("file.txt", "r")
#print(f.read())

cars = ["Ford", "Volvo", "BMW"]
druzyna_1 = 5
druzyna_2 = 5

class MyGridLayout(GridLayout):

    def __init__(self, **kwargs):
        super(MyGridLayout, self).__init__(**kwargs)
        self.cols = 1
        self.two_cols = GridLayout()
        self.two_cols.cols = 2

        self.add_widget(Label(text="KALAMBURY", font_size=64, color=(0.92, 0.45, 0)))

        self.two_cols.add_widget(Label(text="Druzyna 1: "))
        self.druzyna_1 = TextInput(multiline=False)
        self.two_cols.add_widget(self.druzyna_1)

        self.two_cols.add_widget(Label(text="Druzyna 2: "))
        self.druzyna_2 = TextInput(multiline=False)
        self.two_cols.add_widget(self.druzyna_2)

        self.two_cols.add_widget(Label(text="Ilość Rund: "))
        self.ilosc_rund = TextInput(multiline=False)
        self.two_cols.add_widget(self.ilosc_rund)

        self.add_widget(self.two_cols)

        self.button = Button(text="Graj", font_size=64)
        self.button.bind(on_press=self.press)
        self.add_widget(self.button)

        #self.two_cols.add_widget(Label(text="ZEGAR"))

    def press(self, instance):
        self.druzyna_1.text = str(random.randint(0,100))
        self.druzyna_2.text = cars[random.randint(0,len(cars)-1)]
        #self.dr1.text = cars[random.randint(0,len(cars)-1)]
        #self.random_label.text = str(random.randint(0,100))

class MyApp(App):

    def build(self):
        return MyGridLayout()
    
MyApplication = MyApp()
MyApplication.run()