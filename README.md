# clawdocs

Repositori central de configuració per editar Google Sheets i Drive via
Service Account des de sessions de **Claude Code on the web** (Claude Cloud).

## Què fa

A l'inici de cada sessió remota, el hook `.claude/hooks/session-start.sh`:

1. Llegeix el secret `GOOGLE_SA_JSON` (clau JSON del Service Account
   `claude-cloud@clawdocs-492614.iam.gserviceaccount.com`).
2. L'escriu a `/root/.secrets/claude-cloud-sa.json` amb permisos `600`.
3. Exporta `GOOGLE_APPLICATION_CREDENTIALS` apuntant a aquell fitxer
   (via `$CLAUDE_ENV_FILE` perquè persisteixi a la sessió).
4. Instal·la `gspread` i `google-auth` si encara no hi són.

Només s'activa quan `CLAUDE_CODE_REMOTE=true`, així que en local no fa res.

## Setup

A la configuració de l'entorn Claude Cloud per aquest repo:

- Afegir l'env var `GOOGLE_SA_JSON` amb el contingut del JSON de la clau
  del Service Account (minificat en una sola línia).
- El hook ja està registrat a `.claude/settings.json`.

## Normes operatives

- Mai pujar la clau JSON en clar al repo.
- Rotar la clau cada 90 dies (veure el document mestre "General").
- Compartir cada nou Sheet/Doc amb el Service Account abans d'usar-lo.
