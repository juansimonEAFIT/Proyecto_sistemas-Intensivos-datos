<!--
ENTREGABLE 1: documento fuente del PDF (e1_tiendacol.pdf)
Máximo 15 páginas sin anexos + diagrama en PNG/SVG. Sin código.
Todo lo que está dentro de comentarios como este NO aparece al renderizar ni al exportar: son instrucciones para el equipo.
Contexto completo, valores y reglas para agentes: CLAUDE.md (raíz del repo). En los comentarios, "Pn" solo = integrante; en el texto visible, P1–P6 = preguntas de negocio.

REPARTO Y ESTADO (integrantes)
  Integrante P1  Portada + Sección 1 + Sección 2.1 (RF) + Anexo A ............ listo para revisión
  Integrante P2  Sección 2.2 (RNF) + ADR-1 + ADR-2 ............................ pendiente
  Integrante P3  Sección 3 (diagrama) + ADR-3 .................................. pendiente
  Integrante P4  ADR-4 + ADR-5 + ADR-6 + Sección 5 (plan) ...................... pendiente

PRESUPUESTO DE PÁGINAS
  Portada (no cuenta) · 1: 1–2 · 2: 2–3 · 3: 1 · 4: 3–4 · 5: 1 · Total: 8–11 de 15

VALORES COMPARTIDOS: usar exactamente los mismos en todas las secciones (propuestos por P1, pendientes de validar con el equipo)
  Alerta de agotamiento (pregunta P1, RF-07) ...... máximo 2 min desde la venta
  Horizonte de agotamiento (pregunta P1, RF-07) ... 60 min
  Velocidad de venta (pregunta P1, RF-07) ......... últimos 15 min, recalculada cada minuto
  Carrito abandonado (pregunta P2, RF-08) ......... usuario identificado, COP 500.000 o más, 30 min sin compra ni cambios
  Publicación de la lista a Marketing (RF-08) ..... máximo 5 min después de cumplidos los 30
  Ventas por minuto (pregunta P3, RF-09) .......... visibles máximo 2 min después de cerrar el minuto
  Frescura de Gold (preguntas P4, P5, RF-10, RF-11)  máximo 1 hora
  Escala (Anexo A) ................................ 1,5 M usuarios/mes · ≈ 75 M eventos/mes · pico ≈ 3.000 ev/s · capacidad objetivo 5.000 ev/s
  P6 .............................................. dentro del alcance, como opcional (RF-13)
-->

# Universidad EAFIT

## ST1630 — Sistemas Intensivos en Datos · 2026-2

# TiendaCol en tiempo real

### Pipeline de datos para decisiones de e-commerce

**Proyecto final — Entregable 1: Diagnóstico, requisitos y arquitectura**

| | |
|---|---|
| **Nombre del proyecto** | TiendaCol en tiempo real |
| **Dominio** | E-commerce: marketplace multivendedor |
| **Profesor** | Andrés Sacre Alzate |
| **Fecha de entrega** | `[día anterior al inicio de S13]` de 2026 |
| **Repositorio** | https://github.com/juansimonEAFIT/Proyecto_sistemas-Intensivos-datos |

### Integrantes

| Nombre completo | Código EAFIT |
|---|---|
| `Juan Simón Ospina Martínez` | `1000341990` |
| `[Nombre completo P2]` | `[código]` |
| `[Nombre completo P3]` | `[código]` |
| `[Nombre completo P4]` | `[código]` |

<div style="page-break-after: always;"></div>

# 1. Definición del problema

## 1.1 Contexto

TiendaCol es un marketplace colombiano (empresa ficticia) donde vendedores independientes publican productos de tecnología, hogar, moda, belleza y deportes, y los clientes compran desde la web y la app móvil. Opera en las principales ciudades del país, tiene 1,5 millones de usuarios activos al mes y recibe cerca de 2.500 órdenes en un día normal, con un ticket promedio similar al del mercado colombiano (COP 212.373 en 2025 [2]).

Compite en un mercado que crece rápido: en 2025 el comercio electrónico en Colombia vendió COP 145,4 billones en 684,6 millones de transacciones, 19,9 % más transacciones que en 2024 [2]. La demanda tampoco es uniforme. En Black Friday, Cyber Monday y el Hot Sale [6] el tráfico se multiplica en minutos: Black Friday y Cyber Monday 2025 movieron en Colombia COP 2,6 billones y 15,8 millones de transacciones electrónicas en cuatro días, y el canal en línea representó el 27 % de las ventas de Black Friday y el 37 % de las de Cyber Monday [3].

## 1.2 El problema de negocio

Hoy TiendaCol toma decisiones con reportes que salen **al día siguiente** de su base de datos transaccional. Eso le cuesta ventas en tres frentes:

