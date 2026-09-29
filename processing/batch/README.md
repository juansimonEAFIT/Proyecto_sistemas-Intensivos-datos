# processing/batch/

**Capa del diagrama:** Procesamiento Bronze → Silver → Gold. **Pendiente para E2.** Depende del ADR-2 (procesamiento) y del ADR-3 (formato de Gold y modelo dimensional).

| RF | Qué hace |
|---|---|
| RF-05 | Validar el esquema, apartar en cuarentena sin detenerse y eliminar duplicados (Bronze → Silver) |
| RF-06 | Enriquecer eventos y líneas de orden con catálogo y maestros (join) |
| RF-10 | Conversión del embudo por categoría, dispositivo y ciudad, por hora y por día (Gold) |
| RF-11 | Ventas, órdenes y ticket promedio en el modelo dimensional de Gold |
| RF-13 *(opcional)* | Productos comprados y vistos juntos, cada día |

Aquí debe quedar al menos una transformación no trivial en Spark (join, ventanas o agregación), porque el enunciado la exige.
