# Manual de identidad de marca: Sooniverse v2.0

Oct 13, 2026 · @Juan Esteban Cifuentes

## 0. Principio rector

La versión 2.0 reemplaza los tres acentos neón de la 1.0 por una interfaz morada con un solo acento frío. El logo es el único elemento multicolor de cualquier pantalla y no se modifica.

Objetivo de negocio que guía cada decisión: que un CFO, CTO, CISO u oficial de cumplimiento agende la reunión exploratoria de 30 minutos. El diseño debe transmitir exclusividad, seguridad y control, no espectáculo.

Cambios frente a la v1.0:

- El verde Neon Green `#00FF87` sale de la interfaz. Solo vive dentro del logo.
- El cian Electric Cyan `#60EFFF` pasa a ser una señal funcional de "vivo / en línea", no un color decorativo.
- Fondos y superficies adoptan un tinte violeta oscuro en lugar de azul-negro.
- El botón principal deja de usar degradado y pasa a violeta sólido `#7C3AED`.
- Se incorpora el sistema de fondo "Órbitas", derivado del isotipo.
- Se definen estados funcionales para los aplicativos (éxito, error, alerta), ausentes en la v1.0.

Alcance: landing page, chat corporativo, dashboard de API Keys y cualquier pieza digital de Sooniverse.

## 1. Paleta cromática

La interfaz se construye con neutros violáceos (85% de la superficie), violetas de marca (13%) y el logo con su degradado (2%). Quedan prohibidos los fondos claros.

### 1.1 Neutros

| Token | Nombre | HEX | Uso |
| --- | --- | --- | --- |
| `bg-base` | Deep Void | `#0B0716` | Fondo de página y secciones |
| `bg-surface` | Void Surface | `#160F2B` | Cards, modales, dropdowns, inputs |
| `bg-surface-glass` | Void Glass | `rgba(22, 15, 43, 0.72)` | Cards sobre el fondo Órbitas |
| `border` | Orbit Line | `#2E2350` | Bordes de cards, divisores, botón secundario |
| `text-heading` | Pure White | `#FFFFFF` | H1, H2, H3 y "Sooni" del logo |
| `text-primary` | Star White | `#ECE8F7` | Texto de botones secundarios, texto principal en UI |
| `text-secondary` | Dust | `#A99FC4` | Cuerpo de texto, subtítulos, navegación |
| `text-tertiary` | Faint Dust | `#8A80A8` | Metadatos, etiquetas, microcopy |

### 1.2 Violetas de marca

| Token | Nombre | HEX | Uso |
| --- | --- | --- | --- |
| `accent` | Royal Violet | `#7C3AED` | Botón principal, barras de progreso, selección activa |
| `accent-hover` | Cosmic Violet | `#8A2BE2` | Hover del botón principal (color del logo) |
| `accent-soft` | Electric Lavender | `#8B5CF6` | Bordes activos, foco de teclado, gráficos |
| `highlight` | Lavender | `#C4B5FD` | Texto destacado, cifras, tagline, enlaces |
| `badge-bg` | Deep Violet | `#2E1065` | Fondo de badges y etiquetas |
| `badge-text` | Pale Lavender | `#DDD6FE` | Texto sobre `badge-bg` |
| `nebula` | Nebula | `#5B21B6` | Solo en el resplandor del fondo Órbitas |
| `void-indigo` | Indigo Void | `#1E1B4B` | Sombra del fondo y planeta fantasma (color del logo) |

### 1.3 Señal fría

| Token | Nombre | HEX | Uso |
| --- | --- | --- | --- |
| `signal` | Electric Cyan | `#60EFFF` | Exclusivamente estados "vivo / en línea / activo": punto del tagline, nodos del fondo, indicadores de servicio |

El cian no se usa en botones, títulos, enlaces ni bordes decorativos.

### 1.4 Colores restringidos

