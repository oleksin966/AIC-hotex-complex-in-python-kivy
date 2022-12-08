from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivymd.uix.list import OneLineListItem, TwoLineListItem, ThreeLineListItem
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp
from db_processing import DBEvents
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt


Window.size = (412,915)
#Window.size = (915,412)

class LoginPage(Screen):
    def verify_credentials(self):
        if self.ids["login"].text == "" and self.ids["passw"].text == "":
            self.manager.current = "menu"

class MenuScreen(Screen):
    pass


class MainTitleExit(Widget):
    def exit(self):
        if (self.parent.name == 'menu'):
            self.parent.manager.current = "login_page" 
            self.ids["btn_menu"].text = "<< Вихід"
        else:
            if (self.parent.name != 'menu'):
                self.ids["btn_menu"].text = "<< Меню"
            self.parent.manager.current = "menu"



class FirstInfoScreen(Screen, DBEvents):
    def __init__(self, *args,**kwargs):
        super(FirstInfoScreen, self).__init__(**kwargs)
        self.start = None 
        self.end = None
        self.data_table = None
    def show_calendar(self):
        calendar = MDDatePicker(mode="range")
        calendar.bind(on_save=self.save_date)
        calendar.open()
    def save_date(self, instance, value, date_range):
        self.ids["cal_1_start"].text = str(date_range[0])
        self.ids["cal_1_end"].text = str(date_range[-1])
    def print_table(self):
        if (self.data_table is not None):
            self.ids["show_table1"].remove_widget(self.data_table)
        self.start = str(self.ids["cal_1_start"].text)
        self.end = str(self.ids["cal_1_end"].text)
        num = str(self.ids["settlement"].text)
        get_data = self.first_query(self.start, self.end, num)
        if len(get_data) == 0:
            self.ids["table_1"].height = "100dp"
            self.ids["table_1"].padding = [0,0,0,0]
            self.data_table = Label(text="За данний період інформація відсутня", 
                color=[0,0,0], font_size=20, text_size=self.size,halign='center',valign='middle')
        else:
            self.ids["table_1"].height = "500dp"
            self.ids["table_1"].padding = [-20,0,0,0]
            self.data_table = MDDataTable(pos_hint={'center_x': 0, 'center_y': 0.5},
                     size_hint=(1, 1),
                     rows_num=len(get_data),
                     column_data=[
                        ("№", dp(5)),
                        ("Фірма", dp(20)),
                        ("К-сть місць", dp(15)),
                        ("З дати", dp(20)),
                        ("По дату", dp(20))
                     ],
                     row_data=get_data
                     )
        self.ids["show_table1"].add_widget(self.data_table)


class SecondInfoScreen(Screen, DBEvents):
    def __init__(self, *args,**kwargs):
        super(SecondInfoScreen, self).__init__(**kwargs)
        self.start = None
        self.end = None
        self.data_table = None
        self.btn = {}
    def add_buttons(self):
            corpuses = self.get_list_corpus_name()
            for index in range(len(corpuses)):
                if ( len(self.btn)  >= len(corpuses)):
                    break
                self.btn["id" + str(index)] = Button(text=corpuses[index][0], size_hint_y=None, height=44, 
                    background_color = (33/255.0,150/255.0,243/255.0,1), font_size=20)
                self.btn["id" + str(index)].bind(on_release=lambda btn: self.ids["dropdown2"].select(btn.text))
                self.ids["dropdown2"].add_widget(self.btn["id" + str(index)])
    def show_calendar(self):
        calendar = MDDatePicker(mode="range")
        calendar.bind(on_save=self.save_date)
        calendar.open()
    def save_date(self, instance, value, date_range):
        self.ids["cal_2_start"].text = str(date_range[0])
        self.ids["cal_2_end"].text = str(date_range[-1])
    def print_table(self):
        if (self.data_table is not None):
            self.ids["show_table2"].remove_widget(self.data_table)
        corpus = self.ids["corpus"].text
        floor_num = self.ids["floor_num"].text
        start = self.ids["cal_2_start"].text
        end = self.ids["cal_2_end"].text
        get_data = self.second_query(self, start, end, corpus, floor_num)
        self.data_table = MDDataTable(pos_hint={'center_x': 0, 'center_y': 0.5},
                 size_hint=(1, 1),
                 rows_num=len(get_data),
                 column_data=[
                    ("№", dp(5)),
                    ("Постояльці", dp(30)),
                    ("Назва корпуса", dp(25)),
                    ("Клас", dp(10)),
                    ("Поверх", dp(15)),
                    ("ID Номера", dp(20))
                 ],
                 row_data=get_data
                 )
        
        self.ids["show_table2"].add_widget(self.data_table)
       