1. **Productos que se agotan sin aviso durante los picos.** Un producto en tendencia que vende 5 unidades por minuto agota 300 unidades en una hora. Con reportes del día siguiente, Operaciones se entera cuando ya no puede reabastecer, avisar al vendedor ni pausar la publicidad, que sigue llevando clientes a un producto sin stock. Dos de cada tres compradores que encuentran un producto agotado terminan comprando en otra tienda [4].
2. **Carritos abandonados que nadie recupera a tiempo.** El 70,22 % de los carritos de compra en línea se abandonan [1]. A esa tasa, las 2.500 órdenes diarias de TiendaCol implican unos 5.900 carritos abandonados por día. Si cada uno vale en promedio lo mismo que una orden, son cerca de COP 1.250 millones diarios. La industria recomienda enviar el primer recordatorio dentro de la primera hora [5], pero Marketing hoy solo puede enviarlo al día siguiente. Recuperar apenas el 5 % de ese valor (supuesto ilustrativo) equivaldría a unos COP 1.900 millones al mes.
3. **Un embudo de compra que no se entiende.** No se sabe en qué paso (ver producto → agregar al carrito → pagar) se pierden los clientes, ni cómo cambia por categoría, ciudad o dispositivo. Comercial decide dónde invertir en promociones sin saber dónde está la fuga.

## 1.3 Usuarios del sistema y decisiones que toman

| Usuario | Qué necesita | Qué decide con los datos | Urgencia |
|---|---|---|---|
| **Operaciones / inventario** | Alertas de productos que se agotarán en la próxima hora | Reabastecer desde bodega, avisar al vendedor, pausar la publicidad del producto | Minutos |
| **Marketing / CRM** | Lista de carritos abandonados de alto valor | Enviar un recordatorio o un cupón mientras el cliente sigue interesado | Menos de 1 hora |
| **Category managers / Comercial** | Ventas, conversión y ticket promedio por categoría, vendedor, ciudad y día | Qué categorías promocionar, qué vendedores apoyar, dónde invertir | Horas / diaria |
| **Dirección** | Indicadores del negocio y ventas por minuto durante los eventos | Metas, presupuesto, ajuste de campañas en curso y evaluación posterior | Minutos (en eventos) / diaria |

## 1.4 Preguntas que el sistema debe responder

**Operacionales (tiempo real)**

- **P1.** ¿Qué productos se agotarán en los próximos **60 minutos** si mantienen su velocidad de venta de los últimos **15 minutos**? La alerta debe llegar a Operaciones en máximo **2 minutos** desde la venta que la dispara.
- **P2.** ¿Qué usuarios identificados dejaron un carrito con valor de **COP 500.000 o más** (unas 2,4 veces el ticket promedio del mercado [2]) sin comprar ni modificar el carrito durante **30 minutos**? La lista debe estar disponible para Marketing en máximo **5 minutos** después de cumplirse los 30, para que el recordatorio salga dentro de la primera hora [5].
- **P3.** ¿Cuántas órdenes y cuántos pesos se venden **por minuto**, en total y por categoría, durante un evento de descuentos? Cada minuto debe verse a más tardar **2 minutos** después de terminado.

**Analíticas**

- **P4.** ¿Cuál es la tasa de conversión del embudo vista de producto → carrito → compra por categoría, dispositivo (web de escritorio, web móvil, app) y ciudad, **por hora y por día**? Los datos deben tener como máximo **1 hora** de antigüedad.
- **P5.** ¿Cuáles son las ventas totales, el número de órdenes y el ticket promedio por categoría, vendedor, región y fecha? Mismo requisito de frescura: **1 hora**.
- **P6 (opcional).** ¿Qué pares de productos se compran juntos (misma orden) o se ven juntos (misma sesión) con más frecuencia? Se actualiza **una vez al día**.

## 1.5 Por qué no basta una base de datos relacional

El volumen por sí solo no es el argumento. TiendaCol genera cerca de 75 millones de eventos de navegación al mes, alrededor de 1 TB de datos crudos al año (Anexo A), y una base relacional grande podría almacenarlos. Lo que la descarta es la **combinación** de cuatro condiciones:

- **Velocidad y picos.** El tráfico pasa de unos 29 eventos por segundo en un día normal a unos 3.000 en la apertura de ofertas de Black Friday, es decir, unas **100 veces más**. Un servidor dimensionado para el pico queda ocioso el resto del año; el sistema necesita escalar horizontalmente solo cuando hace falta.
- **Cargas que compiten entre sí.** La base transaccional es la que cobra. Las consultas de P4 y P5 recorren cientos de millones de eventos, y correrlas ahí durante un pico frenaría el pago justo cuando más se vende. Por eso los reportes de hoy corren de noche, y por eso llegan con un día de retraso.
- **Variedad.** Conviven órdenes y pagos estructurados, eventos JSON cuyos campos cambian según el tipo de evento y la versión de la app, y atributos de producto distintos por categoría (tallas en moda, especificaciones técnicas en tecnología). Un esquema rígido obligaría a migraciones constantes.
- **Tiempo real.** P1, P2 y P3 pierden su valor si la respuesta tarda horas. Exigen calcular de forma continua sobre flujos de eventos, en ventanas de minutos, y no consultar periódicamente tablas ya guardadas.

# 2. Requisitos funcionales y no funcionales

## 2.1 Requisitos funcionales

Cada requisito indica a qué pregunta de negocio (Sección 1.4) responde, en qué capa del diagrama de arquitectura (Sección 3) se cumple y cómo se verifica. Los umbrales de negocio (COP 500.000, 30 minutos, etc.) son parámetros configurables.

