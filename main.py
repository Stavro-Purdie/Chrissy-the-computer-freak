import PySimpleGUI as sg
import time

# All the stuff inside your window.
layout = [  [sg.Text('Time Survived: 0:00', key='time')],
            [sg.Text('The aim is to remain focused on what you are doing. Do not be distracted by this game. The longer you survive, the higher your score.')],
            [sg.Button('Start')], [sg.Button('Spare Me')],
            [sg.Text('Chat with the man in charge of the game:')],
            [sg.InputText(key='input')],
            [sg.Button('Send')]],

# Create the Window
window = sg.Window('Hello Example', layout)

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()

    # if user closes window or clicks cancel
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break

    # Start a timer and change the time text.
    if event == 'Start':
        start_time = time.time()
        while True:
            current_time = time.time()
            elapsed_time = current_time - start_time
            window['time'].update('Time Survived: ' + time.strftime("%M:%S", time.gmtime(elapsed_time)))
            event, values = window.read(timeout=10)
            if event == 'Spare Me':
                break
            if event == sg.WIN_CLOSED or event == 'Cancel':
                break


window.close()