- **Neon Green `#00FF87`:** prohibido en la interfaz. Permitido solo dentro del logo (isotipo y degradado de "verse").
- **Cosmic Violet `#8A2BE2` como texto:** prohibido en tamaños menores a 24 px, porque su contraste sobre el fondo es de 3.3:1. Para texto violeta se usa `#C4B5FD`.
- **Azules del planeta (`#2563EB`, `#3B82F6`, `#4C1D95`):** reservados al isotipo.

### 1.5 Contrastes verificados (WCAG 2.1)

| Combinación | Contraste | Resultado |
| --- | --- | --- |
| `#ECE8F7` sobre `#0B0716` | 16.5:1 | AAA |
| `#C4B5FD` sobre `#0B0716` | 10.8:1 | AAA |
| `#DDD6FE` sobre `#2E1065` | 11.0:1 | AAA |
| `#A99FC4` sobre `#0B0716` | 8.0:1 | AAA |
| `#A99FC4` sobre `#160F2B` | 7.4:1 | AAA |
| `#FFFFFF` sobre `#7C3AED` | 5.7:1 | AA |
| `#8A80A8` sobre `#160F2B` | 5.0:1 | AA |
| Botón `#7C3AED` frente a `#0B0716` | 3.5:1 | Cumple 3:1 para componentes |

## 2. Psicología del color

La paleta está pensada para un comprador que decide con cautela: alguien que paga más de US$2.000 al mes en IA, teme la fuga de datos y evalúa un ticket de implementación desde $35.000.000 COP.

| Color | Qué comunica | Por qué sirve a Sooniverse |
| --- | --- | --- |
| Morado dominante | Exclusividad, autoridad, innovación con profundidad | Refuerza un servicio selectivo y de ticket alto que filtra a sus clientes |
| Neutros violáceos oscuros | Reserva, seguridad, bóveda | Encarna "tus datos no salen de tu perímetro" y deja que las cifras resalten |
| Cian puntual | Algo encendido y funcionando | Tranquiliza al comprador que teme migrar su operación: la infraestructura está viva |
| Logo multicolor | Firma, origen tecnológico | Al ser el único punto multicolor, gana protagonismo y memoria de marca |

**Por qué salió el verde.** Tres acentos neón compitiendo acercaban la marca a la estética cripto o gaming, lo que resta confianza ante el Perfil B (aseguradoras, EPS, BPO, cobranza). El costo es perder la asociación automática verde = dinero; se compensa con tamaño, tipografía monoespaciada y contexto explícito en las cifras de ahorro.

**Riesgo del morado y cómo controlarlo.** En exceso, el violeta se percibe místico o creativo. Se controla con disciplina: el morado saturado solo aparece en el botón principal y en pocos acentos; el resto de la pantalla es neutro.

**Conversión.** El botón de agendar es el único elemento con relleno violeta sólido en cada pantalla. Por el efecto de aislamiento (Von Restorff), el ojo lo encuentra sin buscarlo.

**Lectura por perfil.** El Perfil A (SaaS, CTO) reconoce en las órbitas y la tipografía mono un lenguaje técnico propio. El Perfil B (empresa tradicional, gerencia y cumplimiento) percibe sobriedad gracias a que el 85% de la pantalla es neutro.

## 3. Degradados oficiales

Existen dos degradados y ninguno se usa en botones, bordes ni fondos de componentes.

### 3.1 `cosmic-gradient` (logo, intocable)

- **Uso exclusivo:** "verse" del wordmark y anillos del isotipo.
- **Valor:** `linear-gradient(135deg, #00FF87 0%, #60EFFF 50%, #8A2BE2 100%)`
- No se altera, no se recolorea y no se reutiliza en otros textos, porque contiene verde.

### 3.2 `highlight-gradient` (frase destacada)

