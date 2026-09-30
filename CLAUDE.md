# CLAUDE.md — Proyecto final ST1630 Sistemas Intensivos en Datos (EAFIT, 2026-2)

> **Para humanos y agentes de IA.** Este archivo es la fuente de verdad del proyecto: qué se entrega, qué ya está escrito, qué valores ya están fijados, qué falta y qué **no** se puede inventar. Un agente debe leerlo completo antes de escribir texto o código.
>
> Última actualización: 2026-09-29.

---

## 0. Resumen en 30 segundos

- **Qué:** proyecto final en grupos de 4. **E1** es un documento sin código (entrega antes de S13) y **E2** es código, presentación, demo y defensa (S16).
- **Dominio:** e-commerce. La empresa es **TiendaCol**, un marketplace colombiano ficticio.
- **Documento del E1:** un **único archivo**, [docs/entregable1/e1_tiendacol.md](docs/entregable1/e1_tiendacol.md). Se exporta a `docs/entregable1/e1_tiendacol.pdf`. **No crear archivos separados por sección:** el equipo lo decidió así.
- **Estado:** la parte del integrante P1 está escrita (portada, Sección 1, Sección 2.1 y Anexo A). Las secciones de los integrantes P2, P3 y P4 tienen solo la estructura, con marcadores `[...]`.
- **Ninguna herramienta está elegida todavía.** Los ADR están vacíos. Un agente **no** elige herramientas por el equipo (ver §9).
- **Bitácora de IA:** [docs/bitacora_ia.md](docs/bitacora_ia.md) está vacía **a propósito**. Se llena en E2. No escribir en ella (ver §9.6).

### Orden de lectura para un agente

Claude Code carga este archivo automáticamente. **Con otro agente (Copilot, Cursor, Codex, ChatGPT…), la primera instrucción debe ser "lee CLAUDE.md completo antes de hacer nada".**

1. Este archivo completo.
2. [docs/entregable1/e1_tiendacol.md](docs/entregable1/e1_tiendacol.md) completo, **incluidos los comentarios `<!-- -->`**. Esos comentarios tienen las instrucciones de cada sección y las notas de defensa.
3. Solo después, escribir en la sección que le corresponde al integrante con el que trabaja.

### Convención importante: "P1" tiene dos significados

- **Integrantes:** P1, P2, P3 y P4 son las personas del equipo (ver §6).
- **Preguntas de negocio:** P1 a P6 son las preguntas que el sistema responde (ver §3.4). Así aparecen en el texto del documento que lee el profesor.

Cuando haya ambigüedad, escribir "**integrante P2**" o "**pregunta P2**". En el texto visible del documento, "P1…P6" siempre significa pregunta.

---

## 1. El curso y la evaluación (resumen de la guía oficial)

La guía oficial ("ST1630 – Proyecto Final – Guía completa", v1.0, septiembre de 2026, Prof. Andrés Sacre Alzate) **no está en el repo**. Esta sección la resume. Si algo de aquí contradice la guía, manda la guía.

**Pregunta central:** *"Dado este problema de negocio, ¿qué pipeline de datos construirías y por qué exactamente así?"* Lo que más se evalúa es **justificar cada decisión técnica** con conceptos del curso.

| Entrega | Fecha | Qué se entrega | Peso en el curso |
|---|---|---|---|
| **E1** | Antes del inicio de S13 (subir al repo antes de las 11:59 p. m. del día anterior) + entrega en EAFIT Interactiva | PDF de máx. 15 páginas sin anexos + diagrama en PNG/SVG + enlace editable (Draw.io o Lucidchart). **Sin código.** | 20 % |
| **E2** | S16 | Repositorio con código (12 %) + presentación y defensa (8 %) | 20 % |

- Los grupos son de exactamente 4. **Cada integrante debe poder defender cualquier parte del sistema.** Si en la defensa un integrante no responde sobre partes que implementó otro, su nota se penaliza (hasta 30 % según la sección de grupos de la guía; hasta 40 % menos que el grupo según la rúbrica del E2).
- **Fechas exactas de S13 y S16:** no se conocen en el repo. **No inventarlas:** preguntarle al humano.

### 1.1 Qué pide el E1, sección por sección

