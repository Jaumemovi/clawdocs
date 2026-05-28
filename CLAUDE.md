# CLAUDE.md — Clawdocs

Notes operatives per a sessions de Claude Code en aquest repo.

## Registre d'execució setmanal (obligatori)

Cada cop que es tanqui un bloc de treball (per exemple: tasca acabada en una sessió, lliurament a client, canvi d'àmbit), cal afegir una fila al sheet **General** → pestanya **Execució setmanal**:

- Sheet: `1NXct3wMopbaPeSzLDVRehjf91hzLRhGPC6RG_yVvV6Q`
- Pestanya: `Execució setmanal` (gid `1337645471`)

Columnes (per ordre):

| Columna | Contingut |
|---|---|
| Data | Data del bloc (YYYY-MM-DD) |
| Setmana ISO | Setmana ISO (YYYY-Www) |
| Client / àmbit | Client o àrea (p.ex. `Komunikate`, `Girofeeds`, `Clawdocs`) |
| Sessió (branca/canal) | Branca git o canal de la sessió (p.ex. `claude/hopeful-mayer-3etGX`) |
| Què s'ha fet | Resum curt del bloc tancat |
| Pendent / proper pas | Què queda obert i quan revisar-ho |
| Estat | `Fet` / `Fet parcial` / `Bloquejat` / `Descartat` |
| Hores aprox. | Temps estimat dedicat al bloc |
| Notes | Context addicional (links, IDs, dependències) |

Regla per a Claude:

1. En tancar un bloc, afegir la fila al final de la pestanya **Execució setmanal** abans de donar la feina per acabada.
2. Si el bloc queda bloquejat o descartat, també s'hi registra (estat `Bloquejat` / `Descartat`).
3. No fer commit final sense haver enregistrat el bloc.
