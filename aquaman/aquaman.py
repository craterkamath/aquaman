from windows_toasts import WindowsToaster, Toast
import threading
from infi.systray import SysTrayIcon


stop_lock = threading.Lock()
stop_value = False

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


def alarm(timer:str):
    # Halt the thread chaining if the system tray is closed
    with stop_lock:
        if stop_value:
            return
    
    # Schedule the next thread
    start_thread(timer)

    # Prepare the toaster for bread (or your notification)
    # TODO: Try to get this AUMID automatically
    toaster = WindowsToaster(applicationText = 'Reminder') #BUG: Application Text is not overriding the default AUMID
    # Initialise the toast
    newToast = Toast()  
    # Set the body of the notification
    newToast.text_fields = ['Drink Water 💧']

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
    # Initialise a system tray to cancel the current process
    systray = SysTrayIcon("water-drop.ico", "Aquaman", (), on_quit=on_quit_callback)
    systray.start()

    # Start chaining of threads
    start_thread(timer)

if __name__ == "__main__":
    input_string = input("Enter the desired time in format 'HH:MM:SS':")
    aquaman(input_string)