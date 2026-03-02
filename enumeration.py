'''
This code enumerates items within text (depending on the desired format) such as "following: i) Peru; ii) Colombia"
It takes text separated by commas "Peru, Colombia and Ecuador" and enumerates it automatically
'''
import win32clipboard, re
import PySimpleGUI as sg
import help_file

'''
Initial parameters
'''


def make_window():

    '''
    Pop-up window to input data
    '''

    sg.theme('Topanga')  # Add some color to the window

    # Parameters
    num_list = ['(i)', 'i)']
    separator_list = [';', ',']

    # Very basic window.  Return values using keys
    layout = [
        [sg.Text('Enter your preferred format.'
                 '\nDefault: (i) Peru; (ii) Ecuador; and (iii) Argentina')],
        [sg.Checkbox('Spanish', default=False, key='-Spanish-')],
        [sg.Text('Numbering format', size=(15, 1)), sg.InputCombo((num_list), default_value=num_list[0], key='-Numbering-', size=(5, 1))],
        [sg.Text('Separator', size=(15, 1)), sg.InputCombo((separator_list), default_value=separator_list[0], key='-Separator-', size=(5,1))],
        [sg.Submit(), sg.Cancel()]
    ]

    window = sg.Window('Enumeration format', layout)
    event, values = window.read()
    if event == 'Cancel': exit()
    window.close()

    return event, values


'''
General Parameters
'''
help_file.window_title('Elements\' enumeration') # Window title

# Roman numbers
roman_1 = ['i)', 'ii)', 'iii)', 'iv)', 'v)', 'vi)', 'vii)', 'viii)', 'ix)', 'x)',
         'xi)', 'xii)', 'xiii)']
roman_2 = ['(i)', '(ii)', '(iii)', '(iv)', '(v)', '(vi)', '(vii)', '(viii)', '(ix)', '(x)',
         '(xi)', '(xii)', '(xiii)']

while True:
    # Retrieve parameters
    event, values = make_window()
    if values['-Numbering-']=='i)':
        roman = roman_1
    elif values['-Numbering-']=='(i)':
        roman = roman_2
    separator = values['-Separator-']
    if values['-Spanish-']:
        last_separator = 'y'
    else:
        last_separator = 'and'

    # Open clipboard and retrieve data
    win32clipboard.OpenClipboard()
    text = win32clipboard.GetClipboardData()

    # If the text contains commas, split the items and recompile them with the roman numbers
    if re.search(',',text):
        items = re.split(', ', text)
        new_text = f'{roman[0]} {items[0]}'
        for i in items[1:-1]:
            new_text += f'{separator} ' + roman[items.index(i)] + ' ' + i
        if items[-1].split(' ')[0]!=last_separator:
            # If the first word of the last item isn't 'and' or 'y', then:
            # last = items[-1].split(f' {last_separator} ')
            # new_text += f'{separator} ' + roman[len(items)-1] + ' ' + last[0]
            # new_text += f'{separator} {last_separator} ' + roman[len(items)] + ' ' + last[1]
            new_text += f'{separator} {last_separator} ' + roman[len(items)-1] + ' ' + items[-1]
        elif len(re.findall(f'{last_separator} ', items[-1]))>1:
            last = re.sub(f'{last_separator} ', '', items[-1], count=1)
            new_text += f'{separator} {last_separator} ' + roman[len(items) - 1] + ' ' + last
        else:
            last = items[-1].split(f'{last_separator} ')
            new_text += f'{separator} {last_separator} ' + roman[len(items)-1] + ' ' + last[1]

    # Print in the console and insert the recompiled text into the clipboard
    print(f'{new_text}\n\n')
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(new_text)
    win32clipboard.CloseClipboard()
    input('PRESS ENTER TO PERFORM AGAIN\n')
