# Manual de Identidad de Marca: Sooniverse v4.0
**Documento Oficial de Diseño, Arquitectura Visual y Sistema de Componentes**  
*Edición v4.0 · Octubre 2026 · Autor: Juan Esteban Cifuentes & Sooniverse Core Team*

---

## 0. Principio Rector v4.0: Alta Tecnología, Máxima Interactividad y Sobriedad Ejecutiva

La versión **v4.0** del manual de identidad de Sooniverse representa la consagración definitiva del lenguaje visual de la plataforma tras la consolidación de la nueva landing page y sus sistemas interactivos.

Sooniverse opera en un segmento de alta exigencia: empresas medianas y corporaciones que invierten más de US$2,000 mensuales en modelos de lenguaje (APIs públicas) y requieren migrar hacia una **plataforma privada de IA** con infraestructura GPU dedicada, costo fijo mensual predecible y blindaje absoluto de datos.

### 0.1 La Premisa de Diseño v4.0
El diseño de Sooniverse **no es una plantilla corporativa gris y estática**, ni tampoco un panel de videojuegos saturado de neón caótico. Es una experiencia inmersiva de **Deep Space Tech**:
1. **Fondo de Universo Profundo:** Una base oscura inmutable (`#070A12`) enriquecida con nebulosas radiales cósmicas exclusivas por sección, generando profundidad infinita sin fatiga visual.
2. **Cian Eléctrico (`#60EFFF`) como Héroe Tecnológico:** Es el color primario de interactividad, precisión y soberanía técnica. Gobierna los titulares de sección, los bordes interactivos, los interruptores, las viñetas luminosas y el punto de partida del botón principal.
3. **Verde Esmeralda (`#00FF87`) como Demostración de Rentabilidad:** Reservado estrictamente para el éxito financiero, las métricas de ahorro (hasta 74%), el precio de tarifa plana fija y la arquitectura libre de coste marginal.
4. **Violeta Cósmico (`#8A2BE2` / `#6366F1`) como Atmósfera y Dimensión:** Aporta la firma misteriosa y espacial de la marca. Fluye en el fondo Órbitas, en las nebulosas ambientales y en el degradado de acción del botón CTA.
5. **Rojo Coral / Alerta (`#F87171`):** Usado con rigor quirúrgico para advertir sobre los riesgos de las APIs de terceros, la fuga de datos confidenciales y la factura variable impredecible.
6. **Microinteracciones Vivas:** Animaciones físicas coherentes, tarjetas con *spotlight* que persiguen la posición exacta del cursor (`.glow-card`), gráficos de barras cinéticos con animaciones diferenciadas y diagramas SVG con paquetes de datos en tránsito continuo.

---

## 1. Paleta Cromática Oficial

La proporción áurea de distribución en pantalla es: **88% Neutros oscuros**, **5% Cian Eléctrico**, **3% Verde Esmeralda**, **2% Acentos Cósmicos / Violeta**, **2% Blanco puro y tipográfico**.

### 1.1 Neutros "Deep Space" (Estructura y Jerarquía)

| Token CSS | Nombre | HEX / RGBA | Uso Exclusivo |
| :--- | :--- | :--- | :--- |
| `--sv-bg-base` | Deep Space Base | `#070A12` | Fondo absoluto del HTML, body, canvas principal y footer. |
| `--sv-bg-surface` | Navy Surface | `#0F172A` | Superficie sólida de cards, modales, tablas y paneles. |
| `--sv-bg-glass` | Navy Glass | `rgba(15, 23, 42, 0.75)` | Paneles translúcidos con `backdrop-filter: blur(12px)`. |
| `--sv-border` | Space Slate Border | `#1E293B` | Bordes pasivos de tarjetas, divisores horizontales, pistas de inputs. |
| `--sv-border-muted`| Muted Border | `#334155` | Ejes de gráficos SVG, divisores internos de tablas. |
| `--sv-text-heading`| Pure Starlight | `#FFFFFF` | H1, H2, H3, números de impacto, cifras principales de tarjetas. |
| `--sv-text-primary`| Cloud Ice | `#F1F5F9` | Textos de alto contraste, párrafos destacados, botones secundarios. |
| `--sv-text-secondary`| Muted Slate | `#94A3B8` | Párrafos de cuerpo, descripciones, preguntas de FAQ, subtítulos. |
| `--sv-text-tertiary` | Cosmic Ash | `#64748B` | Metadatos, etiquetas monoespaciadas, microcopy, notas legales. |

### 1.2 Color Primario Tecnológico: Cian Eléctrico

