from time import sleep
import os
import sys

import win32serviceutil as service
from infi.systray import SysTrayIcon


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


HOVER_TEXT = "Vanguard Toggler (Press to start service)"
WAIT_SECONDS = 5
ICON_ON = resource_path("resources\\on.ico")
ICON_OFF = resource_path("resources\\off.ico")
ICON_WARN = resource_path("resources\\warn.ico")


def vgc_off(tray):
    """Turn service off."""
    print("Attempting tp stop VGC service.")
    os.system('net stop vgc')
    update_tray(tray)


def vgc_on(tray):
    """Turn service on."""
    print("Attempting tp start VGC service.")
    os.system('net start vgc')
    update_tray(tray)


def update_tray(tray):
    """Update tray icon depending on service state."""
    if service.QueryServiceStatus('vgc')[1] == 4:
        tray.update(icon=ICON_ON)
    else:
        tray.update(icon=ICON_OFF)


def tray_daemon(tray):
    """Infinit tray update loop."""
    # It seems like starting and instandly updating tray doesnt work
    sleep(5)
    while True:
        # Exit condition
        if tray._notify_id is None:
            break
        update_tray(tray)
        sleep(WAIT_SECONDS)


def main():
    menu_options = (
        ('Stop VGC Service', None, vgc_off),
        ('Start VGC Service', None, vgc_on),
    )
    tray = SysTrayIcon(
        ICON_WARN,
        HOVER_TEXT,
        menu_options,
        default_menu_index=1,
    )
    tray.start()
    # Following is an infinit loop
    tray_daemon(tray)


if __name__ == "__main__":
    main()
