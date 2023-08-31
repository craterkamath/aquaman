import PySimpleGUI as sg
from aquaman import aquaman

sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.
layout = [  [sg.Text('Please enter the time duration between reminders')],
            [sg.Text('Format HH:MM:SS'), sg.InputText()],
            [sg.Button('Done'), sg.Button('Cancel')] ]

def main():
    # Create the Window
    window = sg.Window('Aquaman - Your water reminder buddy', layout)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            break
        aquaman(values[0])
        break
    window.close()

if __name__ == "__main__":
    main()