| Sección | Extensión | Qué pide la guía |
|---|---|---|
| Portada | — | Nombre completo y código EAFIT de los 4 integrantes, nombre del proyecto y dominio. |
| 1. Definición del problema | 1–2 págs. | Problema de negocio, preguntas analíticas u operacionales, usuarios y qué deciden con los datos, y por qué la escala o la variedad justifican una arquitectura distribuida. **Error frecuente:** describir el sistema técnico en vez del problema. |
| 2. Requisitos | 2–3 págs. | **RF:** mínimo 8, cada uno una oración con verbo de acción. **RNF:** escalabilidad (pico de X eventos/s), disponibilidad (posición CAP justificada), consistencia (garantía de entrega y en qué parte del pipeline), latencia (del evento a Gold), tolerancia a fallos (qué pasa si un nodo cae y cómo se recupera), trazabilidad (linaje de la fuente a Gold). |
| 3. Diagrama | 1 pág. | Un solo diagrama con 5 capas: **Fuente** (formato y frecuencia), **Ingestión** (transporte y garantía de entrega), **Procesamiento** (qué cambia entre entrada y salida), **Almacenamiento** (Bronze/Silver/Gold con su motor y el modelo de Gold) y **Consumo**. Cada caja lleva el nombre de la herramienta concreta ("Delta Lake en S3", no "base de datos"). Debe entenderse en menos de 2 minutos. |
| 4. ADRs | 3–4 págs. | Mínimo 5, cada uno con Contexto · Alternativas consideradas (y por qué se descartaron) · Decisión (con conceptos del curso) · Consecuencias (qué se sacrifica). Decisiones mínimas: motor de streaming y garantía de entrega; Spark Streaming vs Flink vs batch puro; motor de Gold y por qué el modelo dimensional; componente libre y su posición CAP; orquestador y cómo se modelan las dependencias del DAG. |
| 5. Plan | 1 pág. | Qué componente implementa cada integrante, hitos antes de S16 y riesgos técnicos con mitigación. |

### 1.2 Rúbrica del E1

| Criterio | Peso | Para el 100 % |
|---|---|---|
| Definición del problema | 10 % | Problema claro y acotado que justifica la escala; preguntas específicas y medibles. |
| Requisitos funcionales | 15 % | 8 o más, con verbo de acción, todos verificables y trazables al diagrama. |
| Requisitos no funcionales | 15 % | Citan explícitamente CAP, garantía de entrega, latencia, escalabilidad y tolerancia a fallos, con valores concretos. |
| Diagrama de arquitectura | 25 % | 5 capas, cada componente con su servicio concreto, legible sin explicación y con el enlace editable funcionando. |
| Justificación (ADRs) | 25 % | Al menos 5 ADRs completos, y cada uno cita conceptos del curso. |
| Plan de implementación | 10 % | Tareas claras, cronograma realista antes de S16 y riesgos con mitigación. |

**Checklist oficial del E1:**
- PDF en `docs/entregable1/e1_[nombre_proyecto].pdf` (aquí: `e1_tiendacol.pdf`).
- Diagrama en `docs/entregable1/arquitectura.[png|svg]`.
- Enlace editable del diagrama en la Sección 3.
- Las 5 secciones completas.
- Nombres y códigos de los 4 integrantes en la portada.
- **Pull Request abierto con la descripción del proyecto.**

### 1.3 Qué pide el E2 (para planear desde ya)

- **S16, 25 minutos:** 10 de presentación (máx. 15 slides, en `docs/entregable2/`), 8 de demo en vivo y 7 de defensa con preguntas a integrantes específicos.
- **Demo:** se permite un dataset precargado, pero **el procesamiento debe correr en vivo**. Hay que mostrar el productor enviando eventos, el job de Spark procesando, **una consulta a Gold que responda una pregunta de negocio del E1** y el DAG del orquestador. Un video pregrabado sin justificación saca 0.
- **Repositorio:** PR final antes de las 11:59 p. m. del día anterior a S16. README para correr todo desde cero, `docker-compose.yml` (o equivalente) en la raíz, carpetas por componente y `docs/bitacora_ia.md`. Ensayo obligatorio el día anterior.
- **Rúbrica del repositorio:** estructura/README 10 %, streaming de extremo a extremo 20 %, Spark no trivial 20 %, lakehouse con Gold dimensional y consulta de negocio 20 %, orquestación completa (los pasos fallan limpio si falla uno anterior) 15 %, componente libre funcionando según lo propuesto en el E1 15 %.
- **Rúbrica de la presentación:** claridad 15 %, demo 25 %, **defensa individual 40 %**, reflexión (qué cambió respecto al E1 y por qué, con argumentos técnicos) 20 %.
- **Preguntas típicas de la defensa:**
  - ¿Por qué el motor X y no el Y?
  - ¿Qué cambian primero si el volumen se multiplica por 100?
  - ¿Cómo evitan procesar un evento dos veces si Spark falla a la mitad?
  - ¿Cuál es la posición CAP del componente más crítico y qué sacrificaron?
  - ¿Qué pasa si se cae el broker? (muéstrenlo en el código)
  - ¿Por qué esa partition key?

### 1.4 Política de IA e integridad (de la guía)

