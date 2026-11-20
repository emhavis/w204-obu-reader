"""Generate docs/wiring.html (breadboard wiring diagrams). Run: python3 tools/gen_wiring.py"""
import html, pathlib
OUT = pathlib.Path(__file__).resolve().parent.parent / "docs" / "wiring.html"

E = html.escape
def T(x, y, s, cls="lbl", anchor="start", rot=None, extra=""):
    tr = f' transform="rotate({rot} {x} {y})"' if rot is not None else ""
    return f'<text x="{x}" y="{y}" class="{cls}" text-anchor="{anchor}"{tr}{extra}>{E(s)}</text>'

def wire(pts, cls, w=2.6):
    d = " ".join(f"{x},{y}" for x, y in pts)
    s = f'<polyline points="{d}" class="halo" fill="none" stroke-width="{w+3.4}"/>'
    s += f'<polyline points="{d}" class="w {cls}" fill="none" stroke-width="{w}"/>'
    for x, y in (pts[0], pts[-1]):
        s += f'<circle cx="{x}" cy="{y}" r="2.6" class="dot {cls}"/>'
    return s

# ---------- components ----------
ESP_L = ["3V3","EN","VP","VN","34","35","32","33","25","26","27","14","12","GND","13","D2","D3","CMD","5V"]
ESP_R = ["GND","23","22","TX","RX","21","GND","19","18","5","17","16","4","0","2","15","D1","D0","CLK"]
def py(i): return 134 + 24*i
def esp(x, title, used, sub):
    s = f'<rect x="{x}" y="110" width="120" height="480" rx="6" class="pcb-esp"/>'
    s += f'<rect x="{x+28}" y="118" width="64" height="74" rx="3" class="shield"/>'
    s += T(x+60, 160, "ESP32", "pcbtxt b", "middle")
    s += f'<rect x="{x+40}" y="588" width="40" height="22" rx="3" class="usb"/>'
    s += T(x+60, 400, title, "pcbtxt big", "middle", rot=-90)
    s += T(x+60, 400+0, "", "pcbtxt")
    s += T(x+78, 400, sub, "pcbtxt small", "middle", rot=-90)
    for i, n in enumerate(ESP_L):
        on = ("L", n) in used
        s += f'<rect x="{x-6}" y="{py(i)-4}" width="11" height="8" rx="1.5" class="{"pin on" if on else "pin"}"/>'
        s += T(x+10, py(i)+4, n, "pcbtxt" + (" b" if on else " dim"))
    for i, n in enumerate(ESP_R):
        on = ("R", n) in used
        s += f'<rect x="{x+115}" y="{py(i)-4}" width="11" height="8" rx="1.5" class="{"pin on" if on else "pin"}"/>'
        s += T(x+110, py(i)+4, n, "pcbtxt" + (" b" if on else " dim"), "end")
    return s
def eL(x, n): return (x-5, py(ESP_L.index(n)))
def eR(x, n): return (x+125, py(ESP_R.index(n)))

TFT_P = ["VCC","GND","CS","RESET","DC","SDI(MOSI)","SCK","LED","SDO(MISO)","T_CLK","T_CS","T_DIN","T_DO","T_IRQ"]
def tpy(k): return 124 + 15*k
def tft():
    s = '<rect x="575" y="108" width="178" height="226" rx="6" class="pcb-tft"/>'
    s += '<rect x="660" y="118" width="84" height="206" rx="2" class="screen"/>'
    s += T(702, 221, '2.8" ILI9341 TFT + touch', "pcbtxt b", "middle", rot=-90)
    for k, n in enumerate(TFT_P):
        s += f'<rect x="569" y="{tpy(k)-3.5}" width="11" height="7" rx="1.5" class="{"pin" if n=="T_IRQ" else "pin on"}"/>'
        s += T(585, tpy(k)+3.5, n, "pcbtxt sm" + (" dim" if n=="T_IRQ" else ""))
    s += T(650, 330, "", "pcbtxt")
    return s
def tP(n): return (570, tpy(TFT_P.index(n)))

