from windows_toasts import InteractableWindowsToaster, Toast, ToastActivatedEventArgs, ToastButton
import threading
from infi.systray import SysTrayIcon
import pathlib

from register_hkey_aumid import register_hkey

stop_lock = threading.Lock()
stop_value = False

systray_lock = threading.Lock()
systray_obj = None

# Parses input string of format 'HH:MM:SS' and returns seconds
def parse_input_to_seconds(timeDuration:str) -> int:
    h, m, s = timeDuration.split(":")
    return int(h) * 3600 + int(m) * 60 + int(s)

def start_thread(timer:str):
    # Parse the input and convert to seconds
    seconds=parse_input_to_seconds(timer)

    # Initialise the daemon thread to point to the alarm function
    thread = threading.Timer(seconds, alarm, kwargs={"timer":timer})
    thread.daemon = True
    thread.start()

def toast_response_handler(activatedEventArgs: ToastActivatedEventArgs):
    if(activatedEventArgs.arguments=='stop'):
        # Close the tray icon first to avoid race
        with systray_lock:
            systray_obj.shutdown()
        on_quit_callback(None) #invoke the quit callback manually
        

def alarm(timer:str):
    # Halt the thread chaining if the system tray is closed
    with stop_lock:
        if stop_value:
            return
    
    # Schedule the next thread
    start_thread(timer)

    # Prepare the toaster for bread (or your notification)
    # TODO: Try to get this AUMID automatically
    toaster = InteractableWindowsToaster('Reminder', "Aquaman") #BUG: Application Text is not overriding the default AUMID
    # Initialise the toast
    newToast = Toast()  
    # Set the body of the notification
    newToast.text_fields = ['Drink Water 💧']
    # Add buttons to close or acknowledge drinking water
    newToast.AddAction(ToastButton('Done', 'done'))
    newToast.AddAction(ToastButton('Stop Reminders', 'stop'))
    # Set response handler for the toast
    newToast.on_activated = toast_response_handler

    # Schedule a new toast based on the time
    # newTime = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
    toaster.show_toast(newToast)

# This is invoked when the system tray is closed
def on_quit_callback(systray):
    global stop_value

    # flag to stop the chaining of threads
    with stop_lock:
        stop_value = True

def aquaman(timer:str):
    # Register the app on windows registery, the function does nothing if it's already registered
    register_hkey("Aquaman", "Aquaman", None)

    # Initialise a system tray to cancel the current process
    global systray_obj
    with systray_lock:
        systray_obj = SysTrayIcon("water-drop.ico", "Aquaman", (), on_quit=on_quit_callback)
        systray_obj.start()

    # Start chaining of threads
    start_thread(timer)

if __name__ == "__main__":
    input_string = input("Enter the desired time in format 'HH:MM:SS':")
    aquaman(input_string)