- Usar agentes está **permitido y se espera**. El equipo debe entender y poder explicar todo lo que entrega.
- **Buen uso:** "genera el esqueleto del productor", "ayúdame con esta query de Spark".
- **Mal uso:** "diseña la arquitectura completa". Generar una justificación que el equipo no entiende "es la forma más rápida de reprobar la defensa".
- La bitácora de delegación es obligatoria en E2 (sin ella se descuenta 10 % del E2).
- Nota de cero para todos: copiar código de otro grupo, entregar un tutorial sin cambios sustanciales o alterar los resultados de la demo.

---

## 2. Estado del documento E1

Archivo: [docs/entregable1/e1_tiendacol.md](docs/entregable1/e1_tiendacol.md).

| Sección | Responsable | Estado |
|---|---|---|
| Portada | Integrante P1 | Escrita. Faltan nombre y código de los integrantes P2, P3 y P4, y la fecha de entrega. |
| 1. Definición del problema | Integrante P1 | Escrita, lista para revisión. |
| 2.1 Requisitos funcionales (RF-01 a RF-13) | Integrante P1 | Escrita, lista para revisión. |
| 2.2 Requisitos no funcionales | Integrante P2 | Solo estructura (tabla RNF-01 a RNF-06 con `[...]`). |
| 3. Diagrama | Integrante P3 | Solo estructura. La tabla de capas ya trae los RF de cada capa. |
| 4. ADR-1 y ADR-2 | Integrante P2 | Solo estructura. |
| 4. ADR-3 | Integrante P3 | Solo estructura. |
| 4. ADR-4, ADR-5 y ADR-6 | Integrante P4 | Escritos el 2026-09-29, con pendientes de validación marcados como `<!-- PENDIENTE -->`. |
| 5. Plan de implementación | Integrante P4 | Escrito el 2026-09-29. Faltan los nombres de P2 y P3, y validar el reparto del E2. |
| Anexo A. Supuestos de dimensionamiento | Integrante P1 | Escrito. |
| Referencias | Todos | [1] a [6] escritas por el integrante P1. Los demás agregan desde la [7]. |

Presupuesto de páginas: portada (no cuenta) · 1: 1–2 · 2: 2–3 · 3: 1 · 4: 3–4 · 5: 1. **Total: 8–11 de 15.** Si no cabe, la columna "Cómo se verifica" de la Sección 2.1 puede pasar a un anexo.

---

## 3. El problema de negocio (ya definido)

Texto completo en la Sección 1 del documento. Resumen para no tener que inferir:

### 3.1 La empresa

**TiendaCol** es un marketplace colombiano ficticio: vendedores independientes publican productos de tecnología, hogar, moda, belleza y deportes, y los clientes compran desde la web y la app móvil. Opera en las principales ciudades del país. Tiene picos en **Black Friday, Cyber Monday y Hot Sale**. **No usar "Cyber Lunes":** el Cyberlunes de la CCCE se dejó de hacer después de 2023.

### 3.2 Los tres problemas

Hoy decide con reportes **del día siguiente** que salen de la base transaccional. Eso causa:
1. Productos que se agotan sin aviso durante los picos.
2. Carritos abandonados que no se recuperan a tiempo.
3. Un embudo de compra que no se entiende.

### 3.3 Usuarios y decisiones

| Usuario | Decide | Urgencia |
|---|---|---|
| Operaciones / inventario | Reabastecer, avisar al vendedor, pausar publicidad | Minutos |
| Marketing / CRM | Recordatorio o cupón al carrito abandonado | Menos de 1 hora |
| Category managers / Comercial | Qué categorías promocionar, qué vendedores apoyar | Horas / diaria |
| Dirección | Metas, presupuesto, ajuste y evaluación de campañas | Minutos (en eventos) / diaria |

### 3.4 Preguntas de negocio

| Pregunta | Enunciado corto | Tipo |
|---|---|---|
| **P1** | Productos que se agotarán en los próximos 60 min a su velocidad de venta de los últimos 15 min; alerta en máx. 2 min | Tiempo real |
| **P2** | Usuarios identificados con carrito de COP 500.000 o más, sin compra ni cambios en 30 min; lista a Marketing en máx. 5 min | Tiempo real |
| **P3** | Órdenes y COP vendidos por minuto, en total y por categoría, visibles en máx. 2 min | Tiempo real |
| **P4** | Conversión del embudo vista de producto → carrito → compra por categoría, dispositivo y ciudad, por hora y por día; frescura de 1 h | Analítica (Gold) |
| **P5** | Ventas, número de órdenes y ticket promedio por categoría, vendedor, región y fecha; frescura de 1 h | Analítica (Gold) |
| **P6** *(opcional)* | Pares de productos comprados juntos (misma orden) o vistos juntos (misma sesión); diaria | Analítica |

---

## 4. Valores compartidos (usar exactamente estos)

Los propuso el integrante P1 y están **pendientes de validar con el equipo**. Un agente **los usa tal cual** y **no propone valores distintos** por su cuenta. Si el humano quiere cambiar uno, es una decisión del equipo, y hay que actualizarlo en **todos** los lugares de la columna derecha.