| Token CSS | Nombre | HEX / RGBA | Uso Exclusivo |
| :--- | :--- | :--- | :--- |
| `--sv-electric-cyan` | Electric Cyan | `#60EFFF` | Títulos de categoría, acentos de encabezado, slider thumbs, viñetas de solución, enlaces activos, foco. |
| `--sv-secondary-hover`| Cyan Radiant | `#7AF2FF` | Estados hover de elementos cian interactivos. |
| `--sv-cyan-glow` | Cyan Halogen Glow | `rgba(96, 239, 255, 0.15)` | Resplandor perimetral de tarjetas de solución y badges. |
| `--sv-secondary-soft` | Cyan Ambient Wash | `rgba(96, 239, 255, 0.08)` | Fondos de tags y chips informativos de tecnología privada. |

### 1.3 Color de Valor y Ahorro: Verde Esmeralda

| Token CSS | Nombre | HEX / RGBA | Uso Exclusivo |
| :--- | :--- | :--- | :--- |
| `--sv-neon-green` | Emerald Neon | `#00FF87` | Indicadores de ahorro numérico, métricas de ROI, tarjeta de solución de costo, badges de tarifa plana. |
| `--sv-primary-hover`| Emerald Radiant | `#1AFF95` | Hover en elementos verdes interactivos. |
| `--sv-green-glow` | Emerald Halogen Glow | `rgba(0, 255, 135, 0.15)` | Resplandor perimetral en la tarjeta de ahorro y solución de costos. |
| `--sv-primary-soft` | Emerald Ambient Wash | `rgba(0, 255, 135, 0.08)` | Fondos translúcidos de badges como `74% de Ahorro`. |

### 1.4 Acentos Cósmicos y Profundidad

| Token CSS | Nombre | HEX / RGBA | Uso Exclusivo |
| :--- | :--- | :--- | :--- |
| `--sv-cosmic-violet`| Cosmic Violet | `#8A2BE2` | Final del degradado del botón CTA, órbitas elípticas, nebulosa ambiental. |
| `--sv-indigo-bridge`| Indigo Bridge | `#6366F1` | Color de transición intermedia en el degradado del botón primario. |
| `--sv-nebula` | Nebula Mist | `rgba(138, 43, 226, 0.16)`| Resplandor difuminado de fondo en Hero y secciones clave. |

### 1.5 Color de Riesgo y Alerta: Rojo Coral

| Token CSS | Nombre | HEX / RGBA | Uso Exclusivo |
| :--- | :--- | :--- | :--- |
| `--sv-error` / `--sv-danger` | Danger Coral | `#F87171` | Tarjetas de "El Problema", fugas en diagramas SVG, advertencia de falta de techo de gasto. |
| `--sv-danger-light` | Risk Rose | `#FB7185` | Degradado superior de líneas de riesgo en diagramas y alertas. |
| `--sv-danger-glow` | Danger Halogen Glow | `rgba(248, 113, 113, 0.25)`| Resplandor en hover de tarjetas de problema/riesgo. |

### 1.6 Matriz de Contraste y Accesibilidad (WCAG 2.1)

| Elemento de Texto / UI | Fondo | Relación de Contraste | Cumplimiento |
| :--- | :--- | :--- | :--- |
| `#FFFFFF` (Titulares) | `#070A12` (Fondo Base) | **19.8:1** | AAA |
| `#F1F5F9` (Texto Principal) | `#0F172A` (Superficie) | **15.2:1** | AAA |
| `#60EFFF` (Cian Tecnológico) | `#070A12` (Fondo Base) | **13.6:1** | AAA |
| `#00FF87` (Verde Esmeralda) | `#0F172A` (Superficie) | **13.1:1** | AAA |
| `#94A3B8` (Texto Secundario)| `#0F172A` (Superficie) | **7.4:1** | AAA |
| `#64748B` (Metadatos/Mono) | `#0F172A` (Superficie) | **4.6:1** | AA |
| `#FFFFFF` sobre Botón Primario | Gradiente Cian-Violeta | **> 6.5:1** (con text-shadow)| AA / AAA |

---

## 2. Psicología del Color y Conversión B2B

El usuario objetivo es un directivo cauteloso (**CFO, CTO, CISO, VP de Ingeniería**) que enfrenta dos dolores críticos:
1. **Pérdida de control de presupuesto:** Las facturas de OpenAI/Anthropic crecen exponencialmente con cada nuevo usuario interno o proceso automatizado.
2. **Riesgo de cumplimiento y fuga de información:** Pánico a que datos financieros, contractuales o de clientes sean procesados o usados para reentrenar modelos públicos en servidores fuera del país.

```
                  ┌─────────────────────────────────────────────────┐
                  │                 SOONIVERSE v4.0                 │
                  │              ARQUITECTURA DE COLOR              │
                  └─────────────────────────────────────────────────┘
                                           │
         ┌─────────────────────────────────┼─────────────────────────────────┐
         ▼                                 ▼                                 ▼
   [ ROJO CORAL ]                  [ CIAN ELÉCTRICO ]               [ VERDE ESMERALDA ]
   (#F87171)                       (#60EFFF)                        (#00FF87)
   El Problema Actual:             La Solución Técnica:             El Impacto de Negocio:
   • Fuga de datos a terceros      • Despliegue en VPC privada      • Ahorro real de hasta 74%
   • Facturas sin techo            • Soberanía del código           • Coste marginal cero ($0)
   • Riesgo regulatorio / sanción  • Máxima velocidad y control     • Tarifa plana ilimitada
```