- **Uso:** una sola frase clave por pantalla, normalmente la promesa numérica del hero (por ejemplo, "Hasta 74% menos").
- **Valor:** `linear-gradient(135deg, #60EFFF 0%, #B794F6 50%, #A855F7 100%)`
- **Tamaño mínimo:** 24 px en peso 700 u 800. Por debajo de eso se usa `#C4B5FD` sólido.
- Termina en `#A855F7` y no en `#8A2BE2` para mantener legibilidad sobre el fondo (5.0:1).

```css
.text-highlight {
  background: linear-gradient(135deg, #60EFFF 0%, #B794F6 50%, #A855F7 100%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}
```

## 4. Logotipo e identidad verbal

El logo no cambia en la v2.0. Archivos maestros: `logo_sin_fondo.svg` (isotipo) y `logo_completo_sin_fondo_soloNombre2.svg` (isotipo + wordmark).

### 4.1 Naming

- **Escritura correcta:** `Sooniverse` (solo la S en mayúscula).
- **Wordmark:** `Inter` ExtraBold 800, letter-spacing -2 px. "Sooni" en `#FFFFFF`; "verse" con `cosmic-gradient`.
- **Isotipo:** planeta con degradado `#2563EB` → `#4C1D95` → `#1E1B4B`, anillos inclinados -18° y tres nodos (verde, cian, violeta). No se recolorea.

### 4.2 Tagline oficial

- **Texto:** `ADVANCED TECH UNIVERSE`. Queda prohibido "PRIVATE AI PLATFORM" como descriptor general.
- **Estilo:** `JetBrains Mono`, 11–13 px, Bold 700, mayúsculas, letter-spacing 3 px en web (6.5 px en piezas de gran formato).
- **Color:** `#C4B5FD` (antes verde).
- **Prefijo:** punto de 6 px en `#60EFFF` a 8 px a la izquierda, como señal de "plataforma activa".

### 4.3 Uso

- Solo sobre `#0B0716`, `#160F2B` o el fondo Órbitas. Nunca sobre fondos claros.
- Ancho mínimo del logo completo: 140 px en pantalla. Por debajo se usa solo el isotipo.
- Área de respeto: la altura del planeta (círculo central) en los cuatro lados.
- Prohibido: aplicar sombras, contornos, cambiar el degradado o usar el wordmark sin el isotipo en la navbar.

## 5. Tipografía y jerarquía

Dos familias: `Inter` (alternativa `Plus Jakarta Sans`) para prosa y títulos, y `JetBrains Mono` (alternativa `Fira Code`) para datos, métricas, badges y taglines.

| Nivel | Fuente | Tamaño | Peso | Tracking | Color |
| --- | --- | --- | --- | --- | --- |
| H1 (hero) | Inter | 56 px (móvil 36 px) | 800 | -1.5 px | `#FFFFFF` |
| H2 (sección) | Inter | 36 px (móvil 28 px) | 700 | -1 px | `#FFFFFF` |
| H3 (card) | Inter | 22 px | 600 | 0 | `#FFFFFF` |
| Body | Inter | 16 px, line-height 1.6 | 400 | 0 | `#A99FC4` |
| Botón | Inter | 15 px | 700 | 0 | `#FFFFFF` |
| Navegación | Inter | 14 px | 500 | 0 | `#A99FC4`, hover `#ECE8F7` |
| Tagline / badge | JetBrains Mono | 11–13 px, mayúsculas | 700 | 1–3 px | `#C4B5FD` o `#DDD6FE` |
| Métrica | JetBrains Mono | 24–48 px | 700 | 0 | `#C4B5FD` |
| Microcopy | JetBrains Mono | 11–12 px, mayúsculas | 500 | 1.5 px | `#8A80A8` |

Cambio frente a la v1.0: el texto de botones primarios es blanco sobre violeta (antes oscuro sobre degradado), y las métricas pasan de verde a lavanda.

## 6. Sistema de fondo "Órbitas"

El fondo repite a gran escala la geometría del isotipo con tres capas sobre `#0B0716`, todas por debajo del 20% de opacidad. Debe sentirse más que verse.

