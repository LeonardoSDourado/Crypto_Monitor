# Autor Leonardo Dourado
# É proibida a utilização do programa ou cópia de parte do código sem a autorização do autor.

from tkinter.constants import CENTER
import PySimpleGUI as sg
from ConfigureWindow import configure_window
from functions import repeat_by_time_top_gain, repeat_by_time_top_loss, returnConfigFile, clear_gain_fields, clear_loss_fields, get_coins_by_exchange
import threading, multiprocessing
import time

sg.theme('SystemDefault') # Esquema de cores

menu_sup = ['Monitorar', ['Iniciar','!&Parar']],['Configurar',['Configurar']],['Ajuda', ['Ajuda']],['Sair', ['Sair']]

headings = ['Nome', 'Sigla', 'Símbolo','Variação 1h']
header =  [[sg.Text('  ')] + [sg.Text(h, size=(14,1)) for h in headings]]
nome_size = 30
sigla_size = 14
simbolo_size = 14
variacao1h_size = 14

layout=[[sg.Menu(menu_sup, background_color='lightsteelblue',text_color='navy', disabled_text_color='yellow', font='Verdana', pad=(10,10), key='menu_sup')],
        [sg.Text("Monitorar:", size=(10,1)),sg.Checkbox('Altas', size=(10,1), key='Checkbox_top_gain'),sg.Checkbox('Baixas', size=(10,1), key='Checkbox_top_loss')],
        [[sg.Text("Top 10 altas",size=(68,1), pad=(0,0), justification=CENTER)],
        [sg.Text("Nome",size=(nome_size-3,1), pad=(0,0)),sg.Text("Sigla",size=(sigla_size-2,1), pad=(0,0)),sg.Text("Símbolo",size=(simbolo_size-2,1), pad=(0,0)),sg.Text("Variação 1h",size=(variacao1h_size,1), pad=(0,0))],
        [sg.Input(size=(nome_size,1), pad=(0,0),disabled=True,key='top_gain_1_1'),sg.Input(size=(sigla_size,1), pad=(0,0),disabled=True,key='top_gain_1_2'),sg.Input(size=(simbolo_size,1), pad=(0,0),disabled=True,key='top_gain_1_3'),sg.Input(size=(variacao1h_size,1), pad=(0,0),disabled=True,key='top_gain_1_4')],
        [sg.Input(size=(nome_size,1), pad=(0,0),disabled=True,key='top_gain_2_1'),sg.Input(size=(sigla_size,1), pad=(0,0),disabled=True,key='top_gain_2_2'),sg.Input(size=(simbolo_size,1), pad=(0,0),disabled=True,key='top_gain_2_3'),sg.Input(size=(variacao1h_size,1), pad=(0,0),disabled=True,key='top_gain_2_4')],
        [sg.Input(size=(nome_size,1), pad=(0,0),disabled=True,key='top_gain_3_1'),sg.Input(size=(sigla_size,1), pad=(0,0),disabled=True,key='top_gain_3_2'),sg.Input(size=(simbolo_size,1), pad=(0,0),disabled=True,key='top_gain_3_3'),sg.Input(size=(variacao1h_size,1), pad=(0,0),disabled=True,key='top_gain_3_4')],
        [sg.Input(size=(nome_size,1), pad=(0,0),disabled=True,key='top_gain_4_1'),sg.Input(size=(sigla_size,1), pad=(0,0),disabled=True,key='top_gain_4_2'),sg.Input(size=(simbolo_size,1), pad=(0,0),disabled=True,key='top_gain_4_3'),sg.Input(size=(variacao1h_size,1), pad=(0,0),disabled=True,key='top_gain_4_4')],
        [sg.Input(size=(nome_size,1), pad=(0,0),disabled=True,key='top_gain_5_1'),sg.Input(size=(sigla_size,1), pad=(0,0),disabled=True,key='top_gain_5_2'),sg.Input(size=(simbolo_size,1), pad=(0,0),disabled=True,key='top_gain_5_3'),sg.Input(size=(variacao1h_size,1), pad=(0,0),disabled=True,key='top_gain_5_4')],
        [sg.Input(size=(nome_size,1), pad=(0,0),disabled=True,key='top_gain_6_1'),sg.Input(size=(sigla_size,1), pad=(0,0),disabled=True,key='top_gain_6_2'),sg.Input(size=(simbolo_size,1), pad=(0,0),disabled=True,key='top_gain_6_3'),sg.Input(size=(variacao1h_size,1), pad=(0,0),disabled=True,key='top_gain_6_4')],
        [sg.Input(size=(nome_size,1), pad=(0,0),disabled=True,key='top_gain_7_1'),sg.Input(size=(sigla_size,1), pad=(0,0),disabled=True,key='top_gain_7_2'),sg.Input(size=(simbolo_size,1), pad=(0,0),disabled=True,key='top_gain_7_3'),sg.Input(size=(variacao1h_size,1), pad=(0,0),disabled=True,key='top_gain_7_4')],
        [sg.Input(size=(nome_size,1), pad=(0,0),disabled=True,key='top_gain_8_1'),sg.Input(size=(sigla_size,1), pad=(0,0),disabled=True,key='top_gain_8_2'),sg.Input(size=(simbolo_size,1), pad=(0,0),disabled=True,key='top_gain_8_3'),sg.Input(size=(variacao1h_size,1), pad=(0,0),disabled=True,key='top_gain_8_4')],
        [sg.Input(size=(nome_size,1), pad=(0,0),disabled=True,key='top_gain_9_1'),sg.Input(size=(sigla_size,1), pad=(0,0),disabled=True,key='top_gain_9_2'),sg.Input(size=(simbolo_size,1), pad=(0,0),disabled=True,key='top_gain_9_3'),sg.Input(size=(variacao1h_size,1), pad=(0,0),disabled=True,key='top_gain_9_4')],
        [sg.Input(size=(nome_size,1), pad=(0,0),disabled=True,key='top_gain_10_1'),sg.Input(size=(sigla_size,1), pad=(0,0),disabled=True,key='top_gain_10_2'),sg.Input(size=(simbolo_size,1), pad=(0,0),disabled=True,key='top_gain_10_3'),sg.Input(size=(variacao1h_size,1), pad=(0,0),disabled=True,key='top_gain_10_4')],
        [sg.Text("Top 10 baixas",size=(68,1), pad=(0,0), justification=CENTER)],
        [sg.Text("Nome",size=(nome_size-3,1), pad=(0,0)),sg.Text("Sigla",size=(sigla_size-2,1), pad=(0,0)),sg.Text("Símbolo",size=(simbolo_size-2,1), pad=(0,0)),sg.Text("Variação 1h",size=(variacao1h_size,1), pad=(0,0))],
        [sg.Input(size=(nome_size,1), pad=(0,0),disabled=True,key='top_loss_1_1'),sg.Input(size=(sigla_size,1), pad=(0,0),disabled=True,key='top_loss_1_2'),sg.Input(size=(simbolo_size,1), pad=(0,0),disabled=True,key='top_loss_1_3'),sg.Input(size=(variacao1h_size,1), pad=(0,0),disabled=True,key='top_loss_1_4')],
        [sg.Input(size=(nome_size,1), pad=(0,0),disabled=True,key='top_loss_2_1'),sg.Input(size=(sigla_size,1), pad=(0,0),disabled=True,key='top_loss_2_2'),sg.Input(size=(simbolo_size,1), pad=(0,0),disabled=True,key='top_loss_2_3'),sg.Input(size=(variacao1h_size,1), pad=(0,0),disabled=True,key='top_loss_2_4')],
        [sg.Input(size=(nome_size,1), pad=(0,0),disabled=True,key='top_loss_3_1'),sg.Input(size=(sigla_size,1), pad=(0,0),disabled=True,key='top_loss_3_2'),sg.Input(size=(simbolo_size,1), pad=(0,0),disabled=True,key='top_loss_3_3'),sg.Input(size=(variacao1h_size,1), pad=(0,0),disabled=True,key='top_loss_3_4')],
        [sg.Input(size=(nome_size,1), pad=(0,0),disabled=True,key='top_loss_4_1'),sg.Input(size=(sigla_size,1), pad=(0,0),disabled=True,key='top_loss_4_2'),sg.Input(size=(simbolo_size,1), pad=(0,0),disabled=True,key='top_loss_4_3'),sg.Input(size=(variacao1h_size,1), pad=(0,0),disabled=True,key='top_loss_4_4')],
        [sg.Input(size=(nome_size,1), pad=(0,0),disabled=True,key='top_loss_5_1'),sg.Input(size=(sigla_size,1), pad=(0,0),disabled=True,key='top_loss_5_2'),sg.Input(size=(simbolo_size,1), pad=(0,0),disabled=True,key='top_loss_5_3'),sg.Input(size=(variacao1h_size,1), pad=(0,0),disabled=True,key='top_loss_5_4')],
        [sg.Input(size=(nome_size,1), pad=(0,0),disabled=True,key='top_loss_6_1'),sg.Input(size=(sigla_size,1), pad=(0,0),disabled=True,key='top_loss_6_2'),sg.Input(size=(simbolo_size,1), pad=(0,0),disabled=True,key='top_loss_6_3'),sg.Input(size=(variacao1h_size,1), pad=(0,0),disabled=True,key='top_loss_6_4')],
        [sg.Input(size=(nome_size,1), pad=(0,0),disabled=True,key='top_loss_7_1'),sg.Input(size=(sigla_size,1), pad=(0,0),disabled=True,key='top_loss_7_2'),sg.Input(size=(simbolo_size,1), pad=(0,0),disabled=True,key='top_loss_7_3'),sg.Input(size=(variacao1h_size,1), pad=(0,0),disabled=True,key='top_loss_7_4')],
        [sg.Input(size=(nome_size,1), pad=(0,0),disabled=True,key='top_loss_8_1'),sg.Input(size=(sigla_size,1), pad=(0,0),disabled=True,key='top_loss_8_2'),sg.Input(size=(simbolo_size,1), pad=(0,0),disabled=True,key='top_loss_8_3'),sg.Input(size=(variacao1h_size,1), pad=(0,0),disabled=True,key='top_loss_8_4')],
        [sg.Input(size=(nome_size,1), pad=(0,0),disabled=True,key='top_loss_9_1'),sg.Input(size=(sigla_size,1), pad=(0,0),disabled=True,key='top_loss_9_2'),sg.Input(size=(simbolo_size,1), pad=(0,0),disabled=True,key='top_loss_9_3'),sg.Input(size=(variacao1h_size,1), pad=(0,0),disabled=True,key='top_loss_9_4')],
        [sg.Input(size=(nome_size,1), pad=(0,0),disabled=True,key='top_loss_10_1'),sg.Input(size=(sigla_size,1), pad=(0,0),disabled=True,key='top_loss_10_2'),sg.Input(size=(simbolo_size,1), pad=(0,0),disabled=True,key='top_loss_10_3'),sg.Input(size=(variacao1h_size,1), pad=(0,0),disabled=True,key='top_loss_10_4')],
        [sg.Text("Situação:"),sg.Text("Parado",key='status',size=(10,1))]]]

