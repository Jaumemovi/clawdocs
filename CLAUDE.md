# Clawdocs — instruccions de sessió

Aquest repo és el xat de **coordinació** de les sessions Claude Code que treballen
sobre `Jaumemovi/clawdocs`. Està vinculat al sheet mestre **General**.

## Sheet General

- **Title**: `General`
- **ID**: `1NXct3wMopbaPeSzLDVRehjf91hzLRhGPC6RG_yVvV6Q`
- **URL**: https://docs.google.com/spreadsheets/d/1NXct3wMopbaPeSzLDVRehjf91hzLRhGPC6RG_yVvV6Q/edit
- **Accés**: Service Account `claude-cloud@clawdocs-492614.iam.gserviceaccount.com`
  (credencials a `$GOOGLE_APPLICATION_CREDENTIALS`, materialitzades pel hook
  `.claude/hooks/session-start.sh`).

Pestanyes rellevants (consulta abans d'escriure si no recordes l'estructura):
`Canals`, `Agents`, `Mapa JID Sheets`, `Accions`, `Resum converses`,
`Configuració`, `Connexions API Claude`, `Normes i docs`,
`Planificació setmanal`.

## Regla d'anotació

Quan Jaume diu **"anota X"**, **"apunta X"**, **"registra X"** o equivalent en
aquest xat:

1. Decideix la pestanya més apropiada del sheet General:
   - Tasca o tema obert → `Accions`
   - Resum o decisió de conversa → `Resum converses`
   - Nou canal/xat → `Canals`
   - Norma operativa → `Normes i docs`
   - Si tens dubtes, pregunta abans d'escriure.
2. Llegeix la capçalera de la pestanya (`worksheet.row_values(1)`) per omplir
   les columnes correctes.
3. Append amb `gspread` usant la Service Account ja carregada:

   ```python
   import gspread
   gc = gspread.service_account(filename="/root/.secrets/claude-cloud-sa.json")
   sh = gc.open_by_key("1NXct3wMopbaPeSzLDVRehjf91hzLRhGPC6RG_yVvV6Q")
   ws = sh.worksheet("<tab>")
   ws.append_row([...], value_input_option="USER_ENTERED")
   ```
4. Confirma a Jaume amb la pestanya i resum del que s'ha escrit.

## Registre d'aquest xat

Aquest xat està registrat a la pestanya `Canals` del sheet General com:
- Nom: `Clawdocs coord`
- Tipus: `claude-code`
- Display OpenClaw: `claude-code:repo:Jaumemovi/clawdocs`
- Alias curt: `Clawdocs`

## Accés a Google Ads, GA4 i Merchant Center

El hook `session-start.sh` instal·la les llibreries i deixa disponibles tres
helpers reutilitzables:

- **`.claude/helpers/ads.py`** — Google Ads via OAuth + MCC. Llegeix
  credencials de les env vars `GOOGLE_ADS_*`. Funcions: `get_client()`,
  `pull_campaigns(client, customer_id, start, end)`,
  `pull_conversion_actions(client, customer_id)`,
  `list_accessible_customers(client)`.

- **`.claude/helpers/ga4.py`** — GA4 Data API via Service Account. El SA ha
  d'estar afegit com a Viewer/Editor a cada propietat. Funcions:
  `pull_purchases(property_id, start, end)`,
  `pull_purchases_by_ad_campaign(property_id, start, end)`.

- **`.claude/helpers/merchant.py`** — Merchant Center Content API v2.1 via
  Service Account. El SA ha d'estar afegit com a Admin al MCA Moviéndote
  (254198292) per accedir a tots els subcomptes. Funcions: `get_service()`,
  `list_subaccounts(svc, mca_id)`, `pull_account_status(svc, merchant_id)`,
  `pull_product_statuses(svc, merchant_id, only_with_issues=True)`,
  `pull_disapproved_products(svc, merchant_id)`,
  `pull_products(svc, merchant_id, max_results=250)`.

Per a cada client cal apuntar a `Canals` (o a una columna nova/sheet del
client):
- `Google Ads Customer ID` (format `123-456-7890` o sense guions)
- `GA4 Property ID` (9 dígits)
- `Merchant Center ID` (9 dígits) — només si té ecommerce

Subcomptes Merchant Center actuals (sota MCA Moviéndote 254198292):
Lacoop (102897588), Farmacia Marimon (183443137), MarimonTcuida (159030506),
Pozas (411164737).

Exemple d'ús des d'una sessió:

