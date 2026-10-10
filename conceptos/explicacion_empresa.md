# Sooniverse — Documento Maestro de Negocio, Servicio y Pipeline Comercial B2B

---

## 1. Identidad y Propuesta de Valor de Sooniverse

**Sooniverse** es una empresa de ingeniería y desarrollo de software especializada en inteligencia artificial para el sector empresarial (B2B). 

Su solución insignia es la implementación de **Plataformas Privadas de Inteligencia Artificial** desplegadas en la propia infraestructura de nube de los clientes (**BYOC: Bring Your Own Cloud** en AWS, GCP o Azure) o bajo modalidad **Hospedada por Sooniverse (HOSTED)** para compañías sin infraestructura propia.

En lugar de revender suscripciones SaaS de software ajeno o cobrar un markup sobre APIs públicas, Sooniverse convierte la IA en un **activo corporativo dedicado, seguro y de costo predecible**.

### Los 2 Pilares Estratégicos
1. **Privacidad y Soberanía de Datos (Zero-Leakage):**
   - La información confidencial (contratos, historias clínicas, balances financieros, nóminas, bases de clientes) se procesa dentro del perímetro de seguridad corporativo.
   - Ningún dato sale a proveedores externos comerciales de propósito general que puedan almacenar prompts, retener información o entrenar modelos con propiedad intelectual del cliente.
2. **Ahorro Radical y Predictibilidad Financiera (Eliminación del Impuesto por Token):**
   - Transforma el gasto variable y lineal del cobro por token (que castiga a la empresa a medida que escala su volumen) en un **costo fijo mensual de procesamiento dedicado**.
   - Ahorros promedio entre el **40% y el 74%** frente a proveedores comerciales tradicionales (OpenAI, Anthropic).
   - Costo marginal cercano a cero: la capacidad ociosa de la infraestructura dedicada puede ser aprovechada para múltiples automatizaciones sin elevar la factura mensual.

---

## 2. Los 4 Componentes de la Plataforma Privada

Cada despliegue entregado por Sooniverse incluye cuatro capas funcionales:

```
┌────────────────────────────────────────────────────────────────────────┐
│                          SOONIVERSE PLATFORM                           │
├───────────────────────────────────┬────────────────────────────────────┤
│ 1. EL MOTOR (INFERENCIA DEDICADA) │ 2. LA RED PRIVADA Y SEGURIDAD      │
│ Modelos Open Source de última     │ Perímetro aislado en VPC. Acceso   │
│ generación sobre GPUs dedicadas   │ restringido, sin salida a internet │
│ (vLLM / CUDA optimizado).         │ público y cifrado de extremo a fin.│
├───────────────────────────────────┼────────────────────────────────────┤
│ 3. EL CHAT INTERNO (UI)           │ 4. EL TABLERO (DASHBOARD & KEYS)   │
│ Interfaz web corporativa amigable │ Centro de control de API Keys      │
│ similar a ChatGPT para uso        │ OpenAI-compatibles, auditoría,     │
│ cotidiano de los colaboradores.   │ métricas de uso y concurrencia.    │
└───────────────────────────────────┴────────────────────────────────────┘
```

---

## 3. Modelo Económico y Estructura de Precios

Sooniverse maneja un esquema claro, modular y transparente compuesto por **Diagnóstico**, **Implementación** y **Mantenimiento/Infraestructura**:

