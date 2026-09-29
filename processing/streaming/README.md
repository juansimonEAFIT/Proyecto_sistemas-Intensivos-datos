# processing/streaming/

**Capa del diagrama:** Procesamiento en tiempo real. **Pendiente para E2.** Depende del ADR-2 (motor de procesamiento).

| RF | Qué hace | Ventana |
|---|---|---|
| RF-07 | Velocidad de venta por producto y alerta si el stock cubre menos de 60 min; en máx. 2 min | Deslizante de 15 min |
| RF-08 | Carritos de COP 500.000 o más sin compra ni cambios en 30 min; lista a Marketing en máx. 5 min | 30 min de inactividad |
| RF-09 | Órdenes y COP vendidos por minuto, en total y por categoría; en máx. 2 min | Fija de 1 min |