| Capa | Elemento | Valores |
| --- | --- | --- |
| 1. Nebulosa | Dos resplandores radiales | `rgba(91, 33, 182, 0.38)` en la esquina superior derecha (82% / 22%); `rgba(30, 27, 75, 0.75)` en la esquina inferior izquierda |
| 2. Rejilla estelar | Puntos de 0.9 px cada 22 px | `#C4B5FD` al 16%, con máscara radial que se desvanece al alejarse de la nebulosa |
| 3. Órbitas | Tres elipses inclinadas -18° + planeta fantasma | Trazo 1 px `#A78BFA` al 10%, 16% (punteada 2-6) y 14%; planeta `#1E1B4B` al 35% |
| Nodos | Tres puntos sobre las órbitas | Lavanda `#E9E3FF`, cian `#60EFFF` y violeta `#B794F6`, 2.5–3 px, con halo del mismo color al 12–20% |
| Grano (opcional) | Ruido estático | Opacidad 1.5–2% sobre toda la pantalla |

### 6.1 Reglas

- Las órbitas se ubican detrás de la zona sin texto (lado derecho del hero). Nunca cruzan el titular a más del 10% de opacidad.
- Los nodos son los únicos puntos saturados del fondo. No se agregan más de tres por vista.
- Animación permitida: parpadeo lento de los nodos (ciclo de 4 s, opacidad 1 → 0.45, desfasados 1.3 s). Nada más se mueve.
- Con `prefers-reduced-motion: reduce`, la animación se desactiva.
- El fondo se construye con CSS y SVG inline, sin imágenes, para no afectar la carga.

### 6.2 Código de referencia

```html
<section class="orbits">
  <svg class="orbits__layer" viewBox="0 0 660 600" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
    <defs>
      <pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse">
        <circle cx="11" cy="11" r="0.9" fill="#C4B5FD" opacity="0.16"/>
      </pattern>
      <radialGradient id="fade" cx="78%" cy="28%" r="65%">
        <stop offset="0%" stop-color="#fff"/><stop offset="100%" stop-color="#000"/>
      </radialGradient>
      <mask id="m"><rect width="660" height="600" fill="url(#fade)"/></mask>
    </defs>
    <rect width="660" height="600" fill="url(#dots)" mask="url(#m)"/>
    <g transform="translate(545,165) rotate(-18)" fill="none" stroke="#A78BFA">
      <ellipse rx="300" ry="86" stroke-opacity="0.10"/>
      <ellipse rx="215" ry="62" stroke-opacity="0.16" stroke-dasharray="2 6"/>
      <ellipse rx="135" ry="39" stroke-opacity="0.14"/>
      <circle r="44" fill="#1E1B4B" fill-opacity="0.35" stroke-opacity="0.12"/>
    </g>
    <g transform="translate(545,165) rotate(-18)">
      <circle cx="-212" cy="-12" r="9" fill="#C4B5FD" opacity="0.14"/>
      <circle class="node" cx="-212" cy="-12" r="3" fill="#E9E3FF"/>
      <circle cx="128" cy="13" r="8" fill="#60EFFF" opacity="0.12"/>
      <circle class="node" style="animation-delay:1.3s" cx="128" cy="13" r="2.5" fill="#60EFFF"/>
      <circle cx="60" cy="83" r="9" fill="#8A2BE2" opacity="0.2"/>
      <circle class="node" style="animation-delay:2.6s" cx="60" cy="83" r="3" fill="#B794F6"/>
    </g>
  </svg>
  <div class="orbits__content"><!-- contenido del hero --></div>
</section>
```