| Valor | Cifra | Dónde aparece en `e1_tiendacol.md` |
|---|---|---|
| Latencia de la alerta de agotamiento | máx. **2 min** desde la venta | Comentario inicial · 1.4 (P1) · RF-07 · notas de defensa · RNF de latencia (pendiente) |
| Horizonte de agotamiento | **60 min** | 1.4 (P1) · RF-07 |
| Ventana de velocidad de venta | últimos **15 min**, recalculada cada minuto | 1.4 (P1) · RF-07 |
| Carrito abandonado de alto valor | usuario **identificado**, **COP 500.000** o más, **30 min** sin compra ni cambios | 1.4 (P2) · RF-08 |
| Publicación de la lista a Marketing | máx. **5 min** después de cumplidos los 30 | 1.4 (P2) · RF-08 |
| Ventas por minuto | visibles máx. **2 min** después de cerrado el minuto | 1.4 (P3) · RF-09 |
| Frescura de Gold | máx. **1 hora** | 1.4 (P4, P5) · RF-10 · RF-11 · RNF de latencia (pendiente) |
| Usuarios activos al mes | **1,5 millones** | 1.1 · Anexo A |
| Eventos de navegación | ≈ **75 millones/mes** (≈ 1 TB crudo al año) | 1.5 · Anexo A |
| Tráfico | ≈ 29 eventos/s en un día normal; pico ≈ **3.000 eventos/s** en Black Friday | 1.5 · Anexo A |
| Capacidad objetivo | **5.000 eventos/s** | Anexo A · RNF de escalabilidad (pendiente) · ADR-1 (particiones) |
| Órdenes por día | 2.500 (normal) / 24.000 (Black Friday) | 1.1 · Anexo A |
| Ticket promedio | **COP 212.373** (CCCE, 2025) | 1.1 · 1.4 · Anexo A |
| Dispositivos | web de escritorio, web móvil, app | 1.4 (P4) |
| Eventos del clickstream | `page_view`, `search`, `add_to_cart`, `remove_from_cart`, `checkout_start`, `purchase` | RF-01 |
| Zona horaria | hora de Colombia | RF-04 |
| Alcance de P6 | dentro, **como opcional** (RF-13) | 1.4 · RF-13 |

La justificación de cada valor (para la defensa) está en el comentario final de `e1_tiendacol.md`, "NOTAS DE DEFENSA DE P1".

---

## 5. Requisitos funcionales (ya escritos)

Texto completo en la Sección 2.1. Los RF dicen **qué** hace el sistema, **no con qué herramienta**. No agregarles nombres de herramientas.

| ID | Qué exige (resumen) | Pregunta | Capa del diagrama |
|---|---|---|---|
| RF-01 | Ingestar el clickstream en tiempo real y conservarlo sin modificar en Bronze | P1–P4, P6 | Fuente → Ingestión → Bronze |
| RF-02 | Capturar órdenes, líneas, pagos y estados de envío de la base transaccional | P3, P5 | Fuente → Ingestión → Bronze |
| RF-03 | Recibir cada cambio de stock y mantener el stock disponible actual | P1 | Fuente → Ingestión → Procesamiento |
| RF-04 | Cargar el catálogo y los datos maestros cada día antes de las 6:00 a. m. | P4, P5 | Fuente → Ingestión por lotes → Bronze |
| RF-05 | Validar el esquema, apartar en cuarentena sin detenerse y eliminar duplicados | Todas | Bronze → Silver |
| RF-06 | Enriquecer eventos y líneas de orden con catálogo y maestros (**join**) | P1–P5 | Silver |
| RF-07 | Velocidad de venta de 15 min + alerta si la cobertura es menor a 60 min, en máx. 2 min (**ventana**) | P1 | Tiempo real → Consumo (alertas) |
| RF-08 | Carritos de COP 500.000 o más con 30 min de inactividad; lista a Marketing en máx. 5 min (**ventana**) | P2 | Tiempo real → Consumo (Marketing) |
| RF-09 | Órdenes y COP por minuto, en total y por categoría, en máx. 2 min (**ventana**) | P3 | Tiempo real → Consumo (tablero) |
| RF-10 | Conversión del embudo por categoría, dispositivo y ciudad, por hora y día, en Gold en máx. 1 h (**agregación**) | P4 | Silver → Gold |
| RF-11 | Ventas, órdenes y ticket en un **modelo dimensional** de Gold, consultable con SQL y en tablero, frescura de 1 h | P5 | Gold → Consumo |
| RF-12 | Orquestar los procesos por dependencias; si un paso falla, no correr los que dependen de él y notificar | Todas | Orquestación (transversal) |
| RF-13 *(opcional)* | Cada día, los 10 productos más comprados y los 10 más vistos junto con cada producto | P6 | Procesamiento → Gold o componente libre |

