# Full Scan and Maintenance Analysis

The reader's main job: record a **complete, repeatable scan** of the car to the SD card. You bring the scan folder to Claude Code, and Claude analyzes it and writes a **preventive maintenance report**.

```
Car ──OBD-II──▶ Reader (guided scan) ──SD card──▶ scans/<session>/ ──▶ tools/analyze_scan.py ──▶ Claude ──▶ report.md
```

The live TFT and web gauges stay, but they are secondary. They mainly guide you through the scan steps.

---

## 1. What "complete" means, and its limits

| Layer | What we can read | Available |
|---|---|---|
| **Generic OBD-II** (engine + transmission, emissions-related) | Every supported Mode 01 PID, freeze frames (02), stored / pending / permanent DTCs (03 / 07 / 0A), on-board monitor test results (06), vehicle info (09) | From phase 2. Standard, works on every W204 |
| **Mercedes modules** (ESP, SRS, EIS/ESL, SAM front/rear, cluster, transmission VGS, A/C, etc.) | Per-module fault codes, and extra values such as transmission oil temperature, engine oil level and temperature, camshaft adjustment | Phase 5. Needs W204 module addresses and data IDs found by sniffing a scan tool. **Read-only.** |

A scan made before phase 5 covers the engine and transmission emissions data only. The report will say so. It will not claim the whole car is fault-free.

## 2. Scan procedure (guided on the web UI)

The web dashboard runs a step-by-step wizard. Each step is written into the files as a `step` marker, so the analysis compares like with like.

| Step | Condition | Duration | What it's for |
|---|---|---|---|
| **S0 Info** | You enter the odometer (km), the date and km of the last service, the engine code (e.g. M271, M272, OM651), and fuel / notes | n/a | Context. Odometer and service history aren't readable by generic OBD |
| **S1 Key on, engine off** | Ignition on, engine **cold** if possible (parked > 6 h) | ~1 min | VIN, calibration IDs, all DTCs, freeze frames, readiness monitors, Mode 06 results, resting battery voltage, coolant vs intake temperature (sensor plausibility when cold) |
| **S2 Cranking** | Start the engine | ~5 s at 20 Hz | Lowest battery voltage while cranking (battery and starter health) |
| **S3 Warm-up idle** | Idle until coolant ≥ 80 °C, or 10 min max | 5–10 min | Warm-up curve (thermostat), idle stability, switch into closed loop |
| **S4 Warm idle** | Coolant ≥ 80 °C, no load (A/C off) | 2 min | Fuel trims at idle, MAF at idle, O2 sensor switching, charging voltage |
| **S5 2500 rpm hold** | Park/neutral, steady 2500 rpm | 1 min | Fuel trims at higher airflow, compared with S4 (vacuum leak versus MAF/fuel), catalyst O2 behaviour |
| **S6 Drive** | Normal mixed driving, city and highway | 20–30 min | Trims across load, coolant and transmission temperature under load, charging under load, misfire counters |
| **S7 Final** | Engine off at the end | ~1 min | DTCs, pending codes and Mode 06 again (monitors completed during the drive) |

Polling: fast signals (RPM, speed, load, trims, O2, MAF, throttle) at about 5 Hz, using multi-PID requests (up to 6 PIDs per Mode 01 request). Slow signals (temperatures, voltages) at 1 Hz. Requests stay ≥ 20 ms apart (see the safety rules in [PLAN.md](PLAN.md)).

## 3. Scan files (one folder per session)

```
scans/2026-11-20_0930/
  session.json        # vehicle + context from S0, step start/end timestamps, firmware version
  vehicle.json        # VIN, calibration IDs (CALID/CVN), supported PID list per mode
  dtc.json            # S1 and S7: stored / pending / permanent per module, plus freeze frames
  readiness.json      # S1 and S7: monitor status (catalyst, O2, O2 heater, EVAP, EGR, misfire, fuel, components)
  mode06.json         # S1 and S7: every test ID with value, min and max limit, pass/fail
  live.csv            # wide CSV: t_ms, step, <one column per supported PID, in SI units>
  raw_can.log         # optional: raw frames (candump format) for debugging and phase 5 work
```

- `live.csv` column names are fixed and include units: `rpm`, `speed_kmh`, `coolant_c`, `iat_c`, `load_pct`, `maf_gps`, `stft_b1_pct`, `ltft_b1_pct`, `stft_b2_pct`, `ltft_b2_pct`, `o2_b1s1_v`, `o2_b1s2_v`, `throttle_pct`, `timing_deg`, `module_v`, `fuel_status`, … A PID the car doesn't support is left out, not filled with zeros.
- **Privacy:** these files contain the VIN. The `scans/` folder is git-ignored.