```css
.orbits {
  position: relative;
  overflow: hidden;
  background:
    radial-gradient(ellipse 55% 60% at 82% 22%, rgba(91, 33, 182, 0.38), transparent 70%),
    radial-gradient(ellipse 50% 45% at 0% 100%, rgba(30, 27, 75, 0.75), transparent 70%),
    #0B0716;
}
.orbits__layer { position: absolute; inset: 0; width: 100%; height: 100%; pointer-events: none; }
.orbits__content { position: relative; }
@keyframes twinkle { 0%, 100% { opacity: 1; } 50% { opacity: 0.45; } }
.node { animation: twinkle 4s ease-in-out infinite; }
@media (prefers-reduced-motion: reduce) { .node { animation: none; } }
```

## 7. Componentes de interfaz

Radio de esquina máximo 12 px en todo el sistema. Ningún componente usa degradado de fondo.

### 7.1 Cards

- **Sobre fondo liso:** fondo `#160F2B`, borde 1 px `#2E2350`, radio 12 px, padding 16–24 px.
- **Sobre fondo Órbitas (glass):** fondo `rgba(22, 15, 43, 0.72)`, borde 1 px `#2E2350`, `backdrop-filter: blur(12px)`.
- **Hover (si es interactiva):** borde `#8B5CF6`, `translateY(-2px)`, transición `all 0.3s ease`.

### 7.2 Botones

| Tipo | Fondo | Borde | Texto | Hover |
| --- | --- | --- | --- | --- |
| Primario | `#7C3AED` | ninguno | `#FFFFFF`, Inter 700 | Fondo `#8A2BE2`, `translateY(-2px)`, sombra `0 0 24px rgba(124, 58, 237, 0.45)` |
| Secundario | `rgba(22, 15, 43, 0.5)` | 1 px `#2E2350` | `#ECE8F7` | Borde `#8B5CF6` |
| Navbar (agendar) | transparente | 1 px `#7C3AED` | `#ECE8F7` | Fondo `#7C3AED`, texto `#FFFFFF` |

- Padding primario: 12 px × 20 px, radio 10 px.
- Texto del botón en *sentence case* y concreto: "Agendar reunión de 30 min", no "Contáctanos" ni "ENVIAR".
- Un solo botón primario por vista.

### 7.3 Badges

- Fondo `#2E1065`, texto `#DDD6FE`, `JetBrains Mono` 11 px, mayúsculas, letter-spacing 1 px, radio 6 px, padding 3 × 8 px.

### 7.4 Métricas y progreso

- Etiqueta en `#8A80A8` 12 px sobre la cifra.
- Cifra en `JetBrains Mono` 700, `#C4B5FD`.
- Barra de progreso: pista `#2E2350`, relleno `#7C3AED`, alto 6 px, radio 3 px.
- En gráficos de varias series: `#7C3AED`, `#C4B5FD`, `#60EFFF`, en ese orden.

### 7.5 Estado "en línea"

- Punto de 7 px `#60EFFF` a la izquierda del texto de estado. Es el uso principal del cian en la interfaz.

### 7.6 Enlaces y foco

- Enlaces: `#C4B5FD`, subrayado en hover.
- Foco de teclado: `outline: 2px solid #8B5CF6; outline-offset: 2px`. Nunca se elimina.

### 7.7 Brillo (glow)

- Solo en el hover del botón primario y en los nodos del logo y del fondo.
- Fórmula: `box-shadow: 0 0 24px rgba(124, 58, 237, 0.45)`. No se aplica a cards, textos ni iconos.

## 8. Reglas para la landing page

Toda la landing existe para que un prospecto calificado agende la reunión exploratoria gratuita de 30 minutos.

### 8.1 Jerarquía del hero (de arriba abajo)

1. Navbar: logo completo a la izquierda; navegación en `#A99FC4` y botón "Agendar" (tipo navbar) a la derecha.
2. Tagline `ADVANCED TECH UNIVERSE` con punto cian.
3. H1 con una sola frase en `highlight-gradient` (la promesa numérica).
4. Body en `#A99FC4`, máximo dos líneas: privacidad y costo fijo.
5. Botón primario "Agendar reunión de 30 min" + botón secundario "Ver cómo funciona".
6. Microcopy de calificación en mono `#8A80A8`: `SIN COSTO · PARA EQUIPOS CON +US$2K/MES EN IA`.
7. Tres cards glass de prueba: privacidad (badge), ahorro (métrica) e infraestructura (estado en línea).