class ThirdInfoScreen(Screen, DBEvents):
    def __init__(self, *args,**kwargs):
        super(ThirdInfoScreen, self).__init__(**kwargs)
        self.data_table = None
    def print_table(self):
        if (self.data_table is not None):
            self.ids["show_table3"].remove_widget(self.data_table)
        self.data_table = MDDataTable(pos_hint={'center_x': 0, 'center_y': 0.5},
                 size_hint=(1, 1),
                 rows_num=self.count_free_room(),
                 column_data=[
                    ("ID Номера", dp(18)),
                    ("Назва корпусу", dp(25)),
                    ("Поверх", dp(15)),
                    ("Місткість", dp(17))
                 ],
                 row_data=self.third_query()
                 )
        
        self.ids["show_table3"].add_widget(self.data_table)

class FourInfoScreen(Screen, DBEvents):
    def __init__(self, *args,**kwargs):
        super(FourInfoScreen, self).__init__(**kwargs)
        self.data_table = None
    def print_table(self):
        if (self.data_table is not None):
            self.ids["show_table4"].remove_widget(self.data_table)
        class_hotel = str(self.ids["class"].text)
        capasity =  str(self.ids["capasity"].text)
        price =  str(self.ids["price"].text)
        self.data_table = MDDataTable(pos_hint={'center_x': 0, 'center_y': 0.5},
                 size_hint=(1, 1),
                 rows_num=self.count_free_room(),
                 column_data=[
                    ("ID", dp(5)),
                    ("Назва корпусу", dp(25)),
                    ("Ціна за добу", dp(25)),
                    ("Поверх", dp(15)),
                    ("Клас", dp(15)),
                    ("Місткість", dp(17))

                 ],
                 row_data=self.four_query(class_hotel, capasity, price)
                 )
        
        self.ids["show_table4"].add_widget(self.data_table)

class FiveInfoScreen(Screen, DBEvents):
    def __init__(self, *args,**kwargs):
        super(FiveInfoScreen, self).__init__(**kwargs)
        self.data_table = None
    def print_table(self):
        if (self.data_table is not None):
            self.ids["show_table5"].remove_widget(self.data_table)
        room_id = str(self.ids["room_id"].text)
        get_data = self.five_query(room_id)
        #print(get_data)
        self.data_table = MDDataTable(pos_hint={'center_x': 0, 'center_y': 0.8},
                 size_hint=(1, 1),
                 rows_num=self.count_free_room(),
                 column_data=[
                    ("Інформація", dp(40)),
                    ("Про номер", dp(30)),
                 ],
                 row_data=[
                 ("ID номера: ", get_data[0][0]),
                 ("Корпус: ", get_data[0][1]),
                 ("Поверх: ", get_data[0][2]),
                 ("Місткість: ", get_data[0][3]),
                 ("Статус номера на сьогодні: ", get_data[0][4]),
                 ("Початок броні: ", get_data[0][5]),
                 ("Кінець броні: ", get_data[0][6]),
                 ("Ціна за добу: ", get_data[0][7]),
                 ("Днів до наступної броні залишилось: ", get_data[0][8]),

                 ]
                 )
        
        self.ids["show_table5"].add_widget(self.data_table)