### El Efecto de Conversión en el CTA
El botón **"Reservar una reunión"** utiliza un degradado fluido de **Cian a Violeta Cósmico** (`#60EFFF` → `#6366F1` → `#8A2BE2`). Al pasar el ratón, un haz luminoso de luz blanca barre diagonalmente la superficie del botón, y el halo exterior emite un doble resplandor cian y morado. Esto rompe la monotonía del panel oscuro y guía la vista instantáneamente al objetivo de conversión.

---

## 3. Sistema de Degradados Oficiales

### 3.1 `cosmic-gradient` (La Firma del Logo)
Reservado estrictamente para el logotipo ("verse") y los anillos centrales del planeta en diagramas representativos:
```css
background: linear-gradient(135deg, #00FF87 0%, #60EFFF 50%, #8A2BE2 100%);
```

### 3.2 `highlight-gradient` (Promesas de Texto en Titulares)
Utilizado para convertir una frase clave del titular en una declaración luminosa de impacto tecnológico:
```css
.text-highlight {
    background: linear-gradient(135deg, #00FF87 0%, #60EFFF 50%, #8A2BE2 100%);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}
```

### 3.3 `btn-primary-gradient` (El Botón de Conversión)
```css
background: linear-gradient(135deg, #60EFFF 0%, #6366F1 50%, #8A2BE2 100%);
background-size: 200% 100%;
background-position: 0% 50%;
```

### 3.4 Sistema de Atmósferas Radiales por Sección
Para evitar que las secciones parezcan clones repetitivos del Hero o paneles oscuros sin vida, cada sección posee una distribución atmosférica propia construida con gradientes radiales sutiles:

| Sección | Clase CSS | Composición de Gradiente Radial | Sensación Psicológica |
| :--- | :--- | :--- | :--- |
| **Hero** | `.orbits` | Violeta (88% 14%), Cian (70% 48%), Navy Profundo (0% 100%). | Entrada estelar, misterio e infinitud. |
| **Privacidad** | `.bg-section-privacidad` | Navy (12% 20%), Cian difuso 5% (85% 75%), Índigo 8% (20% 90%). | Bóveda blindada, seguridad de red interna. |
| **Ahorro** | `.bg-section-ahorro` | Verde 5% (90% 18%), Violeta 8% (10% 80%), Navy (50% 100%). | Prosperidad, optimización y alivio presupuestario. |
| **Contacto** | `.bg-section-contacto` | Violeta 12% (50% 50%), Cian 8% (85% 20%). | Foco de conversión y bienvenida cálida. |
| **Evidencia** | `.bg-section-evidencia` | Cian 6% (8% 30%), Navy 90% (92% 70%), Violeta 7% (75% 15%). | Datos comprobables en producción y estabilidad. |
| **Servicios** | `.bg-section-servicios` | Violeta 10% (5% 50%), Cian 5% (80% 25%), Navy (60% 95%). | Capacidad de ingeniería avanzada y GPU dedicada. |
| **Calculadora**| `.bg-section-calculadora`| Cian 7% (50% 0%), Verde 4% (15% 75%), Violeta 8% (88% 85%). | Laboratorio numérico interactivo. |
| **FAQ & Glosario**| `.bg-section-faq` | Índigo 8% (85% 30%), Navy 90% (15% 85%), Cian 4% (45% 10%). | Respuestas estructuradas y calma institucional. |

---

## 4. Logotipo e Identidad Verbal

### 4.1 Logotipo Oficial
Archivos maestros del sistema:
- **Isotipo solo:** `logos_v1/logo_sin_fondo.svg`
- **Logo completo:** `logos_v1/logo_completo_sin_fondo_soloNombre2.svg`
- **Logo animado (Navbar):** `logos_v1/animado.svg`

#### Anatomía del Logo
- **"Sooni"**: Tipografía `Inter` ExtraBold 800 en `#FFFFFF` puro.
- **"verse"**: Tipografía `Inter` ExtraBold 800 con `cosmic-gradient` (`#00FF87` → `#60EFFF` → `#8A2BE2`).
- **Isotipo Planetario:** Esfera en degradado cósmico azul/púrpura (`#2563EB` → `#4C1D95` → `#1E1B4B`), rodeada de tres anillos inclinados a **-18°** y coronada por tres nodos activos en **Verde**, **Cian** y **Violeta**.
- **Regla estricta:** El logo jamás se recolorea a monocromático ni se sitúa sobre fondos blancos.

### 4.2 Identidad Verbal y Taglines

1. **Tagline Institucional:**
   ```
   ADVANCED TECH UNIVERSE
   ```
   - Tipografía: `JetBrains Mono`, 11–13 px, Bold 700, mayúsculas, tracking amplio (`letter-spacing: 2.5px`).
   - Color: `#A0AEC6` con punto luminoso de prefijo en `#60EFFF`.

