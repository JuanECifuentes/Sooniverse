# Sooniverse · Perfil de Cliente Ideal y Criterios de Calificación

Documento de trabajo comercial. Deriva de la Propuesta v2, el guion de 5 minutos y el canvas de modelo de negocio.

---

## 1. Corrección al criterio de calificación actual

**Hipótesis de partida:** cliente ideal = gasta $9M COP/mes en IA; la IA es ~14% del presupuesto; por lo tanto factura ≥ $65M COP/mes.

**Qué sobrevive y qué no.**

El umbral de gasto está bien puesto. Lo que falla es el puente hacia facturación. El 14% no es una fracción de la facturación, es aproximadamente lo que pesa la IA dentro de un presupuesto de TI. Y TI pesa entre 3% y 8% de la facturación según el sector. La cadena real es:

```
Gasto IA  →  ÷ 0,10–0,15  →  Presupuesto TI  →  ÷ 0,03–0,08  →  Facturación
$9M/mes                      $60–90M/mes                        $900M–$3.000M/mes
```

Es decir, entre **$11.000 y $36.000 millones COP de facturación anual**, no $780M. La diferencia es de un factor de 15 a 20.

**Excepción que crea el segundo perfil.** En una empresa cuyo producto *es* la IA, la inferencia no es gasto de TI, es costo de venta. Ahí sí puede representar entre 8% y 15% de los ingresos. Una empresa que factura $100M COP/mes y gasta $9M en tokens es perfectamente plausible si esos tokens producen el 100% del valor que vende.

De ahí salen dos perfiles con umbrales de facturación completamente distintos y con discursos de venta distintos.

**Recomendación de fondo:** dejar de calificar por facturación. Es un dato que no se observa antes de la llamada, que varía 20x entre sectores y que no predice el gasto en IA. La variable que sí califica es el **volumen de tokens procesados al mes**, y su proxy comercial, la **factura mensual del proveedor actual**.

---

## 2. El umbral real, calculado con los números de la propuesta

Con los datos del caso de referencia (2.000 millones de tokens/mes):

| | COP por millón de tokens |
|---|---|
| Proveedor premium | $4.612 |
| Proveedor económico | $1.962 |
| Plataforma privada | $2.380.000 fijos/mes (1 GPU L4) |

**Puntos de equilibrio:**

| Escenario | Contra premium | Contra proveedor económico |
|---|---|---|
| Solo infraestructura | 516M tokens/mes (~52.000 ejec.) | 1.213M tokens/mes (~121.000 ejec.) |
| Infra + implementación amortizada a 12 meses | 877M tokens/mes (~88.000 ejec.) | 2.063M tokens/mes (~206.000 ejec.) |
| Para poder prometer 40% de ahorro real en año 1 | 1.462M tokens/mes · factura actual ≥ $6,7M COP | No alcanza |

**Tres conclusiones operativas:**

1. **El piso duro es ~1.500 millones de tokens/mes**, equivalente a una factura de $6,5–7M COP/mes con proveedor premium. Por debajo de eso el ahorro del primer año se lo come la implementación y el 74% deja de ser defendible.
2. **Tu umbral de $9M COP/mes es correcto** como criterio comercial: da 2,2x sobre el punto de equilibrio y deja margen para errores de dimensionamiento.
3. **Si el prospecto ya está en un proveedor económico, el caso por costo no existe.** Necesitaría el volumen completo del caso de referencia solo para empatar. Ese prospecto solo se cierra por privacidad y control, nunca por ahorro. Es un cliente distinto y hay que hablarle distinto.

**Advertencia sobre el 74,2%:** compara el precio de lista de un modelo premium contra un modelo abierto pequeño. No es comparación de igual a igual en calidad. El número aguanta en la sala, pero solo se sostiene después del diagnóstico si la tarea del cliente efectivamente funciona con un modelo de 7 a 14 mil millones de parámetros. Eso convierte la validación de calidad en un filtro de calificación, no en un detalle técnico.

---

## 3. Los dos perfiles

### Perfil A — Producto con IA embebida (COGS)

