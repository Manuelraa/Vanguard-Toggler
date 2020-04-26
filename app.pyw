from time import sleep
import os
import sys

import win32serviceutil as service
from infi.systray import SysTrayIcon


HOVER_TEXT = "Vanguard Toggler"
WAIT_SECONDS = 5


def vgc_off(tray):
    """Turn service off."""
    print("Attempting tp stop VGC service.")
    os.system('net stop vgc')
    tray.update(icon='resources/off.ico')
    update_tray(tray)


def vgc_on(tray):
    """Turn service on."""
    print("Attempting tp start VGC service.")
    os.system('net start vgc')
    update_tray(tray)


def update_tray(tray):
    """Update tray icon depending on service state."""
    if service.QueryServiceStatus('vgc')[1] == 4:
        tray.update(icon='resources/on.ico')
    else:
        tray.update(icon='resources/off.ico')


def tray_daemon(tray):
    """Infinit tray update loop."""
    while True:
        update_tray(tray)
        sleep(WAIT_SECONDS)


def main():

    def on_exit(tray):
        sys.exit()

    menu_options = (
        ('Stop VGC Service', None, vgc_off),
        ('Start VGC Service', None, vgc_on),
    )
    tray = SysTrayIcon(
        "resources/warn.ico",
        HOVER_TEXT,
        menu_options,
        on_quit=on_exit,
        default_menu_index=1
    )
    tray.start()
    # Following is an infinit loop
    tray_daemon(tray)


if __name__ == "__main__":
    main()