2. **Descriptor de Propósito:**
   ```
   Optimización de IA para empresas
   ```
   - Tipografía: `JetBrains Mono`, 11 px, Bold 700, mayúsculas, tracking 2.5px.
   - Color: `#60EFFF` dentro de cápsula `glass-panel`.

3. **Propuesta de Valor Principal (H1):**
   ```
   Convierte tu gasto en IA en una plataforma privada para toda tu empresa.
   ```

---

## 5. Tipografía y Jerarquía

La marca utiliza exclusivamente dos familias de fuentes complementarias cargadas desde Google Fonts:
1. **`Inter`:** Familia tipográfica principal. Entrega neutralidad, elegancia moderna y máxima legibilidad en interfaces de software de misión crítica.
2. **`JetBrains Mono`:** Familia tipográfica secundaria / técnica. Empleada para transmitir rigor ingenieril en datos numéricos, métricas, código, badges, tablas comparativas y microcopy.

### 5.1 Escala Tipográfica

| Nivel | Familia | Tamaño Web (Desktop) | Tamaño Móvil | Peso | Tracking | Color |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **H1 Hero** | Inter | 56 px (3.5rem) | 36 px (2.25rem) | 800 (ExtraBold) | -1.5 px | `#FFFFFF` |
| **H2 Sección** | Inter | 36 px – 40 px | 28 px | 700 (Bold) | -1.0 px | `#FFFFFF` |
| **H3 Tarjeta** | Inter | 20 px – 22 px | 18 px | 700 (Bold) | -0.5 px | `#FFFFFF` |
| **H4 Subtítulo**| Inter | 16 px – 18 px | 15 px | 600 (SemiBold) | 0 px | `#FFFFFF` |
| **Body (Cuerpo)**| Inter | 16 px (1rem) | 14 px – 15 px | 400 (Regular) | 0 px | `#94A3B8` |
| **Botón Primario**| Inter | 14 px – 15 px | 14 px | 700 (Bold) | +0.5 px (Mayús) | `#FFFFFF` |
| **Cifras de Métricas**| JetBrains Mono| 36 px – 48 px | 28 px – 32 px | 700 / 800 | 0 px | `#FFFFFF` / `#00FF87` / `#60EFFF` |
| **Tagline / Badges**| JetBrains Mono| 10 px – 11 px | 10 px | 700 (Bold) | +2.0 px | `#60EFFF` / `#00FF87` / `#94A3B8` |
| **Microcopy / Ejes**| JetBrains Mono| 10 px – 12 px | 10 px | 500 (Medium) | +1.5 px | `#64748B` |

---

## 6. Sistema de Fondo "Órbitas" y Efectos de Fondo

El fondo del Hero es una arquitectura de tres capas que proyecta la ilusión de un planetario tecnológico:

```
[ Capa 0: Ruido Estático (.noise-overlay) ] ── Opacidad 1.5%
        │
[ Capa 1: Deriva Cósmica (.cosmic-bg) ] ──── Nebulosas flotantes animadas (46s / 62s)
        │
[ Capa 2: Órbitas y Rejilla SVG (.orbits) ] ─ Puntos #60EFFF al 15% + Elipses -18° + Nodos Twinkle
        │
[ Capa 3: Contenido HTML (.orbits__content)] ─ Hero Grid, Titular y Gráfico de Barras
```

### 6.1 Código de Implementación del Hero Órbitas
```html
<section id="hero" class="orbits min-h-screen flex items-center pt-32 pb-16 md:pt-24">
    <svg class="orbits__layer" viewBox="0 0 1200 800" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
        <defs>
            <pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse">
                <circle cx="11" cy="11" r="0.9" fill="#60EFFF" opacity="0.15"/>
            </pattern>
            <radialGradient id="fade" cx="78%" cy="28%" r="65%">
                <stop offset="0%" stop-color="#fff"/>
                <stop offset="100%" stop-color="#000"/>
            </radialGradient>
            <mask id="m"><rect width="100%" height="100%" fill="url(#fade)"/></mask>
        </defs>
        <rect width="100%" height="100%" fill="url(#dots)" mask="url(#m)"/>
        
        <!-- Elipses a -18° con nodo fantasma -->
        <g transform="translate(940, 260) rotate(-18)" fill="none">
            <ellipse rx="360" ry="100" stroke="#60EFFF" stroke-opacity="0.10" stroke-width="1"/>
            <ellipse rx="260" ry="74" stroke="#60EFFF" stroke-opacity="0.16" stroke-dasharray="2 6" stroke-width="1"/>
            <ellipse rx="160" ry="46" stroke="#8A2BE2" stroke-opacity="0.14" stroke-width="1"/>
            <circle r="52" fill="#0F172A" fill-opacity="0.35" stroke="#60EFFF" stroke-opacity="0.10"/>
        </g>
        
        <!-- Nodos parpadeantes desfasados -->
        <g transform="translate(940, 260) rotate(-18)">
            <circle cx="-255" cy="-14" r="9" fill="#60EFFF" opacity="0.14"/>
            <circle class="node" cx="-255" cy="-14" r="3" fill="#60EFFF"/>
            <circle cx="155" cy="16" r="8" fill="#FFFFFF" opacity="0.08"/>
            <circle class="node" style="animation-delay:1.3s" cx="155" cy="16" r="2.5" fill="#F1F5F9"/>
            <circle cx="72" cy="100" r="9" fill="#8A2BE2" opacity="0.2"/>
            <circle class="node" style="animation-delay:2.6s" cx="72" cy="100" r="3" fill="#8A2BE2"/>
        </g>
    </svg>
    <div class="orbits__content max-w-7xl mx-auto px-6 lg:px-8 w-full">
        <!-- Contenido Hero -->
    </div>
</section>
```

