# Sessió Claude Code — Maxirent

Sessió dedicada a **Maxirent** (client estacional maig-setembre · rent-a-car,
lloguer motos i lockers a Ibiza). Vinculada al sheet de seguiment propi
(no al General).

## Sheet vinculat

- **Title**: `Maxirent - Seguimiento`
- **ID**: `1Np77IX5xzFDWlK7EC99a_8unppmYLia4XD_ajFH1fJg`
- **URL**: https://docs.google.com/spreadsheets/d/1Np77IX5xzFDWlK7EC99a_8unppmYLia4XD_ajFH1fJg/edit
- **Accés**: Service Account
  `claude-cloud@clawdocs-492614.iam.gserviceaccount.com` (Editor).

Pestanyes:
`00 Setup` · `01 Setmanes` · `02 Accions` · `03 Lectures` · `G Google Ads` ·
`04 Emails` · `99 Converses`.

## Context

- **Ús principal**: Canal client Maxirent (estacional maig-set). Gestió
  Google Ads dels tres dominis: `maxirentibiza.com`, `alquilermotosibiza.com`,
  Ibiza Consigna (lockers).
- **Agents actius**: Client Manager · Tracking/Ads Manager · Reporting Manager.
- **Cadència reporting**: Borrador email setmanal divendres, castellà, 3
  punts. Destinatari: `info@maxirentibiza.com` (Antonia).
- **Notes**: Client estacional. Fora de temporada → pausat (temps va a
  Girofeeds intern o buffer).

## Comptes connectats

- **Google Ads Customer ID**: `136-362-1768` (normalitzat: `1363621768`).
  Accés via helper `/home/user/clawdocs/.claude/helpers/ads.py`.
  ⚠️ **Important**: per evitar SSL handshake fails cal exportar
  `GRPC_DEFAULT_SSL_ROOTS_FILE_PATH=/etc/ssl/certs/ca-certificates.crt`
  abans de cada crida (o al hook session-start).
- **GA4 Property IDs**: PENDENT (cal demanar a Antonia per als 2 dominis i
  afegir SA com a Viewer a cada propietat).

### Estat tracking (snapshot 2026-05-28)

| Item | Estat |
|---|---|
| `Compra` (WEBPAGE 6803860970) | ENABLED · primary · included_in_conv ✅ |
| GA4 import purchase alquilermotosibiza (7210964536) | HIDDEN · ❌ |
| GA4 import purchase maxirentibiza (7210966474) | HIDDEN · ❌ |
| GA4 imports secundaris (reservas, presupuesto, contacto…) | HIDDEN · ❌ |
| Local actions (visits, directions, calls) | ENABLED · no inclosos a conv ✅ |

**Conseqüència**: 30d=210,99€ / 0 conv. Veure `02 Accions` MAX-A001.

## Regla d'anotació

Quan Jaume diu **"anota X"** / **"apunta X"** / **"registra X"** en aquest
xat, escriu al sheet **Maxirent - Seguimiento** (no al General):

```python
import gspread
gc = gspread.service_account(filename="/root/.secrets/claude-cloud-sa.json")
sh = gc.open_by_key("1Np77IX5xzFDWlK7EC99a_8unppmYLia4XD_ajFH1fJg")
ws = sh.worksheet("<pestanya>")
ws.append_row([...], value_input_option="USER_ENTERED")
```

Llegeix sempre la capçalera (`ws.row_values(1)`) abans d'escriure. Tria
la pestanya segons la natura:

- Decisió / bloqueig / feedback operatiu → `99 Converses`
- Acció (proposta/implementada) → `02 Accions` (Estat: Proposat · Aprovat ·
  Implementat · En observació · Tancat · Revertit; ID `MAX-A###`)
- Snapshot mètric → `03 Lectures` (i `G Google Ads` si és detall per campanya)
- Resum setmanal → `01 Setmanes` (una fila per setmana, ID `YYYY-Www`)
- Email client (esborrany Gmail) → `04 Emails`

Si tens dubtes sobre la pestanya, pregunta.

## Normes operatives clau

- **N013** — Propostes només amb eines ja connectades (Sheets, Gmail,
  Calendar, Google Ads, GA4, Merchant Center, Drive). Si una proposta
  requereix infra nova → parking N014, NO al cicle setmanal.
- **N001** — Tot sheet/doc nou s'ha de compartir amb el SA com a Editor.

## Coordinació

- Branca de treball: la indicada al system prompt (no canviar sense permís).
- Sessió registrada a `Sessions actives` del sheet **General**
  (`1NXct3wMopbaPeSzLDVRehjf91hzLRhGPC6RG_yVvV6Q`).
- `Reports clients` del General té la fila de Maxirent amb destinatari,
  idioma, KPIs i link a aquest sheet.
- `Planificació setmanal` del General: Maxirent va als dijous 11:00-12:30 i
  reporting divendres.
