# CLAUDE.md — branca `claude/hopeful-pascal-rOa5f` (Sala Ars)

## Registre d'execució setmanal (obligatori)

Cada cop que es tanca un bloc de treball, afegir **una fila** a la pestanya
`Execució setmanal` del sheet **General**
(`1NXct3wMopbaPeSzLDVRehjf91hzLRhGPC6RG_yVvV6Q`).

Una fila per bloc — no agrupar dies ni clients. Si el bloc toca diversos
clients, una fila per client.

### Columnes (en aquest ordre)

| Columna | Contingut |
| :-- | :-- |
| Data | `YYYY-MM-DD` del dia que es tanca el bloc |
| Setmana ISO | `YYYY-Www` (p.ex. `2026-W22`) |
| Client / àmbit | Nom curt del client o àmbit (p.ex. `Sala Ars`, `Komunikate`, `Girofeeds`, `Personal`) |
| Sessió (branca/canal) | Branca git i/o canal d'origen (p.ex. `claude/hopeful-pascal-rOa5f` / `whatsapp:g-120363428621232806`) |
| Què s'ha fet | Resum operatiu del bloc, amb dades/IDs quan apliqui |
| Pendent / proper pas | Acció concreta següent, amb responsable si no és Claw |
| Estat | `Fet` / `En curs` / `Bloquejat` / `Pendent OK` |
| Hores aprox. | Decimal amb coma (p.ex. `0,75`) |
| Notes | Context addicional, referències, enllaços, bloquejos |

### Regla operativa

- Aplicar **en tancar cada bloc**, no a final de setmana.
- Si el bloc queda bloquejat per validació externa, registrar igualment amb
  estat `Bloquejat` o `Pendent OK` i indicar de qui s'espera.
- Si el bloc té impacte en un sheet de client (p.ex. `Sala Ars`), mantenir
  el detall tècnic allà i deixar a `Execució setmanal` només la línia resum.
- L'idioma de la fila és català.
