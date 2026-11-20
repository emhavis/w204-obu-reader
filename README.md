# W204 OBD Reader (ESP32)

An ESP32-based diagnostic reader for the Mercedes-Benz W204 C-Class (2007–2014). It connects straight to the OBD-II diagnostic CAN bus (500 kbps). It reads generic OBD-II data and Mercedes-specific module data (KWP2000/UDS), and shows it on:

- an onboard TFT screen
- a phone web dashboard (the ESP32 runs its own WiFi network)
- CSV logs on an SD card

Full design and roadmap: [docs/PLAN.md](docs/PLAN.md)

## Hardware

| Part | Notes |
|---|---|
| ESP32-WROOM-32 DevKit (or ESP32-S3) | Built-in TWAI (CAN) controller |
| SN65HVD230 CAN transceiver | 3.3 V |
| OBD-II male plug / pigtail | |
| Automotive buck converter 12 V → 5 V | Rated for 24 V+ input, with a fuse and a TVS diode |
| 2.8" ILI9341 SPI TFT | VSPI |
| microSD SPI module | HSPI |
| Second ESP32 + transceiver | Bench ECU simulator |

## Wiring

| OBD-II pin | Signal | Connects to |
|---|---|---|
| 6 | CAN-H | Transceiver CANH |
| 14 | CAN-L | Transceiver CANL |
| 16 | +12 V (battery) | Fuse → TVS → buck converter input |
| 4 / 5 | Chassis / signal GND | Common GND |

| ESP32 | Transceiver |
|---|---|
| GPIO5 | CTX (TX) |
| GPIO4 | CRX (RX) |
| 3V3 / GND | VCC / GND |

## Project layout

```
src/        reader firmware
sim/        bench ECU simulator firmware
data/www/   web dashboard (uploaded to LittleFS)
tools/      host-side scripts (CAN dump decoding)
docs/       design docs
```

## Build

Requires [PlatformIO](https://platformio.org/).

```sh
pio run -e reader -t upload      # reader firmware
pio run -e reader -t uploadfs    # web dashboard files
pio run -e simulator -t upload   # bench simulator (second ESP32)
pio device monitor
```

## Roadmap

- [ ] Phase 1: CAN bring-up (TWAI, bench test, listen-only sniffing in the car)
- [ ] Phase 2: Generic OBD-II (ISO-TP, Mode 01 PIDs, DTCs, VIN)
- [ ] Phase 3: Outputs (TFT, web dashboard, SD logging)
- [ ] Phase 4: Mercedes-specific data (KWP2000/UDS: transmission temp, oil level/temp, per-module DTCs)
- [ ] Phase 5: Power management and enclosure (sleep, < 1 mA when off)

## Safety

- The firmware sends **read-only** diagnostic services only. Coding, routine-control, IO-control and write services are blocked by a whitelist.
- Clearing DTCs needs explicit confirmation and works only when the vehicle is stationary.
- Diagnostic requests are rate-limited (≥ 20 ms apart).
- Use at your own risk. Test on the bench simulator before connecting to a car.
