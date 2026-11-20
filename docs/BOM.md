# Bill of Materials (BOM)

Parts needed to build the W204 OBD reader and the bench simulator. See [PLAN.md](PLAN.md) for the design and the [README](../README.md) for the wiring.

**Marketplace:** Tokopedia (Indonesia). Every part here is also sold on Shopee under the same search terms.
**Prices:** IDR, collected 2026-11-20 from search-indexed listings. Tokopedia prices and stock change often, so check the live page before you order. Shipping is not included.

**Which list to use:** order from the **optimized shopping list** below. Sections 1–2 list every part per build, with specs, the cheapest seller found for each part, and alternatives.

**Status column:**
- **Listed**: the price comes from a specific Tokopedia listing (linked).
- **Est.**: no clear listing price was found. The figure is a typical market estimate. Use the search term to find a seller.

---

## Shopping list: optimized for fewer sellers (reader + simulator)

This list replaces 8 shipments with **4 online sellers plus one trip to a local shop**. Quantities already cover both builds. The `For` column points to the item IDs in sections 1 and 2, which still have the specs and alternative sellers.

**How it was optimized:**
- **One general electronics store (cncstorebandung) takes most of the parts:** both ESP32 boards, the power module and all the small parts.
- **Only the parts that store doesn't list get their own seller:** the CAN transceiver, the TFT and the OBD cable are specialty items.
- **Common items are bought offline:** the microSD card, fuse holder and plastic box are in any phone, auto-parts or electronics shop. That avoids 3 extra shipments.
- **A cheaper TFT listing** (tokoasia-id, Rp 121.500 versus Rp 216.000) also brings the parts total down.

### Order 1 of 4: cncstorebandung (main order)

