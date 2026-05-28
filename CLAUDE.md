# Sessió Claude Code — Monlau (Motul)

Sessió dedicada a **Monlau / Motul**. Vinculada al sheet de seguiment de
campanyes de Monlau (no al General).

## Sheet vinculat

- **Title**: `Monlau - Seguiment campanyes`
- **ID**: `1sINrqGGYRgOdhkcNm8wkbcg1ZOih65VDCPq2we36308`
- **URL**: https://docs.google.com/spreadsheets/d/1sINrqGGYRgOdhkcNm8wkbcg1ZOih65VDCPq2we36308/edit
- **Accés**: Service Account
  `claude-cloud@clawdocs-492614.iam.gserviceaccount.com`.

## Context

- **Ús principal**: Canal client Monlau/Motul (grup WhatsApp
  `Girofeeds-MonlauMotul`, JID `120363427339174982@g.us`).
- **Agents actius**: Client Manager; Tracking/Ads Manager; SEO Manager;
  Reporting Manager.
- **Cadència reporting**: Setmanal divendres — borrador email amb 3 punts
  d'accions fetes + proper pas.
- **Notes**: Client-facing en castellà si va al client.

## Regla d'anotació

Quan Jaume diu **"anota X"** / **"apunta X"** / **"registra X"** en aquest
xat, escriu al sheet vinculat (no al General):

```python
import gspread
gc = gspread.service_account(filename="/root/.secrets/claude-cloud-sa.json")
sh = gc.open_by_key("1sINrqGGYRgOdhkcNm8wkbcg1ZOih65VDCPq2we36308")
ws = sh.worksheet("<pestanya>")
ws.append_row([...], value_input_option="USER_ENTERED")
```

Llegeix sempre la capçalera (`ws.row_values(1)`) abans d'escriure. Si tens
dubtes sobre la pestanya, pregunta.

## Norma N013 — Propostes només amb eines ja connectades

Quan proposi accions per a Monlau, **només** es poden incloure accions
executables amb les APIs/eines ja connectades a clawdocs:

- Sheets, Gmail, Calendar, Google Ads, GA4, Merchant Center, Drive.

Si una proposta requereix infraestructura nova (nova API, nou helper, nou
parser), **NO** entra al cicle setmanal: va al `Parking d'idees Forta-infra`
(pestanya `Idees futures` del sheet General, veure N014) i s'hi queda fins
que la infra estigui llesta.

Aquesta regla trenca el patró "cada acció client genera infra-task" (vist a
l'avaluació del 27/05: backlog 67% infra vs 7% client).

## Coordinació

Aquesta sessió està registrada a la pestanya `Sessions actives` del sheet
**General** (`1NXct3wMopbaPeSzLDVRehjf91hzLRhGPC6RG_yVvV6Q`). El xat
coordinador de clawdocs hi té visibilitat.