SD_P = ["GND","VCC","MISO","MOSI","SCK","CS"]
def spy(k): return 360 + 24*k
def sd():
    s = '<rect x="90" y="340" width="140" height="162" rx="6" class="pcb-blue"/>'
    s += '<rect x="102" y="372" width="52" height="70" rx="3" class="slot"/>'
    s += T(128, 462, "microSD", "pcbtxt b", "middle")
    s += T(128, 478, "module", "pcbtxt small", "middle")
    for k, n in enumerate(SD_P):
        s += f'<rect x="225" y="{spy(k)-4}" width="11" height="8" rx="1.5" class="pin on"/>'
        s += T(219, spy(k)+4, n, "pcbtxt sm", "end")
    return s
def sP(n): return (236, spy(SD_P.index(n)))

CAN_P = ["3V3","GND","CTX","CRX","CANH","CANL"]
def can(x0, keep):
    xs = [x0 + 15 + 24*k for k in range(6)]
    s = f'<rect x="{x0}" y="410" width="150" height="130" rx="6" class="pcb-blue"/>'
    s += T(x0+75, 432, "SN65HVD230", "pcbtxt b", "middle")
    s += T(x0+75, 447, "CAN transceiver", "pcbtxt small", "middle")
    if keep:
        s += f'<rect x="{x0+22}" y="456" width="106" height="18" rx="9" class="badge ok"/>'
        s += T(x0+75, 469, "120 Ω on board: keep", "badgetxt", "middle")
    else:
        s += f'<rect x="{x0+14}" y="456" width="122" height="18" rx="9" class="badge bad"/>'
        s += T(x0+75, 469, "120 Ω on board: REMOVE", "badgetxt", "middle")
    for x, n in zip(xs, CAN_P):
        s += f'<rect x="{x-4}" y="535" width="8" height="11" rx="1.5" class="pin on"/>'
        s += T(x+4, 529, n, "pcbtxt sm", "start", rot=-90)
    return s, dict(zip(CAN_P, [(x, 546) for x in xs]))

def board(x, w, title, link_x):
    s = f'<rect x="{x}" y="40" width="{w}" height="660" rx="10" class="bb"/>'
    s += f'<rect x="{x+36}" y="96" width="{w-50}" height="548" fill="url(#holes)"/>'
    for y, c, lab in [(62,"rail-p","3V3"),(80,"rail-n","GND"),(660,"rail-p","3V3"),(678,"rail-n","GND")]:
        s += f'<line x1="{x+36}" y1="{y}" x2="{x+w-10}" y2="{y}" class="{c}"/>'
        s += T(x+8, y+4, lab, "rail-lbl")
    s += T(x, 28, title, "board-title")
    # rail links top<->bottom
    s += wire([(link_x, 62), (link_x, 660)], "c-3v3", 2)
    s += wire([(link_x+10, 80), (link_x+10, 678)], "c-gnd", 2)
    return s

def defs():
    return ('<defs><pattern id="holes" width="12" height="12" patternUnits="userSpaceOnUse">'
            '<rect x="4.5" y="4.5" width="3" height="3" rx="0.6" class="hole"/></pattern></defs>')