| ID | Requisito | Trazabilidad | Cómo se verifica |
|---|---|---|---|
| **RF-01** | El sistema debe **ingestar** en tiempo real los eventos de navegación de la web y la app (`page_view`, `search`, `add_to_cart`, `remove_from_cart`, `checkout_start`, `purchase`) y **conservarlos** sin modificar en la capa Bronze, junto con su fecha y hora de ingestión. | P1–P4, P6 · Fuente → Ingestión → Bronze | Se envían 10.000 eventos de prueba con identificador único; los 10.000 aparecen en Bronze con contenido idéntico al enviado. |
| **RF-02** | El sistema debe **capturar** de la base de datos transaccional las órdenes, las líneas de orden, los pagos y los cambios de estado de envío, y llevarlos a la capa Bronze. | P3, P5 · Fuente → Ingestión → Bronze | Se crean 100 órdenes de prueba y se cambia el estado de envío de 20; Bronze contiene las 100 órdenes con sus líneas y pagos, y los 20 cambios. |
| **RF-03** | El sistema debe **recibir** cada cambio de stock por producto y bodega y **mantener** el stock disponible actual de cada producto. | P1 · Fuente → Ingestión → Procesamiento | Tras 50 cambios de stock de prueba, el stock disponible que reporta el sistema coincide con el de la fuente para todos los productos afectados. |
| **RF-04** | El sistema debe **cargar** cada día, antes de las 6:00 a. m. (hora de Colombia), el catálogo de productos (CSV/JSON) y los datos maestros de clientes y vendedores. | P4, P5 · Fuente → Ingestión por lotes → Bronze | A las 6:00 a. m. el número de productos, clientes y vendedores cargados coincide con el de los archivos fuente del día. |
| **RF-05** | El sistema debe **validar** cada registro contra su esquema esperado, **apartar** en una zona de cuarentena los que no lo cumplan sin detener el procesamiento, y **eliminar** los eventos duplicados (mismo identificador de evento). | Todas · Procesamiento Bronze → Silver | En un lote de 10.000 eventos con 100 malformados y 100 duplicados, Silver queda con 9.800 eventos únicos, la cuarentena con 100 y el procesamiento no se detiene. |
| **RF-06** | El sistema debe **enriquecer** cada evento y cada línea de orden con la categoría, el vendedor y el precio del producto (catálogo), y con la ciudad y el departamento del cliente (datos maestros). | P1–P5 · Procesamiento Silver | En una muestra de 1.000 registros de Silver, categoría, vendedor y ciudad coinciden con el catálogo y los maestros vigentes. |
| **RF-07** | El sistema debe **calcular** cada minuto la velocidad de venta de cada producto (unidades vendidas en los últimos 15 minutos) y **generar una alerta** para Operaciones cuando el stock disponible alcance para menos de 60 minutos a esa velocidad. La alerta incluye producto, vendedor, stock, velocidad y tiempo estimado de agotamiento, y llega en máximo 2 minutos desde la venta que la dispara. | P1 · Procesamiento en tiempo real → Consumo (alertas) | Se simulan ventas a velocidad constante de un producto con stock conocido; se calcula a mano la venta con la que la cobertura baja de 60 minutos, y la alerta llega máximo 2 minutos después de esa venta. |
| **RF-08** | El sistema debe **identificar** los carritos abandonados de alto valor (carritos de usuarios identificados con valor de COP 500.000 o más, sin compra ni cambios durante 30 minutos) y **publicar** la lista para Marketing (usuario, productos, valor, hora del último evento) en máximo 5 minutos después de cumplirse los 30. | P2 · Procesamiento en tiempo real → Consumo (Marketing) | Se simulan 3 sesiones: carrito de COP 600.000 sin compra (aparece entre el minuto 30 y el 35), carrito de COP 600.000 con compra en el minuto 20 (no aparece) y carrito de COP 300.000 sin compra (no aparece). |
| **RF-09** | El sistema debe **calcular** para cada minuto el número de órdenes y el valor vendido en COP, en total y por categoría, y **mostrarlo** en un tablero de monitoreo máximo 2 minutos después de terminado ese minuto. | P3 · Procesamiento en tiempo real → Consumo (tablero de eventos) | Se envía un número conocido de compras de prueba en un mismo minuto; el tablero muestra exactamente ese número y ese valor dentro de los 2 minutos siguientes. |
| **RF-10** | El sistema debe **calcular** la tasa de conversión del embudo vista de producto → carrito → compra (proporción de sesiones que pasan de cada etapa a la siguiente) por categoría, dispositivo y ciudad, por hora y por día, y **publicarla** en la capa Gold máximo 1 hora después de terminada cada hora. | P4 · Procesamiento Silver → Gold | Con un conjunto de prueba con conteos conocidos de sesiones por etapa, la consulta a Gold devuelve las mismas tasas calculadas a mano. |
| **RF-11** | El sistema debe **calcular** las ventas totales, el número de órdenes y el ticket promedio por categoría, vendedor, región (ciudad y departamento) y fecha en un modelo dimensional de la capa Gold, **consultable** con SQL y desde un tablero para Comercial y Dirección, con datos de máximo 1 hora de antigüedad. | P5 · Gold → Consumo (tablero) | Para un día de prueba, el total de ventas y de órdenes en Gold coincide exactamente con el de la base transaccional, y cada cifra del tablero coincide con la consulta directa a Gold. |
| **RF-12** | El sistema debe **ejecutar** automáticamente, en el orden de sus dependencias, los procesos programados (carga diaria de catálogo y maestros, Bronze → Silver, Silver → Gold); si un paso falla, **no ejecutar** los pasos que dependen de él y **notificar** la falla. | Todas · Orquestación (transversal) | Se fuerza una falla en la carga del catálogo; los pasos dependientes no se ejecutan y se genera una notificación. Al corregir y reintentar, el flujo termina completo sin intervención manual. |
| **RF-13** *(opcional, P6)* | El sistema debe **identificar** diariamente, para cada producto, los 10 productos que más se compran en la misma orden y los 10 que más se ven en la misma sesión. | P6 · Procesamiento → Gold o componente libre | Con un conjunto de prueba donde A y B aparecen juntos en 50 órdenes y ningún otro producto aparece con A en más de 10, B figura de primero en la lista de A. |

