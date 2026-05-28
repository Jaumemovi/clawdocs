# CLAUDE.md — Repo clawdocs

Guia operativa per a sessions Claude sobre aquest repo.

## Registre d'execució setmanal (obligatori)

Cada cop que es tanca un bloc de treball, **registrar una fila** al sheet General de l'agència:

- **Sheet**: `1NXct3wMopbaPeSzLDVRehjf91hzLRhGPC6RG_yVvV6Q` (General)
- **Pestanya**: `Execució setmanal` (gid `1337645471`)
- **Enllaç directe**: https://docs.google.com/spreadsheets/d/1NXct3wMopbaPeSzLDVRehjf91hzLRhGPC6RG_yVvV6Q/edit#gid=1337645471

### Columnes (en aquest ordre)

| # | Columna | Contingut |
|---|---|---|
| A | Data | `YYYY-MM-DD` del dia que es tanca el bloc |
| B | Setmana ISO | `YYYY-Wxx` (ex: `2026-W22`) |
| C | Client / àmbit | Client (`MarimonTcuida`, `Farmacia Marimon`, `Komunikate`…) o `Intern` |
| D | Sessió (branca/canal) | Nom de branca git, canal WhatsApp, o identificador de sessió |
| E | Què s'ha fet | Resum executiu del bloc — concret i mesurable |
| F | Pendent / proper pas | Acció(ns) per a la propera sessió o setmana |
| G | Estat | `Tancat` · `En curs` · `Bloquejat` |
| H | Hores aprox. | Estimació en hores del temps invertit al bloc |
| I | Notes | Context addicional, IDs, enllaços rellevants |

### Regles d'aplicació

1. **Una fila per bloc de treball**, no una per dia ni una per setmana. Un bloc = una sessió focalitzada amb principi i final clars.
2. **S'afegeix en tancar el bloc**, no al final del dia ni de la setmana.
3. **Estat `Tancat`** només si el bloc ha lliurat el resultat compromès; en cas contrari `En curs` o `Bloquejat` amb explicació al camp Notes.
4. Si el bloc afecta múltiples clients, **una fila per client** (no fusionar).
5. Mantenir el camp **Què s'ha fet** dens i factual: dades, IDs, comptes, enllaços. Evitar genèric ("vam treballar amb el client").
6. El camp **Pendent / proper pas** alimenta directament la planificació de la setmana següent — escriure-ho com una acció executable, no com a desig.

### Accés tècnic per a sessions automatitzades

Auth via service account `claude-cloud@clawdocs-492614.iam.gserviceaccount.com` (variable d'entorn `GOOGLE_SA_JSON`) amb scope `https://www.googleapis.com/auth/spreadsheets`. Append amb `values:append` o `values.update` segons calgui inserir al final o en una fila específica.