---

## 7. Sistema de Componentes y Microinteracciones (UI Kit)

### 7.1 Barra de Navegación Flotante Inteligente (`#main-header`)
- **Estado Inicial (Superior):** Transparente, integrada con el fondo Órbitas, logo a escala completa (3.25rem).
- **Estado Scrolled (> 40px de scroll):** Se contrae suavemente en forma de cápsula flotante centrada (`width: calc(100% - 2rem)`, `max-width: 80rem`), añade fondo `rgba(15, 23, 42, 0.88)` con `backdrop-filter: blur(24px)`, borde sutil `#1E293B`, radio `14px`, sombra perimetral profunda y logo escalado a `2.35rem`.
- **Enlaces de navegación:** Color `#94A3B8`. En hover cambian a `#FFFFFF` y despliegan una línea inferior animada de color Cian Eléctrico (`#60EFFF`) que se expande desde el centro.

### 7.2 Botón de Acción Principal (`.btn-primary` y `.btn-nav`)
El botón estrella de conversión de la marca cuenta con 5 propiedades distintivas:
1. **Fondo en Degradado Activo:** `linear-gradient(135deg, #60EFFF 0%, #6366F1 50%, #8A2BE2 100%)` con `background-size: 200% 100%`.
2. **Efecto Shimmer (Destello de Luz Diagonal):** Un pseudoelemento `::after` con gradiente blanco translúcido en ángulo `-20°` que cruza velozmente el botón de izquierda a derecha al pasar el ratón.
3. **Elevación Física:** `transform: translateY(-3px) scale(1.02)` con curva bezier ultra suave `cubic-bezier(0.16, 1, 0.3, 1)`.
4. **Halo Lácteo Multicapa:** `box-shadow: 0 0 25px rgba(96, 239, 255, 0.55), 0 0 45px rgba(138, 43, 226, 0.45)`.
5. **Flecha Reactiva:** El icono SVG de flecha a la derecha posee la clase `group-hover:translate-x-1`.

```css
.btn-primary {
    position: relative;
    overflow: hidden;
    background: linear-gradient(135deg, #60EFFF 0%, #6366F1 50%, #8A2BE2 100%);
    background-size: 200% 100%;
    background-position: 0% 50%;
    color: #FFFFFF !important;
    font-family: 'Inter', system-ui, sans-serif;
    font-weight: 700;
    border-radius: 10px;
    border: 1px solid rgba(255, 255, 255, 0.25);
    box-shadow: 0 4px 16px rgba(96, 239, 255, 0.25), 0 2px 12px rgba(138, 43, 226, 0.25);
    transition: transform 0.35s cubic-bezier(0.16, 1, 0.3, 1), background-position 0.5s ease, box-shadow 0.35s ease;
    text-shadow: 0 1px 2px rgba(7, 10, 18, 0.5);
}
.btn-primary:hover {
    background-position: 100% 50%;
    transform: translateY(-3px) scale(1.02);
    box-shadow: 0 0 25px rgba(96, 239, 255, 0.55), 0 0 45px rgba(138, 43, 226, 0.45);
}
```

### 7.3 Botón Secundario (`.btn-secondary`)
- Fondo: `rgba(15, 23, 42, 0.7)` con `backdrop-filter: blur(12px)`.
- Borde: 1.5px sólido `rgba(96, 239, 255, 0.45)`.
- Hover: Borde `#60EFFF`, fondo `rgba(96, 239, 255, 0.12)`, elevación `-3px` y halo cian `box-shadow: 0 0 25px rgba(96, 239, 255, 0.4)`.

### 7.4 Tarjetas Interactivas con Spotlight (`.glow-card`)
Las tarjetas Sooniverse incorporan detección matemática del cursor mediante variables CSS dinámicas:
- `var(--mouse-x)` y `var(--mouse-y)` alimentadas por el evento `mousemove`.
- **Efecto de linterna interna (`::before`):** Genera un cono de luz radial translúcido que ilumina sutilmente el contenido donde apunta el mouse.
- **Borde de luz exterior (`::after`):** Máscara CSS `mask-composite: exclude` que ilumina el borde exacto de 1.5px con el color semántico de la tarjeta.