**Cobertura de las restricciones obligatorias:**
- Streaming: RF-01, RF-07, RF-08, RF-09.
- Spark no trivial: join en RF-06, ventanas en RF-07 a RF-09, agregación en RF-10 y RF-11.
- Bronze: RF-01, RF-02, RF-04. Silver: RF-05, RF-06. Gold: RF-10, RF-11.
- Orquestación: RF-12.
- Componente libre: candidatos RF-08, RF-11 y RF-13. Lo decide el ADR-4.

**Nota para RNF y ADR-1:** RF-05 elimina duplicados porque la **fuente** los genera (la app reenvía eventos cuando pierde conexión). Eso aplica sin importar la garantía de entrega que se elija.

---

## 6. Equipo y reparto del E1

| Integrante | Nombre | Rol | Escribe en `e1_tiendacol.md` |
|---|---|---|---|
| **P1** | Juan Simón Ospina Martínez (código 1000341990) | Negocio y requisitos funcionales | Portada, Sección 1, Sección 2.1, Anexo A |
| **P2** | _(por definir)_ | Calidad y streaming | Sección 2.2 (RNF), ADR-1, ADR-2 |
| **P3** | _(por definir)_ | Arquitectura | Sección 3 (diagrama + tabla de capas), ADR-3 |
| **P4** | Juan José Díaz Rodríguez | Componentes y plan | ADR-4, ADR-5, ADR-6 (opcional), Sección 5, repo y PR |

Al final hay **revisión cruzada** (P1 → P2, P2 → P3, P3 → P4, P4 → P1) usando la checklist del comentario final de `e1_tiendacol.md`.

**Nota:** el reparto original menciona "Delta Lake" (ADR-3) y "Airflow" (ADR-5) porque son las **referencias del curso**. **No son decisiones tomadas:** cada ADR debe comparar alternativas de verdad y el equipo elige.

---

## 7. Decisiones técnicas (ADRs): TODAS PENDIENTES

| ADR | Decisión | Opciones a evaluar | Conceptos del curso a citar | Responsable | Estado |
|---|---|---|---|---|---|
| ADR-1 | Motor de streaming y garantía de entrega | Kafka, Kinesis, Redpanda | at-most/at-least/exactly-once, particiones, retención | Integrante P2 | **Decidido por el equipo (2026-09-29): Kafka con at-least-once.** Falta redactarlo. Kinesis queda descartado por el ADR-6 (cobra por shard-hora) |
| ADR-2 | Motor de procesamiento | Spark Structured Streaming, Flink, batch puro | micro-batch vs por evento, checkpoints, watermarks, ventanas | Integrante P2 | **Decidido por el equipo (2026-09-29): Spark.** Falta redactarlo. Ojo: con at-least-once, los jobs de RF-07 a RF-09 leen de Kafka antes de Silver y también tienen que eliminar duplicados por identificador de evento |
| ADR-3 | Formato de Gold y modelo dimensional | Delta Lake, Iceberg | star schema, grano, ACID, schema evolution | Integrante P3 | Pendiente. Por el ADR-6, Gold vive en S3: Delta Lake e Iceberg siguen siendo opciones |
| ADR-4 | Componente libre y su posición CAP | MongoDB, Cassandra, DynamoDB, Redis, Neo4j, Trino/Athena… | CAP (CP vs AP), sharding, partition key | Integrante P4 | **Escrito (2026-09-29): DynamoDB bajo demanda para el RF-08, AP, partition key `user_id`.** Falta confirmar que el Learner Lab permita crear tablas; plan B, MongoDB |
| ADR-5 | Orquestación y dependencias del DAG | Airflow, Dagster, Prefect | DAG, dependencias, reintentos, idempotencia | Integrante P4 | **Escrito (2026-09-29): Airflow con `LocalExecutor`, tres DAG.** Falta validarlo con el equipo |
| ADR-6 *(opcional)* | Plataforma | AWS, GCP, local con Docker | costo, reproducibilidad, servicios gestionados | Integrante P4 | **Escrito (2026-09-29): AWS Academy, híbrido.** Contenedores en EC2 para lo que cobraría por hora, S3 y servicios por uso para el resto |

**Cuando el equipo tome una decisión:** actualizar la columna "Estado" de esta tabla con la opción elegida y la fecha, y escribir el ADR en el documento.

**Restricciones que ya condicionan las decisiones:**
- Tiene que haber Spark en al menos una transformación no trivial. Si se elige Flink para el streaming, Spark debe aparecer en otra parte.
- "Batch puro" no puede resolver el flujo en tiempo real: el enunciado lo prohíbe.

