# Cómo colaborar en este repositorio

Flujo de ramas y Pull Requests del equipo TiendaCol. Si algo de este archivo cambia, se avisa en el chat del grupo **antes** de aplicarlo.

Responsable del flujo: **P4** (repo y PR), según el reparto del E1.

## La idea en una frase

**`main` solo recibe entregas.** Todo lo demás se trabaja en otras ramas y entra por Pull Request.

La razón es la guía del proyecto, que pide dos PR concretos: un PR abierto con la descripción del proyecto en el E1, y un *"PR final con todo el código"* antes de las 11:59 p. m. del día anterior a S16. Si el código ya estuviera en `main`, ese PR final no tendría nada que mostrar.

## Las ramas

```
main ─────────────────────────●───────────────────────────●──►
  │                          ↑ PR "E1"                   ↑ PR final "E2"
  ├── e1 ──●──●──●──●────────┘                           │
  │       (cada quien en su sección)                     │
  │                                                      │
  └── e2 ────────●─────●─────●─────●─────────────────────┘
                 ↑     ↑     ↑     ↑
     p2/kafka ───┘     │     │     │
     p4/docker-compose ┘     │     │
     p3/silver-gold ─────────┘     │
     p4/airflow-dags ──────────────┘
```

| Rama | Para qué | Cómo se escribe en ella |
|---|---|---|
| `main` | Solo lo entregado | Nunca directo. Solo recibe el PR del E1 y el PR final del E2 |
| `e1` | El documento del Entregable 1 | Directo: cada integrante en su propia sección |
| `e2` | Integración del código del Entregable 2 | Nunca directo: solo recibe PR de ramas de trabajo |
| `p<n>/<tema>` | Una tarea del E2 | Directo, solo su dueño |

`e2` se crea desde `main` **después** del merge del PR del E1, al empezar S13. Así arranca con el documento final ya incluido.

## Entregable 1: trabajar en `e1`

No hay ramas por persona: cada uno escribe en una sección distinta de `docs/entregable1/e1_tiendacol.md`, y git junta sin problemas cambios en líneas distintas del mismo archivo.

```powershell
git switch e1
git pull                                   # traer lo que subieron los demás
# ... editar SOLO tu sección ...
git add docs/entregable1/e1_tiendacol.md
git commit -m "E1: <qué cambiaste>"
git pull --rebase                          # por si alguien subió algo mientras editabas
git push
```

Si `git pull --rebase` avisa de un conflicto, casi siempre es porque dos personas editaron la misma línea. Abran el archivo, busquen las marcas `<<<<<<<` y `>>>>>>>`, dejen la versión correcta y sigan con `git add` y `git rebase --continue`. Si no es obvio cuál versión va, pregunten en el grupo antes de decidir.

**El PR del E1** (`e1 → main`) se abre temprano, como borrador (*draft*), y va acumulando los commits. Se hace merge después de entregar el E1.

## Entregable 2: una rama por tarea

```powershell
git switch e2
git pull
git switch -c p4/docker-compose            # p<tu número>/<tema>
# ... trabajar, con commits pequeños ...
git push -u origin p4/docker-compose
```

Después se abre en GitHub un PR **hacia `e2`** (no hacia `main`).

Cuando otra persona hizo merge a `e2` y tu rama todavía no termina, trae sus cambios así:

```powershell
git switch e2
git pull
git switch p4/docker-compose
git merge e2
```

## Reglas de los PR hacia `e2`

1. **Lo aprueba otro integrante, nunca el autor.** No es burocracia: la guía dice que en la defensa el docente pregunta a cada integrante por partes del sistema que no implementó, y la defensa individual vale el 40 % del E2. Quien revisa un PR ya leyó ese código antes de la sesión.
2. **PR pequeños**, de una tarea cada uno. Un PR de 2.000 líneas nadie lo revisa de verdad.
3. **La descripción la llena la plantilla** (`.github/pull_request_template.md`), que pide qué RF cubre y cómo probarlo.
4. Se une con **Squash and merge**, que deja un solo commit por tarea en `e2`, y se borra la rama.

## Nombres y mensajes

- Ramas: `p<n>/<tema>` en minúsculas y con guiones. Ejemplos: `p2/kafka-ingesta`, `p3/modelo-dimensional`, `p4/airflow-dags`.
- Commits: en español, con el componente al inicio. Ejemplos: `E1: ADR-4 (componente libre)`, `ingesta: productor de clickstream a Kafka`, `airflow: dag_horario con sensor de Bronze`.

## Lo que nunca se sube

- El archivo `.env` ni ninguna credencial de AWS. Ya están en `.gitignore`. Las variables de ejemplo van en `.env.example`, sin valores reales.
- Los datasets completos: van en `data/`, que está ignorada. Solo `data/sample/` se sube.

## Protección de ramas (la configura el dueño del repo)

Solo el dueño del repositorio (P1) puede activarlas en GitHub, en *Settings → Branches*:

| Rama | Regla |
|---|---|
| `main` | Exigir PR antes de hacer merge, con 1 aprobación |
| `e2` | Exigir PR antes de hacer merge, con 1 aprobación |
| `e1` | Sin protección: se sube directo |

## Agentes de IA

Los agentes siguen este mismo flujo. No hacen commit, push ni abren PR: le entregan al integrante el comando o el mensaje de commit, y el integrante lo ejecuta. Ver `CLAUDE.md` §9.7.
