# Fault-code descriptions

`analyze_scan.py` looks up the description for each fault code in this order:

1. **`dtc_local.csv`**, your own table. It is **git-ignored** and stays on your machine.
2. **Generic SAE J2012 descriptions** for standard P0xxx / P2xxx codes. These are public, so they can live in the repo.
3. Otherwise `unknown`. The code is still reported, with its module and status.

## Set up

```sh
cp tools/dtc/dtc_local.example.csv tools/dtc/dtc_local.csv
```

## Format

| Column | Meaning |
|---|---|
| `code` | Fault code as the reader reports it, e.g. `P2004`, or a module-specific code |
| `module` | Short module name: `ME` (engine), `TCU` (7G-Tronic), `ESP`, `SRS`, `EIS`, `SAM`, `IC`, ... |
| `description` | Text to show in the report |
| `source` | Where the text came from: `SAE J2012 generic`, `iCarsoft MB`, `WIS`, `own note`, ... |
| `first_seen` | Date the code first appeared on this car (YYYY-MM-DD), optional |
| `notes` | Your own notes: likely cause, fix done, part number |

## Rules

- **Never commit `dtc_local.csv`.** Text copied from WIS, Xentry or a commercial scanner is licensed, and this repo is public. `.gitignore` already excludes the file.
- `dtc_local.example.csv` holds **only generic codes in our own words**. Keep it that way.
- Phase 5 fills the table: during splitter sessions, write down the description the aftermarket scanner shows for each code.
