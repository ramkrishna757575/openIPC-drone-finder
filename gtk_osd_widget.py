import cairo
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import GLib, Gtk


class GtkOSDWidget(Gtk.Window):

    def __init__(self, frequency_provider):
        super().__init__(title="Drone Finder OSD")
        self.frequency_provider = frequency_provider
        self.set_default_size(500, 100)

        # Set window transparency and always-on-top attributes
        self.set_app_paintable(True)
        self.set_decorated(False)
        self.set_keep_above(True)
        self.set_visual(self.get_screen().get_rgba_visual())

        self.text = ""

        # Connect the draw signal
        self.connect("draw", self.on_draw)

        # Periodically update the text
        GLib.timeout_add(1000, self.update_label)  # Update every second

    def update_label(self):
        buzzer_frequency = self.frequency_provider()
        # Update the text
        self.text = f"Signal Strength (1-10) = {buzzer_frequency:.2f}"
        # Trigger a redraw
        self.queue_draw()
        return True  # Keep the timeout active

    def on_draw(self, widget, cr):
        # Set the background color (optional)
        cr.set_source_rgba(0, 0, 0, 0.5)  # Semi-transparent black
        cr.paint()

        # Set the text color
        cr.set_source_rgba(1, 1, 1, 1)  # White color

        # Select font face and size
        cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        cr.set_font_size(20)

        # Move to the position where the text should be drawn
        cr.move_to(10, 30)

        # Show the text
        cr.show_text(self.text)

        return False  # Do not propagate the signal