**Punto de partida para el modelo de Gold (no es decisión):**
- Hechos candidatos: ventas por línea de orden; eventos del embudo.
- Dimensiones candidatas: cliente, producto, categoría, vendedor, fecha/hora, ubicación (ciudad/departamento), dispositivo/canal.
- **Pregunta abierta para el ADR-3:** de dónde sale la ciudad de una sesión anónima (P4).

---

## 8. Fuentes de datos

| Fuente (sistema de TiendaCol) | Contenido | Formato | Frecuencia |
|---|---|---|---|
| Clickstream web y app | Los 6 tipos de evento de §4 | JSON | Continuo |
| Base de datos de órdenes | Órdenes, líneas, pagos, estado del envío | Tablas relacionales | Continuo |
| Catálogo | Producto, categoría, precio, vendedor, atributos (varían por categoría) | CSV / JSON | Diario |
| Inventario | Stock por producto y bodega | Tabla / eventos | Cada cambio |
| Clientes y vendedores | Datos maestros (ciudad, segmento, fecha de registro) | Tablas | Diario |

### 8.1 Datasets para simular las fuentes en E2 (enlaces verificados el 2026-09-29)

| Dataset | Enlace | Qué fuente de TiendaCol simula | Tamaño | Licencia / condiciones de uso |
|---|---|---|---|---|
| **Brazilian E-Commerce Public Dataset by Olist** | https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce | Base de órdenes (órdenes, líneas, pagos, estado de envío), catálogo y maestros de clientes y vendedores (RF-02, RF-04) | ≈ 126 MB; ≈ 100.000 órdenes reales anonimizadas de Brasil, 2016–2018 | **CC BY-NC-SA 4.0**: uso no comercial, citar la fuente, obras derivadas con la misma licencia |
| **REES46: eCommerce behavior data from multi category store** | https://www.kaggle.com/datasets/mkechinov/ecommerce-behavior-data-from-multi-category-store | Clickstream (RF-01) | ≈ 14,7 GB en Kaggle (octubre y noviembre de 2019, ≈ 110 millones de eventos). Los meses de diciembre de 2019 a abril de 2020 están en un servidor externo | Uso libre **citando la fuente**: enlace a la página de Kaggle y a REES46 (https://rees46.com/) |
| **REES46: eCommerce events history in cosmetics shop** *(alternativa liviana)* | https://www.kaggle.com/datasets/mkechinov/ecommerce-events-history-in-cosmetics-shop | Clickstream, si el anterior es muy pesado para los portátiles | ≈ 2,3 GB; ≈ 20 millones de eventos, octubre de 2019 a febrero de 2020 | Mismas condiciones que REES46 |
| **Faker (Python), locale `es_CO`** | https://faker.readthedocs.io/en/master/locales/es_CO.html | Generador propio para la demo en vivo: nombres, departamentos y municipios colombianos | Librería | MIT |

- **Catálogo completo de datasets de REES46:** https://rees46.com/en/datasets
- **Descarga por línea de comandos** (requiere una cuenta de Kaggle y su token de API):
  - `kaggle datasets download -d olistbr/brazilian-ecommerce`
  - `kaggle datasets download -d mkechinov/ecommerce-behavior-data-from-multi-category-store`
- Los datasets **no se suben a git**: van en `data/` (ver §10).

### 8.2 Brechas conocidas entre los datasets y TiendaCol

Son hechos, no decisiones. Cómo resolverlas se decide en E2.

- **Tipos de evento.** REES46 trae `view`, `cart`, `remove_from_cart` y `purchase` según su descripción (revisar qué tipos trae cada mes). **No trae `search` ni `checkout_start`**, que TiendaCol sí tiene (§4), así que habría que generarlos.
- **Geografía.** Olist trae ciudades y estados de Brasil y REES46 no trae ubicación. Para las ciudades colombianas de P4 y P5 hay que mapear o generar los datos (Faker `es_CO` tiene `department()` y `municipality()`).
- **Inventario.** Ningún dataset trae stock por producto y bodega (RF-03); hay que generarlo.
- **Identificadores.** Olist y REES46 no comparten IDs de producto ni de usuario. Hay que definir cómo se relacionan (por ejemplo, por categoría) antes de hacer joins entre ellos.
- **Moneda.** Los precios no están en COP (los de Olist están en reales brasileños); hay que convertirlos o reescalarlos.

No son parte del E1: allí la "Fuente" del diagrama son los sistemas de TiendaCol, no los datasets.

---

## 9. Reglas para agentes de IA

### 9.1 Qué NO puede inventar un agente

Si falta alguno de estos datos, **preguntarle al humano** o dejar el marcador `[...]` con un comentario `<!-- PENDIENTE: ... -->`. Nunca llenarlo con algo que "suena plausible".

