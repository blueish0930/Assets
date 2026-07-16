import io
p = 'D:/UGit/Assets/docs/index.html'
s = io.open(p, encoding='utf-8').read()

# Strategy: find position of `class="ov-body">` then the next `+(d?` and insert between them
marker = 'class="ov-body">'
pos = s.find(marker)
if pos < 0:
    print("Marker not found")
    exit(1)

# After the marker, we expect: `'+(d?`
after = pos + len(marker)
print(f"Marker at {pos}, following chars: {repr(s[after:after+15])}")

# We want to insert the version JS block right after the `>` and before `'+(d?`
# The current text is: class="ov-body">'+(d?
# We insert: +function(){...}()
# So it becomes: class="ov-body">'+function(){...}()+(d?

# Find where `'+(d?` starts
plus_pos = s.find("'+(d?", after)
if plus_pos < 0:
    print("'+(d? not found after marker")
    exit(1)

print(f"'+(d? at {plus_pos}")
print(f"Gap between marker and '+(d?: {repr(s[after:plus_pos])}")

# The gap should be empty or just `\'`
# Insert the version block
ver_js = r'''+function(){var nv=nodeData[a.n]||{};var cv=nv.createdVersion||\'\',mv=nv.lastModifiedVersion||cv;if(!cv&&!mv)return\'\';var vLabels=lang===\'zh\'?{c:\'创建版本\',m:\'最后修改\'}:{c:\'Created\',m:\'Last modified\'};return \'<div style="margin:0 0 12px;padding:8px 12px;background:linear-gradient(135deg,rgba(255,138,43,.12),rgba(255,107,53,.06));border:1px solid rgba(255,138,43,.25);border-radius:10px;font-size:11.5px;color:var(--muted);display:flex;gap:20px;align-items:center;flex-wrap:wrap"><span style="text-transform:uppercase;letter-spacing:.5px;font-size:10px;color:var(--accent);font-weight:800">\'+vLabels.c+\':</span><strong style="color:var(--ink);font-size:12px">\'+(cv||\'\')+\':</strong><span style="opacity:.3">|</span><span style="text-transform:uppercase;letter-spacing:.5px;font-size:10px;color:var(--accent);font-weight:800">\'+vLabels.m+\':</span><strong style="color:var(--ink);font-size:12px">\'+(mv||\'\')+\':</strong></div>\'}()'''

# Insert ver_js right at the `'+(d?` position, so it becomes `'+ver_js+(d?`
s2 = s[:plus_pos] + ver_js + s[plus_pos:]
io.open(p, 'w', encoding='utf-8').write(s2)
print("Injected version info")
print(f"Occurrences of 创建版本: {s2.count('创建版本')}")
print(f"Occurrences of 'Created': {s2.count('Created')}")
