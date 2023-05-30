import gi

from gi.repository import GLib

class ProgressBounce:
    def __init__(self, progress):
        super().__init__()

        self._pulsing = False
        self._progress = progress

    def stop_pulsing(self):
        self._pulsing = False
    
    def pulse(self):
        if not self._pulsing:
            self._progress.set_fraction(0)
        else:
            self._progress.pulse()

        return self._pulsing

    def start_pulsing(self):
        self._pulsing = True
        GLib.timeout_add(60, self.pulse)