```css
/* Variantes de Color para .glow-card */
/* 1. Tarjetas de Problema / Riesgo */
.card-legacy, .card-danger {
    --card-spotlight: rgba(248, 113, 113, 0.32);
    --card-glow-shadow: rgba(248, 113, 113, 0.65);
    --card-border-hover: #F87171;
}

/* 2. Tarjetas de Solución Tecnológica (Privacidad) */
#privacidad .card-solution {
    --card-spotlight: rgba(96, 239, 255, 0.32);
    --card-glow-shadow: rgba(96, 239, 255, 0.70);
    --card-border-hover: #60EFFF;
}

/* 3. Tarjetas de Solución Financiera (Ahorro) */
#ahorro .card-solution {
    --card-spotlight: rgba(0, 255, 135, 0.32);
    --card-glow-shadow: rgba(0, 255, 135, 0.70);
    --card-border-hover: #00FF87;
}

/* 4. Tarjeta de Calculadora "Con Sooniverse" */
.card-calculator-sooniverse {
    --card-spotlight: rgba(96, 239, 255, 0.18);
    --card-glow-shadow: rgba(96, 239, 255, 0.45);
    --card-border-hover: #60EFFF;
    border: 2px solid #60EFFF !important;
}
```

### 7.5 Badges y Tag Pills

```html
<!-- Tag Problema / Sin Perímetro -->
<span class="tag-pill tag-pill-legacy">
    <span class="bullet-legacy mr-2"></span>
    EL PROBLEMA · APIS PÚBLICAS
</span>

<!-- Tag Solución Tecnológica Cian -->
<span class="tag-pill tag-pill-sky">
    <span class="bullet-sky animate-pulse mr-2"></span>
    SOLUCIÓN SOONIVERSE · 100% AISLADA
</span>

<!-- Tag Solución Ahorro Verde -->
<span class="tag-pill tag-pill-green">
    <span class="bullet-green animate-pulse mr-2"></span>
    74% DE AHORRO
</span>
```

### 7.6 Viñetas Luminosas (Bullets)
Puntos de lista de alta presencia que reemplazan los clásicos checkmarks genéricos:
- `.bullet-legacy`: Diámetro 9px, color `#64748B`, halo `box-shadow: 0 0 8px rgba(100, 116, 139, 0.7)`.
- `.bullet-sky`: Diámetro 9px, color `#60EFFF`, doble halo `box-shadow: 0 0 10px rgba(96, 239, 255, 0.9), 0 0 16px rgba(96, 239, 255, 0.5)`.
- `.bullet-green`: Diámetro 9px, color `#00FF87`, doble halo `box-shadow: 0 0 10px rgba(0, 255, 135, 0.9), 0 0 16px rgba(0, 255, 135, 0.5)`.

### 7.7 Sistema Cinético del Gráfico de Inferencia (Hero)
El gráfico comparativo de costos mensuales del Hero comunica visualmente la diferencia entre **volatilidad e incertidumbre** vs **precio plano predecible**:
1. **Carga Escalonada Inicial:** Las 6 barras emergen desde el suelo (`scaleY(0)` a `scaleY(1)`) de manera desfasada en 1.2s mediante `cubic-bezier(0.16, 1, 0.3, 1)`.
2. **Animación Continua Ondulante (Barras Variables 0, 1 y 2):** Oscilan continuamente con una curva fluida (`heroBarWaveVariable` a 3.2s) desfasadas 0.35s entre sí, alcanzando `scaleY(1.08)` a `scaleY(0.93)`. Esto refleja cómo el costo por token sube y baja de forma incontrolable.
3. **Respiración Sincronizada Cuasi-Nula (Barras Cian 3, 4 y 5):** Las 3 barras cian se mueven en bloque conjunto y al mismo tiempo (`heroBarFixedPrice` a 3.2s con retraso 0s) con una variación casi imperceptible (`scaleY(1.018)`). Comunica psicológicamente que el precio mensual es **fijo, inmutable y plano**.
4. **Línea de Tendencia Conectada:** Un elemento SVG dinámico superpuesto dibuja la curva polinómica que conecta exactamente los puntos circulares (`.hero-bar-dot`) de la cima de cada barra.

---

## 8. Reglas de Diseño para Diagramas Arquitectónicos (SVG)

Los diagramas visuales en las cards de Privacidad y Costo deben regirse por las siguientes normas:

```
[ TU EMPRESA ]                                              [ DESTINO ]
┌───────────────────────────┐                      ┌───────────────────────────┐
│ [Perímetro Punteado]      │      Flujo Animado   │                           │
│ stroke-dasharray="5 4"    │ ───────────────────> │  • API Pública (Fuga)     │
│ • Documentos              │   (.flow-dash)       │  ó                        │
│ • Bases de datos          │                      │  • LLM Dedicado en VPC    │
└───────────────────────────┘                      └───────────────────────────┘
```