def reader_board(fig2):
    s = board(20, 740, "Breadboard A · READER", 64)
    x = 330
    used = {("L","3V3"),("R","GND"),("R","5"),("R","4")}
    per = {("L","26"),("L","27"),("L","14"),("L","13"),("L","5V"),("R","23"),("R","22"),("R","21"),("R","19"),("R","18"),("R","2"),("R","15")}
    used |= per
    if fig2: used.add(("L","35"))
    s += esp(x, "READER", used, "DevKitC V4 · WROOM-32")
    # peripherals (faded in fig2)
    p = '<g class="faded">' if fig2 else '<g>'
    p += tft() + sd()
    # TFT signals
    tw = [("RESET","22",470),("SDI(MOSI)","23",478),("T_DIN","23",486),("T_CS","21",494),
          ("SDO(MISO)","19",502),("T_DO","19",510),("SCK","18",518),("T_CLK","18",526),("DC","2",534),("CS","15",542)]
    for tp, ep, lane in tw:
        a = eR(x, ep); b = tP(tp)
        p += wire([a, (lane, a[1]), (lane, b[1]), b], "c-tft")
    p += wire([tP("VCC"), (558, tpy(0)), (558, 62)], "c-3v3")
    p += wire([tP("GND"), (552, tpy(1)), (552, 80)], "c-gnd")
    p += wire([tP("LED"), (564, tpy(7)), (564, 62)], "c-3v3")
    # SD
    for sp, ep, lane in [("MISO","26",300),("CS","27",292),("SCK","14",284),("MOSI","13",276)]:
        a = eL(x, ep); b = sP(sp)
        p += wire([a, (lane, a[1]), (lane, b[1]), b], "c-sd")
    a = eL(x, "5V"); b = sP("VCC")
    p += wire([a, (268, a[1]), (268, b[1]), b], "c-5v")
    p += wire([sP("GND"), (250, sP("GND")[1]), (250, 80)], "c-gnd")
    p += '</g>'
    s += p
    if fig2:
        s += f'<rect x="586" y="342" width="164" height="22" rx="4" class="note-bg"/>'
        s += T(668, 357, "TFT + SD: same as Figure 1", "note", "middle")
    # ESP power
    s += wire([eL(x,"3V3"), (312, 134), (312, 62)], "c-3v3")
    s += wire([eR(x,"GND"), (462, 134), (462, 80)], "c-gnd")
    # transceiver
    cs, cp = can(575, keep=not fig2)
    s += cs
    a = eR(x,"5"); s += wire([a, (548, a[1]), (548, 600), (cp["CTX"][0], 600), cp["CTX"]], "c-ctx")
    a = eR(x,"4"); s += wire([a, (556, a[1]), (556, 612), (cp["CRX"][0], 612), cp["CRX"]], "c-crx")
    s += wire([cp["3V3"], (cp["3V3"][0], 660)], "c-3v3")
    s += wire([cp["GND"], (cp["GND"][0], 678)], "c-gnd")
    return s, cp

def resistor_v(x, y1, y2, label, lx_anchor="end"):
    m = (y1+y2)/2
    s = wire([(x,y1),(x,m-26)], "c-sense") + wire([(x,m+26),(x,y2)], "c-sense")
    s += f'<rect x="{x-7}" y="{m-26}" width="14" height="52" rx="3" class="res"/>'
    s += T(x-12, m+4, label, "lbl", lx_anchor)
    return s

def fig1():
    W, H = 1220, 800
    s = f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Bench setup: reader ESP32 with TFT, SD module and CAN transceiver on breadboard A; simulator ESP32 with CAN transceiver on breadboard B; the two transceivers joined CAN-H to CAN-H and CAN-L to CAN-L, grounds linked, both boards powered from PC USB.">'
    s += defs()
    rb, cp = reader_board(False)
    s += rb
    s += board(800, 400, "Breadboard B · SIMULATOR", 844)
    x2 = 880
    s += esp(x2, "SIMULATOR", {("L","3V3"),("R","GND"),("R","5"),("R","4")}, "DevKitC V4 · WROOM-32")
    cs, cp2 = can(1040, keep=True)
    s += cs
    s += wire([eL(x2,"3V3"), (862,134), (862,62)], "c-3v3")
    s += wire([eR(x2,"GND"), (1012,134), (1012,80)], "c-gnd")
    a = eR(x2,"5"); s += wire([a, (1020,a[1]), (1020,600), (cp2["CTX"][0],600), cp2["CTX"]], "c-ctx")
    a = eR(x2,"4"); s += wire([a, (1028,a[1]), (1028,612), (cp2["CRX"][0],612), cp2["CRX"]], "c-crx")
    s += wire([cp2["3V3"], (cp2["3V3"][0],660)], "c-3v3")
    s += wire([cp2["GND"], (cp2["GND"][0],678)], "c-gnd")
    # common GND
    s += wire([(740,80),(740,50),(856,50),(856,80)], "c-gnd")
    s += T(798, 44, "GND link", "lbl b", "middle")
    # CAN pair
    s += wire([cp["CANH"], (cp["CANH"][0],735), (cp2["CANH"][0],735), cp2["CANH"]], "c-canh", 3)
    s += wire([cp["CANL"], (cp["CANL"][0],750), (cp2["CANL"][0],750), cp2["CANL"]], "c-canl", 3)
    s += T(930, 772, "CAN-H ↔ CAN-H, CAN-L ↔ CAN-L · twisted pair, 20–50 cm", "lbl b", "middle")
    s += T(390, 632, "USB → PC", "lbl b", "middle")
    s += T(940, 632, "USB → PC", "lbl b", "middle")
    s += '</svg>'
    return s