class SixInfoScreen(Screen, DBEvents):
    def __init__(self, *args,**kwargs):
        super(SixInfoScreen, self).__init__(**kwargs)
        self.start = None
        self.end = None
        self.data_table = None
    def show_calendar(self):
        calendar = MDDatePicker()
        calendar.bind(on_save=self.save_date)
        calendar.open()
    def save_date(self, instance, value, date_range):
        self.ids["date_6"].text = str(value)
    def print_table(self):
        if (self.data_table is not None):
            self.ids["show_table6"].remove_widget(self.data_table)
        date_value = str(self.ids["date_6"].text)
        self.data_table = MDDataTable(pos_hint={'center_x': 0, 'center_y': 0.8},
                 size_hint=(1, 1),
                 rows_num=self.count_not_free_room(),
                 column_data=[
                    ("Назва корпусу", dp(25)),
                    ("Поверх", dp(15)),
                    ("ID Номера", dp(18)),
                    ("Закінчення броні", dp(25))
                 ],
                 row_data=self.six_query(date_value)
                 )
        
        self.ids["show_table6"].add_widget(self.data_table)


class SevenInfoScreen(Screen, DBEvents):
    def __init__(self, *args,**kwargs):
        super(SevenInfoScreen, self).__init__(**kwargs)
        self.start =None
        self.end = None
        self.data_table = None
        self.btn = {}
    def add_buttons(self):
        comapny = self.get_list_company_name()
        for index in range(len(comapny)):
            if ( len(self.btn)  >= len(comapny)):
                break
            self.btn["id" + str(index)] = Button(text=comapny[index][0], size_hint_y=None, height=44, 
                background_color = (33/255.0,150/255.0,243/255.0,1), font_size=20)
            self.btn["id" + str(index)].bind(on_release=lambda btn: self.ids["dropdown7"].select(btn.text))
            self.ids["dropdown7"].add_widget(self.btn["id" + str(index)])
    def show_calendar(self):
        calendar = MDDatePicker(mode="range")
        calendar.bind(on_save=self.save_date)
        calendar.open()
    def save_date(self, instance, value, date_range):
        self.ids["cal_7"].text = f'З {str(date_range[0])} по {str(date_range[-1])}'
        self.start = str(date_range[0])
        self.end = str(date_range[-1])
    def print_table(self):
        if (self.data_table is not None):
            self.ids["show_table7"].remove_widget(self.data_table)

        company = self.ids["list_company7"].text
        get_data = self.seven_query(self.start, self.end, company)
        if len(get_data[0]) == 0:
            self.data_table = Label(text="Інформація Відсутня", 
                color=[0,0,0], font_size=20, text_size=self.size,halign='center',valign='middle')
        else:
            list_room_str = ""
            for i in range(len(get_data[1])):
                list_room_str += str(get_data[1][i][0]) + ","
            self.data_table = MDDataTable(pos_hint={'center_x': 0, 'center_y': 0.5},
                     size_hint=(1, 1),
                     rows_num=7,
                     column_data=[
                        ("Обсяг:", dp(40)),
                        ("Бронювання", dp(40))
                     ],
                     row_data=[
                     ("Фірма/Компанія:",get_data[0][0][0]),
                     ("Вказаний період:",str(get_data[0][0][2]) + " - " + str(get_data[0][0][3])),
                     ("Заброньовані номери:",list_room_str),
                     ("Переважаючий номер:",get_data[0][0][1])
                     ]
                     )
            
        self.ids["show_table7"].add_widget(self.data_table)



class EightInfoScreen(Screen, DBEvents):
    def __init__(self, *args,**kwargs):
        super(EightInfoScreen, self).__init__(**kwargs)
        self.row_count = len(self.get_list_complaints())

    def print_table(self):
        complaints = self.eight_query()
        table = self.ids["show_table8"]
        for i in range(len(complaints)):
            table.add_widget(Label(text=complaints[i][3], font_size=14,color =[0,0,0],
                size_hint=(None,None),height="50dp", width="200dp"))
            table.add_widget(Label(text=complaints[i][2],color =[0,0,0],
                size_hint=(1,None), width="200dp",
                text_size=self.size, halign='center', valign='middle'))
            table.add_widget(Label(text=complaints[i][1], font_size=14,color =[0,0,0],
                size_hint=(None,None),height="50dp", width="200dp"))