### 8.2 Reglas de conversión

- Todos los botones primarios de la página llevan al mismo destino: el agendamiento.
- El botón primario es el único relleno violeta sólido visible en cada pantalla.
- El microcopy de calificación acompaña siempre al CTA principal, para filtrar curiosos antes de la reunión.
- Repetir el CTA al final de cada bloque largo (cómo funciona, precios, casos), sin cambiar su texto.
- El fondo Órbitas completo va solo en el hero y en el bloque final de CTA. Las secciones intermedias usan `#0B0716` liso o solo la nebulosa.

## 9. Reglas para los aplicativos (chat y dashboard)

En pantallas de trabajo diario la prioridad es la lectura cómoda durante horas, así que el fondo y los acentos se reducen.

### 9.1 Fondo

- Solo la capa de nebulosa y la rejilla estelar. Sin órbitas ni nodos animados detrás de datos o conversaciones.
- Paneles y barras laterales en `#160F2B` sólido, sin glass, para no perder contraste.

### 9.2 Estados funcionales

Estos colores no son de marca: aparecen solo cuando hay algo que comunicar, en tamaño pequeño (iconos, texto de estado, bordes de alerta).

| Estado | HEX | Fondo de aviso | Uso |
| --- | --- | --- | --- |
| Éxito | `#4ADE80` | `rgba(74, 222, 128, 0.10)` | Operación completada, key creada |
| Error | `#F87171` | `rgba(248, 113, 113, 0.10)` | Fallo de petición, key revocada |
| Alerta | `#FBBF24` | `rgba(251, 191, 36, 0.10)` | Límite de concurrencia, cuota cercana |
| Activo / en línea | `#60EFFF` | ninguno | Nodo GPU, servicio disponible |

### 9.3 Componentes específicos

- **Chat:** burbuja del usuario en `#2E1065` con texto `#ECE8F7`; respuesta del modelo sin burbuja, sobre el fondo, en `#ECE8F7`.
- **Dashboard:** fila seleccionada en `#2E1065`; tablas con divisores `#2E2350`; API Keys y valores técnicos en `JetBrains Mono`.
- **Densidad:** body de 14 px en tablas y paneles; 16 px en el chat.
- **Botón primario** (crear key, enviar): mismo estilo que en la landing, uno por vista.

## 10. Tokens para desarrolladores

Fuente única de verdad para la landing y los aplicativos. Ningún componente debe usar un HEX fuera de esta lista.

```css
:root {
  /* Neutros */
  --sv-bg-base: #0B0716;
  --sv-bg-surface: #160F2B;
  --sv-bg-glass: rgba(22, 15, 43, 0.72);
  --sv-border: #2E2350;
  --sv-text-heading: #FFFFFF;
  --sv-text-primary: #ECE8F7;
  --sv-text-secondary: #A99FC4;
  --sv-text-tertiary: #8A80A8;

  /* Violetas */
  --sv-accent: #7C3AED;
  --sv-accent-hover: #8A2BE2;
  --sv-accent-soft: #8B5CF6;
  --sv-highlight: #C4B5FD;
  --sv-badge-bg: #2E1065;
  --sv-badge-text: #DDD6FE;
  --sv-nebula: #5B21B6;
  --sv-void-indigo: #1E1B4B;

  /* Señal y estados */
  --sv-signal: #60EFFF;
  --sv-success: #4ADE80;
  --sv-error: #F87171;
  --sv-warning: #FBBF24;

  /* Degradados */
  --sv-gradient-logo: linear-gradient(135deg, #00FF87 0%, #60EFFF 50%, #8A2BE2 100%);
  --sv-gradient-highlight: linear-gradient(135deg, #60EFFF 0%, #B794F6 50%, #A855F7 100%);

  /* Forma y movimiento */
  --sv-radius-card: 12px;
  --sv-radius-button: 10px;
  --sv-radius-badge: 6px;
  --sv-glow: 0 0 24px rgba(124, 58, 237, 0.45);
  --sv-transition: all 0.3s ease;

  /* Tipografía */
  --sv-font-sans: 'Inter', 'Plus Jakarta Sans', -apple-system, sans-serif;
  --sv-font-mono: 'JetBrains Mono', 'Fira Code', ui-monospace, monospace;
}
```