1. **Delimitación de la Empresa:** Siempre debe estar contenida dentro de un rectángulo con borde punteado (`stroke-dasharray="5 4"`, stroke `#64748B`), con el rótulo `TU EMPRESA` en `JetBrains Mono` 8px Bold.
2. **Perímetro de Red Privada:** En la solución Sooniverse, el contenedor global abarca toda la arquitectura con un borde en gradiente cósmico (`stroke="url(#solPurpleGrad)" stroke-dasharray="6 6"`), candado cerrado y sello de `100% AISLADO`.
3. **Flujos de Datos en Movimiento:**
   - Líneas de base: Opacidad 0.3 o 0.4.
   - Líneas de flujo: `stroke-dasharray: 6 8` animadas continuamente con `@keyframes flowDash { to { stroke-dashoffset: -28; } }`.
   - Paquetes en tránsito: Nodos circulares o rectangulares recorriendo el path con `<animateMotion>`.
4. **Simbolismo de Seguridad:**
   - Riesgo / Problema: Candado abierto en `#F87171`, signo de exclamación `!` en nubes públicas externas y barra inferior con `⚠ RIESGO DE SEGURIDAD Y CUMPLIMIENTO`.
   - Solución Sooniverse: Candado cerrado en `#60EFFF`, logo planetario oficial y label `Nodo Seguro en tu VPC`.

---

## 9. Tokens de Implementación Técnica

### 9.1 Bloque CSS `:root` Maestro
```css
:root {
    /* ── Neutros Deep Space ── */
    --sv-bg-base: #070A12;
    --sv-bg-surface: #0F172A;
    --sv-bg-glass: rgba(15, 23, 42, 0.75);
    --sv-border: #1E293B;
    --sv-border-hover: rgba(96, 239, 255, 0.55);
    --sv-badge-bg: rgba(15, 23, 42, 0.9);
    --sv-badge-text: #94A3B8;
    
    /* ── Tipografía ── */
    --sv-text-heading: #FFFFFF;
    --sv-text-primary: #F1F5F9;
    --sv-text-secondary: #94A3B8;
    --sv-text-tertiary: #64748B;

    /* ── Acentos Oficiales ── */
    --sv-electric-cyan: #60EFFF;
    --sv-neon-green: #00FF87;
    --sv-cosmic-violet: #8A2BE2;
    --sv-indigo-bridge: #6366F1;
    --sv-danger: #F87171;
    --sv-warning: #FBBF24;

    /* ── Ambientales y Resplandores ── */
    --sv-nebula: rgba(138, 43, 226, 0.18);
    --sv-cyan-glow: rgba(96, 239, 255, 0.15);
    --sv-green-glow: rgba(0, 255, 135, 0.15);
    --sv-danger-glow: rgba(248, 113, 113, 0.25);
    --sv-void-indigo: rgba(15, 23, 42, 0.7);

    /* ── Degradados ── */
    --sv-cosmic-gradient: linear-gradient(135deg, #00FF87 0%, #60EFFF 50%, #8A2BE2 100%);
    --sv-btn-gradient: linear-gradient(135deg, #60EFFF 0%, #6366F1 50%, #8A2BE2 100%);

    /* ── Geometría y Sombras ── */
    --sv-radius-card: 16px;
    --sv-radius-button: 10px;
    --sv-radius-badge: 6px;
    --sv-glow: 0 0 25px rgba(96, 239, 255, 0.35);

    /* ── Fuentes ── */
    --sv-font-sans: 'Inter', system-ui, -apple-system, sans-serif;
    --sv-font-mono: 'JetBrains Mono', monospace;
}
```

### 9.2 Configuración Tailwind CSS (`tailwind.config.js`)
```javascript
module.exports = {
  theme: {
    extend: {
      colors: {
        space: {
          base: '#070A12',
          surface: '#0F172A',
          border: '#1E293B',
          muted: '#334155',
        },
        brand: {
          cyan: '#60EFFF',
          green: '#00FF87',
          violet: '#8A2BE2',
          indigo: '#6366F1',
          danger: '#F87171',
        },
        ink: {
          heading: '#FFFFFF',
          primary: '#F1F5F9',
          secondary: '#94A3B8',
          tertiary: '#64748B',
        }
      },
      borderRadius: {
        card: '16px',
        btn: '10px',
        badge: '6px',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'monospace'],
      },
      boxShadow: {
        'glow-cyan': '0 0 25px rgba(96, 239, 255, 0.35)',
        'glow-green': '0 0 25px rgba(0, 255, 135, 0.35)',
        'glow-danger': '0 0 25px rgba(248, 113, 113, 0.35)',
      }
    }
  }
};
```

---

## 10. Instrucción Maestra para Inteligencia Artificial (System Prompt)