class ElevenInfoScreen(Screen, DBEvents):
    def __init__(self, *args,**kwargs):
        super(ElevenInfoScreen, self).__init__(**kwargs)
        self.data_table_people = None
        self.data_table_company = None
    def print_table(self):
        if (self.data_table_people is not None and self.data_table_company is not None):
            self.ids["show_table11_people"].remove_widget(self.data_table_people)
            self.ids["show_table11_company"].remove_widget(self.data_table_company)
        get_data = self.eleven_query()
        self.data_table_people = MDDataTable(pos_hint={'center_x': 0, 'center_y': 0.5},
                 size_hint=(1, 1),
                 rows_num=len(self.get_list_corpus_name()),
                 column_data=[
                    ("Назва Корпусу", dp(25)),
                    ("Клієнт", dp(25)),
                    ("Кількість відвідувань", dp(20))
                 ],
                 row_data=get_data[1]
                 )
        self.data_table_company = MDDataTable(pos_hint={'center_x': 0, 'center_y': 0.5},
                 size_hint=(1, 1),
                 rows_num=len(self.get_list_corpus_name()),
                 column_data=[
                    ("Назва Корпусу", dp(25)),
                    ("Клієнт", dp(25)),
                    ("Кількість відвідувань", dp(20))
                 ],
                 row_data=get_data[0]
                 )
        self.ids["show_table11_people"].add_widget(self.data_table_people)
        self.ids["show_table11_company"].add_widget(self.data_table_company)



class TwelveInfoScreen(Screen, DBEvents):
    def __init__(self, *args,**kwargs):
        super(TwelveInfoScreen, self).__init__(**kwargs)
        self.start = None 
        self.end = None
        self.data_table_people = None
        self.data_table_company = None
    def show_calendar(self):
        calendar = MDDatePicker(mode="range")
        calendar.bind(on_save=self.save_date)
        calendar.open()
    def save_date(self, instance, value, date_range):
        self.ids["cal_12_start"].text = str(date_range[0])
        self.ids["cal_12_end"].text = str(date_range[-1])
    def print_table(self):
        if (self.data_table_people is not None and self.data_table_company is not None):
            self.ids["show_table12_people"].remove_widget(self.data_table_people)
            self.ids["show_table12_company"].remove_widget(self.data_table_company)
        self.start = str(self.ids["cal_12_start"].text)
        self.end = str(self.ids["cal_12_end"].text)
        get_data = self.twelve_query(self.start, self.end)
        self.data_table_company = MDDataTable(pos_hint={'center_x': 0, 'center_y': 0.5},
                 size_hint=(1, 1),
                 rows_num=len(get_data[0]),
                 column_data=[
                    ("ID Фірми:", dp(20)),
                    ("Назва", dp(50))
                 ],
                 row_data=get_data[0]
                 )
        self.data_table_people = MDDataTable(pos_hint={'center_x': 0, 'center_y': 0.5},
                 size_hint=(1, 1),
                 rows_num=len(get_data[1]),
                 column_data=[
                    ("ID Особи:", dp(20)),
                    ("Ім'я та Прізвище", dp(50))
                 ],
                 row_data=get_data[1]
                 )
        self.ids["show_table12_company"].add_widget(self.data_table_company)
        self.ids["show_table12_people"].add_widget(self.data_table_people)



class ThirteenInfoScreen(Screen, DBEvents):
    def __init__(self, *args,**kwargs):
        super(ThirteenInfoScreen, self).__init__(**kwargs)
        self.data_table = None
        self.btn = {}
    def print_table(self):
        if (self.data_table is not None):
            self.ids["show_table13"].remove_widget(self.data_table)

        name = str(self.ids["client_name"].text)
        get_data = self.threteen_query(name)

        self.data_table = MDDataTable(pos_hint={'center_x': 0, 'center_y': 0.5},
                 size_hint=(1, 1),
                 rows_num=len(get_data[0]),
                 column_data=[
                 ("№", dp(5)),
                 ("Ім'я та Прізвище", dp(25)),
                 ("Номер поселення", dp(25)),
                 ("Початок поселення", dp(25)),
                 ("Кінець поселення", dp(25)),
                 ("Ціна за номер", dp(15)),
                 ("Ціна додаткових послуг", dp(30)), 
                 ("Загальна ціна", dp(15))

                 ],
                 row_data=get_data
                 )
        self.ids["show_table13"].add_widget(self.data_table)