## 2.2 Requisitos no funcionales

<!--
P2: cada requisito debe tener un valor concreto y decir cómo se mide. La guía pide citar explícitamente los conceptos del curso:
  Escalabilidad ....... "soportar un pico de X eventos/s sin degradación" (valor compartido: 5.000 ev/s, Anexo A)
  Disponibilidad ...... posición CAP y su justificación (CP vs AP). Se decide por componente, no para todo el sistema.
  Consistencia ........ qué garantía de entrega (at-most-once / at-least-once / exactly-once) y EN QUÉ PARTE del pipeline. Puede ser distinta por flujo.
  Latencia ............ tiempo máximo desde el evento hasta Gold. Separar el tiempo real (2 min: RF-07, RF-09) de la frescura analítica (1 h: RF-10, RF-11).
  Tolerancia a fallos . qué pasa si un nodo falla y cómo se recupera (tiempo máximo sin servicio, si se pierden o se reprocesan eventos).
  Trazabilidad ........ cómo se audita el linaje de un dato desde la fuente hasta Gold (id del evento, fecha de ingestión, fuente).
Rúbrica (15 %): para el 100 % deben estar CAP, garantía de entrega, latencia, escalabilidad y tolerancia a fallos, con valores concretos.
Nota: RF-05 elimina duplicados porque la FUENTE los genera (la app reenvía eventos cuando pierde conexión), sin importar la garantía que elija el ADR-1.
-->

| ID | Categoría | Requisito | Valor concreto | Cómo se mide |
|---|---|---|---|---|
| RNF-01 | Escalabilidad | `[...]` | `[...]` | `[...]` |
| RNF-02 | Disponibilidad (CAP) | `[...]` | `[...]` | `[...]` |
| RNF-03 | Consistencia (garantía de entrega) | `[...]` | `[...]` | `[...]` |
| RNF-04 | Latencia | `[...]` | `[...]` | `[...]` |
| RNF-05 | Tolerancia a fallos | `[...]` | `[...]` | `[...]` |
| RNF-06 | Trazabilidad | `[...]` | `[...]` | `[...]` |

# 3. Diagrama de arquitectura de datos por capas

<!--
P3: un solo diagrama con las 5 capas, exportado en PNG/SVG de alta resolución como docs/entregable1/arquitectura.png (o .svg), más el enlace editable de Draw.io o Lucidchart.
La guía pide mostrar en cada capa:
  Fuente .......... sistemas origen, con su formato y frecuencia
  Ingestión ....... mecanismo de transporte y garantía de entrega
  Procesamiento ... transformaciones y qué cambia entre la entrada y la salida
  Almacenamiento .. Bronze, Silver y Gold con el motor de cada una y el modelo de Gold (star schema)
  Consumo ......... cómo consumen los usuarios (tablero, alertas, SQL, API)
Cada caja debe tener el nombre de la herramienta concreta ("Delta Lake en S3", no "base de datos").
Para que los RF sean "trazables al diagrama", anotar sobre cada caja los ID de los RF que cumple (ver la tabla de abajo).
Rúbrica (25 %): legible sin explicación adicional. Si necesita más de 2 minutos de explicación, le falta claridad.
-->

**Enlace editable:** `[URL de Draw.io / Lucidchart]`

![Diagrama de arquitectura de TiendaCol](arquitectura.png)

| Capa | Componentes (herramienta concreta) | Qué hace | RF que cumple |
|---|---|---|---|
| Fuente | `[...]` | `[...]` | RF-01, RF-02, RF-03, RF-04 |
| Ingestión | `[...]` | `[...]` | RF-01, RF-02, RF-03, RF-04 |
| Procesamiento | `[...]` | `[...]` | RF-05, RF-06, RF-07, RF-08, RF-09, RF-10, RF-13 |
| Almacenamiento: Bronze | `[...]` | `[...]` | RF-01, RF-02, RF-04 |
| Almacenamiento: Silver | `[...]` | `[...]` | RF-05, RF-06 |
| Almacenamiento: Gold | `[...]` | `[...]` | RF-10, RF-11, RF-13 |
| Consumo | `[...]` | `[...]` | RF-07, RF-08, RF-09, RF-11 |
| Orquestación (transversal) | `[...]` | `[...]` | RF-12 |