def fig2():
    W, H = 1220, 800
    s = f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="In-car reader: OBD-II pin 16 feeds a 1 A fuse, a TVS diode to ground, a 1N5822 diode and a 470 µF capacitor into the LM2596, whose 5 V USB output powers the ESP32. OBD pins 4 and 5 are ground. OBD pins 6 and 14 go to the transceiver CAN-H and CAN-L, with its 120 ohm resistor removed. A 100k/22k divider from the protected 12 V feeds GPIO35.">'
    s += defs()
    rb, cp = reader_board(True)
    s += rb
    # divider on board A
    s += resistor_v(220, 120, 254, "100 kΩ")
    s += wire([(220,254),(190,254)], "c-sense")
    s += f'<rect x="140" y="247" width="50" height="14" rx="3" class="res"/>'
    s += wire([(140,254),(110,254),(110,80)], "c-gnd")
    s += T(165, 241, "22 kΩ", "lbl", "middle")
    s += wire([(220,254),(220,300),(169,300)], "c-sense")
    s += '<line x1="169" y1="289" x2="169" y2="311" class="plate"/><line x1="162" y1="289" x2="162" y2="311" class="plate"/>'
    s += wire([(162,300),(110,300),(110,254)], "c-gnd")
    s += T(165, 327, "100 nF", "lbl", "middle")
    s += wire([(220,254), eL(330,"35")], "c-sense")
    s += T(272, 248, "SENSE", "lbl b", "middle")
    # power section
    s += '<rect x="800" y="140" width="400" height="280" rx="10" class="bb"/>'
    s += T(812, 162, "Power section", "board-title")
    # 12V from plug pin16
    s += wire([(1076,480),(830,480),(830,200),(870,200)], "c-12v", 3)
    s += '<rect x="870" y="191" width="50" height="18" rx="9" class="fuse"/>'
    s += '<line x1="874" y1="200" x2="916" y2="200" class="fusewire"/>'
    s += T(895, 182, "1 A fuse", "lbl b", "middle")
    s += wire([(920,200),(962,200)], "c-12v", 3)
    # TVS
    s += wire([(940,200),(940,268)], "c-12v") + wire([(940,298),(940,380)], "c-gnd")
    s += '<polygon points="930,298 950,298 940,280" class="dsym"/><polyline points="926,276 930,280 950,280 954,284" class="dbar" fill="none"/>'
    s += T(956, 300, "TVS", "lbl b") + T(956, 314, "P6KE24A", "lbl")
    # Schottky
    s += '<polygon points="962,190 962,210 984,200" class="dsym"/><line x1="985" y1="189" x2="985" y2="211" class="dbar"/>'
    s += T(974, 182, "1N5822", "lbl b", "middle")
    s += wire([(985,200),(1070,200)], "c-12v", 3)
    s += T(1006, 222, "VBAT", "lbl", "middle")
    # cap
    s += wire([(1030,200),(1030,282)], "c-12v") + wire([(1030,292),(1030,380)], "c-gnd")
    s += '<line x1="1018" y1="282" x2="1042" y2="282" class="plate"/><line x1="1018" y1="292" x2="1042" y2="292" class="plate"/>'
    s += T(1014, 276, "+", "lbl b", "end")
    s += T(1036, 352, "470 µF", "lbl", "start") + T(1036, 366, "35 V", "lbl", "start")
    # LM2596
    s += '<rect x="1070" y="168" width="120" height="162" rx="6" class="pcb-blue"/>'
    s += T(1130, 236, "LM2596", "pcbtxt b", "middle") + T(1130, 252, "5 V fixed", "pcbtxt small", "middle")
    s += T(1078, 204, "IN+", "pcbtxt sm") + T(1078, 304, "IN−", "pcbtxt sm")
    s += '<rect x="1110" y="330" width="40" height="16" rx="2" class="usb"/>'
    s += T(1160, 343, "USB out", "lbl", "start")
    # GND bus
    s += wire([(1070,300),(1060,300),(1060,380)], "c-gnd")
    s += wire([(850,380),(1060,380)], "c-gnd", 3)
    s += T(900, 398, "GND bus", "lbl", "middle")
    # OBD plug
    s += '<path d="M1080 466 L1190 470 L1190 556 L1080 560 Z" class="plug"/>'
    s += T(1135, 458, "OBD-II plug → car", "lbl b", "middle")
    pins = [(480,"16","+12 V","c-12v"),(496,"4","chassis GND","c-gnd"),(512,"5","signal GND","c-gnd"),(528,"6","CAN-H","c-canh"),(544,"14","CAN-L","c-canl")]
    for y, n, lab, c in pins:
        s += f'<rect x="1074" y="{y-3}" width="10" height="6" rx="1" class="pin on"/>'
        s += T(1092, y+4, f"{n} · {lab}", "plugtxt")
    s += wire([(1076,496),(850,496),(850,380)], "c-gnd")
    s += wire([(1076,512),(866,512),(866,380)], "c-gnd")
    s += wire([(1076,528),(1046,528),(1046,735),(cp["CANH"][0],735),cp["CANH"]], "c-canh", 3)
    s += wire([(1076,544),(1062,544),(1062,750),(cp["CANL"][0],750),cp["CANL"]], "c-canl", 3)
    s += T(880, 772, "OBD pin 6 → CAN-H, pin 14 → CAN-L (twist the pair)", "lbl b", "middle")
    # GND to board A
    s += wire([(850,380),(790,380),(790,80),(750,80)], "c-gnd")
    # USB cable
    s += wire([(1130,346),(1130,440),(780,440),(780,715),(390,715),(390,612)], "c-usb", 5)
    s += T(560, 708, "USB cable · 5 V to ESP32", "lbl b", "middle")
    # VBAT sense run
    s += wire([(1006,200),(1006,24),(220,24),(220,120)], "c-sense")
    s += T(600, 18, "VBAT (after fuse + diode) → divider", "lbl b", "middle")
    s += '</svg>'
    return s

