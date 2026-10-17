# Resultados Empíricos de Benchmark y Análisis de Concurrencia (4 y 8 Workers)

**Fecha de Ejecución:** Octubre 2026  
**Entorno:** Base de Datos de Pruebas (`COL`)  
**Contrato Evaluado:** 11992090  
**Documento:** Pliego de Condiciones (`OC11992090.pdf`, 1,29 MB)  
**Hardware LLM:** AWS EC2 con NVIDIA L40S (48 GB VRAM) corriendo `cyankiwi/Qwen3.5-4B-AWQ-4bit`  

---

## 1. Tabla Comparativa de Pruebas Reales (Concurrencia 2 vs 4 vs 8)

| Métrica | Concurrencia = 2 (Línea Base) | Concurrencia = 4 | Concurrencia = 8 |
| :--- | :---: | :---: | :---: |
| **Tiempo Total Reloj (Wall-Clock)** | **146,23 segundos** (~2,44 min) | **86,04 segundos** (~1,43 min) | **80,57 segundos** (~1,34 min) |
| **Fase de Extracción (11 grupos)** | 105,96 segundos | 63,18 segundos | 60,32 segundos |
| **Fase de Segunda Vía (Recovery)** | 19,08 segundos | 0,63 segundos | 0,77 segundos |
| **Fase de Redacción y Prosa** | 7,00 segundos | 6,03 segundos | 5,05 segundos |
| **Fase de Validación y Reparación**| 0,10 segundos | 3,55 segundos | 3,36 segundos |
| **Tiempo Acumulado LLM (Suma)** | 257,73 segundos | 215,38 segundos | 388,76 segundos |
| **Llamadas LLM Realizadas** | 33 llamadas | 33 llamadas | 33 llamadas |
| **Tokens de Entrada (Prompt)** | 163.730 | 180.298 | 178.366 |
| **Tokens de Salida (Completion)** | 35.646 | 22.762 | 23.928 |
| **Total Tokens por Contrato** | **199.376 tokens** | **203.060 tokens** | **202.294 tokens** |

### Observaciones Técnicas Clave del Benchmark:
1. **El salto de 2 a 4 workers reduce el tiempo de proceso un 41%** (de 146 s a 86 s), acelerando significativamente la fase de extracción más pesada.
2. **El salto de 4 a 8 workers ofrece una mejora marginal** (de 86 s a 80 s, solo 6 segundos menos), mientras que el tiempo acumulado de GPU sube de 215 s a 388 s. Esto demuestra que la GPU L40S alcanza su punto de saturación óptimo con 4 a 6 peticiones en paralelo.

---

## 2. Capacidad Máxima de Generación en 720 Horas (1 Mes 24/7)

Un mes de 720 horas dispone de **2.592.000 segundos**. Considerando el funcionamiento continuo al 100% de la GPU:

### Con Concurrencia = 4 (86,04 segundos / contrato):
* **Capacidad Máxima Mensual:** 30.125 contratos al mes (~1.004 contratos al día).
* **Tokens de Entrada (Prompt):** 5.431 Millones de tokens (~5,43 Billones).
* **Tokens de Salida (Completion):** 685,7 Millones de tokens (~686 Millones).
* **Volumen Total en 720h:** **~6,12 Billones de tokens**.

### Con Concurrencia = 8 (80,57 segundos / contrato):
* **Capacidad Máxima Mensual:** 32.170 contratos al mes (~1.072 contratos al día).
* **Tokens de Entrada (Prompt):** 5.738 Millones de tokens (~5,74 Billones).
* **Tokens de Salida (Completion):** 769,8 Millones de tokens (~770 Millones).
* **Volumen Total en 720h:** **~6,51 Billones de tokens**.

---

## 3. Costo Unitario Concreto por Contrato

Tomando el promedio de consumo del contrato analizado (~179.000 tokens de entrada y ~23.300 tokens de salida):

* **DeepInfra (Qwen 3.5 9B):**
  * Costo Entrada (a $0,10 por millón): $0,0179 USD
  * Costo Salida (a $0,15 por millón): $0,0035 USD
  * **Costo por Contrato:** **$0,0214 USD** (~2,14 centavos de dólar)

* **OpenAI (GPT-6 Luna):**
  * Costo Entrada (a $0,10 por millón): $0,0179 USD
  * Costo Salida (a $0,50 por millón): $0,0117 USD
  * **Costo por Contrato:** **$0,0296 USD** (~2,96 centavos de dólar)

---

## 4. Nuevo Punto de Equilibrio: ¿Cuándo es Rentable la GPU Propia?

Costo mensual de mantener la instancia `g6e.xlarge` (L40S 48 GB) en AWS:
* **Modalidad On-Demand:** $1.380 USD / mes
* **Modalidad Reservada 1 año:** $890 USD / mes

### Frente a DeepInfra (Qwen 3.5 9B a $0,0214 USD por contrato):
* Con AWS Reservada ($890 USD/mes): Requiere procesar **41.589 contratos al mes** (~1.386 contratos diarios).
* Con AWS On-Demand ($1.380 USD/mes): Requiere procesar **64.486 contratos al mes** (~2.150 contratos diarios).

> **Conclusión frente a DeepInfra:**  
> Como una sola GPU L40S solo puede procesar un máximo de **32.170 contratos al mes** (incluso a concurrencia 8), **nunca es más rentable tener una GPU propia en AWS que usar DeepInfra en un único servidor**. Para alcanzar los 41.500 contratos necesarios, tendrías que pagar una segunda GPU en AWS, duplicando el costo de infraestructura a más de $1.800 USD/mes.

### Frente a OpenAI (GPT-6 Luna a $0,0296 USD por contrato):
* Con AWS Reservada ($890 USD/mes): Requiere procesar **30.068 contratos al mes** (~1.002 contratos diarios).
* Con AWS On-Demand ($1.380 USD/mes): Requiere procesar **46.622 contratos al mes** (~1.554 contratos diarios).

> **Conclusión frente a OpenAI:**  
> Al optimizar la concurrencia a 8 workers (capacidad de 32.170 contratos/mes), **la GPU reservada a 1 año se vuelve rentable frente a OpenAI si procesas más de 30.000 contratos mensuales (más de 1.000 contratos al día)**. Sin embargo, para 500 contratos diarios (15.000 al mes), OpenAI sigue siendo casi la mitad de barato que la GPU ($444 USD vs $890 USD).

---

## 5. Matriz Final de Costos para 500 Contratos Diarios (15.000 al mes)

* **DeepInfra (Qwen 3.5 9B):** **$321 USD al mes** (Más rentable de todas)
* **OpenAI (GPT-6 Luna):** **$444 USD al mes** (Segunda más rentable)
* **AWS Reservada 1 año:** **$890 USD al mes**
* **AWS On-Demand:** **$1.380 USD al mes**
