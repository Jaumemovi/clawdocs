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

## Registre d'execució setmanal (obligatori)

Cada cop que es tanqui un bloc de treball (resposta a un mail, auditoria,
lectura, implementació, gestió amb proveïdor, etc.), afegir una fila a la
pestanya `Execució setmanal` del sheet **General**
(`1NXct3wMopbaPeSzLDVRehjf91hzLRhGPC6RG_yVvV6Q`). Una fila per bloc.

**Columnes** (capçalera fixa):

1. `Data` — `YYYY-MM-DD` del dia que es tanca el bloc.
2. `Setmana ISO` — `YYYY-Www` (p. ex. `2026-W22`).
3. `Client / àmbit` — `Farmacia Marimon` (o subàmbit si cal: `Farmacia Marimon / MC`, `Farmacia Marimon / Boardfy`, etc.).
4. `Sessió (branca/canal)` — `claude/gallant-albattani-RJ9ky` (branca d'aquesta sessió) o el canal WhatsApp si l'origen ha estat allà.
5. `Què s'ha fet` — frase concreta i verificable del que s'ha tancat.
6. `Pendent / proper pas` — què queda obert i qui ho bloqueja (Juan, Boardfy, Girofeeds, etc.).
7. `Estat` — `Fet` | `En curs` | `Bloquejat` | `Cancel·lat`.
8. `Hores aprox.` — decimal (p. ex. `0.5`, `1.25`). Estimar a la baixa si dubte.
9. `Notes` — context addicional, IDs d'acció relacionats (`A001`, `A009`), referències a `Lectures`, etc.

**Snippet a executar al tancar bloc:**

```python
import gspread, datetime
gc = gspread.service_account(filename="/root/.secrets/claude-cloud-sa.json")
gen = gc.open_by_key("1NXct3wMopbaPeSzLDVRehjf91hzLRhGPC6RG_yVvV6Q")
ws = gen.worksheet("Execució setmanal")
today = datetime.date.today()
iso_year, iso_week, _ = today.isocalendar()
ws.append_row([
    today.isoformat(),
    f"{iso_year}-W{iso_week:02d}",
    "Farmacia Marimon",
    "claude/gallant-albattani-RJ9ky",
    "<què s'ha fet>",
    "<pendent / proper pas>",
    "Fet",                # o En curs / Bloquejat / Cancel·lat
    0.5,                  # hores aprox.
    "<notes>",
], value_input_option="USER_ENTERED")
```

**Regla d'aplicació:** registrar **abans** d'anunciar al xat que un bloc
està tancat. Si oblido fer-ho, el bloc no compta com a tancat fins que
quedi reflectit a `Execució setmanal`.