```python
import sys; sys.path.append("/home/user/clawdocs/.claude/helpers")
from ads import get_client, pull_campaigns
from ga4 import pull_purchases_by_ad_campaign
from merchant import get_service, pull_disapproved_products

ads = get_client()
ads_rows = pull_campaigns(ads, "3823744676", "2026-05-15", "2026-05-22")
ga4_rows = pull_purchases_by_ad_campaign("PROPERTY_ID", "2026-05-15", "2026-05-22")
mc = get_service()
disapproved = pull_disapproved_products(mc, "411164737")  # Pozas
```

## Branca de treball

La branca de treball per defecte ve indicada en el system prompt de la sessió
(camp "Git Development Branch Requirements"). No canviar de branca sense
permís explícit.

## Registre d'execució setmanal (obligatori)

Cada cop que es tanqui un **bloc de treball** (fi d'una franja del planning,
fi d'una tasca rellevant, o fi de sessió Claude Code) cal anotar una fila a
la pestanya **`Execució setmanal`** del sheet **General**
(`1NXct3wMopbaPeSzLDVRehjf91hzLRhGPC6RG_yVvV6Q`). No és opcional.

### Columnes (capçalera ja existent — respectar ordre)

| Columna | Contingut |
|---|---|
| `Data` | Format `YYYY-MM-DD` |
| `Setmana ISO` | Format `2026-W22` (calcular amb `datetime.date.isocalendar()`) |
| `Client / àmbit` | Client (Lacoop, Pozas, Marimon...) o àmbit (Infra, Personal, Renda, Girofeeds intern...) |
| `Sessió (branca/canal)` | Nom de la branca git actual o canal d'origen (ex: `claude/cool-hopper-YjVtf` o `Clawdocs coord`) |
| `Què s'ha fet` | Resum factual concret del bloc (1-3 línies, sense floritura) |
| `Pendent / proper pas` | Què queda obert després d'aquest bloc |
| `Estat` | `Fet` / `Parcial` / `Bloquejat` / `Pausa` |
| `Hores aprox.` | Decimal, ex: `0.75`, `1.5` |
| `Notes` | Observacions opcionals (problemes, decisions, riscos) |

### Codi d'anotació

```python
import gspread
from datetime import datetime
from zoneinfo import ZoneInfo

gc = gspread.service_account(filename="/root/.secrets/claude-cloud-sa.json")
sh = gc.open_by_key("1NXct3wMopbaPeSzLDVRehjf91hzLRhGPC6RG_yVvV6Q")
ws = sh.worksheet("Execució setmanal")

# OBLIGATORI: usar timezone Europe/Madrid explícit.
# El contenidor de Claude Code on the web corre en UTC; entre 00:00-02:00 CEST
# (00:00-01:00 CET) datetime.date.today() retornaria el dia anterior i les
# anotacions quedarien amb data incorrecta. Mai usar date.today() naïf.
avui = datetime.now(ZoneInfo("Europe/Madrid")).date()
iso_year, iso_week, _ = avui.isocalendar()
setmana_iso = f"{iso_year}-W{iso_week:02d}"

ws.append_row([
    avui.isoformat(),
    setmana_iso,
    "<Client o àmbit>",
    "<branca git o canal>",
    "<Què s'ha fet>",
    "<Pendent / proper pas>",
    "<Fet|Parcial|Bloquejat|Pausa>",
    "<hores aprox>",
    "<notes opcionals>",
], value_input_option="USER_ENTERED")
```

### Quan anotar

- **Final de cada franja del planning** (Pozas 10:00-11:00 → fi franja → anotar)
- **Final d'una tasca puntual rellevant** que no estava al planning fix (resposta a un mail urgent, gestió d'una incidència)
- **Final de sessió Claude Code** (abans de tancar)
- **Pausa llarga inesperada** (interrupció >1h) → anotar com a `Parcial` o `Pausa`

### Què NO cal anotar

- Bloc de menys de 15 minuts sense impacte (revisar un mail, etc.)
- Activitats personals fora de la franja de feina (gym, escola, dinar)
- Tasques merament administratives mecàniques (renovar contrasenya, etc.)

## Bootstrap de sessió

Aquest repo serveix també com a base per a sessions Claude Code dedicades a
un àmbit concret (client extern o canal intern). Cada sessió viu en la seva
pròpia branca i queda **vinculada al sheet de l'àmbit** (no al General) per
a totes les anotacions.

### Frase disparadora

Quan Jaume escriu en una sessió nova:

> **"Bootstrap aquesta sessió per a `<ALIAS>`."**

…la sessió ha d'executar el procediment següent **sense més preguntes** (si
l'alias existeix a `Canals` i té `Sheet ID`):

### Procediment

1. Assegura't que el hook `.claude/hooks/session-start.sh` ja ha exportat
   `GOOGLE_APPLICATION_CREDENTIALS`. Si no, executa'l manualment.
