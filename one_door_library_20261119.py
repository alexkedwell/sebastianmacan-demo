"""Nov 19 2026 (Alex): one door. Re-download now IS the Library.
- downloads.html becomes a forward to the library (old page kept in _removed/), so every old link, bookmark
  and the delivery server's 'get fresh links' messages land in the library.
- Footers: the duplicate 'Re-download' link next to 'Library' goes; on the legal pages it becomes 'Library'."""
import io, glob, os, shutil
def rd(p): return io.open(p, encoding="utf-8").read()
def wr(p, s): io.open(p, "w", encoding="utf-8", newline="").write(s)
LIB = "https://dl.sebastianmacan.com/library"

if not os.path.exists("_removed/downloads_page_2026-11-19.html"):
    shutil.copy("downloads.html", "_removed/downloads_page_2026-11-19.html")

dup = ' · <a href="downloads.html">Re-download</a>'
legal = '<a href="/downloads.html">Re-download</a>'
a = b = 0
for p in sorted(glob.glob("*.html") + glob.glob("_tpl/*.html") + glob.glob("gen_*.py")):
    if p == "downloads.html": continue
    s = rd(p); o = s
    if dup in s:
        assert f'<a href="{LIB}">Library</a>{dup}' in s, p
        s = s.replace(dup, ""); a += 1
    if legal in s:
        s = s.replace(legal, f'<a href="{LIB}">Library</a>'); b += 1
    if s != o: wr(p, s)
print("duplicate footer link removed on", a, "files; renamed to Library on", b, "files")

wr("downloads.html", f"""<!doctype html>
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
<p>Your downloads live in your library now. <a href="{LIB}">Open my library</a></p>
</body>
</html>
""")
left = [p for p in glob.glob("*.html") + glob.glob("_tpl/*.html") + glob.glob("gen_*.py") if "Re-download" in rd(p)]
print("files still saying Re-download:", left or "none")
