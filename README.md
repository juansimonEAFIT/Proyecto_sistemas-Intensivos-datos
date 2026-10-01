# TiendaCol — Pipeline de datos para e-commerce

Proyecto final de **ST1630 – Sistemas Intensivos en Datos** (Universidad EAFIT, 2026-2).

TiendaCol (nombre provisional) es un marketplace colombiano ficticio. Hoy toma decisiones con reportes del día siguiente y eso le cuesta ventas: productos que se agotan sin aviso en los picos, carritos abandonados que nadie recupera a tiempo y un embudo de compra que no se entiende. Este proyecto diseña (E1) e implementa (E2) el pipeline de datos que resuelve esos problemas.

El contexto completo, las restricciones, las decisiones técnicas, los enlaces a los datasets y las reglas para agentes de IA están en [CLAUDE.md](CLAUDE.md).

## Estado

| Entrega | Estado |
|---|---|
| E1: documento + diagrama (sin código) | Cierre técnico completo: [Markdown](docs/entregable1/e1_tiendacol.md), [PDF](docs/entregable1/e1_tiendacol.pdf) y [diagrama editable](docs/entregable1/arquitectura.drawio) |
| E2: código + presentación + demo | No iniciado |

Decisiones de arquitectura aprobadas para el E1: plataforma **AWS Academy híbrida** (ADR-6), orquestación con **Airflow** (ADR-5), componente libre **DynamoDB** (ADR-4), **Delta Lake** (ADR-3), **Spark** (ADR-2) y **Kafka con at-least-once** (ADR-1). El estado de cada una está en la §7 de [CLAUDE.md](CLAUDE.md).

## Estructura del repositorio

Las carpetas de componentes son marcadores de posición para E2: cada una tiene un README con su propósito y los requisitos funcionales que cubre. El detalle está en la §10 de [CLAUDE.md](CLAUDE.md).

```
/
├── CLAUDE.md               # contexto del proyecto y reglas para agentes de IA
├── CONTRIBUTING.md         # flujo de ramas y Pull Requests del equipo
├── README.md               # este archivo
├── .github/
│   └── pull_request_template.md
├── docker-compose.yml      # (E2) servicios del pipeline; aún sin definir
├── .env.example            # variables de entorno (copiar a .env)
├── .gitignore
├── docs/
│   ├── entregable1/        # documento E1 (e1_tiendacol.md → PDF) y diagrama
│   ├── entregable2/        # slides (E2)
│   └── bitacora_ia.md      # uso de IA, obligatoria en E2 (sin ella: -10%)
├── data/                   # datasets (no se suben a git; solo sample/)
├── generator/              # simulador de eventos para la demo
├── ingestion/              # fuentes → Bronze
├── processing/
│   ├── streaming/          # tiempo real
│   └── batch/              # Bronze → Silver → Gold
├── orchestration/          # DAG(s)
├── serving/                # componente libre, alertas, tableros y consultas
├── scripts/                # herramientas reproducibles, incluida la exportación del E1
└── tests/                  # verificación de los RF
```

## Exportar el E1

Con Python, Google Chrome y los paquetes `markdown` y `pypdf` instalados:

```powershell
python scripts/export_e1.py
```

El comando genera `docs/entregable1/e1_tiendacol.pdf`, cuenta sus páginas y falla si el cuerpo anterior al Anexo A supera las 15 páginas permitidas.

## Cómo colaborar

`main` solo recibe entregas. El E1 se escribe en la rama `e1` y el código del E2 entra por Pull Request a `e2`. El flujo completo, con los comandos, está en [CONTRIBUTING.md](CONTRIBUTING.md).

## Cómo correr el pipeline

_Pendiente para E2._ Esta sección debe permitir a cualquiera levantar el pipeline desde cero.

## Equipo

| Rol | Integrante |
|---|---|
| P1 | Juan Simón Ospina Martínez |
| P2 | Sebastián Durán |
| P3 | Daniel Arcila Salazar |
| P4 | Juan José Díaz Rodríguez |