2. Llegeix la fila del client a la pestanya `Canals` del sheet General
   buscant per `Alias curt` (case-insensitive):

   ```python
   import gspread
   gc = gspread.service_account(filename="/root/.secrets/claude-cloud-sa.json")
   gen = gc.open_by_key("1NXct3wMopbaPeSzLDVRehjf91hzLRhGPC6RG_yVvV6Q")
   canals = gen.worksheet("Canals")
   rows = canals.get_all_records()
   row = next((r for r in rows if r["Alias curt"].strip().lower() == "<alias>".lower()), None)
   ```

   Si `row is None` → atura't i demana a Jaume que primer registri l'àmbit
   (no inventis fila).
3. Extreu: `Sheet seguiment` (nom), `Sheet ID`, `Agents actius`,
   `Ús principal`, `Cadència`, `Notes agents`.

   **Si `Sheet ID` està buit o és `pendent crear`** → atura't i pregunta a
   Jaume:
   > "L'alias `<ALIAS>` no té sheet associat a `Canals`. Vols:
   > (a) crear-ne un nou (digues nom i quina plantilla: client setmanal,
   > seguiment personal, etc.),
   > (b) vincular provisionalment al General, o
   > (c) cancel·lar el bootstrap?"

   Segons la resposta: crea el sheet (compartint-lo amb el SA), actualitza
   la fila de `Canals` amb el nou `Sheet seguiment`/`Sheet ID`, i continua.
4. **Sobreescriu** el `CLAUDE.md` d'aquesta branca amb la plantilla de
   sessió d'àmbit (veure sota), substituint la regla d'anotació perquè
   apunti al sheet de l'àmbit en comptes del General.
5. Registra la sessió a la pestanya `Sessions actives` del sheet General:

   ```python
   sessions = gen.worksheet("Sessions actives")
   sessions.append_row([
       "<YYYY-MM-DD>",          # Data obertura
       "<ALIAS>",               # Client alias (o àmbit intern)
       "Jaumemovi/clawdocs",    # Repo
       "<branca actual>",       # Branca (de git branch --show-current)
       "<Sheet seguiment>",     # Sheet vinculat
       "<Sheet ID>",            # Sheet ID
       "actiu",                 # Estat
       "<YYYY-MM-DD>",          # Última activitat
       "Bootstrap automàtic via CLAUDE.md de clawdocs.",
   ], value_input_option="USER_ENTERED")
   ```
6. Commit + push del nou `CLAUDE.md` a la branca actual.
7. Confirma a Jaume: "Sessió vinculada al sheet **\<Sheet seguiment\>**
   per a **\<ALIAS\>**. A partir d'ara *anota X* va aquí."

### Plantilla de CLAUDE.md per a sessió d'àmbit

```markdown
# Sessió Claude Code — <ALIAS>

Sessió dedicada a **<ALIAS>**. Vinculada al sheet de seguiment
corresponent (no al General).

## Sheet vinculat

- **Title**: `<Sheet seguiment>`
- **ID**: `<Sheet ID>`
- **URL**: https://docs.google.com/spreadsheets/d/<Sheet ID>/edit
- **Accés**: Service Account
  `claude-cloud@clawdocs-492614.iam.gserviceaccount.com`.

## Context

- **Ús principal**: <Ús principal>
- **Agents actius**: <Agents actius>
- **Cadència reporting**: <Cadència>
- **Notes**: <Notes agents>

## Regla d'anotació

Quan Jaume diu **"anota X"** / **"apunta X"** / **"registra X"** en aquest
xat, escriu al sheet vinculat (no al General):

```python
import gspread
gc = gspread.service_account(filename="/root/.secrets/claude-cloud-sa.json")
sh = gc.open_by_key("<Sheet ID>")
ws = sh.worksheet("<pestanya>")
ws.append_row([...], value_input_option="USER_ENTERED")
```

Llegeix sempre la capçalera (`ws.row_values(1)`) abans d'escriure. Si tens
dubtes sobre la pestanya, pregunta.

## Coordinació

Aquesta sessió està registrada a la pestanya `Sessions actives` del sheet
**General** (`1NXct3wMopbaPeSzLDVRehjf91hzLRhGPC6RG_yVvV6Q`). El xat
coordinador de clawdocs hi té visibilitat.
```

### Si l'alias no existeix

Diu a Jaume: "L'alias `<ALIAS>` no està a `Canals` del sheet General. Vols
que el creï? Em cal: nom complet, tipus (client/intern), sheet de seguiment
(ID o crear nou), agents actius i cadència de reporting."
