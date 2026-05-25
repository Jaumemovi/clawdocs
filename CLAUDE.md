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

Aquesta sessió desenvolupa sobre `claude/cool-hopper-YjVtf`. No canviar de
branca sense permís explícit.