CSS = r"""
:root{
  --bg:#eef1f0; --surface:#ffffff; --fg:#1b2226; --muted:#5a666d; --line:#d3d9d8; --accent:#0f6b5c;
  --bb:#fbfcfc; --bb-edge:#c4cccb; --hole:#c7cfce;
  --pcb-esp:#202528; --pcb-blue:#1d4f8f; --pcb-tft:#8f2a2a; --pcb-fg:#eef3f1; --pin:#9aa3a8; --pin-on:#e0b84a;
  --w3:#d92b2b; --w5:#e8700f; --w12:#8b3fd6; --wg:#2b3135; --wtft:#2563eb; --wsd:#0d9488;
  --wctx:#c99400; --wcrx:#1f9d48; --wch:#db2777; --wcl:#4f46e5; --wsense:#0891b2; --wusb:#7b858b;
  --ok:#1f9d48; --bad:#d92b2b;
  --f-head:"IBM Plex Sans Condensed","Arial Narrow",system-ui,sans-serif;
  --f-body:"IBM Plex Sans",system-ui,-apple-system,"Segoe UI",sans-serif;
  --f-mono:"IBM Plex Mono",ui-monospace,Menlo,Consolas,monospace;
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){
  --bg:#121618; --surface:#1a2023; --fg:#e2e8ea; --muted:#9aa6ac; --line:#2c3438; --accent:#4fc4ac;
  --bb:#1f2629; --bb-edge:#3a4448; --hole:#38434a; --pin:#5f696e;
  --w3:#ff5a5a; --w5:#ff9640; --w12:#b783ff; --wg:#c9d1d4; --wtft:#5b93ff; --wsd:#2dd4bf;
  --wctx:#f2c230; --wcrx:#3ccf6e; --wch:#ff5fa2; --wcl:#8b85ff; --wsense:#22c3e6; --wusb:#8e989d; color-scheme:dark}}
:root[data-theme="dark"]{
  --bg:#121618; --surface:#1a2023; --fg:#e2e8ea; --muted:#9aa6ac; --line:#2c3438; --accent:#4fc4ac;
  --bb:#1f2629; --bb-edge:#3a4448; --hole:#38434a; --pin:#5f696e;
  --w3:#ff5a5a; --w5:#ff9640; --w12:#b783ff; --wg:#c9d1d4; --wtft:#5b93ff; --wsd:#2dd4bf;
  --wctx:#f2c230; --wcrx:#3ccf6e; --wch:#ff5fa2; --wcl:#8b85ff; --wsense:#22c3e6; --wusb:#8e989d; color-scheme:dark}
body{background:var(--bg);color:var(--fg);font:15px/1.55 var(--f-body);}
.wrap{max-width:1180px;margin:0 auto;padding-block:28px 56px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));display:grid;gap:28px}
header h1{font:600 2rem/1.15 var(--f-head);margin:0;letter-spacing:.01em;text-wrap:balance}
header p{margin:.4rem 0 0;color:var(--muted);max-width:68ch}
.eyebrow{font:500 .75rem var(--f-mono);letter-spacing:.12em;text-transform:uppercase;color:var(--accent)}
h2{font:600 1.35rem/1.2 var(--f-head);margin:0 0 .3rem;text-wrap:balance}
section{display:grid;gap:12px;min-width:0}
figure{margin:0;background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:14px;display:grid;gap:10px;min-width:0}
.scroll{overflow-x:auto}
.scroll svg{display:block;width:100%;min-width:980px;height:auto}
figcaption{color:var(--muted);font-size:.92rem;max-width:90ch}
.legend{display:flex;flex-wrap:wrap;gap:8px 18px;font:12.5px var(--f-mono);color:var(--fg)}
.legend span{display:inline-flex;align-items:center;gap:7px}
.legend i{display:inline-block;width:22px;height:4px;border-radius:2px}
table{border-collapse:collapse;width:100%;font-size:.92rem;font-variant-numeric:tabular-nums}
th,td{text-align:left;padding:7px 10px;border-bottom:1px solid var(--line);vertical-align:top}
th{font:600 .72rem var(--f-mono);letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
td code,li code{font:.88em var(--f-mono);background:color-mix(in srgb,var(--fg) 7%,transparent);padding:1px 5px;border-radius:4px}
.tables{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:16px}
.card{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:14px 16px;min-width:0;overflow-x:auto}
.card h3{font:600 1rem var(--f-head);margin:0 0 6px}
ol.checks{margin:0;padding-left:1.3rem;display:grid;gap:8px;max-width:80ch}
.sw{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:6px;vertical-align:middle}
/* svg */
.bb{fill:var(--bb);stroke:var(--bb-edge);stroke-width:1.5}
.hole{fill:var(--hole)}
.rail-p{stroke:var(--w3);stroke-width:1.6;opacity:.75}
.rail-n{stroke:var(--wcl);stroke-width:1.6;opacity:.75}
.rail-lbl{font:600 10px var(--f-mono);fill:var(--muted)}
.board-title{font:600 13px var(--f-mono);fill:var(--fg);letter-spacing:.06em}
.pcb-esp{fill:var(--pcb-esp)} .pcb-blue{fill:var(--pcb-blue)} .pcb-tft{fill:var(--pcb-tft)}
.shield{fill:#9aa3a8;opacity:.35}
.screen{fill:#0d1114;stroke:#3a4247}
.slot{fill:none;stroke:var(--pcb-fg);stroke-opacity:.5;stroke-dasharray:3 3}
.usb{fill:#b9c0c4;stroke:#6b757a}
.pin{fill:var(--pin)} .pin.on{fill:var(--pin-on)}
.pcbtxt{font:11px var(--f-mono);fill:var(--pcb-fg)}
.pcbtxt.sm{font-size:10px}
.pcbtxt.small{font-size:9.5px;opacity:.8}
.pcbtxt.big{font:600 15px var(--f-mono);letter-spacing:.2em}
.pcbtxt.b{font-weight:600}
.pcbtxt.dim{opacity:.42}
.lbl{font:11.5px var(--f-mono);fill:var(--fg)}
.lbl.b{font-weight:600}
.plugtxt{font:10.5px var(--f-mono);fill:#eef3f1}
.note{font:600 11px var(--f-mono);fill:var(--fg)}
.note-bg{fill:var(--surface);stroke:var(--line)}
.badge.ok{fill:var(--ok)} .badge.bad{fill:var(--bad)}
.badgetxt{font:600 10px var(--f-mono);fill:#fff}
.faded{opacity:.28}
.halo{stroke:var(--bb);stroke-linecap:round;stroke-linejoin:round}
.w{stroke-linecap:round;stroke-linejoin:round}
.dot{stroke:none}
.c-3v3{stroke:var(--w3)} .dot.c-3v3{fill:var(--w3)}
.c-5v{stroke:var(--w5)} .dot.c-5v{fill:var(--w5)}
.c-12v{stroke:var(--w12)} .dot.c-12v{fill:var(--w12)}
.c-gnd{stroke:var(--wg)} .dot.c-gnd{fill:var(--wg)}
.c-tft{stroke:var(--wtft)} .dot.c-tft{fill:var(--wtft)}
.c-sd{stroke:var(--wsd)} .dot.c-sd{fill:var(--wsd)}
.c-ctx{stroke:var(--wctx)} .dot.c-ctx{fill:var(--wctx)}
.c-crx{stroke:var(--wcrx)} .dot.c-crx{fill:var(--wcrx)}
.c-canh{stroke:var(--wch)} .dot.c-canh{fill:var(--wch)}
.c-canl{stroke:var(--wcl)} .dot.c-canl{fill:var(--wcl)}
.c-sense{stroke:var(--wsense)} .dot.c-sense{fill:var(--wsense)}
.c-usb{stroke:var(--wusb)} .dot.c-usb{fill:var(--wusb)}
.res{fill:#d8c3a0;stroke:#8a6f45}
.plate{stroke:var(--fg);stroke-width:3}
.fuse{fill:#f3e3a6;stroke:#9a7d1e}
.fusewire{stroke:#6b5a1a;stroke-width:1.2}
.dsym{fill:var(--fg)}
.dbar{stroke:var(--fg);stroke-width:2.4}
.plug{fill:#2a2f33;stroke:#555f64}
"""