Empresa de software colombiana o latinoamericana cuyo producto entrega salidas generadas por IA a sus propios clientes. La factura de tokens está en el estado de resultados como costo de venta y aparece en cada revisión de margen bruto.

- Facturación: **$1.100M a $4.000M COP/año** (la inferencia pesa 8–15% de los ingresos)
- Tamaño: 15 a 80 personas, de las cuales 5 a 25 son ingeniería
- Quién siente el dolor: el CTO o el fundador técnico, cada 30 días, al ver el dashboard del proveedor
- Cómo llega la urgencia: el margen bruto no sube porque cada cliente nuevo trae su propio costo de tokens
- Ciclo de venta esperado: 3 a 6 semanas
- Ventaja: la migración es real de un día, porque ya consumen un endpoint compatible con OpenAI
- Riesgo: son empresas con caja ajustada; el cobro de implementación pesa y hay que estructurarlo

**Ejemplos de forma, no de nombre:** plataformas de reclutamiento que tamizan hojas de vida, legaltech que revisa contratos, healthtech que estructura historia clínica, herramientas de atención al cliente que resumen conversaciones, plataformas de gestión documental.

### Perfil B — Operación documental de alto volumen

Empresa mediana o grande, no tecnológica, que ya metió IA en un proceso de backoffice repetitivo y le funcionó. La factura la paga TI u operaciones y ya llamó la atención de finanzas.

- Facturación: **$11.000M a $36.000M COP/año**
- Tamaño: 200 a 2.000 empleados
- Quién siente el dolor: el gerente de operaciones (el costo le impide escalar el proceso) y el CFO (la línea creció 3x en el año)
- Cómo llega la urgencia: quieren automatizar el segundo y el tercer proceso, y la cotización de tokens los frenó
- Ciclo de venta esperado: 2 a 4 meses, con comité
- Ventaja: es el cliente para el que el argumento de "la capacidad queda instalada" fue escrito
- Riesgo: puede no tener nube propia ni gente de infraestructura, lo que empuja a la modalidad hospedada

**Prioridad comercial sugerida:** el Perfil A cierra más rápido y valida el producto; el Perfil B deja mejor ticket y mantenimiento recurrente. Arrancar por A, construir referencias, entrar a B con casos.

---

## 4. Criterios mínimos excluyentes

Los siete deben cumplirse. Si falla uno, no es prospecto, es conversación.

**1. IA en producción hace al menos 3 meses, con factura verificable.**
No pilotos, no pruebas de concepto, no "estamos evaluando". El discurso completo de Sooniverse consiste en reducir una factura que ya existe. Sin factura no hay ancla, no hay 74% y no hay diagnóstico que entregar.

**2. Volumen igual o superior a 1.500 millones de tokens/mes, concentrado en una o dos automatizaciones.**
La concentración importa tanto como el total. Un cliente con 2.000M de tokens repartidos en veinte casos de uso distintos es un proyecto de migración de veinte integraciones, no un cambio de endpoint. Uno con 1.500M en un solo flujo se migra en una semana.

**3. La tarea principal debe ser trabajo de volumen, no razonamiento de frontera.**
Califica: clasificación, extracción de campos, resumen, normalización, redacción sobre plantilla, RAG sobre documentación propia. No califica: generación de código, agentes con múltiples pasos y herramientas, análisis que hoy solo resuelve un modelo de gama alta. Si el cliente escogió el modelo premium porque probó los baratos y no le sirvieron, el ahorro no es alcanzable.

**4. La carga debe ser distribuible en el tiempo.**
El costo de $2.380.000 asume una GPU encendida y ocupada 24/7. Si las 200.000 ejecuciones caen en dos horas del cierre de mes, hay que dimensionar para el pico y el ahorro desaparece. Criterio práctico: relación pico/promedio menor a 4x, o disposición del cliente a aceptar cola y procesamiento por lotes.

