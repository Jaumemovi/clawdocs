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

## Branca de treball

La branca de treball per defecte ve indicada en el system prompt de la sessió
(camp "Git Development Branch Requirements"). No canviar de branca sense
permís explícit.

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