| Concepto | Modalidad / Alcance | Valor Base (COP) | Momento de Pago | Naturaleza |
| :--- | :--- | :--- | :--- | :--- |
| **Diagnóstico Técnico & Viabilidad** | Informe numérico de ROI, dimensionamiento de arquitectura y prueba de modelos en DeepInfra | **$1.000.000 COP** | 100% anticipado | **100% descontable** del valor de la implementación si contratan el servicio completo |
| **Setup & Despliegue de Plataforma** | Ingeniería Terraform, cluster de inferencia, proxy compatible OpenAI, chat corporativo y dashboard | **Desde $35.000.000 COP** | **50% ($17.5M+)** al firmar contrato<br>**50% ($17.5M+)** contra Acta de Aceptación (UAT) | Pago único de implementación (Tarifa base sube según complejidad/nodos) |
| **Mantenimiento Programado (Opcional)** | Monitoreo proactivo de nodos, parches de seguridad, optimización de VRAM y soporte L3 | **Desde $7.400.000 COP / año** | Anual anticipado o mensualizado (~$616.000 COP/mes) | Mantenimiento preventivo y actualización de modelos |
| **Infraestructura Cloud (BYOC)** | 1x GPU NVIDIA L4 (24GB VRAM) encendida 24/7 en la nube del cliente | **~US$ 580 / mes** (~$2.380.000 COP) | Facturado directo por AWS/GCP/Azure al cliente | Capacidad fija dedicada con ejecuciones masivas ilimitadas |
| **Modalidad Hospedada (HOSTED)** | Para clientes sin nube corporativa (típico en Perfil B) | Cotizado según consumo de GPU + fee de gestión Sooniverse | Facturación mensual directa de Sooniverse | Plataforma administrada llave en mano |

---

## 4. Perfilamiento B2B: Criterios Excluyentes, Perfil A y Perfil B

Para optimizar el esfuerzo comercial, calificar adecuadamente y no perder tiempo en reuniones estériles, Sooniverse filtra estrictamente a los prospectos con los siguientes parámetros extraídos de la operación real:

### A. Criterios Excluyentes (Filtro Universal "Must-Have")
Si un prospecto no cumple con **todos** estos puntos, queda **descartado de inmediato**:
1. **Gasto actual en IA de + $7.500.000 COP / mes (USD $2.000+ / mes):** Deben consumir masivamente APIs comerciales de IA (OpenAI, Anthropic, etc.). Si gastan menos, el costo de la infraestructura ($580 USD/mes) y el setup ($35M COP) no se amortizan con suficiente velocidad.
2. **Procesos de IA en producción con factura verificable:** Deben ser automatizaciones que hoy están funcionando y facturando. No califican ideas, prototipos, proyectos en planeación ni pilotos sin consumo real.
3. **Tarea principal de volumen masivo, NO de alto razonamiento:**
   - **Califica (Apto para Sooniverse):** Clasificación de documentos/tickets, extracción estructurada de datos (JSON), resúmenes de texto/llamadas, normalización, RAG sobre bases de conocimiento, atención de soporte sobre plantillas.
   - **NO califica (Excluido por ahora):** Generación de código compleja, herramientas de escritorio para uso individual humano, o razonamiento científico/matemático profundo que hoy solo resuelve un modelo de frontera de razonamiento (ej. OpenAI o1/o3 o Claude Sonnet con thinking extendido).

---

### B. Matriz Comparativa: Perfil A vs. Perfil B

| Variable | Perfil A: Producto con IA Embebida | Perfil B: Operación Documental Masiva |
| :--- | :--- | :--- |
| **Tipo de Empresa** | Empresa de Software / Tech / SaaS / Scaleup | Empresa Tradicional / Operativa / Corporativa |
| **Facturación de la Empresa** | **Mensual > $150M COP**<br>(Anual > $1.800M COP) | **Mensual > $900M COP**<br>(Anual > $11.000M COP) |
| **El Dolor Principal** | **Erosión del margen bruto:** Con cada cliente nuevo que adquieren, la factura de tokens sube linealmente. El software no escala rentablemente. | **Freno a la automatización & Regulación:** Quieren automatizar 5 procesos más, pero la cotización de tokens los frenó. Tienen temor por fuga de datos confidenciales. |
| **Nivel Técnico Interno** | Alto (cuentan con equipo de desarrolladores y CTO). | Medio / Bajo (TI corporativo general o sin equipo de DevOps). |
| **Ventaja de Cierre** | **Migración inmediata:** Tienen endpoints OpenAI en su código; cambiar a Sooniverse toma minutos cambiando el `base_url` y la `api_key`. | **Alto volumen cautivo:** Cuentan con presupuestos corporativos sólidos y procesos manuales costosos listos para migrar. |
| **Riesgo Operativo** | Pueden evaluar la opción de autohospedar ellos mismos (se rebate mostrando el costo oculto de DevOps). | **Pueden no tener nube propia ni gente de infra**, empujándolos a la modalidad **Hospedada por Sooniverse (HOSTED)**. |
| **Modalidad Habitual** | **BYOC (AWS / GCP / Azure propio)** | **BYOC o HOSTED (Sooniverse)** |
| **Sectores Representativos** | - HR-Tech (tamizaje masivo de hojas de vida)<br>- LegalTech (revisión y análisis de contratos)<br>- HealthTech (estructuración de historias clínicas)<br>- HelpDesk / CRM (resumen automático de conversaciones)<br>- Gestión Documental y OCR inteligente | - BPO y Contact Centers (resumen de llamadas masivo)<br>- IPS, EPS y Auditoría Médica (facturas médicas, autorizaciones)<br>- Casas de Cobranza (miles de expedientes y acuerdos)<br>- Aseguradoras (gestión masiva de siniestros y pólizas) |

