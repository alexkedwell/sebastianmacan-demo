"""Nov 20 2026 (Alex): sebastianmacan.com/library forwards to the library; after-download panel loses the trailing 'No password.'"""
import io, glob, os
def rd(p): return io.open(p, encoding="utf-8").read()
def wr(p, s): io.open(p, "w", encoding="utf-8", newline="").write(s)
LIB = "https://dl.sebastianmacan.com/library"
os.makedirs("library", exist_ok=True)
wr("library/index.html", f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Your library · Sebastian Macan</title>
<meta name="robots" content="noindex">
<link rel="canonical" href="{LIB}">
<meta http-equiv="refresh" content="0; url={LIB}">
<script>location.replace("{LIB}");</script>
<style>body{{margin:0;background:#0b0b0d;color:#f2f2f5;font-family:Inter,-apple-system,BlinkMacSystemFont,'Segoe UI',system-ui,sans-serif;display:flex;min-height:100vh;align-items:center;justify-content:center;text-align:center;padding:24px}}a{{color:#f2f2f5;font-weight:800}}</style>
</head>
<body>
<p><a href="{LIB}">Open my library</a></p>
</body>
</html>
""")
s = rd("js/email-gate.js")
a = "To open it, enter your email and we send you a sign-in code. No password.</p>"
assert s.count(a) == 1
wr("js/email-gate.js", s.replace(a, "To open it, enter your email and we send you a sign-in code.</p>"))
n = 0
for p in glob.glob("*.html") + glob.glob("_tpl/*") + glob.glob("gen_*.py"):
    s = rd(p)
    if "js/email-gate.js?v=lib4" in s: wr(p, s.replace("js/email-gate.js?v=lib4", "js/email-gate.js?v=lib5")); n += 1
print("ok, version bumped on", n, "files")
