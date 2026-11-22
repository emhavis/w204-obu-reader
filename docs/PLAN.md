# W204 ESP32 Sensor Reader — Plan

## Context
**Primary goal (updated 2026-11-20):** make a **complete, guided scan** of the car's sensors and fault codes, save it to the SD card, and bring it to Claude Code. Claude analyzes it and writes a **preventive maintenance report**. The scan procedure, file format and analysis rules are in [SCAN.md](SCAN.md). The live display and dashboard are now secondary: they guide the scan steps.

Build a sensor reader for a Mercedes-Benz W204 (C-Class 2007–2014) on an ESP32. It plugs straight into the OBD-II port (500 kbps diagnostic CAN on pins 6 and 14). It reads generic OBD-II data first, then Mercedes-specific module data over KWP2000/UDS. Results show on an onboard TFT screen, on a phone web dashboard over the ESP32's own WiFi network, and are logged to an SD card. The project folder is empty, so everything is new.

**Feasibility:** Yes. The ESP32 has a built-in CAN controller (TWAI) and needs only a 3.3 V transceiver. Generic OBD-II is well documented. The risk is in the Mercedes-specific data: the ECU addresses and data identifiers (DIDs) are not public. We find them by sniffing a scan tool session or from community sources. That is why it is a separate phase.

## Immediate step: set up the repo (do first)
1. `git init -b main` in the project folder.
2. `.gitignore`: `.pio/`, `.vscode/*` (keep `extensions.json`), `*.bin`, `.DS_Store`, `logs/`, `*.csv` dumps, `secrets.h`.
3. `docs/PLAN.md`: a copy of this plan, kept in the repo.
4. `README.md`: project summary, hardware/BOM, wiring table, phase checklist, safety rules, link to `docs/PLAN.md`.
5. Placeholder layout: `src/`, `sim/`, `data/www/`, `tools/`, and a minimal `platformio.ini` with `reader` and `simulator` envs.
6. Initial commit: "Initial project scaffold and plan". No push until the user gives a remote URL (then `git remote add origin <url> && git push -u origin main`).
Note: the folder is inside OneDrive. OneDrive syncing `.git/` can cause conflicts, so the user may want to exclude it or keep the repo outside OneDrive.

## Hardware (BOM)
- ESP32-WROOM-32 DevKit, or ESP32-S3 (both have TWAI)
- SN65HVD230 CAN transceiver (3.3 V). TWAI TX on GPIO5, RX on GPIO4. Transceiver CANH/CANL go to OBD pins 6/14.
- OBD-II male plug or pigtail. Pin 16 is +12 V, pins 4 and 5 are GND.
- Automotive-grade buck converter (12 V to 5 V, rated for 24 V+ input), plus a fuse and a TVS diode on the 12 V line
- 2.8" ILI9341 SPI TFT, using the LovyanGFX or TFT_eSPI library
- microSD SPI module, on a separate SPI bus (VSPI for the TFT, HSPI for the SD card)
- Second ESP32 and transceiver for a bench simulator (strongly recommended)

## Firmware architecture (PlatformIO + Arduino, FreeRTOS tasks)
```
platformio.ini            # envs: reader, simulator
src/main.cpp              # task setup
src/can/twai_bus.{h,cpp}  # TWAI init (normal + listen-only), send/recv queues
src/can/isotp.{h,cpp}     # ISO 15765-2: single/first/consecutive/flow-control frames
src/diag/obd2.{h,cpp}     # Mode 01 PIDs, Mode 03/04/07 DTCs, Mode 09 VIN
src/diag/mb_diag.{h,cpp}  # KWP2000 (0x1A,0x21,0x18) / UDS (0x22,0x19) read-only services, tester present
src/diag/signals.h        # table: {name, ecuTx, ecuRx, service, id, bytes, scale, offset, unit, period}
src/data/datastore.{h,cpp}# latest values + timestamps, mutex-protected
src/ui/display.{h,cpp}    # gauge pages, button/touch page switching
src/web/web.{h,cpp}       # WiFi AP, ESPAsyncWebServer, WebSocket push (~5 Hz)
data/www/index.html,app.js# served from LittleFS
src/log/sdlog.{h,cpp}     # CSV per trip, buffered writes, raw CAN dump mode
src/power/power.{h,cpp}   # 12 V monitor via divider/ADC, deep sleep when engine off / bus silent
sim/sim_main.cpp          # simulator: answers OBD PIDs + fake MB DIDs
```
Tasks: `canTask` (core 0) runs the polling scheduler over `signals.h`, scheduling each signal by its period. `uiTask`, `webTask` and `logTask` (core 1) read from the datastore.