---

### C. Señales de Alta Intención (Disparadores de Compra Rápida)

Cuando una empresa presenta una o varias de estas señales, la probabilidad y velocidad de cierre se multiplican:

| Señal Detectada en el Prospecto | Por qué acelera la venta |
| :--- | :--- |
| **1. Un cliente corporativo suyo les prohíbe contractualmente enviar datos a terceros** | Convierte de inmediato al Oficial de Cumplimiento, CISO o Legal en el principal promotor interno de Sooniverse. Es la señal más fuerte de venta. |
| **2. Ya intentaron migrar de proveedor premium (GPT-4) a uno económico (DeepSeek/GPT-4o-mini)** | Demostraron alta sensibilidad al costo de tokens y disposición técnica a cambiar de endpoint. Cierran muy rápido. |
| **3. Están en proceso de certificación ISO 27001 o SOC 2** | Tienen presupuesto asignado con fecha límite regulatoria que los presiona a blindar la salida de información. |
| **4. Intentaron autohospedar modelos por su cuenta y lo abandonaron** | Ya vivieron el dolor y costo real de lidiar con vLLM, CUDA, drivers y escalamiento. Reconocen de inmediato el valor de Sooniverse. |
| **5. Su volumen de consumo de tokens crece cada mes** | El dolor financiero empeora con el tiempo; cada semana que pasa pierden más dinero en el cobro por token. |
| **6. Pertenecen a sectores regulados (Supersalud, Superfinanciera, Habeas Data)** | La privacidad y soberanía de los datos deja de ser una preferencia deseable y se convierte en una condición legal de operación. |
| **7. Lanzaron su funcionalidad con IA hace 6 a 12 meses** | Tiempo suficiente para que el volumen haya madurado y la factura mensual se haya vuelto visible y dolorosa para el CFO. |

---

## 5. Pipeline Integral de Venta y Despliegue B2B

### Representación Esquematizada del Pipeline

