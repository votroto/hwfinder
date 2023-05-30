import gi

from gi.repository import GLib
from gi.repository import Gio

class AsyncSubprocess:
    def __init__(self, cmd, data_handler, finish_handler):
        flags = Gio.SubprocessFlags.STDOUT_PIPE
        
        self.cancellable = Gio.Cancellable()
        self.data_handler = data_handler
        self.finish_handler = finish_handler
        self.process = Gio.Subprocess.new(cmd, flags)
        stream = self.process.get_stdout_pipe()
        self.data_stream = Gio.DataInputStream.new(stream)

    def run(self):
        self.process.wait_check_async(
            cancellable=self.cancellable, callback=self.finish_handler
        )
        self._queue_read()

    def _queue_read(self):
        priority = GLib.PRIORITY_DEFAULT
        self.data_stream.read_line_async(
            io_priority=priority,
            cancellable=self.cancellable,
            callback=self._on_data,
        )

    def _on_data(self, source, result):
        line, length = source.read_line_finish_utf8(result)
        if line:
            self.data_handler(line)
            GLib.idle_add(self._queue_read)
        else:
            self.cancellable.cancel()