**5. El cliente puede definir qué es una respuesta correcta.**
Debe tener, o estar dispuesto a construir en el diagnóstico, un conjunto de 30 a 50 ejemplos reales con la salida esperada. Sin ese conjunto no hay forma de demostrar que el modelo abierto cumple, la entrega se vuelve una discusión de opiniones y el proyecto no se cierra nunca. Este es el criterio que más proyectos salva y el que más se olvida.

**6. Hay un dueño identificable de la factura, y esa factura le duele.**
Nombre y cargo concreto. Umbral: el gasto en IA representa más del 5% del COGS del producto (Perfil A) o más del 10% del presupuesto de TI (Perfil B). Si el gasto está diluido y nadie lo revisa mensualmente, no hay urgencia y el diagnóstico se posterga indefinidamente.

**7. Hay una vía de despliegue viable.**
O tiene cuenta propia en AWS, Azure o GCP con alguien que administra infraestructura, o acepta explícitamente la modalidad hospedada por Sooniverse. Una empresa que no quiere administrar nada y a la vez exige que los datos no salgan de su perímetro no tiene solución dentro del modelo actual.

---

## 5. Señales de alta intención

No son excluyentes. Priorizan la agenda.

| Señal | Por qué importa |
|---|---|
| Un cliente empresarial suyo le prohíbe contractualmente enviar datos a terceros | Convierte al oficial de cumplimiento en promotor interno. Es la señal más fuerte del conjunto |
| Ya migraron una vez de proveedor premium a uno económico | Demostraron sensibilidad al costo y disposición a cambiar de endpoint. Cierran rápido |
| Ya usan un gateway (LiteLLM, OpenRouter, o uno propio) | La migración es un cambio de configuración. Prueba de concepto en horas |
| Están en certificación ISO 27001 o SOC 2 | Hay presupuesto asignado y un plazo que presiona |
| Intentaron autohospedar y lo abandonaron | Ya conocen el costo real de aprender. El argumento de "competimos contra su lista de prioridades" aterriza solo |
| El volumen crece más de 10% mensual | El dolor empeora sin que usted haga nada |
| Sector regulado: Supersalud, Superfinanciera, habeas data sobre datos sensibles | La privacidad deja de ser preferencia y pasa a ser condición |
| Anunciaron una función con IA hace 6 a 12 meses | Tiempo suficiente para que el volumen madure y la factura se vuelva visible |

---

## 6. Anti-perfil

Descartar rápido y sin culpa. El guion ya trae la respuesta para esto ("si los números no le dan, se lo decimos").

- **Quiere empezar con IA.** No hay factura que reducir. Toda la propuesta pierde el ancla.
- **Menos de 800 millones de tokens/mes.** El punto de equilibrio es negativo. Venderle una GPU es venderle capacidad ociosa.
- **Ya está en proveedor económico con volumen menor a 2.000M tokens/mes.** Solo se puede vender privacidad, y si no hay presión regulatoria, no hay venta.
- **El caso de uso central exige un modelo de frontera.** El ahorro es inalcanzable y la entrega será un fracaso de calidad.
- **Carga multimodal pesada (imagen, audio, video).** Cambia todo el dimensionamiento y el caso de referencia no aplica.
- **Contrato empresarial anual ya pagado con el proveedor actual.** No hay ahorro este año. Volver al vencimiento.
- **Entidad pública con proceso de licitación.** El ciclo no cabe en el modelo de diagnóstico y construcción.
- **No puede articular qué salida espera del modelo.** Ver criterio 5.

---

## 7. Micro-segmentos concretos en Colombia

Cuatro nichos donde volumen, sensibilidad de datos y madurez coinciden. Ordenados por facilidad de entrada.

**1. BPO y contact centers de más de 300 puestos.**
El volumen es aritmético: 300 agentes × 40 interacciones/día × 22 días son 264.000 ejecuciones al mes solo en resumen de llamadas o clasificación de tickets. Y traen la mejor cuña de todas: sus propios contratos con clientes internacionales suelen prohibir enviar datos del cliente final a servicios de terceros. El BPO no puede usar el proveedor comercial aunque quiera. Concentración en Bogotá, Medellín, Barranquilla y Manizales.