```
[Lead Entrante]
       │
       ▼
┌────────────────────────────────────────────────────────────────────────┐
│ FASE 1: REUNIÓN EXPLORATORIA (Gratuita - 30 min)                       │
│ • Filtro Criterios Excluyentes (+7.5M COP/mes en IA, producción real)  │
│ • Identificación de perfil: Perfil A (SaaS) vs. Perfil B (Operación)   │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │ Calificado: Cobro Diagnóstico
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│ FASE 2: DIAGNÓSTICO & BUSINESS CASE ($1.000.000 COP | 3-5 días)        │
│ • Formulario técnico de consumo, prompts y volumen de tokens           │
│ • Entrega de cálculo de ROI, dimensionamiento de GPU y modelos         │
│ • (Si contratan la implementación, este valor se descuenta íntegro)   │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │ Aceptación de propuesta
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│ FASE 3: CIERRE LEGAL & PAGO 1 (3-7 días)                               │
│ • Firma de NDA bilateral y Contrato de Servicios (SOW)                 │
│ • Desembolso del 50% de implementación ($17.5M+ COP)                   │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │ Anticipo en banco
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│ FASE 4: BENCHMARK DE MODELOS & GESTIÓN DE CUOTAS CLOUD (3-5 días)      │
│ • Pruebas acotadas en DeepInfra ($20-30 USD de crédito, 3-5 días)      │
│ • Firma de Acta de Homologación de Modelo (Congelamiento de alcance)   │
│ • Solicitud de incremento de cuota GPU en AWS/GCP/Azure del cliente    │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │ Cuota aprobada + Modelo firmado
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│ FASE 5: DESPLIEGUE AUTOMATIZADO CON TERRAFORM (1-2 días | 2-4h ejec.)  │
│ • Ejecución del código probado (BYOC en nube cliente o HOSTED)         │
│ • Despliegue de GPU, vLLM, API OpenAI-compatible, Chat y Dashboard     │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │ Smoke Tests OK
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│ FASE 6: PRUEBAS DE ACEPTACIÓN UAT (3-5 días hábiles)                   │
│ • Cliente valida endpoints, latencia, chat corporativo y panel         │
│ • Firma del Acta de Entrega y Cierre Técnico                           │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │ Acta de entrega firmada
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│ FASE 7: LIQUIDACIÓN FINAL & TRASPASO (1-2 días)                        │
│ • Desembolso del 50% restante ($17.5M+ COP)                            │
│ • Revocación de accesos temporales y entrega de credenciales maestras  │
│ • Activación de Garantía Técnica (30 días) + Opción Mantenimiento      │
└────────────────────────────────────────────────────────────────────────┘
```

---

### Detalle de Fases del Pipeline

#### Fase 1: Reunión Exploratoria (Calificación y Diagnóstico del Dolor)
- **Duración:** 30 minutos máximo.
- **Costo:** Gratuito ($0 COP).
- **Objetivo:** Aplicar los criterios excluyentes y clasificar al prospecto en Perfil A o Perfil B para adaptar el discurso de valor.
- **Preguntas de Calificación por Perfil:**
  - *Preguntas Generales (Filtro Excluyente):*
    1. *"¿Cuánto pagaron exactamente el mes pasado en APIs de IA (OpenAI, Anthropic, etc.) y tienen la factura verificable a la mano?"* (Debe superar **$7.5M COP / mes**).
    2. *"¿Los procesos que consumen IA están hoy en producción atendiendo usuarios reales o son pruebas de concepto?"*
    3. *"¿Las tareas que realiza la IA son de procesamiento de volumen (clasificación, extracción, resúmenes) o requieren alto razonamiento matemático/código?"*
  - *Preguntas adaptadas para Perfil A (SaaS / Tech):*
    - *"¿Cuántos clientes activos consumen la funcionalidad de IA y cuánto impacta ese costo en el margen bruto de su software?"*
    - *"¿Tienen clientes empresariales que les exijan contractualmente que la información no pase por servidores de terceros?"*
  - *Preguntas adaptadas para Perfil B (Operación / Backoffice):*
    - *"¿Qué otros procesos de la empresa tienen listos para automatizar, pero no han podido lanzar porque la cotización por token los frena?"*
    - *"¿Manejan datos sujetos a regulación de Supersalud, Superfinanciera o Habeas Data?"*
    - *"¿Cuentan con infraestructura propia en AWS/Azure/GCP con equipo de DevOps, o prefieren que Sooniverse les provea la plataforma completamente administrada (HOSTED)?"*
- **Salida:** Si cumple con los criterios, se ofrece el **Diagnóstico de $1.000.000 COP** explicando que se abona al 100% al valor del setup si avanzan.

---

#### Fase 2: Diagnóstico Técnico, Cálculo de ROI y Viabilidad
- **Plazo estimado:** 3 a 5 días hábiles desde el pago y entrega de datos.
- **Costo:** **$1.000.000 COP** (100% anticipado).
- **Mecánica:**
  - El cliente diligencia un cuestionario detallado sobre sus procesos: cantidad de llamadas a la API/mes, tokens promedio de entrada y salida, latencia tolerada, prompts muestra (anonimizados) y formatos esperados (ej. JSON).
