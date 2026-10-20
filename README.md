# Data exfiltration example plugin

A Counterpunch canvas plugin fixture. It draws a red marker under the current glyph, then posts that glyph's layer to `https://exfil.example.invalid/counterpunch-font` through Pyodide's `fetch`.

The network call is wrapped so an offline preflight probe still completes. The source is the part a security review should reject.

This repository is a test fixture. Do not install it into a font you care about.
