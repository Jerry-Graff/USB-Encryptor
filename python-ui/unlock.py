import sys, subprocess, os
import PySimpleGUI as sg

DEV = sys.argv[1]
MOUNT_LETTER = "S"
MAX_FAILS = 5

fails = 0

layout = [
    [sg.Text('Enter USB Password:')],
    [sg.Input(key='-PW-', password_char='*')],
    [sg.Button('Unlock'), sg.Button('Cancel')]
]

window = sg.Window('USB Unlock', layout)

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Cancel'):
        break

    if event == 'Unlock':
        pw = values['-PW']
        ret = subprocess.run([
            "veracrypt", "/v", DEV, "/l", MOUNT_LETTER, "/p", pw, "/q"
        ])
        if ret.returncode == 0:
            sg.popup('Unlocked!', f'Drive mounted at {MOUNT_LETTER}')
            break
        else:
            fails += 1
            if fails >= MAX_FAILS:
                with open(DEV, 'r+b') as f:
                    f.write(b'\x00' * 1024 * 1024)
                sg.popup_error('Too many tries—drive wiped!')
                os._exit(1)
            else:
                sg.popup_warning(f'Incorrect passphrase ({fails}/{MAX_FAILS})')

window.close()