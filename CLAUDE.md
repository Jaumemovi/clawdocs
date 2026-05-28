# clawdocs - notes per Claude

## Registre d'execució setmanal (obligatori)

Cada cop que tanco un **bloc de treball** (acció completada, decisió presa,
entregable enviat, sessió finalitzada), he d'afegir **una fila** a la
pestanya `Execució setmanal` del Sheet **General**
(`1NXct3wMopbaPeSzLDVRehjf91hzLRhGPC6RG_yVvV6Q`).

### Columnes (en aquest ordre)

| # | Columna | Contingut |
|---|---|---|
| 1 | Data | `YYYY-MM-DD` del dia en què s'ha tancat el bloc |
| 2 | Setmana ISO | `YYYY-Www` (ex. `2026-W22`) |
| 3 | Client / àmbit | Nom client o àmbit intern (ex. `Lacoop`, `clawdocs-infra`) |
| 4 | Sessió (branca/canal) | Branca git, canal Slack/WhatsApp o ID sessió |
| 5 | Què s'ha fet | Descripció concreta del bloc tancat |
| 6 | Pendent / proper pas | Què queda obert o quin és el següent moviment |
| 7 | Estat | `Fet` / `En curs` / `Bloquejat` / `Enviat client` |
| 8 | Hores aprox. | Decimal (ex. `0.25`, `1.5`) |
| 9 | Notes | Referències: commit, PR, Sheet, missatge, context tècnic |

### Regla operativa

- **Una fila per bloc**, no per sessió sencera: si en una sessió tanco 3
  blocs independents, registro 3 files.
- **Append**, no sobreescriure: les files anteriors es mantenen.
- Si el bloc afecta un client amb Sheet propi de seguiment, també
  s'actualitza allà (pestanya `Accions` del Sheet del client); aquest
  registre és el log transversal d'execució.
- Si oblido registrar un bloc tancat, l'afegeixo retroactivament amb la
  data real del tancament.