## 4. How to get an analysis

1. Copy the session folder from the SD card (or download it from the web UI) into `scans/` in this repo.
2. In Claude Code, ask: *"analyze scans/2026-11-20_0930"*.
3. Claude runs `tools/analyze_scan.py`. The script computes per-step statistics and checks the rules in section 5, then writes `summary.json` into the session folder. Claude reads it, together with the raw data where something looks off, and writes `scans/<session>/report.md`.
4. With more than one session, Claude also compares them over time (for example, LTFT drifting more lean each month). Trends predict failures better than any single scan.

### Report format

- **Vehicle and scan coverage:** what was read, and what wasn't (e.g. Mercedes modules not yet supported).
- **Fault codes:** each code with its meaning, the likely cause, and whether it's current, pending or historical.
- **Findings:** each one with its evidence (the numbers and the step), what it indicates, and how confident the conclusion is.
- **Preventive maintenance plan:** ranked by urgency.
  - **Now:** safety, or damage likely if ignored.
  - **Soon:** within about 1,000 km or 1 month.
  - **Next service:** add to the next A/B service.
  - **Monitor:** recheck at the next scan.
- **Next scan:** when to scan again, and what to watch.

The report helps you decide what to check. It doesn't replace a mechanic's inspection. Every recommendation names the evidence behind it, so a workshop can verify it.

## 5. Analysis rules (starting thresholds)

These are general OBD-II rules of thumb, adapted for Mercedes petrol engines. They are tuned once there is real baseline data from this car. Fuel-trim rules only use samples with `fuel_status` = closed loop.

| Area | Signal / step | Normal | Flag when | Points to | Preventive action |
|---|---|---|---|---|---|
| Fuel mixture | LTFT, S4 idle | within ±5 % | beyond ±10 % | Lean at idle that improves at S5: **vacuum / intake leak** (PCV, intake hoses). Lean at both: **MAF or fuel delivery** | Smoke test for leaks. Clean or check the MAF. Fuel filter or pressure check |
| Fuel mixture | STFT + LTFT, S5 / S6 | within ±10 % | beyond ±15 %, or bank 1 and bank 2 differ by > 8 % (V6) | A one-bank problem: leak, injector or O2 sensor on that bank | Inspect that bank's intake and injectors |
| Upstream O2 | o2_b1s1_v, S5 | switches 0.1–0.9 V, ≥ about 1 switch/s | slow, stuck, or limited range | **Ageing O2 sensor** | Replace the sensor if slow and over about 150,000 km |
| Catalyst | o2_b1s2_v vs s1, S5; Mode 06 catalyst test | downstream steady at about 0.6–0.8 V | downstream follows upstream; Mode 06 near its limit | **Catalyst efficiency dropping** | Fix misfires or rich running first, then monitor |
| Misfire | Mode 06 misfire counters per cylinder, S7 | about 0 on all cylinders | one cylinder clearly higher, or rising between scans | **Spark plug or ignition coil** on that cylinder | Plugs (M271/M272: about 60,000–100,000 km by MB schedule), swap coils to test |
| Cooling | coolant_c warm-up curve, S3/S6 | reaches about 80 °C within 10–15 min, holds 80–105 °C | stays < 80 °C while driving, or > 110 °C | Low: **thermostat stuck open** (common on M271/M272, P0128). High: thermostat stuck, pump, fan or radiator | Thermostat. Coolant service every 3–4 years |
| Sensor plausibility | coolant_c vs iat_c, S1 after a cold soak | within about 5 °C | differ by > 10 °C | A faulty temperature sensor | Check the sensor before trusting other readings |
| Battery | module_v, S1 resting | ≥ 12.4 V | < 12.2 V | **Weak or undercharged battery** (W204 electronics are sensitive to low voltage) | Battery test. Check for drain if repeated |
| Battery / starter | module_v minimum, S2 | ≥ 10.0 V | < 9.6 V | **Battery near end of life** | Replace the battery before it fails |
| Charging | module_v, S4/S6 | 13.5–14.8 V (smart charging varies) | < 13.2 V or > 15.0 V | **Alternator or regulator** | Test the alternator and belt |
| Air flow | maf_gps, S4 | ≈ 0.9–1.2 g/s per litre of displacement at idle (rule of thumb) | well below that | **Dirty or failing MAF**, or an intake leak after the MAF | Clean or check the MAF and air filter |
| Transmission | trans oil temp (phase 5), S6 | 70–100 °C | sustained > 110 °C | Fluid wear, cooler problem | 722.9 fluid and filter service about every 60,000 km |
| Readiness | readiness.json, S7 | all complete | incomplete after a 30 min drive | Codes recently cleared or battery disconnected, or a monitor can't complete | Rescan after more driving. Look for the blocking condition |
| DTCs | dtc.json | none | any stored, pending or permanent code | Depends on the code | Explained per code in the report |

