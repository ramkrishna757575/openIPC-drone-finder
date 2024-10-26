# main.py
import argparse
import sys

from PyQt5 import QtCore, QtWidgets

from frequency_updater import (
    get_current_frequency,
    start_frequency_updater,
    set_verbose_mode,
)
from osd_widget import OSDWidget

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Drone Finder.")
    parser.add_argument(
        "--verbose", action="store_true", help="Enable verbose mode for logging"
    )  # Verbose argument added

    parser.add_argument(
        "--osd", action="store_true", help="Enable OSD mode for displaying frequency"
    ) # OSD argument added

    # Parse the arguments
    args = parser.parse_args()

    # Enable verbose mode if specified
    set_verbose_mode(args.verbose) # Set verbose mode based on argument

    # Start the frequency updater in a separate thread
    start_frequency_updater()

    if args.osd:
        # Set up the PyQt5 application
        app = QtWidgets.QApplication(sys.argv)
        osd = OSDWidget(get_current_frequency)

        # Timer to refresh the OSD widget periodically
        timer = QtCore.QTimer()
        timer.timeout.connect(osd.update_osd)
        timer.start(100)
        osd.show()
        sys.exit(app.exec_())