- **La herramienta elegida en cualquier ADR.** El agente puede explicar y comparar opciones, pero la "Decisión" la escribe a partir de lo que el humano diga que el equipo eligió y por qué.
- Nombres y códigos de los integrantes P2, P3 y P4. Fechas exactas de S13 y S16.
- Cifras de mercado o estadísticas sin una fuente real y verificable con URL. Toda cifra externa va con su referencia numerada.
- Valores de negocio distintos a los de §4.
- Enlaces: la URL editable del diagrama y cualquier URL no verificada.
- En E2: latencias medidas, throughput real o resultados de la demo que no se hayan medido de verdad (alterar resultados de la demo es falta de integridad).

### 9.2 Cómo editar `e1_tiendacol.md`

- **Un solo archivo.** No crear archivos por sección ni borradores paralelos.
- Editar **solo la sección del integrante** con el que se trabaja. Si se detecta un error en la sección de otro, avisar al humano en vez de cambiarla.
- Reemplazar los marcadores `[...]`. Los comentarios `<!-- -->` no se ven en el PDF: se pueden conservar. No borrar los comentarios de otras secciones.
- Mantener la numeración: RF-xx, RNF-xx, ADR-x, preguntas P1–P6 y referencias [n]. Las referencias nuevas van desde la [7], al final de la lista existente.
- Si un RNF o un ADR necesita un requisito funcional nuevo, avisar al humano (la Sección 2.1 es del integrante P1) y no agregarlo por cuenta propia.
- **Formato de números colombiano:** punto para miles y coma para decimales ("COP 500.000", "70,22 %", "2,5 millones"). Moneda: COP.
- **Idioma:** español. Frases cortas y concretas. En la Sección 1, hablar del **problema de negocio**, no de herramientas.

### 9.3 Cómo escribir un ADR

- Estructura fija: **Contexto** (qué RF, pregunta o restricción lo motiva, con números de §4) · **Alternativas consideradas** (al menos 2 reales, con ventajas y desventajas **para este problema**) · **Decisión** (con conceptos del curso) · **Consecuencias** (qué se sacrifica).
- Cada ADR tiene en su comentario `<!-- -->` los conceptos a citar y las preguntas que el equipo debe poder responder. Usarlos.
- Si el humano pide "escribe mi ADR" y no dijo qué eligió el equipo: primero explicar las alternativas, luego **preguntar qué eligieron y por qué**, y después redactar.

### 9.4 Diagrama (integrante P3)

El entregable se hace en **Draw.io o Lucidchart**. Un agente puede ayudar a listar las cajas, sus etiquetas y las flechas, o hacer un borrador en texto o Mermaid para discutir, pero no reemplaza el diagrama. Cada caja debe llevar la herramienta concreta y los ID de los RF que cumple (tabla de la Sección 3 del documento).

### 9.5 Explicar todo

Cada integrante debe poder defender cualquier parte. Todo texto o código generado se acompaña de su porqué, con conceptos del curso: CAP, garantías de entrega, ventanas, watermarks, particionamiento, modelo dimensional, grano, schema evolution, idempotencia.

### 9.6 Bitácora

El equipo decidió dejar [docs/bitacora_ia.md](docs/bitacora_ia.md) **vacía durante el E1** y llenarla en E2. **No escribir en ella.**

Al terminar una tarea relevante, darle al humano en el chat un resumen de 2–3 líneas para que lo guarde: fecha, integrante, herramienta, tarea delegada, qué produjo el agente y qué decidió el equipo. En E2 se usará este formato:

```markdown
## AAAA-MM-DD — [Integrante] — [Herramienta: Claude / ChatGPT / Copilot…]
- **Tarea delegada:** qué se le pidió al agente
- **Qué produjo el agente:** resumen
- **Qué decidió / modificó el equipo:** qué se aceptó, qué se cambió y por qué
- **Archivo(s) afectados:** ruta
```

### 9.7 Git

- Remoto: `https://github.com/juansimonEAFIT/Proyecto_sistemas-Intensivos-datos.git`.
- **Flujo de ramas y PR: acordado el 2026-09-29, detallado en [CONTRIBUTING.md](CONTRIBUTING.md).** Lo coordina el integrante P4. Resumen: `main` solo recibe entregas; el E1 se escribe directo en la rama `e1`; el código del E2 va en ramas `p<n>/<tema>` que entran por PR a `e2`, y cada PR lo aprueba otro integrante. El PR `e1 → main` es el que pide la guía para el E1, y el PR `e2 → main` es el "PR final con todo el código" de S16.
- Antes de editar, confirmar en qué rama se está: el documento del E1 se edita en `e1`, nunca en `main`.
- No hacer commit, push ni abrir PRs. El agente le entrega al humano los comandos y el mensaje de commit, y el humano los ejecuta.
- La carpeta local está dentro de OneDrive. Si varias personas trabajan a la vez, es más seguro que cada una clone el repo en una carpeta fuera de OneDrive.