| ✓ | Item | Qty | Unit (Rp) | Line (Rp) | For | Status |
|---|---|---|---|---|---|---|
| ☐ | [ESP32 DevKitC V4 WROOM-32D + micro-USB cable](https://www.tokopedia.com/cncstorebandung/esp32-esp-32-devkitc-v4-wroom-32d-wifi-bluetooth-plus-kabel-micro-usb) (4.9★, 201 in stock) | 2 | 81.500 | 163.000 | R1, S1 | Listed |
| ☐ | [LM2596 step-down, 6–40 V in → 5 V 3 A, dual USB out](https://www.tokopedia.com/cncstorebandung/dc-dc-step-down-lm2596-6v-40v-to-5v-3a-dual-usb-output-module) | 1 | 12.900 | 12.900 | R4 | Listed |
| ☐ | microSD SPI module | 1 | ~8.500 | 8.500 | R9 | Ask seller |
| ☐ | Breadboard 830 + jumper wires (M-M, M-F) | 1 set | ~30.000 | 30.000 | S3 | Ask seller |
| ☐ | Perfboard, pin headers, JST connectors, hook-up wire | 1 set | ~25.000 | 25.000 | R13 | Ask seller |
| ☐ | Resistors 100 kΩ + 22 kΩ + 120 Ω ×2 (CAN bench termination), 100 nF caps, 470 µF/35 V cap | 1 set | ~5.000 | 5.000 | R11 | Ask seller |
| ☐ | TVS diode P6KE24A (or SMBJ24A) | 2 | ~3.000 | 6.000 | R6 | Ask seller |
| ☐ | Schottky diode 1N5822 (or SS34) | 1 | ~2.000 | 2.000 | R7 | Ask seller |
| | **Order subtotal** | | | **252.400** | | |

### Order 2 of 4: solarperfect

| ✓ | Item | Qty | Unit (Rp) | Line (Rp) | For | Status |
|---|---|---|---|---|---|---|
| ☐ | [SN65HVD230 CAN module (CJMCU-230)](https://tokopedia.com/solarperfect/cjmcu-230-bus-transceiver-sn65hvd230-can-communication-module) (4.9★, 42 in stock) | 2 | 25.300 | 50.600 | R2, S2 | Listed |

### Order 3 of 4: tokoasia-id

| ✓ | Item | Qty | Unit (Rp) | Line (Rp) | For | Status |
|---|---|---|---|---|---|---|
| ☐ | [2.8" SPI TFT ILI9341 240×320 with touch](https://www.tokopedia.com/tokoasia-id/2-4in-spi-tft-lcd-display-module-2-8in-spi-touch-panel-9-io-spi-touch-panel-with-pcb-5v-3-3v-ili9341-240x320-resolution-ili9341-driver-chip-industrial-lcd-module) (6 left) | 1 | 121.500 | 121.500 | R8 | Listed, check variant |

The listing sells both 2.4" and 2.8". Pick the **2.8"** variant and check that it is still Rp 121.500. If it's gone or costs much more, use [klinikrasid](https://www.tokopedia.com/klinikrasid/lcd-tft-touchscreen-2-8-in-spi-serial-ili9341-240-320-for-arduino) at Rp 216.000 instead.

### Order 4 of 4: rachman-shop

| ✓ | Item | Qty | Unit (Rp) | Line (Rp) | For | Status |
|---|---|---|---|---|---|---|
| ☐ | [OBD2 16-pin male → open-wire cable, 30 cm](https://www.tokopedia.com/rachman-shop/obd2-16pin-male-plug-connector-adapter-kabel) | 1 | ~75.000 | 75.000 | R3 | Price not shown, check |

### Local shop (no shipping)

| ✓ | Item | Qty | Est. (Rp) | For | Where |
|---|---|---|---|---|---|
| ☐ | microSD card 32 GB (SanDisk Ultra or similar) | 1 | ~75.000 | R10 | Phone or computer shop |
| ☐ | Inline fuse holder + 1 A fuse | 1 | ~10.000 | R5 | Auto-parts shop (toko variasi / onderdil mobil) |
| ☐ | ABS project box ~100 × 60 × 25 mm | 1 | ~25.000 | R12 | Electronics shop |
| | **Local subtotal** | | **110.000** | | |

### Optional: 12 V bench test (not in the total)

Only needed if you want to test the power section (fuse, TVS, Schottky, LM2596) on the desk before the car. Add these to the cncstorebandung order if they stock them (ask in chat), or buy them at the local shop.

| ✓ | Item | Qty | Est. (Rp) | For | Where |
|---|---|---|---|---|---|
| ☐ | 12 V 2 A DC adapter (5.5 × 2.1 mm barrel plug) | 1 | ~35.000 | O1 | search "adaptor 12V 2A" |
| ☐ | Female DC jack to screw terminal (5.5 × 2.1 mm) | 1 | ~5.000 | O2 | search "DC jack female terminal" |
| | **Optional subtotal** | | **~40.000** | | |

### Total

| Order | Rp |
|---|---|
| 1. cncstorebandung | 252.400 |
| 2. solarperfect | 50.600 |
| 3. tokoasia-id | 121.500 |
| 4. rachman-shop | 75.000 |
| Local shop | 110.000 |
| **Total parts** | **≈ 609.500** |
| Shipping | 4 shipments instead of 8 |

Compared with the per-part list in sections 1–2 (Rp 675.598 in parts, up to 8 shipments), this saves about **Rp 66.000 on parts** and **4 shipping fees**. Grouping most items in one order also makes it easier to reach the minimum spend for a free-shipping voucher.

### Before you check out: merge to 3 sellers if you can

Use Tokopedia chat to ask **cncstorebandung**: *"Ada SN65HVD230 CAN module? Ada micro SD module, breadboard, resistor, P6KE24A, 1N5822?"* ("Do you have…?")
- If they have the **SN65HVD230**, drop Order 2. That leaves **3 sellers**.
- If they lack some small parts, buy those at the local shop or add them to the solarperfect order instead. Don't open a new seller for them.
- **Same idea for solarperfect:** they sell other ESP32 boards. If they have the ESP32 DevKit (WROOM-32), you could move the ESP32s there.

**Note on R4:** the cncstorebandung LM2596 has a fixed 5 V output with USB sockets. Power the ESP32 with a short USB cable from it, so there's no voltage adjustment to get wrong. The fuse, TVS and Schottky diode still go on the 12 V input side.

---

## 1. Reader (the device in the car)

| # | Part | Spec / what to check | Qty | Unit (Rp) | Subtotal (Rp) | Status | Where to buy / search term |
|---|---|---|---|---|---|---|---|
| R1 | ESP32 DevKit | ESP32-WROOM-32 (TWAI built in), DOIT DevKit V1, USB-C | 1 | 68.999 | 68.999 | Listed | [sensorku-bekasi](https://www.tokopedia.com/sensorku-bekasi/esp32-esp-32-wroom-32-doit-devkit-v1-usb-c) · alt: [cncstorebandung DevKitC V4 + cable, Rp81.500](https://www.tokopedia.com/cncstorebandung/esp32-esp-32-devkitc-v4-wroom-32d-wifi-bluetooth-plus-kabel-micro-usb) |
| R2 | CAN transceiver | SN65HVD230 module (CJMCU-230), **3.3 V** | 1 | 25.300 | 25.300 | Listed | [solarperfect](https://tokopedia.com/solarperfect/cjmcu-230-bus-transceiver-sn65hvd230-can-communication-module) · alt: [galerielectro, Rp25.000](https://www.tokopedia.com/galerielectro/sn65hvd230-can-bus-transceiver-communication-module) |
| R3 | OBD-II male pigtail | 16-pin J1962 male plug to open wires, ~30 cm. Pins 4, 5, 6, 14 and 16 must be wired | 1 | ~75.000 | 75.000 | Est. | [rachman-shop "OBD2 16Pin Male Plug Connector Adapter Kabel"](https://www.tokopedia.com/rachman-shop/obd2-16pin-male-plug-connector-adapter-kabel) · search "kabel OBD2 male 16 pin" |
| R4 | Buck converter 12 V → 5 V | LM2596 adjustable, **input up to 40 V**, 3 A. Set output to 5.0 V **before** connecting the ESP32 | 1 | 9.500 | 9.500 | Listed | [emjteknik](https://www.tokopedia.com/emjteknik/lm2596-adjustable-dc-dc-step-down-module) · alt: [multitronic Type F fixed 5 V, Rp8.000](https://www.tokopedia.com/multitronic/module-step-down-lm2596-type-f) |
| R5 | Inline fuse holder + fuse | Mini blade or 5×20 mm glass, with **1 A** fuse | 1 | ~10.000 | 10.000 | Est. | search "fuse holder inline kabel" / "rumah sekring inline" |
| R6 | TVS diode | SMBJ24A (SMD) or P6KE24A (through-hole), 600 W. Buy 2, one spare | 2 | ~3.000 | 6.000 | Est. | search "P6KE24A" / "SMBJ24A" |
| R7 | Reverse-polarity diode | SS34 or 1N5822 Schottky, in series with +12 V | 1 | ~2.000 | 2.000 | Est. | search "dioda 1N5822" / "SS34" |
| R8 | TFT display | 2.8" ILI9341 SPI, 240×320, XPT2046 resistive touch | 1 | 216.000 | 216.000 | Listed | [klinikrasid](https://www.tokopedia.com/klinikrasid/lcd-tft-touchscreen-2-8-in-spi-serial-ili9341-240-320-for-arduino) |
| R9 | microSD module | SPI, with onboard level shifter / 3.3 V regulator | 1 | 8.500 | 8.500 | Listed | [tekno-kreasi-elektronik](https://www.tokopedia.com/tekno-kreasi-elektronik/micro-sd-card-module-spi-arduino-welded) · alt: [cncstorejogja](https://www.tokopedia.com/cncstorejogja/cnc-micro-sd-card-spi-module-microsd) |
| R10 | microSD card | 32 GB SanDisk Ultra (SDHC, formats as FAT32) | 1 | 75.000 | 75.000 | Listed | [stardisc89](https://www.tokopedia.com/stardisc89/sandisk-ultra-microsd-32gb-class-10-no-adapter-original) · upgrade: [High Endurance 32 GB, Rp235.000](https://www.tokopedia.com/genzymart/sandisk-high-endurance-microsdhc-card-100mb-s-32gb-sdsqqnr-032g-gn6ia) |
| R11 | 12 V sense divider + passives | 100 kΩ + 22 kΩ resistors (12 V → ADC), 120 Ω ×2 (plug-in CAN termination for the bench, one spare), 100 nF caps, 470 µF/35 V cap on buck input | 1 set | ~5.000 | 5.000 | Est. | search "resistor 1/4 watt" / "elco 470uF 35V" |
| R12 | Enclosure | ABS project box, ~100 × 60 × 25 mm, with a cut-out for the TFT | 1 | ~25.000 | 25.000 | Est. | search "box project ABS hitam" / "kotak elektronik plastik" |
| R13 | Build hardware | Perfboard (PCB lubang), pin headers, JST connectors, hook-up wire, heat-shrink | 1 set | ~25.000 | 25.000 | Est. | search "PCB lubang" / "konektor JST" |
| | **Reader subtotal** | | | | **551.299** | | |

## 2. Bench simulator (strongly recommended)

A second ESP32 plays the car's ECU on your desk. You can test the firmware without plugging into the car.

| # | Part | Spec | Qty | Unit (Rp) | Subtotal (Rp) | Status | Where to buy |
|---|---|---|---|---|---|---|---|
| S1 | ESP32 DevKit | Same as R1 | 1 | 68.999 | 68.999 | Listed | Same as R1 |
| S2 | CAN transceiver | Same as R2 | 1 | 25.300 | 25.300 | Listed | Same as R2 |
| S3 | Breadboard + jumper wires | 830-point breadboard, M-M and M-F jumpers | 1 set | ~30.000 | 30.000 | Est. | search "breadboard 830 + kabel jumper" |
| | **Simulator subtotal** | | | | **124.299** | | |

## 2b. Optional: 12 V bench test

For testing the in-car power section on the desk, without the car. The bench setup itself (Figure 1 in [wiring.html](wiring.html)) runs from PC USB and doesn't need this. The free alternative is to test the power section in the car with the ESP32 unplugged and check for 5.0 V at the LM2596's USB output.

| # | Part | Spec | Qty | Unit (Rp) | Subtotal (Rp) | Status | Where to buy |
|---|---|---|---|---|---|---|---|
| O1 | 12 V DC adapter | 12 V, 2 A, 5.5 × 2.1 mm barrel plug. Feeds the power section in place of OBD pin 16 / GND | 1 | ~35.000 | 35.000 | Est. | search "adaptor 12V 2A" |
| O2 | Female DC jack terminal | 5.5 × 2.1 mm female jack with screw terminals (+ / −), to connect the adapter to the fuse input and GND bus | 1 | ~5.000 | 5.000 | Est. | search "DC jack female terminal" |
| | **Optional subtotal** (not in the totals below) | | | | **~40.000** | | |

**How to use it:** connect the jack's **+** to the fuse input (where OBD pin 16 goes), and **−** to the GND bus (where pins 4/5 go). Leave the ESP32 unplugged, power up, and check for 5.0 V at the LM2596 USB output. Then unplug the adapter before connecting the OBD plug. Never connect both at once. An adapter can't test the 14.4 V charging voltage or overvoltage cases. Only an adjustable bench supply can (Rp 300k+, not needed).

## 3. Totals

| Group | Rp |
|---|---|
| Reader | 551.299 |
| Bench simulator | 124.299 |
| **Grand total (before shipping)** | **≈ 675.598** |

Of that, Rp 497.598 (74%) is from listed prices and Rp 178.000 is estimated. Expect the real total to land between **Rp 600.000 and Rp 750.000**, plus shipping from 2–4 sellers.

**Ways to cut cost:**
- **TFT (R8)** is 39% of the reader cost. A 2.8" ILI9341 **without touch** is usually cheaper, and the plan already supports button page switching. Or skip the TFT and use only the phone web dashboard.
- Buy R1 + S1 and R2 + S2 from the **same seller** to pay shipping once.
- If you already own a breadboard, resistors and wires, drop S3, R11 and R13 (about Rp 60.000).

## 4. Buying notes (read before ordering)

1. **CAN termination resistor (R2/S2).** Most SN65HVD230 modules have a 120 Ω resistor on board (often marked `121`, near CANH/CANL).
   - **In the car:** the bus is already terminated. **Remove or cut** the 120 Ω on the reader's module, or it will load the W204 diagnostic bus.
   - **On the bench:** keep it on both modules. That gives the correct 2 × 120 Ω termination.
2. **Buck converter input rating (R4).** Do **not** use a Mini-360 or MP1584 module. They are rated to only 23–28 V, and a jump-start or load dump can go over that. The LM2596 is rated to 40 V.
3. **TVS clamp margin (R6).** The SMBJ24A clamps at about 39 V at full surge current, just under the LM2596's 40 V limit. The fuse (R5) must be upstream of the TVS, so a sustained overvoltage blows the fuse rather than the converter.
4. **ESP32 variant (R1).** Any WROOM-32 / 32D / 32E board works. Avoid **ESP32-C3** and **ESP32-S2** boards unless you check TWAI support and pin mapping. If you choose an **ESP32-S3**, `platformio.ini` needs a different `board`.
5. **OBD pigtail (R3).** Check the listing photo or ask the seller if **all 16 pins** are wired. Some cheap cables wire only the ELM327 pins. You need 4, 5, 6, 14 and 16. Test each wire with a multimeter before connecting it to the car.
6. **microSD card (R10).** Use 32 GB or smaller. The ESP32 SD library expects FAT32, and 64 GB+ cards ship as exFAT. In a hot parked car, a **High Endurance** card lasts longer.
7. **Tools not included:** soldering iron, multimeter, USB data cable (if the board ships without one).
