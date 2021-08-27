# Autor Leonardo Dourado
# É proibida a utilização do programa ou cópia de parte do código sem a autorização do autor.

import PySimpleGUI as sg
from functions import loadConfigFile, saveParametersInFile, returnConfigFile

def configure_window():
    '''Essa função invoca a janela de configuração do sistema.'''

    config_parameters = returnConfigFile()

    sg.theme('SystemDefault') # Esquema de cores

    menu_sup = ['&Configuração',['&Carregar','&Salvar']],['&Ajuda', ['&Sobre']],['&Sair', ['&Sair']]

    label_size = 25
    input_text_size = 30

    layout=[[sg.Menu(menu_sup, background_color='lightsteelblue',text_color='navy', disabled_text_color='yellow', font='Verdana', pad=(10,10))],
            [sg.Text('Quantidade de moedas listadas',size=(label_size,1)), sg.InputText(config_parameters[0],size=(input_text_size,1))],
            [sg.Text('Marketcap mínimo',size=(label_size,1)), sg.InputText(config_parameters[1],size=(input_text_size,1))],
            [sg.Text('Volume mínimo em 24h',size=(label_size,1)), sg.InputText(config_parameters[2],size=(input_text_size,1))],
            [sg.Text('Atualização do dados em seg.',size=(label_size,1)), sg.InputText(config_parameters[3],size=(input_text_size,1))]]

    window = sg.Window('Crypto Monitorator',location=(20,20),finalize=True).Layout(layout)

    while True:
        button, values = window.Read()

        if button == 'Sair':
            break
        elif button == ' ':
            break
        elif button == sg.WIN_CLOSED:
            break
        elif values == None:
            break
        else:
            top_currencies = values[1] # Quantidade de moedas listadas no top
            marketcap_greater = values[2] # Valor de mercado mínimo
            volume24h = values[3] # Volume mínimo em U$ negociado nas últimas 24 horas
            exchanges = ["binance"] # Exchange que as moedas precisam estar listadas
            time_refresh_seconds = values[4] # Atualização da tela em segundos
            loadConfigFile(window)

            if button=='Carregar':
                loadConfigFile(window)
                pass
            elif button=='Salvar':
                saveParametersInFile(top_currencies,marketcap_greater,volume24h,time_refresh_seconds)
                pass
                loadConfigFile(window)
            elif button=='Sobre':
                pass
            else:
                break

    window.close()