---

## 10. Estructura del repositorio

Las carpetas y archivos marcados con **(E2)** ya existen como **marcadores de posición**: cada carpeta tiene un `README.md` que dice para qué sirve y qué RF cubre, y `docker-compose.yml` no define servicios todavía. Todavía no hay código. Los nombres pueden cambiar cuando el equipo elija las herramientas en los ADR; si cambian, actualizar este árbol. La rúbrica del E2 pide "carpetas organizadas por componente", un README para correr todo desde cero y un `docker-compose.yml` o equivalente en la raíz.

```
/
├── CLAUDE.md                      # este archivo: fuente de verdad para humanos y agentes
├── CONTRIBUTING.md                # flujo de ramas y PR del equipo (ver §9.7)
├── README.md                      # descripción; en E2, cómo correr el pipeline desde cero
├── .github/
│   └── pull_request_template.md   # plantilla que GitHub carga al abrir un PR
├── docker-compose.yml             # (E2) levanta todos los servicios, o su equivalente según el ADR-6
├── .env.example                   # (E2) variables de configuración, sin secretos
├── .gitignore                     # (E2) excluye data/, credenciales y archivos temporales
├── docs/
│   ├── entregable1/
│   │   ├── e1_tiendacol.md        # documento E1 completo (fuente del PDF)
│   │   ├── e1_tiendacol.pdf       # (pendiente) exportación final
│   │   └── arquitectura.png       # (pendiente, integrante P3) o .svg
│   ├── entregable2/               # slides de E2 (máx. 15)
│   └── bitacora_ia.md             # vacía hasta E2 (ver §9.6); OBLIGATORIA en E2 (sin ella: -10 %)
├── data/                          # (E2) datasets descargados de §8.1; NO se suben a git
│   └── sample/                    # (E2) muestra pequeña para pruebas y demo (esta sí se puede subir)
├── generator/                     # (E2) simulador de eventos para la demo en vivo (Fuente)
├── ingestion/                     # (E2) de las fuentes al transporte y a Bronze · RF-01 a RF-04
├── processing/
│   ├── streaming/                 # (E2) jobs en tiempo real · RF-07, RF-08, RF-09
│   └── batch/                     # (E2) Bronze → Silver → Gold · RF-05, RF-06, RF-10, RF-11, RF-13
├── orchestration/                 # (E2) DAG(s) del orquestador · RF-12
├── serving/                       # (E2) componente libre, alertas, tableros y consultas sobre Gold · consumo de RF-07 a RF-09 y RF-11
└── tests/                         # (E2) pruebas de la columna "Cómo se verifica" de cada RF
```

Relacionar cada carpeta con sus RF ayuda a cumplir un criterio de la rúbrica del E2: "el diagrama final es coherente con el código". Si una carpeta no cumple ningún RF, o un RF no tiene carpeta, algo falta o sobra.

---

## 11. Glosario rápido

- **Streaming:** procesar los datos a medida que llegan.
- **Micro-batch / por evento:** procesar en lotes pequeños cada pocos segundos (Spark Structured Streaming) o cada evento al llegar (Flink).
- **Ventana (tumbling / sliding / session):** fija sin traslape, deslizante con traslape, o cerrada por inactividad.
- **Watermark:** cuánto espera el motor a los eventos que llegan tarde (tiempo del evento vs tiempo de procesamiento).
- **Checkpoint:** progreso y estado guardados para reanudar tras una falla sin perder ni repetir trabajo.
- **Garantía de entrega:** *at-most-once* (se puede perder), *at-least-once* (se puede duplicar), *exactly-once* (ni se pierde ni se duplica; se logra de extremo a extremo).
- **Partición / partition key:** unidad de paralelismo y distribución. El orden solo se garantiza dentro de una partición. Una mala clave crea *hot spots*.
- **Bronze / Silver / Gold:** datos crudos / limpios y deduplicados / modelados para el negocio.
- **Delta Lake / Iceberg:** formatos de tabla abiertos con ACID, historial (*time travel*) y evolución de esquema.
- **Modelo dimensional (star schema):** tabla de hechos (lo que pasó y cuánto) rodeada de dimensiones (quién, qué, dónde, cuándo).
- **Grano:** qué representa exactamente una fila de la tabla de hechos.
- **SCD:** dimensión de cambio lento; cómo guardar la historia cuando cambia un atributo (precio, categoría).
- **Teorema CAP:** ante una partición de red, se prioriza consistencia (CP) o disponibilidad (AP). Depende de la configuración.
- **Idempotencia:** ejecutar dos veces deja el mismo resultado que ejecutar una vez.
- **DAG:** grafo de tareas con dependencias que el orquestador ejecuta en orden.
- **ADR:** registro de una decisión técnica: contexto, alternativas, decisión y consecuencias.
