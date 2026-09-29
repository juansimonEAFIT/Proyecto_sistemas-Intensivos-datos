# generator/

**Capa del diagrama:** Fuente. **Pendiente para E2.**

Simulador que emite en tiempo real los datos de TiendaCol para la demo en vivo:

- Eventos del clickstream: `page_view`, `search`, `add_to_cart`, `remove_from_cart`, `checkout_start`, `purchase`.
- Órdenes y pagos.
- Cambios de inventario.

Alimenta a RF-01, RF-02 y RF-03. Puede reproducir eventos de REES46 y Olist y completar lo que les falta con Faker `es_CO` (ver `CLAUDE.md`, §8.2).