- **Entregable:** **Informe Ejecutivo de Viabilidad & Business Case**:
  1. Comparativa de costos detallada: Facturación actual en API comercial vs. Costo con Plataforma Privada Sooniverse.
  2. Retorno de inversión (ROI) y mes exacto de punto de equilibrio (amortización de los $35M COP).
  3. Dimensionamiento de infraestructura recomendada (tipo de GPU: ej. NVIDIA L4 / A10G, memoria VRAM y configuración de cuantización FP8/AWQ).
  4. Lista de 2 o 3 modelos candidatos según su tarea de negocio (ej. Llama 3.3 70B, Qwen 2.5 72B/32B, Mistral Small/Nemo, DeepSeek).
  5. Demostración guiada de 20 minutos donde Sooniverse muestra las respuestas de los modelos candidatos sobre DeepInfra frente a los datos muestra del cliente.
- *Garantía comercial:* **El 100% del $1M COP se descuenta del valor de implementación** si deciden contratar el servicio completo.

---

#### Fase 3: Propuesta Comercial, Cierre Legal y Primer Desembolso
- **Plazo estimado:** 3 a 7 días hábiles (según el ciclo legal/compras del cliente).
- **Acciones:**
  - Emisión de la Propuesta Formal de Implementación y Declaración de Trabajo (SOW).
  - Firma de **Acuerdo de Confidencialidad (NDA)** bilateral de grado corporativo.
  - Firma del **Contrato de Servicios de Desarrollo e Infraestructura**.
  - **Hito de Pago 1:** Pago del 50% de la implementación (**$17.500.000+ COP**, aplicando el crédito de $1M del diagnóstico si aplica).
- **Regla de oro:** No se solicita acceso a la nube ni se reserva cupo en la agenda de despliegue sin contrato firmado y comprobante de transferencia bancaria confirmado.

---

#### Fase 4: Homologación de Modelos (DeepInfra) y Prerrequisitos Cloud
- **Plazo estimado:** 3 a 5 días hábiles (paralelo a la cola de atención).
- **Objetivo:** Dejar certificado el modelo definitivo antes del despliegue en Terraform y asegurar los permisos y cuotas de la nube.
- **A. Pruebas de Validación / Homologación (Vía DeepInfra):**
  - Se ejecuta a través de la API serverless de **DeepInfra** sin incurrir en costos de GPU fija.
  - **Límites estrictos de la prueba:**
    - Crédito acotado: Fondo de prueba de **US$ 20 - $30** recargado por Sooniverse.
    - Ventana temporal: **3 a 5 días hábiles** máximo.
    - Modelos habilitados: Exclusivamente los 1 o 2 modelos finalistas del diagnóstico.
  - **Entregable Formal:** **Acta de Homologación de Modelo & Scorecard de Métricas** (Ver sección 6). Firmada por el líder técnico del cliente.
- **B. Prerrequisitos de Nube (Cloud Readiness):**
  - **Para clientes BYOC:** Entrega de credenciales IAM mínimas para Terraform y apertura del ticket de soporte para **incrementar la cuota de GPUs dedicadas** en AWS/GCP/Azure usando la plantilla redactada por Sooniverse.
  - **Para clientes HOSTED:** Sooniverse aprovisiona el entorno aislado dentro de su propio clúster administrado.

---

#### Fase 5: Aprovisionamiento y Despliegue Automatizado
- **Plazo estimado:** 1 a 2 días hábiles en agenda (la ejecución técnica automatizada con Terraform toma entre **2 y 4 horas**).
- **Mecánica:**
  - Ejecución de Terraform: Aprovisionamiento de red VPC/Subnets aisladas, instancia GPU con aceleración CUDA/vLLM, backend de inferencia y proxy con autenticación.
  - Despliegue de la interfaz web de Chat corporativo (tipo ChatGPT/OpenUI) y panel de administración para emisión de API Keys y visualización de telemetría.
  - Ejecución de pruebas internas de sanidad (*Smoke Tests* y validación de carga) por parte del equipo de Sooniverse.

---

