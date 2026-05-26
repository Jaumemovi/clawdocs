# CLAUDE.md — Clawdocs

Instruccions específiques per a sessions de Claude Code sobre aquest repo.

## Context

Aquest repo gestiona configuració per editar Google Sheets/Drive (i, des de
2026-05-26, Google Ads) via Service Account des de sessions de Claude Code
on the web. El hook `.claude/hooks/session-start.sh` materialitza credencials
i exporta `GRPC_DEFAULT_SSL_ROOTS_FILE_PATH` perquè gRPC accepti la CA del
proxy d'egress.

## Sheet de seguiment per client

Cada client té el seu propi Google Sheet amb pestanyes estandarditzades:
`Dashboard`, `Accions`, `Lectures`, `Costos SKU`, `Productes a revisar`,
`Configuració`, `Canvis`, `Reports clients`, `Converses`. Vegeu cada pestanya
per la seva capçalera concreta.

- **Accions**: master list de propostes/auditoria. Estat actual de cada item.
  No crear pestanyes setmanals (`Feines YYYY-MM-DD`): tot va aquí.
- **Canvis**: registre operacional de cada mutate fet (C001, C002, …). Una
  fila per canvi amb baseline + criteri de rollback.
- **Reports clients**: una fila per punt de report. Una columna per data.
  Sense subpestanyes per setmana.
- **Converses**: registre cronològic de sessions amb el client/equip.

## Protocols de sessió

### Inici de sessió

1. Verificar branca de treball segons instruccions (`claude/*`).
2. Confirmar accés: Sheets via SA, Google Ads via OAuth (sanitize env vars que
   poden venir amb `<...>` literals).
3. Llegir l'última fila de `Converses` del sheet del client per recuperar
   context i pendents.

### Durant la sessió

1. Cada mutate a Google Ads (campaign, budget, status, conversion goal, etc.)
   registrar-lo com a nova fila a `Canvis` amb un C-ID seqüencial (C001,
   C002, …) i criteri de rollback.
2. Si un mutate resol una P-acció existent a `Accions`, actualitzar la fila
   corresponent (camps Aprovat / Implementat / Estat / Notes amb referència
   al C-ID).
3. Si és una acció nova no llistada a P, afegir-la com a A-acció al final.

### Fi de sessió (obligatori)

Abans de tancar la sessió, afegir una fila a la pestanya `Converses` del
sheet del client amb:

- `Data`: avui
- `Canal`: "Claude Code (web session)" o similar
- `Client`: nom del client
- `Tema`: títol curt (què hem fet)
- `Resum conversa`: narrativa de la sessió (què s'ha discutit + descobert +
  decisions preses). Llegible per un humà que no hi era present.
- `Decisions`: llista numerada de decisions concretes preses durant la sessió.
- `Accions derivades`: pendents per al client (què ha de fer ell) +
  pendents tècnics per a la propera sessió Claude.
- `Responsable`: "Claude / Jaume" o similar
- `Estat`: "Fet"
- `Referència missatge / enllaç`: identificador de la sessió
- `Notes internes`: branca git, commits rellevants, paths d'altres pestanyes
  modificades.

Aquest registre serveix per:
- Tenir històric del que s'ha decidit i per què.
- Permetre que una sessió futura recuperi context sense haver de rellegir
  tots els canvis o el codi.
- Documentar canvis estructurals que no queden a `Canvis` (per exemple,
  reorganitzacions del propi sheet).

## Operacions amb Google Ads

- `GOOGLE_ADS_LOGIN_CUSTOMER_ID` i altres env vars poden venir amb `<...>`
  literals; sanititzar amb `strip('<>')` o regex de dígits.
- `GRPC_DEFAULT_SSL_ROOTS_FILE_PATH=/etc/ssl/certs/ca-certificates.crt` ja
  l'exporta el hook; sense això el client peta amb `CERTIFICATE_VERIFY_FAILED`.
- Mutates de `conversion_action` per a tipus sistema (Android installs, Smart
  Campaign) no estan permesos: usar `customer_conversion_goal` per al control
  d'Account Default i `campaign_conversion_goal` per als overrides.
- Field mask: especificar paths explícits (`update_mask.paths.append(...)`).
  `field_mask()` automàtic ignora els camps amb valor per defecte
  (p.ex. `biddable=False` bool default).
- `change_event`: max 30 dies enrere. Per història més llarga, fer-ho amb dates
  explícites just dins el límit (29 dies) o consultar `change_status`.
- `segments.date DURING LAST_90_DAYS`: no funciona. Usar dates explícites.

## Normes operatives (de README.md)

- Mai pujar clau JSON en clar al repo.
- Rotar clau SA cada 90 dies.
- Compartir cada nou Sheet/Doc amb el SA abans d'usar-lo.
- Per Google Ads: només mutacions amb OK explícit del client.