LEG = [("3V3","--w3"),("5V","--w5"),("+12 V (car)","--w12"),("GND","--wg"),("TFT SPI","--wtft"),("SD SPI","--wsd"),
       ("CTX (TWAI TX)","--wctx"),("CRX (TWAI RX)","--wcrx"),("CAN-H","--wch"),("CAN-L","--wcl"),("12 V sense","--wsense"),("USB cable","--wusb")]
legend = '<div class="legend">' + "".join(f'<span><i style="background:var({v})"></i>{E(n)}</span>' for n, v in LEG) + '</div>'

def table(head, rows):
    h = "<tr>" + "".join(f"<th>{c}</th>" for c in head) + "</tr>"
    b = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f"<table>{h}{b}</table>"

reader_rows = [
 ("<code>3V3</code>","3V3 rail → TFT VCC + LED, transceiver 3V3",""),
 ("<code>GND</code>","GND rail (all modules)",""),
 ("<code>GPIO5</code>","Transceiver <code>CTX</code>","TWAI TX"),
 ("<code>GPIO4</code>","Transceiver <code>CRX</code>","TWAI RX"),
 ("<code>GPIO18</code>","TFT <code>SCK</code> + <code>T_CLK</code>","VSPI"),
 ("<code>GPIO23</code>","TFT <code>SDI</code> + <code>T_DIN</code>","VSPI"),
 ("<code>GPIO19</code>","TFT <code>SDO</code> + <code>T_DO</code>","VSPI"),
 ("<code>GPIO15</code>","TFT <code>CS</code>",""),
 ("<code>GPIO2</code>","TFT <code>DC</code>",""),
 ("<code>GPIO22</code>","TFT <code>RESET</code>",""),
 ("<code>GPIO21</code>","TFT <code>T_CS</code> (touch)","<code>T_IRQ</code> not connected"),
 ("<code>GPIO14</code>","SD <code>SCK</code>","HSPI"),
 ("<code>GPIO13</code>","SD <code>MOSI</code>","HSPI"),
 ("<code>GPIO26</code>","SD <code>MISO</code>","not GPIO12 (boot pin)"),
 ("<code>GPIO27</code>","SD <code>CS</code>",""),
 ("<code>5V</code>","SD <code>VCC</code>","module has its own 3.3 V regulator"),
 ("<code>GPIO35</code>","12 V sense divider","car only · ADC1"),
]
sim_rows = [("<code>3V3</code>","Transceiver 3V3",""),("<code>GND</code>","Transceiver GND + GND link to board A",""),
            ("<code>GPIO5</code>","Transceiver <code>CTX</code>",""),("<code>GPIO4</code>","Transceiver <code>CRX</code>",""),("USB","PC","power + serial")]
