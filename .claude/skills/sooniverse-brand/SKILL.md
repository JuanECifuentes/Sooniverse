---
name: sooniverse-brand
description: Reglas oficiales de identidad de marca y sistema visual de Sooniverse v4.0 (paleta cromática estricta, tipografía, componentes, microinteracciones, spotlight glow cards, botones, SVGs arquitectónicos, diseño responsivo y tono verbal). Usar SIEMPRE antes de escribir o modificar HTML/CSS/plantillas/componentes visuales de este proyecto, landing, booking (/agendar/), CRM/panel interno, correos electrónicos, diagramas SVG o cualquier pieza visual. Dispara con: "landing", "CRM", "dashboard", "plantilla", "email/correo HTML", "color", "botón", "tarjeta/card", "logo", "SVG", "diagrama", "estilo", "Tailwind", "identidad de marca", "branding", "responsivo", "agendar", "booking".
---

# Identidad de Marca y Sistema Visual — Sooniverse v4.0

> **Documento Oficial de Referencia:** Destilado directo de [`conceptos/Manual de identidad de marca Sooniverse v4.0.md`](file:///c:/Users/Cifu/Documents/Servicios/sooniverse/conceptos/Manual%20de%20identidad%20de%20marca%20Sooniverse%20v4.0.md).  
> **Hoja de Estilos Central v4.0:** [`static/css/sooniverse-v4.css`](file:///c:/Users/Cifu/Documents/Servicios/sooniverse/static/css/sooniverse-v4.css).  
> **Regla de Oro:** Ante cualquier duda de diseño, estas reglas priman sobre cualquier instinto genérico de "landing SaaS clara o corporativa gris". Sooniverse es una experiencia inmersiva **Deep Space Tech**: oscura, de altísimo contraste, con microinteracciones cinéticas vivas, resplandores controlados y sobriedad ejecutiva para directivos C-Level (CFO, CTO, CISO).

---

## 1. Paleta Cromática Oficial v4.0

**Proporción de pantalla:** 88% Neutros oscuros, 5% Cian Eléctrico, 3% Verde Esmeralda, 2% Violeta Cósmico, 2% Blanco puro y tipográfico.

| Rol Semántico | Nombre | HEX / RGBA | Token CSS (`:root`) | Uso Exclusivo y Obligatorio |
| :--- | :--- | :--- | :--- | :--- |
| **Fondo Base** | Deep Space | `#070A12` | `--sv-bg-base` | Fondo absoluto de HTML, body, canvas, footer y pantallas públicas. |
| **Superficie Sólida** | Navy Surface | `#0F172A` | `--sv-bg-surface` | Fondo de cards, modales, tablas, menús y dropdowns. |
| **Superficie Cristal** | Navy Glass | `rgba(15, 23, 42, 0.75)` | `--sv-bg-glass` | Paneles flotantes translúcidos con `backdrop-filter: blur(12px)`. |
| **Borde Estructural** | Space Slate | `#1E293B` | `--sv-border` | Bordes pasivos de tarjetas, divisores horizontales, pistas de inputs. |
| **Borde Secundario** | Muted Slate | `#334155` | `--sv-border-muted` | Ejes de gráficos SVG, divisores internos de tablas. |
| **Titulares / Impacto** | Pure Starlight | `#FFFFFF` | `--sv-text-heading` | H1, H2, H3, cifras principales de tarjetas, texto de botón CTA. |
| **Texto Principal** | Cloud Ice | `#F1F5F9` | `--sv-text-primary` | Textos de alto contraste, párrafos destacados, botones secundarios. |
| **Texto Secundario** | Muted Slate | `#94A3B8` | `--sv-text-secondary` | Párrafos de cuerpo, descripciones, preguntas de FAQ, subtítulos. |
| **Metadatos / Mono** | Cosmic Ash | `#64748B` | `--sv-text-tertiary` | Metadatos, etiquetas monoespaciadas, microcopy, notas legales. |
| **Héroe Tecnológico** | **Electric Cyan** | **`#60EFFF`** | `--sv-electric-cyan` | **Color primario de interactividad y tecnología:** títulos de categoría, bordes interactivos, slider thumbs, viñetas `.bullet-sky`, enlaces activos, foco, switches y punto de inicio del botón CTA. |
| **Ahorro y Rentabilidad**| **Emerald Neon** | **`#00FF87`** | `--sv-neon-green` | **Color exclusivo de valor y ahorro:** indicadores de ahorro (ej. 74%), métricas de ROI, tarjeta de solución de costo, badges de tarifa plana. |
| **Atmósfera / Profundidad**| **Cosmic Violet** | **`#8A2BE2`** | `--sv-cosmic-violet` | Nebulosas radiales, órbitas del hero, resplandor ambiental y fase final del degradado del botón CTA. |
| **Puente Cósmico** | Indigo Bridge | `#6366F1` | `--sv-indigo-bridge` | Color de transición intermedia en el degradado del botón primario. |
| **Riesgo y Peligro** | **Danger Coral** | **`#F87171`** | `--sv-danger` | **Uso estricto de alerta:** tarjetas de "El Problema", diagramas de fuga de datos en APIs públicas, factura sin techo de gasto. |

> [!WARNING]
> **TERMINANTEMENTE PROHIBIDO:** Usar `#FFFFFF` o gris claro como fondo, colores pasteles deslavados o interfaces estilo "SaaS estándar aburrido". Tampoco sobrecargar de arcoíris: el Verde (`#00FF87`) es para ahorro y finanzas; el Cian (`#60EFFF`) es para tecnología, privacidad y controles; el Rojo (`#F87171`) es para advertir el problema de las APIs comerciales.

---

## 2. Sistema de Degradados Oficiales

### 2.1 `cosmic-gradient` (Firma del Logo y `.text-highlight`)
```css
/* Para el sufijo del logo ("verse") y frases destacadas en titulares */
background: linear-gradient(135deg, #00FF87 0%, #60EFFF 50%, #8A2BE2 100%);
```
En texto se utiliza la clase `.text-highlight`:
```css
.text-highlight {
    background: linear-gradient(135deg, #00FF87 0%, #60EFFF 50%, #8A2BE2 100%);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}
```

### 2.2 `btn-primary-gradient` (Botón de Conversión CTA)
```css
/* Degradado de Cian a Violeta Cósmico */
background: linear-gradient(135deg, #60EFFF 0%, #6366F1 50%, #8A2BE2 100%);
background-size: 200% 100%;
background-position: 0% 50%;
```

### 2.3 Nebulosas Radiales por Sección
Cada sección tiene una atmósfera radial sutil que rompe la monotonía oscura:
- **Hero:** `.orbits` (Violeta 88% 14%, Cian 70% 48%, Navy Profundo 0% 100%).
- **Privacidad:** `.bg-section-privacidad` (Navy 12% 20%, Cian difuso 5%, Índigo 8%).
- **Ahorro:** `.bg-section-ahorro` (Verde 5%, Violeta 8%, Navy 50% 100%).
- **Contacto / Booking:** `.bg-section-contacto` (Violeta 12%, Cian 8%).
- **Evidencia:** `.bg-section-evidencia` (Cian 6%, Navy 90%, Violeta 7%).
- **Servicios:** `.bg-section-servicios` (Violeta 10%, Cian 5%, Navy 60%).
- **Calculadora:** `.bg-section-calculadora` (Cian 7%, Verde 4%, Violeta 8%).
- **FAQ:** `.bg-section-faq` (Índigo 8%, Navy 90%, Cian 4%).

---

## 3. Tipografía y Jerarquía

Fuentes oficiales cargadas desde Google Fonts:
1. **`Inter`** (300 a 800): Tipografía principal para prosa, títulos, navegación y botones.
2. **`JetBrains Mono`** (400 a 700): Tipografía secundaria para cifras métricas, código, sliders, badges, kickers, tablas y microcopy.

### Escala Oficial
- **H1 Hero:** `Inter` ExtraBold (800), Desktop `56px` (`3.5rem`), Móvil `36px` (`2.25rem`), tracking `-1.5px`, color `#FFFFFF`.
- **H2 Sección:** `Inter` Bold (700), Desktop `36px - 40px`, Móvil `28px`, tracking `-1.0px`, color `#FFFFFF`.
- **H3 Tarjeta:** `Inter` Bold (700), Desktop `20px - 22px`, Móvil `18px`, tracking `-0.5px`, color `#FFFFFF`.
- **Body:** `Inter` Regular (400), Desktop `16px`, Móvil `14px - 15px`, line-height `1.6`, color `#94A3B8`.
- **Cifras de Métricas:** `JetBrains Mono` Bold/ExtraBold (700/800), `28px - 48px`, color `#FFFFFF`, `#00FF87` o `#60EFFF`.
- **Badges / Kickers:** `JetBrains Mono` Bold (700), `10px - 11px`, UPPERCASE, tracking `+2.0px` a `+2.5px`.

---

## 4. Naming e Identidad Verbal

- **Nombre exacto:** **`Sooniverse`** (solo la 'S' mayúscula).
- **Anatomía del Logo:**
  - **`Sooni`** en blanco puro (`#FFFFFF`), `Inter` ExtraBold 800.
  - **`verse`** con `cosmic-gradient` (`#00FF87` → `#60EFFF` → `#8A2BE2`), `Inter` ExtraBold 800.
  - Patrón HTML: `<span style="color:#FFFFFF">Sooni</span><span class="text-highlight">verse</span>`.
  - Isotipo planetario oficial: 3 anillos inclinados a `-18°` con nodos en verde, cian y violeta (`logos_v1/logo_sin_fondo.svg`, `logos_v1/animado.svg`).
- **Tagline Institucional:** `ADVANCED TECH UNIVERSE` (`JetBrains Mono`, 11–13px, bold, tracking 2.5px, color `#A0AEC6` con nodo `#60EFFF`).
- **Descriptor de Propósito:** `Optimización de IA para empresas` (`JetBrains Mono`, 11px, bold, color `#60EFFF` dentro de `.glass-panel`).
- **Propuesta de Valor (H1):** *Convierte tu gasto en IA en una plataforma privada para toda tu empresa.*
- **Prohibición:** Nunca usar "PRIVATE AI PLATFORM" como descriptor general de la marca.

---

## 5. Sistema de Componentes y Microinteracciones (UI Kit v4.0)

### 5.1 Botón de Acción Principal (`.btn-primary` y `.btn-nav`)
El botón estrella de conversión B2B cuenta con 5 propiedades distintivas obligatorias:
1. **Fondo Gradiente Activo:** `linear-gradient(135deg, #60EFFF 0%, #6366F1 50%, #8A2BE2 100%)` con `background-size: 200% 100%`.
2. **Texto Blanco Puro:** `color: #FFFFFF !important; font-weight: 700; text-shadow: 0 1px 2px rgba(7, 10, 18, 0.5);`.
3. **Efecto Shimmer (Destello Diagonal):** Pseudoelemento `::after` a `-20°` que cruza el botón al hacer hover.
4. **Transición a Púrpura:** En hover pasa a `background-position: 100% 50% !important;` y pulsa suavemente (`btnPurplePulse`).
5. **Elevación y Halo Doble:** `transform: translateY(-4px) scale(1.03)` con `box-shadow: 0 0 30px rgba(138, 43, 226, 0.75), 0 0 55px rgba(96, 239, 255, 0.50)`. Flecha reactiva con clase `group-hover:translate-x-1`.

### 5.2 Botón Secundario (`.btn-secondary`)
- Fondo: `rgba(15, 23, 42, 0.7)` con `backdrop-filter: blur(12px)`.
- Borde: 1.5px sólido `rgba(96, 239, 255, 0.45)`.
- Hover: Borde `#60EFFF`, fondo `rgba(96, 239, 255, 0.12)`, elevación `-3px` y halo cian `0 0 25px rgba(96, 239, 255, 0.4)`.

### 5.3 Tarjetas con Spotlight Interactivo (`.glow-card`)
Las tarjetas principales Sooniverse detectan el cursor mediante variables CSS dinámicas:
- Variables `--mouse-x` y `--mouse-y` actualizadas por JavaScript (`mousemove`).
- `::before`: Proyecta un foco de linterna radial translúcido sobre el contenido.
- `::after`: Ilumina el borde exacto de 1.5px con el color semántico de la tarjeta:
  - **Problema / Riesgo (`.card-legacy`, `.card-danger`):** Borde y spotlight en Rojo Coral (`rgba(248, 113, 113, 0.32)` / hover `#F87171`).
  - **Solución Privacidad (`#privacidad .card-solution`):** Borde y spotlight en Cian Eléctrico (`rgba(96, 239, 255, 0.32)` / hover `#60EFFF`).
  - **Solución Ahorro (`#ahorro .card-solution`):** Borde y spotlight en Verde Esmeralda (`rgba(0, 255, 135, 0.32)` / hover `#00FF87`).
  - **Calculadora (`.card-calculator-sooniverse`):** Borde destacado 2px `#60EFFF` con halo cian.

### 5.4 Tag Pills y Badges
- **Problema:** `.tag-pill.tag-pill-legacy` con punto `.bullet-legacy` (`#64748B`).
- **Solución Técnica:** `.tag-pill.tag-pill-sky` con punto `.bullet-sky` (`#60EFFF`).
- **Ahorro / Tarifa Plana:** `.tag-pill.tag-pill-green` con punto `.bullet-green` (`#00FF87`).

### 5.5 Viñetas Luminosas (Bullets)
Reemplazan los checkmarks genéricos:
- `.bullet-legacy`: Diámetro 9px, color `#64748B`, halo `box-shadow: 0 0 8px rgba(100, 116, 139, 0.7)`.
- `.bullet-sky`: Diámetro 9px, color `#60EFFF`, halo `box-shadow: 0 0 10px rgba(96, 239, 255, 0.9), 0 0 16px rgba(96, 239, 255, 0.5)`.
- `.bullet-green`: Diámetro 9px, color `#00FF87`, halo `box-shadow: 0 0 10px rgba(0, 255, 135, 0.9), 0 0 16px rgba(0, 255, 135, 0.5)`.

### 5.6 Gráfico Cinético de Inferencia (Hero Bars)
- Barras variables (índices 0, 1, 2): Carga inicial y oscilación continua no uniforme (`heroBarWave`) desfasada a 3.2s, reflejando volatilidad de costos.
- Barras cian fijas (índices 3, 4, 5): Movimiento sincronizado en bloque y cuasi-nulo (`heroBarFixedPrice` a 3.2s, variación < 1.8%), transmitiendo estabilidad de precio plano.

### 5.7 Diagramas Arquitectónicos (SVG)
- **Delimitación de la Empresa:** Rectángulo con perímetro punteado `stroke-dasharray="5 4"`, borde `#64748B` y etiqueta `TU EMPRESA` en JetBrains Mono 8px bold.
- **Flujos en movimiento:** Líneas continuas con `stroke-dasharray="6 8"`, clase `.flow-dash` y paquetes de datos en tránsito con `<animateMotion>`.
- **Perímetro de red privada:** Contenedor envolvente con gradiente cósmico, candado cerrado y label `100% AISLADO`.

---

## 6. Sistema Responsivo para Móvil (Reglas Obligatorias)

1. **Cero Scroll Horizontal:**
   - Todo layout debe respetar `html, body { max-width: 100vw; overflow-x: hidden; position: relative; }` y `box-sizing: border-box;`.
2. **Dimensiones de SVGs y Tarjetas en Móvil (`< 768px`):**
   - Los diagramas `svg.diagram` se acotan a `max-height: 125px !important;`.
   - Los gráficos de costo en cajas se acotan a `max-height: 52px !important;`.
   - `.card-legacy` y `.card-solution` tienen límite `max-height: calc(100vh - 40px)` y padding compacto (`1.1rem 1rem`), asegurando que **nunca superen la altura del viewport móvil**.
3. **Tipografía Responsiva de Precios (`US$ 2,250` / `US$ 579`):**
   - **En Desktop:** Deben mostrarse a tamaño completo e imponente con `text-3xl` (`1.875rem` / `30px`, font-extrabold).
   - **En Móvil (`< 768px`):** Escalan proporcionalmente a `1.35rem` (~21.6px) mediante la clase `.card-cost-value`, evitando que dominen visualmente la tarjeta.
4. **Dropdowns y Filtros Móviles (Agenda `/agendar/`):**
   - Menús desplegables (`.tz-dropdown-menu`, `.phone-dropdown-menu`) acotados con `width: min(280px, calc(100vw - 28px));` y `max-height: 250px` con scroll interno táctil y buscadores en tiempo real.

---

## 7. Dónde Vive Cada Pieza del Proyecto

| Elemento / Sistema | Ubicación Oficial |
| :--- | :--- |
| **Manual Maestro v4.0** | `conceptos/Manual de identidad de marca Sooniverse v4.0.md` |
| **CSS Central v4.0** | `static/css/sooniverse-v4.css` |
| **Landing Page** | `apps/core/templates/core/landing.html` |
| **Agenda Pública (Booking)** | `apps/core/templates/core/booking/agendar.html` |
| **Base Pública** | `apps/core/templates/core/base_public.html` |
| **Base Panel Interno** | `apps/core/templates/core/base_internal.html` |
| **Plantilla Base Correos** | `apps/core/templates/core/emails/base_email.html` |
| **SVGs de Diagramas** | `apps/core/templates/core/includes/svg_*.html` |
| **Logos Oficiales** | `static/logos_v1/animado.svg`, `logo_sin_fondo.svg` |

---

## 8. Nota Operativa sobre Tailwind CSS

El archivo `static/css/dist/tailwind.css` es un build precompilado y purgado para producción.
- **Regla:** Si una clase utilitaria de Tailwind no existe en el build actual (por ejemplo, variantes compuestas arbitrarias), el navegador la ignorará silenciosamente.
- **Solución estándar:** Definir las reglas de marca y estilos responsivos en `static/css/sooniverse-v4.css` o dentro de la etiqueta `<style>` del template correspondiente, reutilizando las variables y clases oficiales documentadas en este manual.
