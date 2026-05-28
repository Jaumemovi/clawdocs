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

## Registre d'execució setmanal (obligatori)

Cada vegada que tanqui un **bloc de treball** (qualsevol unitat amb un
inici i un final clars: report enviat, proposta enviada, acció executada,
diagnòstic tancat, infra dropejada, etc.), apunto **una fila** a la
pestanya `Execució setmanal` del sheet **General**
(`1NXct3wMopbaPeSzLDVRehjf91hzLRhGPC6RG_yVvV6Q`).

Columnes (en ordre exacte):

1. **Data** — `YYYY-MM-DD` del tancament del bloc.
2. **Setmana ISO** — format `YYYY-Www` (p. ex. `2026-W22`).
3. **Client / àmbit** — `Monlau Motorsport` per defecte en aquesta sessió;
   `clawdocs-infra` si és feina transversal.
4. **Sessió (branca/canal)** — nom de la branca git activa
   (p. ex. `claude/wizardly-davinci-eDeKB`) o canal d'origen.
5. **Què s'ha fet** — frase curta i factual del bloc tancat.
6. **Pendent / proper pas** — què queda obert (o `—` si està del tot tancat).
7. **Estat** — `Fet` · `Parcial` · `Bloquejat` · `Esperant client`.
8. **Hores aprox.** — estimació en hores (p. ex. `0.5`, `1.5`).
9. **Notes** — referències útils (ID draft Gmail, commit hash, link Excel,
   norma aplicada, etc.).

Snippet:

```python
import gspread
gc = gspread.service_account(filename="/root/.secrets/claude-cloud-sa.json")
sh = gc.open_by_key("1NXct3wMopbaPeSzLDVRehjf91hzLRhGPC6RG_yVvV6Q")
ws = sh.worksheet("Execució setmanal")
ws.append_row([
    "YYYY-MM-DD","YYYY-Www","Monlau Motorsport","<branca>",
    "<què s'ha fet>","<pendent>","Fet","0.5","<notes>"
], value_input_option="USER_ENTERED")
```

**Regla operativa**: el registre es fa **al moment de tancar el bloc**, no
al final del dia ni de la setmana. Si dubto si una cosa compta com a bloc,
l'apunto (millor sobre-registrar que perdre traça).