# 4. Justificación de decisiones técnicas (ADRs)

<!--
Rúbrica (25 %): al menos 5 ADRs completos con contexto, alternativas, decisión y consecuencias, y cada ADR debe citar conceptos del curso.
Las 5 decisiones mínimas que pide la guía son ADR-1 a ADR-5. El ADR-6 es opcional, pero conviene decidirlo temprano porque limita a los demás (Kinesis y Athena solo existen en AWS).
"Alternativas consideradas" debe decir por qué se descartó cada opción PARA ESTE PROBLEMA, no en general.
"Consecuencias" debe decir qué se sacrifica.
-->

## ADR-1. Motor de streaming y garantía de entrega

<!--
Responsable: P2
Insumos para el contexto: clickstream JSON continuo · pico de 5.000 ev/s (Anexo A) · RF-01, RF-07, RF-08 y RF-09 exigen tiempo real · el enunciado prohíbe simular el streaming con batch.
Conceptos a citar:
  Garantías: at-most-once (se puede perder, no se duplica) · at-least-once (no se pierde, se puede duplicar) · exactly-once (de extremo a extremo: fuente re-leíble + checkpoints + destino idempotente o transaccional; no es solo del broker).
  Particiones: unidad de paralelismo; el orden solo se garantiza dentro de una partición; la clave del mensaje decide la partición.
  Retención: permite reprocesar (replay) después de un error.
Preguntas que deben poder responder:
  1. Por tipo de evento, ¿qué es peor: perderlo o duplicarlo? (un purchase duplicado infla la velocidad de venta de RF-07; un add_to_cart perdido esconde un carrito de RF-08)
  2. ¿Qué garantía se configura y en qué punto se logra?
  3. ¿Qué clave de partición? (RF-07 agrupa por producto, RF-08 por usuario; cuidado con las particiones "calientes" de un producto en tendencia)
  4. ¿Cuántas particiones para 5.000 ev/s y por qué?
  5. ¿Cuánta retención?
  6. ¿Está atado a una plataforma (ADR-6)?
-->

**Contexto.** `[...]`

**Alternativas consideradas.**

| Alternativa | Ventajas para este problema | Desventajas / por qué se descarta |
|---|---|---|
| Kafka | `[...]` | `[...]` |
| Kinesis | `[...]` | `[...]` |
| Redpanda | `[...]` | `[...]` |

**Decisión.** `[...]`

**Consecuencias.** `[...]`

## ADR-2. Motor de procesamiento

<!--
Responsable: P2
Insumos para el contexto: RF-07 (ventana de 15 min), RF-08 (30 min sin actividad), RF-09 (por minuto), RF-06 (join con catálogo y maestros), RF-10 y RF-11 (agregaciones). Latencias de 2 min y 1 h.
El enunciado exige Spark en al menos una transformación no trivial (join, ventanas o agregación).
Conceptos a citar:
  Micro-batch vs por evento: Spark Structured Streaming procesa en lotes pequeños (latencia de segundos); Flink procesa evento a evento (latencia de milisegundos).
  Checkpoints: guardan offsets y estado para reanudar sin perder ni repetir trabajo.
  Ventanas: tumbling (RF-09), sliding (RF-07), session (RF-08).
  Watermarks: cuánto esperar los eventos tardíos (tiempo del evento vs tiempo de procesamiento; la app móvil puede enviar eventos con minutos de retraso).
Preguntas que deben poder responder:
  1. ¿Micro-batch cumple los 2 min con margen?
  2. ¿Qué ventana y qué tamaño usa cada RF?
  3. ¿Qué watermark y por qué?
  4. RF-08 detecta la AUSENCIA de un purchase: ¿cómo se expresa eso en el motor?
  5. ¿Qué pasa si el job se cae a mitad de un pico? ¿Dónde viven los checkpoints?
  6. Si eligen Flink, ¿dónde queda Spark?
  7. Batch puro no sirve para el tiempo real (lo prohíbe el enunciado): expliquen por qué se descarta y si sirve en otra parte del pipeline.
-->

**Contexto.** `[...]`

**Alternativas consideradas.**

| Alternativa | Ventajas para este problema | Desventajas / por qué se descarta |
|---|---|---|
| Spark Structured Streaming | `[...]` | `[...]` |
| Flink | `[...]` | `[...]` |
| Batch puro | `[...]` | `[...]` |

**Decisión.** `[...]`

**Consecuencias.** `[...]`

## ADR-3. Formato de la capa Gold y modelo dimensional

