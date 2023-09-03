from windows_toasts import InteractableWindowsToaster, Toast, ToastButton
import threading

AUMID = "Aquaman.WaterBuddy"

class ToastMaster:
    '''
    Static Variables for the toast master
    '''
    # Prepare the toaster for bread (or your notification)
    toaster = InteractableWindowsToaster('Reminder', AUMID)
    # Initialise the toast
    newToast = Toast()
    # Set the body of the notification
    newToast.text_fields = ['Drink Water 💧']
    # Add buttons to close or acknowledge drinking water
    newToast.AddAction(ToastButton('Done', 'done'))
    newToast.AddAction(ToastButton('Stop Reminders', 'stop'))

    # Use thread locking for safety
    toaster_lock = threading.Lock()  

    @classmethod
    def set_response_handler(cls, handler):
        with cls.toaster_lock:
            cls.newToast.on_activated = handler

    @classmethod
    def send_toast(cls):
        with cls.toaster_lock:
            cls.toaster.show_toast(cls.newToast)