# CLAUDE.md — clawdocs

## Registre d'execució setmanal (obligatori)

Cada cop que es tanqui un bloc de treball (sessió, tasca operativa significativa,
fix, setup, diagnòstic, entrega o canvi rellevant), s'ha d'afegir **una fila
nova** a la pestanya **`Execució setmanal`** del Sheet **General**
(`1NXct3wMopbaPeSzLDVRehjf91hzLRhGPC6RG_yVvV6Q`).

Una fila per bloc de treball. No agrupar blocs diferents en una sola fila.

### Columnes (ordre estricte)

| Columna | Contingut |
| :-- | :-- |
| Data | `YYYY-MM-DD` del dia que es tanca el bloc |
| Setmana ISO | `YYYY-Www` (p.ex. `2026-W22`) |
| Client / àmbit | Nom client (Arren, Pozas, Monlau...) o àmbit intern (Clawdocs, Infra) |
| Sessió (branca/canal) | Branca git i/o canal WhatsApp/font de la feina |
| Què s'ha fet | Descripció concreta i accionable del bloc tancat |
| Pendent / proper pas | Què queda obert i quin és el següent moviment |
| Estat | `Fet` / `En curs` / `Bloquejat` / `En observació` / `Enviar client` |
| Hores aprox. | Temps dedicat al bloc (decimal, p.ex. `0,5` / `1,25`) |
| Notes | Context intern útil per recuperar el fil més tard |

### Regla operativa

- Escriure la fila **abans de fer commit final / push** del bloc.
- Si el bloc no toca codi, escriure-la igualment en tancar.
- Si un bloc es reprèn en un altre dia, fer una fila nova (no editar l'anterior).
- Accés escriptura via Service Account ja configurat
  (`GOOGLE_APPLICATION_CREDENTIALS`, `gspread`).