<!--
Responsable: P3
La guía pide justificar el motor de Gold y POR QUÉ el modelo dimensional es adecuado para el caso.
Insumos para el contexto: RF-10 (P4) y RF-11 (P5) · variedad de datos (JSON, atributos por categoría) · catálogo que cambia cada día.
  Hechos candidatos: ventas por línea de orden; eventos del embudo.
  Dimensiones candidatas: cliente, producto, categoría, vendedor, fecha/hora, ubicación, dispositivo/canal.
Conceptos a citar: ACID (streaming y batch escriben en las mismas tablas) · schema evolution · time travel · star schema · grano.
Preguntas que deben poder responder:
  1. ¿Cuál es el grano de cada tabla de hechos?
  2. ¿Qué medidas se pueden sumar? (el ticket promedio NO se suma: es ventas / órdenes)
  3. ¿Cómo responde el modelo a P4 y P5? Explíquenlo en palabras; si no se puede, falta algo.
  4. El precio y la categoría cambian: ¿se guarda el precio pagado en el hecho? ¿Hay historia en la dimensión (SCD)?
  5. ¿Qué se hace en Silver y qué en Gold?
  6. ¿Qué motores leen Gold y son compatibles con el formato?
  7. ¿Cómo se particiona físicamente (por fecha)?
  8. En P4 "por ciudad": ¿de dónde sale la ciudad de una sesión anónima?
-->

**Contexto.** `[...]`

**Alternativas consideradas.**

| Alternativa | Ventajas para este problema | Desventajas / por qué se descarta |
|---|---|---|
| Delta Lake | `[...]` | `[...]` |
| Iceberg | `[...]` | `[...]` |

**Decisión.** `[formato elegido + modelo dimensional: tablas de hechos con su grano y dimensiones]`

**Consecuencias.** `[...]`

## ADR-4. Componente libre

<!--
Responsable: P4
La guía pide justificar la elección y su POSICIÓN CAP en el contexto del problema.
Candidatos que ya aparecen en los RF: servir la lista de RF-08 a Marketing, las consultas de RF-11 o los pares de RF-13 (P6).
Conceptos a citar:
  CAP: la clasificación depende de la configuración (nivel de consistencia en Cassandra, write/read concern en MongoDB); citen la configuración, no solo la etiqueta.
  Sharding · partition key (se elige a partir de las consultas que se van a hacer; una mala clave crea hot spots).
Preguntas que deben poder responder:
  1. ¿Qué RF o usuario lo necesita, y por qué el lakehouse solo no basta?
  2. ¿Cuál es el patrón de acceso? (búsqueda por clave con baja latencia, SQL analítico, recorrido de relaciones)
  3. Para ese uso, ¿qué es peor: un dato algo desactualizado o no responder? (AP vs CP)
  4. ¿Qué partition key y qué consulta la motiva?
  5. ¿Quién alimenta el componente y con qué frecuencia?
  6. Si es un motor de consulta (Trino/Athena), CAP aplica menos: justifiquen con separación de cómputo y almacenamiento, formatos soportados y costo por datos escaneados.
-->

**Contexto.** `[...]`

**Alternativas consideradas.**

| Alternativa | Ventajas para este problema | Desventajas / por qué se descarta |
|---|---|---|
| MongoDB | `[...]` | `[...]` |
| Cassandra | `[...]` | `[...]` |
| Redis | `[...]` | `[...]` |
| Neo4j | `[...]` | `[...]` |
| Trino / Athena | `[...]` | `[...]` |

**Decisión.** `[componente + posición CAP + partition key]`

**Consecuencias.** `[...]`

## ADR-5. Orquestación

<!--
Responsable: P4
La guía pide justificar la herramienta y CÓMO SE MODELAN LAS DEPENDENCIAS DEL DAG.
Insumos para el contexto: RF-12 · fuentes diarias (RF-04) y continuas (RF-01 a RF-03) · Bronze → Silver → Gold.
Conceptos a citar: DAG · dependencias · reintentos · idempotencia (un "append" duplica filas si se reintenta; sobrescribir la partición del día o un MERGE no).
Preguntas que deben poder responder:
  1. ¿Qué tareas tiene el DAG y qué depende de qué? (se puede incluir un mini-diagrama)
  2. El streaming corre sin parar: ¿qué papel tiene el orquestador frente a él? El enunciado pide "todo el pipeline orquestado".
  3. ¿Cada tarea es idempotente? ¿Cómo?
  4. ¿Qué pasa si una tarea falla a las 3 a. m.?
  5. ¿Cómo se reprocesan días pasados (backfill)?
-->

**Contexto.** `[...]`

**Alternativas consideradas.**

| Alternativa | Ventajas para este problema | Desventajas / por qué se descarta |
|---|---|---|
| Airflow | `[...]` | `[...]` |
| Dagster | `[...]` | `[...]` |
| Prefect | `[...]` | `[...]` |

**Decisión.** `[herramienta + cómo se modelan las dependencias del DAG]`

**Consecuencias.** `[...]`

## ADR-6. Plataforma (opcional)

<!--
Responsable: P4
Conceptos a citar: servicios gestionados · reproducibilidad (el README debe permitir correr todo desde cero) · costo.
Preguntas que deben poder responder:
  1. ¿Dónde corre la demo en vivo de S16 y qué pasa si falla la red?
  2. Si es local: ¿qué portátil aguanta al mismo tiempo el broker, el procesamiento, el orquestador y el componente libre? Medirlo pronto.
  3. Si es nube: ¿qué créditos tienen, cuánto costaría un mes y cómo evitan recursos olvidados encendidos?
  4. ¿Qué condiciona en los otros ADRs?