```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        void: { DEFAULT: '#0B0716', surface: '#160F2B', border: '#2E2350', indigo: '#1E1B4B' },
        ink: { heading: '#FFFFFF', primary: '#ECE8F7', secondary: '#A99FC4', tertiary: '#8A80A8' },
        violet: { accent: '#7C3AED', hover: '#8A2BE2', soft: '#8B5CF6', highlight: '#C4B5FD', badge: '#2E1065', 'badge-text': '#DDD6FE', nebula: '#5B21B6' },
        signal: '#60EFFF',
        state: { success: '#4ADE80', error: '#F87171', warning: '#FBBF24' },
      },
      borderRadius: { card: '12px', button: '10px', badge: '6px' },
      boxShadow: { glow: '0 0 24px rgba(124, 58, 237, 0.45)' },
      fontFamily: {
        sans: ['Inter', 'Plus Jakarta Sans', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
      },
    },
  },
};
```

## 11. Instrucción maestra para IA

Copiar este bloque al inicio de cualquier prompt que genere diseño, código o imágenes para Sooniverse.

```text
[INSTRUCCIÓN MAESTRA DE DISEÑO: SOONIVERSE v2.0]
Eres un diseñador frontend experto. Para la marca Sooniverse:
- Fondo absoluto #0B0716; superficies #160F2B; bordes #2E2350. Nunca fondos claros.
- La interfaz es morada: botón primario #7C3AED con texto blanco (hover #8A2BE2), texto destacado #C4B5FD, badges #2E1065 con texto #DDD6FE.
- El cian #60EFFF solo indica estados "vivo / en línea". No lo uses en botones, títulos ni decoración.
- El verde #00FF87 está prohibido en la interfaz; solo existe dentro del logo.
- El logo no se modifica: "Sooni" en #FFFFFF y "verse" con linear-gradient(135deg, #00FF87, #60EFFF, #8A2BE2).
- Una sola frase por pantalla puede usar linear-gradient(135deg, #60EFFF, #B794F6, #A855F7), a 24 px o más.
- Ningún botón, borde ni card lleva degradado. Radio máximo 12 px.
- Fondo del hero: sistema "Órbitas" (nebulosa violeta, rejilla de puntos lavanda, tres elipses a -18° con tres nodos), siempre por debajo del 20% de opacidad.
- Tipografía: Inter para prosa y títulos; JetBrains Mono para datos, badges y taglines.
- Un solo botón primario por vista; en la landing siempre lleva a "Agendar reunión de 30 min".
- El tono es sobrio, exclusivo y de alta seguridad. Si el resultado parece una plantilla corporativa genérica o una web cripto/gaming con neón por todas partes, descártalo y rehazlo.
```

### 11.1 Checklist de revisión

- [ ] Ningún verde fuera del logo (salvo el estado de éxito en aplicativos).
- [ ] Un solo relleno violeta sólido por pantalla (el botón primario).
- [ ] El cian solo aparece en indicadores de estado y nodos.
- [ ] Como máximo una frase con `highlight-gradient`.
- [ ] Todo el texto cumple al menos AA (4.5:1).
- [ ] Las órbitas no cruzan el titular y la animación respeta `prefers-reduced-motion`.
- [ ] El logo usa los SVG maestros sin modificar.
