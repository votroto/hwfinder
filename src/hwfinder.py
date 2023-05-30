#!/usr/bin/env python3
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import GLib
from gi.repository import Gtk, Gdk, Gio

from GioProgressBounce import ProgressBounce
from GioAsyncSubprocess import AsyncSubprocess
from back_end import handle_row_activated, handle_search, fetch_arp


def on_activate(app):
    liststore = Gtk.ListStore(str, int)

    builder = Gtk.Builder()
    builder.add_from_file("ui/hwfinder.ui")

    window = builder.get_object("root")
    listview = builder.get_object("listview")
    findbutton = builder.get_object("findbutton")
    progress = builder.get_object("progress")

    bouncer = ProgressBounce(progress)
    listview.set_model(liststore)

    listview.connect("row-activated", handle_row_activated, liststore)
    findbutton.connect("clicked", handle_search, bouncer)

    GLib.timeout_add_seconds(1, fetch_arp, liststore)
    fetch_arp(liststore)

    window.set_application(app)
    window.show_all()


if __name__ == "__main__":
    app = Gtk.Application(application_id="cz.votroto.hwfinder")
    app.connect("activate", on_activate)
    app.run(None)
