import PySimpleGUI as sg
import os
import glob


dirIs = os.getcwd()
txtfiles = []
all_txt_files = []
sg.theme('DarkAmber')

# ------------ FORMATING THE SYSTEM DATE ----------------
from datetime import date
today = date.today()
d1 = today.strftime("%d%m%Y") # ddmmYY


# --------------- WHAT FILES OF CURRENT MONTH IN THE FOLDER? -------------
def existing_entries():
    global all_txt_files
    fileNames = glob.glob("/Users/georgiostrialonis/Documents/calendar_notes/*.txt")
    for i in range(len(fileNames)):
        existing_files = fileNames[i] # these include the path also
        files_as_txt = existing_files.split('/')[-1] # this prints, e.g. 09112021.txt
        all_txt_files.append(files_as_txt) # all files as a single list
# print(all_txt_files)  
# ---------------- MAIN PROGRAM: SMALL WINDOW WITH CALENDAR BUTTON -----
def main():
    global chosen_date, file_name, all_txt_files

    layout = [
            [sg.Text("ALWAYS press the CALENDAR button first"'\n'"and then CHOOSE a DATE", key='-TXT-', justification='center')],
            [sg.Input(key='-IN-', size=(40,1), visible=False), sg.CalendarButton('CALENDAR', font=(18), button_color=('orange', 'black'), size=(18,1), close_when_date_chosen=False,  target='-IN-', no_titlebar=False, format="%d-%m-%Y")],
            [sg.Button('Make an Entry'), sg.Button('Open Entry', enable_events=True), sg.Exit()]
            ]

    window = sg.Window('window', layout, location=(450,0), element_justification='c', finalize=True)
    
    while True:
        event, values = window.read()
        chosen_date = values['-IN-'] # this shows the date chosen, e.g 24-11-2021
        if event == 'Exit' or event == sg.WIN_CLOSED:
            break
        if event == 'Make an Entry':
            make_entry()
        if event == 'Open Entry':
            open_entry()
        
    window.close()

# ---------------- MAKE ENTRIES / NOTES -------------------------
def make_entry():
    global chosen_date, all_txt_files
    existing_entries()
    file_name = chosen_date
    file_name = file_name.replace('-', '')+'.txt' # replace dashes
    
    print(all_txt_files)
    if chosen_date == '': # if no calendar date has been chosen ...then
        sg.popup('Click on CALENDAR first to choose date')
        main()

    elif file_name in all_txt_files: # if such an entry already exists as file ...
        sg.popup("File exists. Open it from main window.")
        main()

    else:
        layout = [
            [sg.Text('', font=(14), enable_events=True, key='note-here')],
            [sg.Multiline(size=(50,10), font=(14), key='-notes-', autoscroll=True)],
            [sg.Button('Save Note', enable_events=True, button_color='orange'), sg.Exit()]
              ]

        window = sg.Window("Take notes here", layout, location=(750,150), finalize=True)
    
        window['note-here'].update('Take a note for the date of: '+ chosen_date)


        while True:
            event, values = window.read()
            if event == 'Exit' or event == sg.WIN_CLOSED:
                break
        # --------------- SAVE ENTRY -------------
            if event == 'Save Note':
                file_name = chosen_date.replace('-', '')
                file_name = file_name+'.txt'

                with open('/Users/georgiostrialonis/Documents/calendar_notes/'+file_name, 'a') as file:
                    file.write(values['-notes-'])
                    chosen_date = None
                
        window.close()

# ------------------- OPEN ENTRY -------------------
def open_entry():
    global chosen_date, file_name, contents
    existing_entries()
    print('existing entries in open: ', all_txt_files)
    # ------------ check if file exists ----------
    #file_name = chosen_date
    file_name = chosen_date.replace('-', '')
    file_name = file_name+'.txt'
    print('filename: ', file_name)
    print('chosen date: ', chosen_date)

    if chosen_date == '':
        sg.popup('Click on CALENDAR first to choose date')
        main()
    elif file_name not in all_txt_files:
        sg.popup('Entry does not exist. Make one!')
    else:
        layout = [[sg.Text('Date:', key='-showdate-')],
            [sg.Multiline(size=(50,10), font=(14), key='-seeEntry-', autoscroll=True)],
            [sg.Button('SN', enable_events=True), sg.Exit()]]
    
        window = sg.Window("This is the note", layout, location=(750,150), finalize=True)
        
        # file_name = chosen_date.replace('-', '')
        # file_name = file_name+'.txt'
    
        with open('/Users/georgiostrialonis/Documents/calendar_notes/'+file_name, 'r') as file:
            contents = file.read()

            window['-seeEntry-'].update(contents)
            window['-showdate-'].update('Date: ' + chosen_date, text_color='orange')

        while True:
            try:
                event, values = window.read()
                if event == 'Exit' or event == sg.WIN_CLOSED:
                    break
                if event == 'SN':
                    with open('/Users/georgiostrialonis/Documents/calendar_notes/'+file_name, 'w') as file:
                        file.write(values['-seeEntry-'])
                
            except:
                FileNotFoundError

            
        window.close()
# ----------------- EDIT ENTRY --------------------------
def edit_entry():
    global file_name

    layout = [
            [sg.Text('', font=(14), enable_events=True, key='edit-here')],
            [sg.Multiline(size=(50,10), font=(14), key='-edits-', autoscroll=True)],
            [sg.Button('Save Note', enable_events=True, button_color='orange'), sg.Exit()]
              ]

    window = sg.Window("EDIT NOTE", layout, location=(750,150), finalize=True)
    
    window['edit-here'].update('Date: '+ chosen_date)

    while True:
        event, values = window.read()
        if event == 'Exit' or event == sg.WIN_CLOSED:
            break
        
        with open('/Users/georgiostrialonis/Documents/calendar_notes/'+file_name, 'r') as file:
            contents = file.read()
            window['-edits-'].update(contents)

    window.close()

if __name__ == '__main__':
    main()
