# cairo_renderer.py

import cairo


class CairoRenderer:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def render(self, buzzer_frequency):
        # Set up the surface and context for rendering
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.width, self.height)
        context = cairo.Context(surface)

        # Draw semi-transparent background
        context.set_source_rgba(0, 0, 0, 0.5)
        context.rectangle(0, 0, self.width, self.height)
        context.fill()

        # Set up the font and text color
        context.set_source_rgb(1, 1, 1)  # White color
        context.select_font_face(
            "Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD
        )
        context.set_font_size(24)

        # Render the buzzer frequency
        text = f"Signal Strength (1-10) = {buzzer_frequency:.2f}"
        x_bearing, y_bearing, text_width, text_height = context.text_extents(text)[:4]
        context.move_to((self.width - text_width) / 2, (self.height + text_height) / 2)
        context.show_text(text)

        return surface