Copia y pega este bloque íntegro al inicio de cualquier prompt o sesión de desarrollo con un LLM (Gemini, Claude, GPT) para garantizar que todo componente, arte o vista creada preserve milimétricamente la identidad Sooniverse v4.0:

```text
[INSTRUCCIÓN MAESTRA DE DISEÑO Y CÓDIGO: SOONIVERSE v4.0]
Actúa como Diseñador de Interfaces Senior y Desarrollador Frontend experto para Sooniverse.
Debes aplicar rigurosamente las siguientes directrices sin desentonar en ningún aspecto estético:

1. FILOSOFÍA VISUAL:
- Estética Deep Space Tech: Alta interactividad, acabados de cristal ahumado (glassmorphism), bordes luminosos y ambientación cósmica.
- Fondo absoluto: SIEMPRE #070A12. Superficies de tarjetas: #0F172A. Bordes pasivos: #1E293B. Queda TERMINANTEMENTE PROHIBIDO el uso de fondos claros o blancos.

2. ASIGNACIÓN SEMÁNTICA DE COLORES:
- Cian Eléctrico (#60EFFF): Es el héroe tecnológico de la interfaz. Se usa en titulares de sección, badges de tecnología privada, thumbs de sliders, viñetas de solución técnica (.bullet-sky), enlaces activos y foco.
- Verde Esmeralda (#00FF87): Es el color de rentabilidad y ahorro. Reservado para porcentajes de ahorro (ej. 74%), métricas financieras, tarjeta de solución de costo mensual fijo y badges de tarifa plana.
- Violeta Cósmico (#8A2BE2) e Índigo (#6366F1): Color ambiental y de profundidad. Vive en nebulosas radiales, órbitas del hero y como fase final del degradado del botón CTA.
- Rojo Coral (#F87171): Reservado exclusivamente para advertencias, tarjetas de "El Problema", diagramas de fuga de datos en APIs públicas y facturación variable sin techo.

3. COMPONENTES Y BOTONES:
- Botón Primario de Conversión: Lleva gradient de Cian a Violeta: linear-gradient(135deg, #60EFFF 0%, #6366F1 50%, #8A2BE2 100%), texto blanco en negrita, efecto shimmer diagonal (::after) y elevación con halo doble al hover. Siempre incluye flecha con group-hover:translate-x-1.
- Tarjetas Interactivas (.glow-card): Superficie #0F172A, radio 16px, foco de linterna interna que sigue al ratón (--mouse-x, --mouse-y) y borde luminoso perimetral según el tipo (Rojo en problema, Cian en privacidad, Verde en ahorro).

4. TIPOGRAFÍA:
- Títulos y cuerpo: 'Inter', sans-serif. Titulares principales siempre en #FFFFFF con tracking negativo (-1px a -1.5px).
- Datos técnicos, cifras, badges y tablas: 'JetBrains Mono', monospace.

5. TONO Y REGLAS DE ORO:
- Trato ejecutivo C-Level (CFO, CTO, CISO): Seguro, potente, transparente y de altísima fidelidad.
- No generes nunca interfaces aburridas o grises tipo SaaS tradicional, pero tampoco sobrecargues de arcoíris. Sigue la proporción 88% neutros, 5% cian, 3% verde y 2% violeta.
```

---

## 11. Lista de Verificación y Auditoría Visual (Checklist de Calidad)

Antes de fusionar código o aprobar una pieza gráfica, valida que cumpla cada uno de estos puntos:

- [ ] **Fondo Absoluto:** Utiliza `#070A12` como color base. Ningún contenedor principal tiene fondo blanco o gris claro.
- [ ] **Semántica Cian vs Verde:** El Verde (`#00FF87`) se limita a métricas de ahorro y costo plano; el Cian (`#60EFFF`) comanda las soluciones técnicas, títulos y controles interactivos.
- [ ] **Presencia del Rojo:** El color `#F87171` solo aparece en tarjetas o elementos que ilustran el problema de las APIs públicas o advertencias de riesgo.
- [ ] **Botón CTA Oficial:** El botón "Reservar una reunión" usa el degradado cian-violeta con texto `#FFFFFF`, efecto de brillo y flecha dinámica.
- [ ] **Tarjetas con Spotlight:** Toda tarjeta principal implementa la clase `.glow-card` con las variables de cursor y halo perimetral en hover.
- [ ] **Diagramas SVG:** Los diagramas arquitectónicos delimitan la empresa con línea punteada `stroke-dasharray="5 4"`, etiqueta "TU EMPRESA" y flujos con animación `animateMotion`.
- [ ] **Tipografías Correctas:** `Inter` en títulos y narrativa; `JetBrains Mono` en métricas, números, sliders y tags.
- [ ] **Compatibilidad Accesible:** Todo texto sobre fondo oscuro supera la relación 4.5:1 (AA) y los titulares superan 7:1 (AAA).
- [ ] **Respeto a Movimiento Reducido:** Se incluye la regla `@media (prefers-reduced-motion: reduce)` que pausa las oscilaciones continuas en barras y nodos.
