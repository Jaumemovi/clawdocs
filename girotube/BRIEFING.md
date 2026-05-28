# Briefing per a claw — bug del sync de Girotube a YouTube

**Repo on tens els recursos:** `jaumemovi/clawdocs`, branca `claude/charming-fermi-I5Zw7`.
**Sheet:** `1p_VAArPDYneFkDFk8qsyhz7-LXXUnvagPJRp6zoxrj4`.
**Codi del cron:** viu a `~/.openclaw/workspace/` a la teva màquina.

## El bug en una frase

Des del 2026-05-23, després d'un `invalid_grant` el 2026-05-21 que va obligar a reautoritzar l'OAuth, el sync `approved_only_sync` escriu a playlists d'un compte de YouTube **diferent** del d'@calnene: les `PLzPacBemLhu…` en comptes de les canòniques `PLcc3M6PJoP7…` que apareixen a la pestanya `Playlists` del Sheet.

**Causa arrel:** el codi té els IDs de playlist hardcoded i no valida la identitat OAuth abans d'escriure.

**Evidència** (mira la pestanya `Videos` del Sheet):
- Fins 2026-05-20: entrades amb `Playlist ID` que comença per `PLcc…` ✓
- A partir de 2026-05-23 (primera execució de `approved_only_sync`): entrades amb `Playlist ID` que comença per `PLzPacBemLhu…` ✗
- 59 escriptures al lloc equivocat. Detall a `recovery/recovery_list.json`.

## Pla d'acció (en aquest ordre exacte)

### Pas 0 — Atura el cron abans de fer res

No tornis a deixar-lo programat fins que tinguis verificats els passos 1–5. Si el cron està a `crontab`, comenta la línia; si està a systemd, `systemctl stop <unit>`. Confirma-ho al teu usuari abans de continuar.

### Pas 1 — Porta els helpers a `~/.openclaw/workspace/`

Copia aquests dos fitxers des de `jaumemovi/clawdocs@claude/charming-fermi-I5Zw7`:

- `girotube/sheet_resolver.py` → `~/.openclaw/workspace/sheet_resolver.py`
- `girotube/recover_missynced.py` → `~/.openclaw/workspace/recover_missynced.py`

`sheet_resolver.py` exposa:
- `load_canonical_playlists()` → `{nom_playlist: playlist_id}` llegint la pestanya `Playlists`. **Aquesta serà la nova font única de veritat.**
- `load_config()` → `{clau: valor}` de la pestanya `Config`.
- `assert_youtube_owner(youtube, expected_channel_id)` → fa `channels().list(mine=True)` i llança `WrongYoutubeAccountError` si l'OAuth pertany a un altre canal.

### Pas 2 — Modifica el codi del sync

Localitza el script que executa `approved_only_sync` (i el cron llegat `youtube_extend_5h_each.py`). Aplica aquests canvis:

1. **Elimina qualsevol diccionari hardcoded amb IDs `PLzPacBemLhu…`.** Substitueix per:
   ```python
   from sheet_resolver import load_canonical_playlists, load_config, assert_youtube_owner
   playlists = load_canonical_playlists()
   ```

2. **Just després de construir el client YouTube**, afegeix la guarda d'identitat:
   ```python
   youtube = build("youtube", "v3", credentials=creds)
   cfg = load_config()
   expected_owner = cfg.get("youtube_owner_channel_id")
   if not expected_owner:
       raise RuntimeError("Config!youtube_owner_channel_id no configurat — refuso escriure")
   assert_youtube_owner(youtube, expected_owner)  # llança WrongYoutubeAccountError si no quadra
   ```

3. **Quan resolguis el target d'un candidat:**
   ```python
   target_id = playlists.get(candidate["Playlist"])
   if not target_id:
       log.warning("no playlist_id for %s, skipping", candidate["Playlist"])
       continue
   ```

4. Assegura't que **cap altre punt del codi** escriu a YouTube sense passar per aquesta guarda. Cerca `playlistItems().insert`, `playlistItems().delete`, `playlists().update`.

### Pas 3 — Configura la guarda al Sheet

Necessites el channel ID (UC...) d'@calnene. El més ràpid:

```bash
# amb l'OAuth d'@calnene activa
python -c "from googleapiclient.discovery import build; from youtube_api import load_credentials; \
  y=build('youtube','v3',credentials=load_credentials(interactive=False)); \
  print(y.channels().list(part='id,snippet',mine=True).execute()['items'][0])"
```

Després afegeix una fila a la pestanya `Config` del Sheet:

| Clau | Valor | Notes |
|---|---|---|
| `youtube_owner_channel_id` | `UC...` (el d'@calnene) | Compte propietari de les playlists PLcc...; el sync abortarà si l'OAuth no coincideix |

### Pas 4 — Reautoritza OAuth amb @calnene

L'OAuth actual pertany a un compte que NO és @calnene. Esborra el `token.json` (o el refresh-token persistent que usi el cron) i refés el flow d'autorització iniciant sessió amb @calnene. Després d'això:

```bash
# verifica
python -c "from sheet_resolver import load_config, assert_youtube_owner; \
  from googleapiclient.discovery import build; from youtube_api import load_credentials; \
  y=build('youtube','v3',credentials=load_credentials(interactive=False)); \
  print('owner:', assert_youtube_owner(y, load_config()['youtube_owner_channel_id']))"
```

Hauria d'imprimir l'UC d'@calnene sense excepcions.

### Pas 5 — Recupera els vídeos perduts

Descarrega `recovery/recovery_list.json` del repo `clawdocs` a una ruta local. Llavors:

```bash
cd ~/.openclaw/workspace
python recover_missynced.py /ruta/a/recovery_list.json --dry-run             # verificació
python recover_missynced.py /ruta/a/recovery_list.json --skip-news           # recupera els 23 familiars
```

L'script refusa córrer si la guarda OAuth no passa, així que és segur.

**Per què `--skip-news`:** dels 59 ítems, 36 són `replaced_today` de la playlist Notícies (notícies caducades, el cron les esborra cada dia). Recuperar-les no aporta res. Els 23 restants (Viatges 13, Cuina 7, Fabricando 2, Emma 1) sí que volem que tornin a la playlist familiar.

### Pas 6 — Dry run del cron sencer

Abans de tornar a programar res:

1. Executa el sync amb una variable d'entorn tipus `GIROTUBE_DRYRUN=1` (o afegeix la flag si no existeix) i mira els logs.
2. Comprova: (a) `assert_youtube_owner` passa, (b) cada `target_id` que el codi vol tocar comença per `PLcc`, mai per `PLzPacBemLhu`, (c) els 5 IDs canon esperats apareixen al log.
3. Si tot quadra, reactiva el cron (`crontab -e` o `systemctl start`).

### Pas 7 — Decideix què fer amb les `PLzPacBemLhu…`

Tres opcions, parla-ho amb el Jaume:

- **A.** Deixar-les òrfenes al compte equivocat. Cost zero, però queden brutícia.
- **B.** Si el compte equivocat també és teu, esborrar les playlists des de la UI de YouTube.
- **C.** Deixar-les com a backup temporal i decidir d'aquí una setmana.

## Comprovacions finals

- [ ] Pas 0: cron aturat
- [ ] Pas 1: helpers copiats
- [ ] Pas 2: codi modificat, hardcoded eliminats
- [ ] Pas 3: `youtube_owner_channel_id` al Config
- [ ] Pas 4: OAuth reautoritzada amb @calnene, guarda passa
- [ ] Pas 5: 23 vídeos recuperats (mira el log final de `recover_missynced.py`)
- [ ] Pas 6: dry-run del cron net
- [ ] Pas 7: decisió sobre les `PLzPacBemLhu…`
- [ ] Cron reactivat
- [ ] Una execució real del cron post-fix verifica que escriu a `PLcc…`

Si tens dubtes a qualsevol pas, atura't i pregunta al Jaume abans de continuar.

---

## Post-mortem — 2026-05-26

Incident resolt seguint el pla. Resum executiu del que va passar i com va quedar:

### Línia temporal

- **2026-05-20 i abans:** cron legat `youtube_extend_5h_each.py` escrivint correctament a les playlists `PLcc...` d'@calnene.
- **2026-05-21 10:05:** OAuth `invalid_grant: Token has been expired or revoked`.
- **2026-05-21–22:** reautorització que va seleccionar per defecte el canal personal de l'usuari (NO @calnene).
- **2026-05-23 23:00:** primera execució de `approved_only_sync` amb el nou token. Crea i alimenta playlists `PLzPacBemLhu...` al canal equivocat, sense que cap guarda detectés el desviament.
- **2026-05-26:** Jaume detecta la divergència mirant el Sheet. 59 escriptures al lloc equivocat (36 Notícies + 13 Viatges + 7 Cuina + 2 Fabricando + 1 Emma).

### Causa arrel

Doble:
1. Els IDs de playlist estaven hardcoded al codi del sync, no es llegien del Sheet.
2. Cap pas del codi validava que l'OAuth pertanyés al canal esperat abans d'escriure.

### Fix aplicat

- `girotube/sheet_resolver.py` integrat al workspace de claw: `load_canonical_playlists()` llegeix la pestanya `Playlists`, `assert_youtube_owner()` aborta si `channels.list(mine=True).id != UCR-IFJOi-plA9i2Nn2lL1lw`.
- Eliminats tots els IDs `PLzPacBemLhu...` hardcoded al codi i config (només queden a logs històrics i comentaris del script de recovery).
- `Config!youtube_owner_channel_id = UCR-IFJOi-plA9i2Nn2lL1lw` afegit com a guarda al Sheet.
- Bonus: throttling a `search.list` al cron legat per evitar 429 per límit de 10 cerques/min.

### Recuperació

`girotube/recover_missynced.py --skip-news` va recuperar **23/23 vídeos familiars** a les `PLcc...` correctes (6 added + 17 already_present d'un primer llançament que no va imprimir sortida visible). Les 36 entrades de Notícies es van descartar perquè eren `replaced_today` (notícies caducades).

### Estat final

- Crons reactivats:
  - `Girotube - 10 vídeos bons diaris` a les 09:20 Europe/Madrid.
  - `Girotube - actualitzar Notícies avui` a les 09:45 i 19:45 Europe/Madrid.
- 5 playlists actives al cron principal: Viatges, Cuina, Fabricando, Emma, Arquitectura — totes amb ID canònic.
- Playlist Ciència fora del cron fins que tingui playlist ID al Sheet.
- Playlists `PLzPacBemLhu...` (5) deixades òrfenes al canal equivocat. **Revisió per esborrar-les: 2026-06-04.**

### Per blindar-ho a futur

- L'assert d'identitat OAuth és la guarda definitiva: encara que un altre cop l'OAuth es reautoritzi malament, el codi avortarà amb un error clar enlloc d'escriure al lloc equivocat.
- El Sheet és ara la font única de veritat de playlist IDs. Per afegir o moure una playlist, només cal editar el Sheet — no cal tocar codi.
- Vigilar la primera execució post-fix (2026-05-27 09:20): si la pestanya `Videos` registra entrades amb `Playlist ID` començant per `PLcc`, tot OK.

