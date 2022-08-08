from Quartz import CGWindowListCopyWindowInfo, kCGNullWindowID, kCGWindowListOptionAll
import os

class Screenshotter:

    def __init__(self, window_name):
        self.window_name = window_name
        self._window_id = Screenshotter._find_window_id(window_name)

    @staticmethod
    def _find_window_id(window_name):
        print(f'Searching window id of {window_name}')

        windowList = CGWindowListCopyWindowInfo(kCGWindowListOptionAll, kCGNullWindowID)

        for window in windowList:
            # print(window.get('kCGWindowName', ''))
            if(window_name.lower() in window.get('kCGWindowName', '').lower()):
                window_id = window['kCGWindowNumber']
                print('Found window id %s' % window_id)
                return window_id

        print('Unable to find window id')
        return None

    def capture(self, file_name):       
        # -x mutes sound
        # -o do not capture shadow of window
        # -l specifies windowId
        status = os.system(f'screencapture -x -o -l{self._window_id} {file_name}')
        return status == 0
