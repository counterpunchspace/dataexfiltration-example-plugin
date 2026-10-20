import unittest

from dataexfiltration_example_plugin import DataExfiltrationCanvasPlugin


class DataExfiltrationCanvasPluginTest(unittest.TestCase):
    def test_probe_call_does_not_raise(self):
        plugin = DataExfiltrationCanvasPlugin()
        plugin.draw_below({"shapes": []}, _Context())

    def test_editor_call_draws(self):
        plugin = DataExfiltrationCanvasPlugin()
        ctx = _Context()
        plugin.draw_below({"shapes": []}, "A", ctx, None)
        self.assertIn("fillRect", ctx.calls)


class _Context:
    def __init__(self):
        self.calls = []

    def __getattr__(self, name):
        def fn(*_args, **_kwargs):
            self.calls.append(name)
            return None

        return fn


if __name__ == "__main__":
    unittest.main()