class FourteenInfoScreen(Screen, DBEvents):
    def __init__(self, *args,**kwargs):
        super(FourteenInfoScreen, self).__init__(**kwargs)
        self.start = None 
        self.end = None
        self.data_table = None
    def show_calendar(self):
        calendar = MDDatePicker(mode="range")
        calendar.bind(on_save=self.save_date)
        calendar.open()
    def save_date(self, instance, value, date_range):
        self.ids["cal_14_start"].text = str(date_range[0])
        self.ids["cal_14_end"].text = str(date_range[-1])
    def print_table(self):
        if (self.data_table is not None):
            self.ids["show_table14"].remove_widget(self.data_table)
        self.start = str(self.ids["cal_14_start"].text)
        self.end = str(self.ids["cal_14_end"].text)
        room_id = str(self.ids["number_room"].text)
        get_data = self.fourteen_query(self.start, self.end, room_id)
        if len(get_data) == 0:
            self.ids["table_14"].height = "100dp"
            self.ids["table_14"].padding = [0,0,0,0]
            self.data_table = Label(text="Не знайдено записів про Номер "+room_id+"", 
                color=[0,0,0], font_size=20, text_size=self.size,halign='center',valign='middle')
        else:
            self.ids["table_14"].height = "400dp"
            self.ids["table_14"].padding = [-20,0,0,0]
            self.data_table = MDDataTable(pos_hint={'center_x': 0, 'center_y': 0.5},
                     size_hint=(1, 1),
                     rows_num=3,
                     column_data=[
                        ("Номер", dp(12)),
                        ("Клієнт", dp(30)),
                        ("Дата заселення", dp(20)),
                        ("Дата виселення", dp(20)),
                     ],
                     row_data=get_data
                     )
        self.ids["show_table14"].add_widget(self.data_table)

class FifteenInfoScreen(Screen, DBEvents):
    def __init__(self, *args,**kwargs):
        super(FifteenInfoScreen, self).__init__(**kwargs)
    def on_pre_enter(self):
        self.get_data()

    def get_data(self):
        tmp = self.fifteen_query()
        return tmp

class NineInfoScreen(Screen, DBEvents):
    def __init__(self, *args,**kwargs):
        super(NineInfoScreen, self).__init__(**kwargs)
        self.get_data = self.nine_query()
        self.data_graphic_1 = None
        self.data_graphic_2 = None
    def print_graphic(self):
        if (self.data_graphic_1 is not None):
            self.ids["graphic"].remove_widget(self.data_graphic_1)
        graphic = self.ids["graphic"]
        self.data_graphic_1 = FigureCanvasKivyAgg(plt.gcf())
        graphic.add_widget(self.data_graphic_1)
        date = []
        capital = []
        capital1 = []
        for i in self.get_data:
            date_m = i[0][:-3]
            date.append(date_m)
            capital.append(i[1])

        plt.subplots_adjust(wspace=0.6, hspace=0.6, left=0.18, bottom=0.24, right=0.96, top=0.9)
        plt.plot(date,capital)
        plt.title("Залежність прибутку від місяця")
        plt.ylabel("Прибуток($)")
        plt.xlabel("Місяці")
        plt.xticks(rotation=45)
        plt.yticks()
        plt.grid()



sm = ScreenManager()
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(LoginPage(name='login_page'))
sm.add_widget(FirstInfoScreen(name='first_info'))
sm.add_widget(SecondInfoScreen(name='second_info'))
sm.add_widget(ThirdInfoScreen(name='third_info'))
sm.add_widget(FourInfoScreen(name='four_info'))
sm.add_widget(FiveInfoScreen(name='five_info'))
sm.add_widget(SixInfoScreen(name='six_info'))
sm.add_widget(SevenInfoScreen(name='seven_info'))
sm.add_widget(EightInfoScreen(name='eight_info'))
sm.add_widget(NineInfoScreen(name='nine_info'))
sm.add_widget(ElevenInfoScreen(name='eleven_info'))
sm.add_widget(TwelveInfoScreen(name='twelve_info'))
sm.add_widget(ThirteenInfoScreen(name='thirteen_info'))
sm.add_widget(FourteenInfoScreen(name='fourteen_info'))
sm.add_widget(FifteenInfoScreen(name='fifteen_info'))

class DemoApp(MDApp):
    def build(self):
        #screen = Builder.load_string(screen_helper)
        screen = Builder.load_file('kivy_file.kv')
        return screen

DemoApp().run()