window = sg.Window('Crypto Monitor',location=(20,20),finalize=True).Layout(layout)

get_coins_by_exchange("binance") # Baixa a lista de moedas da exchange e salva em arquivo.

#x = None
#y = None

while True:
    global x
    global y
    button, values = window.Read()
    if values == None:
        break
    else:
        if button=='Sair':
            break
        elif button==sg.WIN_CLOSED:
            break
        elif button=='Sobre':
            pass
        elif button=='Ajuda':
            pass
        elif button=='Iniciar':
            window.Element('status').Update("Executando")
            menu_sup = ['Monitorar', ['!&Iniciar','Parar']],['Configurar',['!&Configurar']],['Ajuda', ['Ajuda']],['Sair', ['Sair']]
            window.Element("menu_sup").Update(menu_sup)

            if(values['Checkbox_top_gain']==True):
                x = threading.Thread(target=repeat_by_time_top_gain, args=(10, int(returnConfigFile()[1]), int(returnConfigFile()[2]), ["binance"], window,), daemon=True)
                x.start()
                window['Checkbox_top_gain'].Update(disabled=True)
            else:
                clear_gain_fields(10, window)
                window['Checkbox_top_gain'].Update(disabled=True)

            if(values['Checkbox_top_loss']==True):
                y = threading.Thread(target=repeat_by_time_top_loss, args=(10, int(returnConfigFile()[1]), int(returnConfigFile()[2]), ["binance"], window,), daemon=True)
                y.start()
                window['Checkbox_top_loss'].Update(disabled=True)
            else:
                clear_loss_fields(10, window)
                window['Checkbox_top_loss'].Update(disabled=True)
        elif button=='Parar':
            if(values['Checkbox_top_gain']==True):
                x.join()
                window['Checkbox_top_gain'].Update(disabled=False)
            else:
                window['Checkbox_top_gain'].Update(disabled=False)

            if(values['Checkbox_top_loss']==True):
                y.join()
                window['Checkbox_top_loss'].Update(disabled=False)
            else:
                window['Checkbox_top_loss'].Update(disabled=False)

            clear_gain_fields(10, window)
            clear_loss_fields(10, window)
            window.Element('status').Update("Parado")
            menu_sup = ['Monitorar', ['Iniciar','Parar']],['Configurar',['Configurar']],['Ajuda', ['Ajuda']],['Sair', ['Sair']]
            window.Element("menu_sup").Update(menu_sup)
        elif button=='Configurar':
            configure_window()
        else:
            window.close()

window.close()