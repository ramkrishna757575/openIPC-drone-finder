# main.py
import argparse

import gi

from gtk_osd_widget import GtkOSDWidget

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk

from frequency_updater import (
    get_current_frequency,
    set_verbose_mode,
    start_frequency_updater,
)

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Drone Finder.")
    parser.add_argument(
        "--verbose", action="store_true", help="Enable verbose mode for logging"
    )  # Verbose argument added

    parser.add_argument(
        "--osd", action="store_true", help="Enable OSD mode for displaying frequency"
    )  # OSD argument added

    # Parse the arguments
    args = parser.parse_args()

    # Enable verbose mode if specified
    set_verbose_mode(args.verbose)  # Set verbose mode based on argument

    # Start the frequency updater in a separate thread
    start_frequency_updater()

    if args.osd:
        # Set up the Gtk application
        win = GtkOSDWidget(get_current_frequency)
        win.connect("destroy", Gtk.main_quit)
        win.show_all()
        Gtk.main()