**2. IPS, EPS y auditoría de cuentas médicas.**
Auditoría de facturas, glosas, lectura de historia clínica, autorizaciones. Volumen alto y sostenido, texto no estructurado, y datos sensibles bajo habeas data y normativa de historia clínica. Es el segmento donde la privacidad no se argumenta, se exige.

**3. Casas de cobranza y aseguradoras en gestión de siniestros.**
Miles de expedientes al mes, lectura de documentos, clasificación, redacción de comunicaciones sobre plantilla. Es exactamente el tipo de tarea que un modelo abierto pequeño resuelve bien, y el volumen es predecible.

**4. SaaS colombiano con función de IA lanzada y en crecimiento.**
El Perfil A puro. Se identifican mirando su página de producto y sus vacantes. Ciclo corto, decisor único, migración trivial.

---

## 8. Mapa de decisión

| Rol | Qué le importa | Cómo entra en la conversación |
|---|---|---|
| **Promotor**: tech lead dueño de la automatización | Que no se le rompa lo que funciona; que no le agreguen trabajo | Es quien conoce el volumen real. Sin él no hay diagnóstico posible |
| **Comprador económico**: CTO (Perfil A) o gerente de operaciones (Perfil B) | Poder automatizar más sin pedir más presupuesto | Es a quien se le dice la frase de "qué más podemos automatizar con lo que ya pagamos" |
| **Aprobador**: CFO | Previsibilidad del gasto, no solo su reducción | Le interesa que el costo deje de ser variable |
| **Patrocinador oculto**: oficial de cumplimiento o CISO | Que los datos dejen de salir | En sectores regulados deja de ser obstáculo y pasa a ser el motor del proyecto. Buscarlo temprano |
| **Opositor natural**: ingeniero senior de infraestructura | Su criterio técnico y su territorio | Dirá "yo puedo montar esto". El guion ya trae la respuesta: no se compite contra su capacidad, se compite contra su lista de prioridades. Nunca contradecirlo |

---

## 9. Nueve preguntas para calificar en la primera llamada

Ordenadas para descartar barato y temprano.

1. ¿Qué procesos suyos usan IA hoy y desde cuándo están en producción?
2. ¿Cuánto pagó el mes pasado y a quién? (Si no lo sabe de memoria, el criterio 6 falla.)
3. ¿Cuántas ejecuciones al mes tiene el proceso más pesado, y cuántas de esas veinticuatro horas se concentran?
4. ¿Ese proceso qué hace exactamente: clasifica, extrae, resume, o redacta?
5. ¿Por qué escogieron ese modelo? ¿Probaron alguno más económico y no les sirvió?
6. ¿Cómo saben hoy que una respuesta salió bien? ¿Tienen ejemplos guardados con la respuesta esperada?
7. ¿Hay algún tipo de dato que hoy no pasen por IA porque no se sienten cómodos? ¿Algún cliente o regulador que lo restrinja por escrito?
8. ¿Qué automatizaciones tienen frenadas porque el costo no daba?
9. ¿Tienen nube propia y alguien que la administre?

**Regla de descarte:** si las preguntas 2 y 3 no tienen respuesta numérica en la llamada, no se agenda diagnóstico. Se pide que la consigan y se reagenda. Un diagnóstico sin cifras de partida no produce el documento que cierra la venta.

---

## 10. Resumen de umbrales

| Variable | Mínimo | Ideal |
|---|---|---|
| Tokens/mes | 1.500 millones | 2.000 a 6.000 millones |
| Factura mensual de IA (proveedor premium) | $6,5M COP | $9M a $25M COP |
| Antigüedad en producción | 3 meses | 12 meses o más |
| Concentración del volumen | 1 o 2 automatizaciones cubren el 70% | Una sola cubre el 80% |
| Pico / promedio de carga | Menos de 4x | Menos de 2x |
| Facturación anual, Perfil A | $1.100M COP | $2.000M a $4.000M COP |
| Facturación anual, Perfil B | $11.000M COP | $15.000M a $36.000M COP |
| Conjunto de ejemplos de validación | Dispuesto a construirlo | Ya existe |
