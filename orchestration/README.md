# orchestration/

**Capa del diagrama:** Orquestación (transversal). **Pendiente para E2.** Depende del ADR-5 (orquestación).

**RF-12:** ejecutar automáticamente, en el orden de sus dependencias, la carga diaria de catálogo y maestros, Bronze → Silver y Silver → Gold. Si un paso falla, no se ejecutan los que dependen de él y se notifica la falla.

Para la demo del E2 hay que mostrar el DAG con el pipeline completo y su estado.