-->

**Contexto.** `[...]`

**Alternativas consideradas.**

| Alternativa | Ventajas para este problema | Desventajas / por qué se descarta |
|---|---|---|
| AWS | `[...]` | `[...]` |
| GCP | `[...]` | `[...]` |
| Local con Docker | `[...]` | `[...]` |

**Decisión.** `[...]`

**Consecuencias.** `[...]`

# 5. Plan de implementación

<!--
Responsable: P4
La guía pide: qué componente implementa cada integrante, hitos intermedios antes de S16 y riesgos técnicos con su plan de mitigación.
Rúbrica (10 %): cronograma realista y riesgos con mitigación. Un cronograma vago o riesgos sin mitigación bajan la nota al 60 %.
Fechas del curso: S13 retroalimentación del E1 · S14 asesoría de implementación (opcional) · S16 presentación (10 min) + demo en vivo (8 min) + defensa (7 min), con el PR final abierto antes de las 11:59 p. m. del día anterior y un ensayo obligatorio ese mismo día.
Riesgos candidatos (evaluar cuáles aplican):
  los datasets son demasiado grandes para los portátiles del equipo;
  incompatibilidad de versiones entre broker, motor de procesamiento y formato de tabla;
  la demo en vivo falla por red, recursos o credenciales (¿plan B con datos precargados?);
  costos de nube por recursos que quedan encendidos;
  en la defensa le preguntan a un integrante por la parte que no implementó.
-->

## 5.1 Responsabilidades

| Integrante | Componente(s) que implementa | RF que cubre |
|---|---|---|
| `[P1]` | `[...]` | `[...]` |
| `[P2]` | `[...]` | `[...]` |
| `[P3]` | `[...]` | `[...]` |
| `[P4]` | `[...]` | `[...]` |

## 5.2 Cronograma hasta S16

| Semana | Hito | Responsable(s) | Criterio de "terminado" |
|---|---|---|---|
| S13 | `[...]` | `[...]` | `[...]` |
| S14 | `[...]` | `[...]` | `[...]` |
| S15 | `[...]` | `[...]` | `[...]` |
| S16 | Presentación, demo en vivo y defensa | Todos | PR final abierto y demo ensayada de principio a fin el día anterior |

## 5.3 Riesgos técnicos y mitigación

| Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|
| `[...]` | `[alta / media / baja]` | `[alto / medio / bajo]` | `[...]` |

<div style="page-break-after: always;"></div>

# Anexo A. Supuestos de dimensionamiento de TiendaCol

Valores supuestos para la empresa ficticia, coherentes con el mercado colombiano [2][3]. Los requisitos no funcionales (Sección 2.2) usan estas mismas cifras.

| Supuesto | Día normal | Black Friday / Cyber Monday |
|---|---|---|
| Usuarios activos al mes | 1,5 millones | — |
| Sesiones por día | 100.000 | 800.000 |
| Eventos por sesión | 25 | 30 |
| Eventos por día | 2,5 millones | 24 millones |
| Eventos por segundo, promedio del día | ≈ 29 | ≈ 280 |
| Eventos por segundo, hora pico | ≈ 55 (8 % del tráfico del día) | ≈ 1.000 (15 % del tráfico del día) |
| Eventos por segundo, minutos de apertura de ofertas | — | ≈ 3.000 (3 veces la hora pico) |
| Capacidad objetivo con margen | — | **5.000 eventos/s** |
| Conversión de sesión a orden | 2,5 % | 3 % |
| Órdenes por día | 2.500 | 24.000 |
| Ventas por día (ticket de COP 212.373 [2]) | ≈ COP 530 millones | ≈ COP 5.100 millones |
| Eventos de navegación al mes | ≈ 75 millones | — |
| Datos crudos al año (≈ 1 KB por evento) | ≈ 1 TB | — |

Como control de realismo: las ventas anuales de TiendaCol (≈ COP 194.000 millones) serían cerca del 0,13 % del comercio electrónico colombiano de 2025 [2], una escala plausible para un marketplace mediano.

# Referencias

1. Baymard Institute. *Cart Abandonment Rate Statistics* (promedio de 50 estudios, actualizado el 22 de septiembre de 2025). https://baymard.com/lists/cart-abandonment-rate
2. Cámara Colombiana de Comercio Electrónico (CCCE). *Informe de cierre ecommerce 2025, versión pública* (febrero de 2026). https://ccce.org.co/noticias/informe-de-cierre-ecommerce-2025-version-publica/
3. Infobae, con datos de Credibanco. *Black Friday y Cyber Monday 2025 dejaron ventas por encima de 2,6 billones de pesos en Colombia* (6 de diciembre de 2025). https://www.infobae.com/tecno/2025/12/06/black-friday-y-cyber-monday-2025-dejaron-ventas-por-encima-de-26-billones-de-pesos-en-colombia/
4. SGB Media, sobre la encuesta de AlixPartners (2024). *Study: Out-of-Stocks Drive 66 Percent of Consumers to Another Retailer*. https://sgbonline.com/study-out-of-stocks-drive-66-percent-of-consumers-to-another-retailer/
5. Rejoiner. *When Is the Best Time to Send an Abandoned Cart Email?* (fuente de la industria). https://www.rejoiner.com/resources/abandoned-cart-email-timing
6. Cámara Colombiana de Comercio Electrónico (CCCE). *Llega una nueva versión de Hot Sale en Colombia* (2025). https://ccce.org.co/noticias/llega-una-nueva-version-de-hotsale-en-colombia/