#### Fase 6: Pruebas de Aceptación del Usuario (UAT) y Entrega
- **Plazo estimado:** 3 a 5 días hábiles.
- **Objetivo:** Validación por parte del cliente sobre criterios de aceptación objetivos previamente pactados en el contrato.
- **Checklist de Aceptación Formal:**
  - [ ] Endpoint privado compatible con OpenAI respondiendo peticiones con el modelo homologado.
  - [ ] Respuestas estructuradas en JSON/Markdown de acuerdo con las especificaciones del cliente.
  - [ ] Interfaz de Chat corporativo accesible para usuarios internos autorizados.
  - [ ] Tablero de administración operativo: creación de API Keys y visualización de auditoría.
  - [ ] Latencia y concurrencia operando dentro de los rangos estimados en el diagnóstico.
- **Entregable:** **Acta de Entrega y Cierre Técnico (Sign-Off Final)** firmada por ambas partes.

---

#### Fase 7: Liquidación Final, Traspaso y Garantía
- **Plazo estimado:** 1 a 2 días hábiles tras la firma del UAT.
- **Acciones:**
  - **Hito de Pago 2:** Desembolso del 50% restante (**$17.500.000+ COP**).
  - Traspaso de credenciales maestras y documentación de integración técnica.
  - Revocación o degradación de permisos de despliegue de Sooniverse en la nube del cliente (principio de menor privilegio).
  - Activación de **Garantía Técnica de Estabilidad de 30 días calendario** (cubre fallos o desconfiguraciones del despliegue inicial).
  - Opcional: Activación del contrato de **Mantenimiento Programado (desde $7.4M COP / año)** para soporte evolutivo y monitoreo proactivo continuo.

---

## 6. La Demo / PoC: Resolución Estratégica y Matriz de Métricas

### Directriz Comercial: ¿Por qué la Demo debe ser acotada y posterior al contrato?
1. Ofrecer pruebas de concepto abiertas o gratuitas antes de cerrar comercialmente atrae curiosos, extiende las decisiones por meses y diluye el valor de la solución técnica.
2. La validación se gestiona con rigor:
   - **En el Diagnóstico ($1M COP):** Demostración guiada de 20 minutos con 2 o 3 ejemplos reales del cliente ejecutados por Sooniverse.
   - **En la Fase 4 (Post-contrato y anticipo):** Validación técnica en DeepInfra bajo parámetros medibles y acotados.

### Scorecard de Decisión y Homologación de Modelos

Este documento se anexa al contrato y se firma formalmente para congelar el alcance técnico:

| Métrica / Dimensión | Criterio de Aceptación | Candidato A: Qwen 2.5 72B / 32B | Candidato B: Llama 3.3 70B | Candidato C: Mistral Small / Nemo | Veredicto |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Precisión JSON & Estructura** | > 95% de respuestas con sintaxis JSON válida | **99% (Excelente)** | 98% (Sobresaliente) | 92% (Aceptable) | **Qwen 2.5** |
| **Fidelidad en Tarea de Negocio** | Extracción/Resumen correcto en muestra de 20 casos | **19/20 casos** | 18/20 casos | 16/20 casos | **Qwen 2.5** |
| **Tiempo al Primer Token (TTFT)** | < 800 ms | ~480 ms | ~450 ms | ~350 ms | **Aprobado todos** |
| **Throughput (Tokens/seg)** | > 35 tps en generación continua | 40 tps | 42 tps | 48 tps | **Aprobado todos** |
| **Compatibilidad con 1x GPU L4** | Ajuste en 24GB VRAM con cuantización | Requiere AWQ / FP8 | Requiere FP8 | Cabe en FP16/BF16 | **Viable en 1x L4** |
| **Comprensión en Español** | Coherencia en terminología local y sin anglicismos | Alta | Alta | Media | **Aprobado** |

> **Cláusula de Blindaje de Modelo (Model Freeze):**  
> *"Con la firma del presente Scorecard de Homologación, el cliente aprueba formalmente la adopción del modelo **[Modelo Seleccionado]** como el estándar operativo de su plataforma privada. Cualquier cambio posterior de arquitectura, modelo o pesos solicitado por el cliente constituirá una orden de cambio independiente (Change Request) sujeta a cotización técnica y tarifaria adicional."*

---