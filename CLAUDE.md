# CLAUDE.md — clawdocs

## Registre d'execució setmanal (obligatori)

Cada cop que es tanqui un bloc de treball (un encàrrec acabat, un commit/push,
o un canvi de context cap a un altre client/àmbit), s'ha d'afegir **una fila**
a la pestanya `Execució setmanal` del sheet **General**
(`1NXct3wMopbaPeSzLDVRehjf91hzLRhGPC6RG_yVvV6Q`).

Columnes (en aquest ordre exacte):

| # | Columna | Contingut |
|---|---|---|
| A | Data | `YYYY-MM-DD` del dia que es tanca el bloc |
| B | Setmana ISO | `YYYY-Www` (p. ex. `2026-W22`) |
| C | Client / àmbit | Nom del client o àrea (ex: `Ride On`, `Clawdocs`, `General`) |
| D | Sessió (branca/canal) | Branca git activa o canal de comunicació |
| E | Què s'ha fet | Resum curt del bloc tancat |
| F | Pendent / proper pas | El que queda obert o el següent pas previst |
| G | Estat | `Fet`, `En curs`, `Bloquejat`, `Cancel·lat` |
| H | Hores aprox. | Estimació en hores (decimals OK, p. ex. `0.5`) |
| I | Notes | Context addicional, enllaços, riscos |

Regla operativa:

- Append, mai sobreescriure files existents.
- Una fila per bloc — si hi ha dues feines en paral·lel per al mateix client, dues files.
- Si el bloc inclou commit/push, posar a Notes el SHA curt o l'enllaç del PR.
- Si l'usuari no demana explícitament un commit, igualment registrar el bloc quan es tanqui.
