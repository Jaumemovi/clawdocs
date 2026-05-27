# Sessió Claude Code — Farmacia Marimon

Sessió dedicada a **Farmacia Marimon**. Vinculada al sheet de seguiment
corresponent (no al General).

## Sheet vinculat

- **Title**: `Marimon_GoogleAds_Seguiment`
- **ID**: `1vjuWAL3E6WvZPiXcz_sDRjQV2KjEPlMT17okV94JJCQ`
- **URL**: https://docs.google.com/spreadsheets/d/1vjuWAL3E6WvZPiXcz_sDRjQV2KjEPlMT17okV94JJCQ/edit
- **Accés**: Service Account
  `claude-cloud@clawdocs-492614.iam.gserviceaccount.com`.

## Context

- **Ús principal**: Canal Girofeeds-FarmaciaMarimon
- **Agents actius**: Client Manager; Tracking/Ads Manager; Reporting Manager
- **Cadència reporting**: Setmanal divendres
- **Notes**: Farmacia Marimón

## Regla d'anotació

Quan Jaume diu **"anota X"** / **"apunta X"** / **"registra X"** en aquest
xat, escriu al sheet vinculat (no al General):

```python
import gspread
gc = gspread.service_account(filename="/root/.secrets/claude-cloud-sa.json")
sh = gc.open_by_key("1vjuWAL3E6WvZPiXcz_sDRjQV2KjEPlMT17okV94JJCQ")
ws = sh.worksheet("<pestanya>")
ws.append_row([...], value_input_option="USER_ENTERED")
```

Llegeix sempre la capçalera (`ws.row_values(1)`) abans d'escriure. Si tens
dubtes sobre la pestanya, pregunta.

## Coordinació

Aquesta sessió està registrada a la pestanya `Sessions actives` del sheet
**General** (`1NXct3wMopbaPeSzLDVRehjf91hzLRhGPC6RG_yVvV6Q`). El xat
coordinador de clawdocs hi té visibilitat.
