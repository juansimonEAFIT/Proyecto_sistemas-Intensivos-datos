# ingestion/

**Capa del diagrama:** Ingestión → Bronze. **Pendiente para E2.** Depende del ADR-1 (motor de streaming y garantía de entrega) y del ADR-6 (plataforma).

| RF | Qué hace |
|---|---|
| RF-01 | Ingestar el clickstream en tiempo real y conservarlo sin modificar en Bronze |
| RF-02 | Capturar órdenes, líneas, pagos y estados de envío |
| RF-03 | Recibir cada cambio de stock |
| RF-04 | Cargar el catálogo y los datos maestros cada día antes de las 6:00 a. m. |