## Phases
1. **CAN bring-up:** TWAI driver, then a test with the bench simulator, then in-car **listen-only** sniffing, logging raw frames to SD.
2. **Generic OBD-II, full coverage:** ISO-TP layer. Discover supported PIDs and poll **all** of them, using multi-PID requests. Read freeze frames (Mode 02), stored / pending / permanent DTCs (03 / 07 / 0A), on-board monitor results (06), and VIN / calibration IDs (09). Clearing DTCs stays behind the confirmation rule.
3. **Guided scan + export:** scan wizard on the web UI (steps S0–S7 in [SCAN.md](SCAN.md)), session folder on SD (`session.json`, `dtc.json`, `readiness.json`, `mode06.json`, `live.csv`), download from the web UI. Simulator generates sample scans with injected faults.
4. **Analysis tooling:** `tools/analyze_scan.py` computes per-step statistics, applies the rules in SCAN.md §5 and writes `summary.json`. Claude turns it into `report.md` with the maintenance plan. Tune thresholds on the first real scans of this car.
5. **Mercedes-specific:** generic KWP/UDS read client. Find ECU request/response IDs by sniffing a scan tool (Xentry, iCarsoft MB, Carly, etc.) talking to the car. Fill `signals.h` with confirmed DIDs: transmission oil temperature (722.6/722.9), engine oil temperature and level, and per-module DTCs (SAM, EIS, ESP, SRS). Add a tooling script (`tools/decode_dump.py`) to analyze the raw dumps.
   This phase extends the scan to every module the gateway exposes: per-module fault codes in `dtc.json`, and the extra values as columns in `live.csv`.
   **Fault-code descriptions.** Mercedes does not sell its fault-code database as a file. The official texts exist only inside Xentry.
   - **Lookup order:** local table `tools/dtc/dtc_local.csv` (git-ignored) → generic SAE J2012 text → `unknown`. Format and setup are in [tools/dtc/README.md](../tools/dtc/README.md).
   - **Filling the local table:** during splitter sessions (aftermarket MB scanner and the reader on the same port), write down the description the scanner shows for each code.
   - **Licensed text stays local.** Never commit text copied from WIS, Xentry or a commercial scanner, because the repo is public. Only generic codes in our own words go in `dtc_local.example.csv`.
   - **Official sources:** Mercedes-Benz B2B Connect (b2bconnect.mercedes-benz.com) sells time-based WIS repair-information passes and XENTRY licences. Check whether Indonesia is supported, or ask Mercedes-Benz Indonesia after-sales. Before buying XENTRY Pass Thru, confirm it covers a 2009 W204. Avoid pirated WIS/EPC/Xentry downloads.
   - **Optional hardware:** an OBD splitter cable and an aftermarket MB scanner (iCarsoft MB or Autel). Both are needed to sniff module addresses and fault-code texts.
6. **Outputs polish:** TFT gauge pages, live web dashboard.
7. **Power and enclosure:** sleep and wake on CAN activity or ignition voltage, so the reader doesn't drain the battery.

## Safety rules (enforced in code)
- Read-only diagnostic services only. No coding, routine control, IO control or write services. Use a whitelist in `mb_diag`.
- Clearing DTCs needs explicit user confirmation and works only when the vehicle is stationary.
- Limit request rate (≥20 ms between requests) so diagnostic traffic doesn't overload the gateway.

## Verification
- `pio run -e reader` and `pio run -e simulator` build cleanly.
- Bench test: reader plus simulator on a 120 Ω-terminated CAN pair. Live values appear on the TFT, the web page and the SD CSV.
- In the car: values match a known OBD app (e.g. Car Scanner) for RPM, coolant and speed. DTC list matches a scan tool.
- Mercedes-specific values are checked against a dealer or aftermarket MB scan tool.
- Battery current with the car off and the reader in sleep is under 1 mA.