<!-- P2, P3 y P4: agregar aquí sus referencias, desde la [7]. -->

<!--
====================================================================
REVISIÓN CRUZADA ANTES DE EXPORTAR (P1 → P2, P2 → P3, P3 → P4, P4 → P1)
  [ ] Los valores compartidos (comentario del inicio) son iguales en todas las secciones.
  [ ] Cada RF aparece en el diagrama y cada caja del diagrama cumple algún RF.
  [ ] Cada herramienta del diagrama está justificada en un ADR o en el texto.
  [ ] Los RNF son alcanzables con lo que eligen los ADRs (p. ej., si un RNF exige exactly-once, ADR-1 y ADR-2 explican cómo se logra).
  [ ] Cada ADR compara al menos 2 alternativas de verdad y cita conceptos del curso.
  [ ] El modelo del ADR-3 responde P4 y P5.
  [ ] Se cumplen las restricciones obligatorias: streaming real, Spark no trivial, Bronze/Silver/Gold, Gold dimensional consultable, orquestación y componente libre.
  [ ] Portada con los nombres completos y los códigos EAFIT de los 4 integrantes.
  [ ] 15 páginas o menos sin anexos. Si no cabe, pasar la columna "Cómo se verifica" de la Sección 2.1 a un anexo.
  [ ] Checklist de la guía: PDF en docs/entregable1/e1_tiendacol.pdf, diagrama en docs/entregable1/arquitectura.png o .svg, enlace editable en la Sección 3 y PR abierto con la descripción del proyecto.

====================================================================
NOTAS DE DEFENSA DE P1: por qué cada valor (cualquier integrante debe poder explicarlas)

  P1, horizonte de 60 min: tiempo mínimo para actuar (mover stock, llamar al vendedor, pausar una campaña). Con 15 min no alcanza a actuar nadie; con 24 h la alerta es ruido.
  P1, velocidad de los últimos 15 min: detecta a tiempo que un producto se volvió tendencia sin reaccionar a una sola compra grande. Con 1 min habría falsas alarmas; con 1 h, se notaría tarde.
  P1, alerta en 2 min: es pequeña frente al horizonte de 60 min (quedan al menos 58 para actuar). Bajarla a segundos no cambia la decisión y encarece el sistema.
  P2, COP 500.000: unas 2,4 veces el ticket promedio de la CCCE (COP 212.373). Un cupón solo se justifica en carritos grandes. Es configurable.
  P2, 30 + 5 min: el recordatorio sale antes de la primera hora, que es la ventana que recomienda la industria. Con menos de 30 min se molesta a quien sigue comparando.
  P2, solo usuarios identificados: a un anónimo no hay a quién escribirle, pero sí cuenta en el embudo de P4.
  P3, por minuto y visible en 2 min: Dirección ajusta campañas en curso; se reutiliza el límite de 2 min de P1 para no tener dos valores distintos.
  P4 y P5, 1 hora: P4 se pide "por hora" y Comercial decide en horas o días. Pedir tiempo real aquí encarece el sistema sin cambiar ninguna decisión.
  5.000 ev/s: Anexo A, fila por fila (pico de ≈ 3.000 en la apertura de ofertas + margen de ≈ 1,7 veces). Si cambia un supuesto, se recalcula.
  Sección 1.5: ~1 TB al año NO justifica por sí solo una arquitectura distribuida; la justifica la COMBINACIÓN de picos de 100 veces, cargas que compiten, variedad y tiempo real. Decirlo así es más defendible que exagerar el volumen.
  Los RF dicen QUÉ hace el sistema, no con qué herramienta, para no tomar decisiones que les tocan a P2, P3 y P4.

  Cómo los RF cubren las restricciones obligatorias:
    Streaming ........... RF-01, RF-07, RF-08, RF-09
    Spark: join ......... RF-06 · Spark: ventanas ... RF-07, RF-08, RF-09 · Spark: agregación ... RF-10, RF-11
    Bronze / Silver / Gold ... RF-01, RF-02, RF-04 / RF-05, RF-06 / RF-10, RF-11
    Gold dimensional .... RF-11 · Orquestación ... RF-12 · Componente libre ... candidatos RF-08, RF-11, RF-13 (lo decide el ADR-4)

  Nota sobre los eventos: el Cyberlunes de la CCCE se dejó de hacer después de 2023; por eso el texto usa Black Friday, Cyber Monday y Hot Sale, que sí tienen datos de 2025.
====================================================================
-->
