from kivy.app import App
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.metrics import dp

import random

with open('file.txt', 'r', encoding="utf-8") as file:
    words = file.read().splitlines()
    i = 0
    for val in words:
        words[i] = val.split(":")
        i += 1
    print(words)

class MainLayout(FloatLayout):
    stopwatch_txt = StringProperty()
    button_txt = StringProperty()
    records_count = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.stage = 0
        self.current_team = 1
        self.team1_players = 0
        self.team1_cp = 0
        self.team2_players = 0
        self.team2_cp = 0
        self.rounds = 0
        self.current_round = 0
        self.t1_points = 0
        self.t2_points = 0
        self.timePerRound = [0,0,0]
        self.seconds = self.timePerRound[2]
        self.minutes = self.timePerRound[1]
        self.houres = self.timePerRound[0]
        self.button_txt = "START"

    def next_stage(self):
        self.stage += 1
        if self.stage == 1:
            self.settings()
        elif self.stage == 2:
            self.setSettings()
        elif self.stage == 3:
            self.start_stopwatch()
        elif self.stage == 4:
            self.reset()
        else:
            self.restart()

    def update_time(self, args):
        self.seconds -= 1
        if(self.houres == 0 and self.minutes == 0 and self.seconds <= 0):
            self.timeOut()
        if(self.houres < 24):
            if(self.seconds < 0):
                self.minutes -= 1
                self.seconds = 59
            if(self.minutes < 0):
                self.houres -= 1
                self.minutes = 59
                self.seconds = 0
        self.stopwatch_txt = f'{str(self.houres).rjust(2, "0")}:{str(self.minutes).rjust(2, "0")}:{str(self.seconds).rjust(2, "0")}'
        
    def settings(self):
        self.ids['laps'].add_widget(Label(text= "Ilość graczy w druzynie 1:", color=[1,1,1,1], texture_size=self.size, font_size=dp(32)))
        self.players_t1 = TextInput(multiline=False)
        self.ids['laps'].add_widget(self.players_t1)
        self.ids['laps'].add_widget(Label(text= "Ilość graczy w druzynie 2:", color=[1,1,1,1], texture_size=self.size, font_size=dp(32)))
        self.players_t2 = TextInput(multiline=False)
        self.ids['laps'].add_widget(self.players_t2)
        self.ids['laps'].add_widget(Label(text= "Ilość rund:", color=[1,1,1,1], texture_size=self.size, font_size=dp(32)))
        self.round = TextInput(multiline=False)
        self.ids['laps'].add_widget(self.round)
        self.ids['laps'].add_widget(Label(text= "Czas rundy(w sekundach):", color=[1,1,1,1], texture_size=self.size, font_size=dp(32)))
        self.tpr = TextInput(multiline=False)
        self.ids['laps'].add_widget(self.tpr)

    def setSettings(self):
        self.team1_players = int(self.players_t1.text)
        self.team2_players = int(self.players_t2.text)
        self.rounds = int(self.round.text)
        timrPerRoundInSeconds= int(self.tpr.text)
        self.timePerRound[2]=timrPerRoundInSeconds%60
        timrPerRoundInSeconds=int(timrPerRoundInSeconds/60)
        self.timePerRound[1]=timrPerRoundInSeconds%60
        self.timePerRound[0]=int(timrPerRoundInSeconds/60)
        self.seconds=self.timePerRound[2]
        self.minutes=self.timePerRound[1]
        self.houres =self.timePerRound[0]
        self.next_stage()

    def start_stopwatch(self):
        self.ids['laps'].clear_widgets()
        num = random.randint(0,len(words)-1)
        Clock.schedule_interval(self.update_time, 1)
        if self.current_team == 1:
            self.current_round += 1
            if self.current_round > self.rounds:
                self.end()
            self.team1_cp += 1
            if self.team1_cp > self.team1_players:
                self.team1_cp = 1
            self.current_team = 2
            self.ids['laps'].add_widget(Label(text= "RUNDA: "+str(self.current_round)+" Dryżyna: 1 Gracz: "+str(self.team1_cp), color=[0,0,1,1], texture_size=self.size, font_size=dp(32)))
        else:
            self.team2_cp += 1
            if self.team2_cp > self.team2_players:
                self.team2_cp = 1
            self.current_team = 1
            self.ids['laps'].add_widget(Label(text= "RUNDA: "+str(self.current_round)+" Dryżyna: 2 Gracz: "+str(self.team2_cp), color=[1,0,0,1], texture_size=self.size, font_size=dp(32)))
        self.ids['laps'].add_widget(Label(text= "Kategoria: "+words[num][1], color=[1,1,1,1], texture_size=self.size, font_size=dp(32)))
        self.ids['laps'].add_widget(Label(text= "Hasło: "+words[num][0], color=[1,1,1,1], texture_size=self.size, font_size=dp(32)))
        #self.ids['laps'].add_widget(Label(text=str(self.t1_points)+" "+str(self.t2_points)))
        self.button_txt = "STOP"

    def reset(self):
        if self.current_team == 1:
            self.t2_points += 1
        else:
            self.t1_points += 1
        self.seconds = self.timePerRound[2]
        self.minutes = self.timePerRound[1]
        self.houres = self.timePerRound[0]
        Clock.unschedule(self.update_time)
        self.stage -= 2
        self.button_txt = "START"

    def timeOut(self):
        if self.current_team == 1:
            self.t2_points -= 1
        else:
            self.t1_points -= 1
        self.reset()

    def end(self):
        self.ids['laps'].clear_widgets()
        Clock.unschedule(self.update_time)
        self.stage+=10
        self.ids['laps'].add_widget(Label(text= "KONIEC GRY!!!", color=[1,1,1,1], texture_size=self.size, font_size=dp(32)))
        if self.t1_points>self.t2_points:
            self.ids['laps'].add_widget(Label(text= "Wygrała drużyna 1, wynikiem "+str(self.t1_points)+" do "+str(self.t2_points)+"!", color=[0,0,1,1], texture_size=self.size, font_size=dp(32)))
        elif self.t2_points>self.t1_points:
            self.ids['laps'].add_widget(Label(text= "Wygrała drużyna 2, wynikiem "+str(self.t2_points)+" do "+str(self.t1_points)+"!", color=[1,0,0,1], texture_size=self.size, font_size=dp(32)))
        else:
            self.ids['laps'].add_widget(Label(text= "Remis, obie drużyny zdobyły po "+str(self.t1_points)+" punktów!", color=[1,1,1,1], texture_size=self.size, font_size=dp(32)))

    def restart(self):
        self.ids['laps'].clear_widgets()
        self.stage = 0
        self.current_team = 1
        self.team1_players = 0
        self.team1_cp = 0
        self.team2_players = 0
        self.team2_cp = 0
        self.rounds = 0
        self.current_round = 0
        self.t1_points = 0
        self.t2_points = 0
        self.timePerRound = [0,0,0]
        self.seconds = self.timePerRound[2]
        self.minutes = self.timePerRound[1]
        self.houres = self.timePerRound[0]
        self.button_txt = "START"

class MainApp(App):

    def build(self):
        Window.size = [360, 640]
        return Builder.load_file('main.kv')


if __name__ == '__main__':
    MainApp().run()