obd_rows = [("16","+12 V battery","1 A fuse → TVS → 1N5822 → 470 µF → LM2596 IN+"),
            ("4","Chassis GND","GND bus"),("5","Signal GND","GND bus"),
            ("6","CAN-H","Transceiver <code>CANH</code>"),("14","CAN-L","Transceiver <code>CANL</code>")]

page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>W204 Reader Wiring</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans+Condensed:wght@600&family=IBM+Plex+Sans:wght@400;600&display=swap">
<style>{CSS}</style>
</head><body>
<div class="wrap">
<header>
  <div class="eyebrow">w204-obu-reader · hardware</div>
  <h1>W204 Reader Wiring</h1>
  <p>Breadboard wiring for the ESP32 OBD reader. Figure 1 is the bench setup: the reader and the ECU simulator talk over CAN on your desk. Figure 2 is the same reader in the car, powered from the OBD-II port. All pin numbers are ESP32 GPIO numbers as printed on the DevKitC V4.</p>
</header>

<section>
  {legend}
</section>

<section>
  <h2>Figure 1 · Bench: reader + simulator</h2>
  <figure>
    <div class="scroll">{fig1()}</div>
    <figcaption>Both ESP32s run from PC USB. The two transceivers connect CAN-H to CAN-H and CAN-L to CAN-L, and the GND rails are linked. Keep the 120 Ω resistor on both transceiver boards: together they terminate the bench bus. With power off you should measure about 60 Ω between CAN-H and CAN-L.</figcaption>
  </figure>