**W204 items to watch** (cross-checked against fault codes and data once Mercedes module scanning works):
- **Camshaft adjuster solenoid oil leak into the wiring** (M271/M272). Watch for camshaft position codes, then check the connectors.
- **Electronic steering lock (ESL/ELV) failure** (EIS/ESL fault codes, phase 5).
- **722.9 conductor plate / speed sensor faults** (transmission codes, limp mode).
- **Battery and low-voltage faults** spread across many modules (several modules logging voltage codes points to the battery, not the modules).

## 6. Open questions (vehicle info still needed)

These set the right thresholds and the W204 checks for this car. Fill them in when you know them. They also go into `session.json` at step S0 of each scan.

| ✓ | Question | Why it matters | Answer |
|---|---|---|---|
| ☑ | Engine and variant (e.g. C200 Kompressor M271, C250 M271 EVO, C300 M272, C200 CDI OM651) | Petrol or diesel changes most rules (diesels have no narrowband O2 or catalyst checks; they have DPF and EGR instead). Also sets the bank-2 checks and the expected MAF at idle | **M272 V6 3.0 L petrol** (sold as C280 or C300 depending on market) |
| ☑ | Model year (and pre- or post-facelift, 2011+) | Which modules and protocols to expect (KWP2000 vs UDS), and the known issues for that year | **2009, pre-facelift** |
| ☑ | Transmission (7G-Tronic 722.9, 5-speed 722.6, or manual) | Transmission fluid service interval and fault-code checks | **7G-Tronic automatic (722.9)** |
| ☐ | Current odometer (km) | Wear-based items (plugs, O2 sensors, fluids) and the baseline for trend tracking | _pending_ |
| ☐ | Last service: date, km, A or B service | Where the car is in the Mercedes maintenance schedule | _pending_ |
| ☐ | Last spark plug change (km/date) | Misfire findings and plug replacement timing | _pending_ |
| ☐ | Last transmission fluid change (km/date) | Transmission service recommendation | _pending_ |
| ☐ | Battery age (install date) | Battery and cranking findings | _pending_ |
| ☐ | Last coolant change, brake fluid change | Time-based items the scan can't measure | _pending_ |
| ☐ | Known symptoms (warning lights, rough idle, harsh shifts, starting problems, noises) | Focus the analysis on what you already notice | _pending_ |

### What this means for this car (M272 3.0 V6, 2009 pre-facelift, 722.9)

- **Two banks.** The scan records and compares both: `stft_b2_pct`, `ltft_b2_pct`, `o2_b2s1_v`, `o2_b2s2_v`. A trim difference between banks of more than 8 % is flagged (SCAN.md §5).
- **Expected MAF at warm idle:** about **2.7–3.6 g/s** (3.0 L × 0.9–1.2 g/s per litre).
- **M272 checks added to the analysis:**
  - **Intake manifold runner flap (tumble flap) lever failure:** a common M272 fault. Watch for intake runner control codes (P2004–P2007 range).
  - **Camshaft adjuster solenoids leaking oil into the wiring:** watch for camshaft position / timing codes (P0010–P0019). Inspect the solenoid connectors at each oil service.
  - **Balance shaft / idler sprocket wear:** this mainly affected engines built before about mid-2006, so a 2009 engine is very likely the fixed version. The same timing-correlation codes (P0016–P0019) would still show it.
  - **Thermostat stuck open** (P0128, slow warm-up) and **oil leaks** around the oil cooler and crankcase breather. The scan only sees the thermostat; leaks need a visual check.
- **722.9 checks:** conductor plate / speed sensor fault codes, transmission oil temperature once phase 5 works. Recommended fluid and filter service about every 60,000 km.
- **Protocol:** pre-facelift W204 modules most likely use **KWP2000** (the facelift moved toward UDS). Phase 5 confirms this by sniffing.

## 7. Work items this adds

- Firmware: discover supported PIDs, then poll all of them. Read Modes 02, 06, 09 and 0A. Add the guided scan wizard on the web UI, write the session files above, and download them from the web UI.
- `tools/analyze_scan.py`: load a session, compute per-step statistics, apply the rules in section 5, and write `summary.json`.
- Simulator: generate realistic sample scans, including injected faults (lean trim, slow O2, cold thermostat, weak battery), to test the whole chain before the first scan of the real car.