</section>

<section>
  <h2>Figure 2 · Reader in the car</h2>
  <figure>
    <div class="scroll">{fig2()}</div>
    <figcaption>The faded parts are wired exactly as in Figure 1. What's new: OBD-II pin 16 feeds the protected 12 V supply into the LM2596, whose USB output powers the ESP32. Pins 6 and 14 go to the transceiver. A 100 kΩ / 22 kΩ divider brings the battery voltage to GPIO35 (14.4 V reads as about 2.6 V). The car's bus is already terminated, so <strong>remove the 120 Ω resistor</strong> from the reader's transceiver.</figcaption>
  </figure>
</section>

<section>
  <h2>Pin map</h2>
  <div class="tables">
    <div class="card"><h3>Reader ESP32</h3>{table(["ESP32","Connects to","Note"], reader_rows)}</div>
    <div class="card" style="display:grid;gap:16px;align-content:start">
      <div><h3>Simulator ESP32</h3>{table(["ESP32","Connects to","Note"], sim_rows)}</div>
      <div><h3>OBD-II plug (car)</h3>{table(["Pin","Signal","Goes to"], obd_rows)}</div>
    </div>
  </div>
</section>

<section>
  <h2>Before you power up</h2>
  <ol class="checks">
    <li><strong>Bench first.</strong> Get the reader talking to the simulator (Figure 1) before you plug anything into the car.</li>
    <li><strong>Termination.</strong> Most SN65HVD230 boards have a 120 Ω resistor marked <code>121</code>. Bench: keep it on both boards. Car: lift or cut it on the reader's board. Check with a meter: about 60 Ω across CAN-H/CAN-L on the bench, and about 60 Ω at the car's OBD pins 6–14 with the ignition off.</li>
    <li><strong>Test the power section on its own.</strong> Feed it 12–14 V from a bench supply or the car with no ESP32 connected. Check for 5.0 V on the LM2596's USB output before you plug the ESP32 in.</li>
    <li><strong>One power source at a time.</strong> In the car the ESP32's USB port is taken by the LM2596 cable. To watch serial logs in the car, unplug that cable and use the laptop's USB instead, with the laptop on battery.</li>
    <li><strong>Boot pins.</strong> GPIO2 (TFT DC) and GPIO15 (TFT CS) are ESP32 boot-strap pins. They work with the TFT attached, but if flashing ever fails, unplug the TFT and retry. GPIO12 is deliberately unused, because pulling it high at boot breaks startup.</li>
    <li><strong>Breadboard fit.</strong> The DevKitC V4 is wide. On one 830-point breadboard it leaves only one free hole per pin on one side. Put two breadboards side by side with the ESP32 across the gap, or use the female-to-male jumpers straight to the header.</li>
    <li><strong>OBD cable colours vary by seller.</strong> Identify pins 4, 5, 6, 14 and 16 with a continuity test before you solder anything.</li>
  </ol>
</section>
</div>
</body></html>
"""
open(OUT, "w").write(page)
print(len(page))
