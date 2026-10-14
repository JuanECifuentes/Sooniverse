# Manual de identidad de marca: Sooniverse v3.0

Oct 13, 2026 · @Juan Esteban Cifuentes

## 0. Principio rector

La v3.0 convierte el azul cielo `#8CBFF9` en el color principal de Sooniverse y lo usa con moderación sobre neutros azul marino. El logo es el único elemento con colores intensos (verde, cian, violeta) y no se modifica.

Objetivo de negocio: que un CFO, CTO, CISO u oficial de cumplimiento agende la reunión exploratoria gratuita de 30 minutos. La interfaz debe transmitir calma, claridad y control.

Cambios frente a la v2.0:

- El color principal pasa del violeta `#7C3AED` al azul cielo `#8CBFF9`. Lo usan el botón de agendar, los indicadores de estado y el progreso.
- Los neutros pasan de un tinte violeta a azul marino.
- El cian `#60EFFF` y el verde `#00FF87` salen por completo de la interfaz. Solo viven dentro del logo.
- Los violetas quedan como color ambiental: solo en el fondo Órbitas y en el final del degradado de la frase destacada.
- El `highlight-gradient` ahora inicia en `#8CBFF9`.
- Badges, tagline y métricas pasan a neutros, para que el azul cielo no se repita en exceso.

Alcance: landing page, chat corporativo, dashboard de API Keys y cualquier pieza digital de Sooniverse.

## 1. Paleta cromática

Proporción de uso: neutros azul marino 92%, azul cielo 5%, logo 2%, toques violeta del fondo 1%. Quedan prohibidos los fondos claros.

### 1.1 Neutros

| Token | Nombre | HEX | Uso |
| --- | --- | --- | --- |
| `bg-base` | Deep Space | `#090A17` | Fondo de página y secciones |
| `bg-surface` | Navy Surface | `#0F1526` | Cards, modales, dropdowns, inputs |
| `bg-glass` | Navy Glass | `rgba(15, 21, 38, 0.72)` | Cards sobre el fondo Órbitas |
| `border` | Orbit Line | `#1F2940` | Bordes, divisores, botón secundario, pista de progreso |
| `badge-bg` | Steel | `#1A2238` | Fondo de badges y etiquetas |
| `text-heading` | Pure White | `#FFFFFF` | H1, H2, H3, cifras y "Sooni" del logo |
| `text-primary` | Cloud White | `#EDF2FA` | Texto principal en UI y botones secundarios |
| `badge-text` | Mist | `#C9D6EA` | Texto sobre `badge-bg` |
| `text-secondary` | Slate Mist | `#A0AEC6` | Cuerpo de texto, navegación, tagline |
| `text-tertiary` | Faint Slate | `#7E8BA3` | Metadatos, etiquetas, microcopy |

### 1.2 Color principal

| Token | Nombre | HEX | Uso |
| --- | --- | --- | --- |
| `primary` | Sky Bridge | `#8CBFF9` | Botón principal, borde del "Agendar" en navbar, barras de progreso, puntos de estado, enlaces, foco |
| `primary-hover` | Sky Light | `#A8D0FB` | Hover del botón principal |
| `on-primary` | Deep Space | `#090A17` | Texto sobre `primary` |
| `primary-soft` | Sky Mist | `#D6E8FD` | Nodos del fondo |

El azul cielo nunca se usa en cuerpo de texto, títulos, badges ni fondos de cards. Si aparece en más de cuatro lugares por pantalla, sobra en alguno.

### 1.3 Colores ambientales (solo fondo y degradado)

| Token | HEX | Dónde |
| --- | --- | --- |
| `nebula` | `#5B21B6` al 32% | Resplandor superior derecho del fondo |
| `void-indigo` | `#1E1B4B` al 70% | Sombra inferior izquierda y planeta fantasma |
| `orbit-violet` | `#A78BFA` al 14% | Órbita interior |
| `node-violet` | `#B794F6` | Un nodo del fondo y punto medio del degradado |
| `gradient-end` | `#A855F7` | Final del `highlight-gradient` |

Ningún componente (botón, card, badge, texto) usa estos violetas.

### 1.4 Colores restringidos

- **Neon Green `#00FF87` y Electric Cyan `#60EFFF`:** prohibidos en la interfaz. Solo existen dentro del logo.
- **Violeta `#7C3AED` (v2.0):** retirado como color de acción.
- **Azules del planeta (`#2563EB`, `#3B82F6`, `#4C1D95`):** reservados al isotipo.

### 1.5 Contrastes verificados (WCAG 2.1)

| Combinación | Contraste | Resultado |
| --- | --- | --- |
| `#EDF2FA` sobre `#090A17` | 17.5:1 | AAA |
| `#D6E8FD` sobre `#1A2238` | 12.7:1 | AAA |
| `#090A17` sobre `#A8D0FB` (hover) | 12.3:1 | AAA |
| `#C9D6EA` sobre `#1A2238` | 10.8:1 | AAA |
| `#090A17` sobre `#8CBFF9` (botón) | 10.2:1 | AAA |
| `#8CBFF9` sobre `#0F1526` | 9.5:1 | AAA |
| `#A0AEC6` sobre `#090A17` | 8.8:1 | AAA |
| `#A0AEC6` sobre `#0F1526` | 8.1:1 | AAA |
| `#7E8BA3` sobre `#0F1526` | 5.3:1 | AA |
| `#A855F7` sobre `#090A17` (final del degradado) | 5.0:1 | AA |

## 2. Psicología del color

La paleta se dirige a un comprador cauteloso: gasta más de US$2.000 al mes en IA, teme la fuga de datos y evalúa una implementación desde $35.000.000 COP.

| Color | Qué comunica | Por qué sirve a Sooniverse |
| --- | --- | --- |
| Azul cielo `#8CBFF9` | Calma, claridad, transparencia, confianza | Es el registro más institucional; reduce la fricción de agendar y tranquiliza al Perfil B (aseguradoras, EPS, cumplimiento) |
| Azul marino oscuro | Seguridad, solidez, bóveda | Encarna "tus datos no salen de tu perímetro" y deja que el botón y las cifras resalten |
| Toques violeta en el fondo | Exclusividad, profundidad, universo | Conservan el carácter premium sin cargar la interfaz |
| Logo multicolor | Firma tecnológica | Al ser lo único intenso de la pantalla, gana protagonismo y recordación |

**Conversión.** El botón de agendar es el único relleno azul cielo sólido de cada pantalla y el elemento más luminoso después del titular. Por el efecto de aislamiento (Von Restorff), el ojo lo encuentra sin buscarlo.

**El degradado como puente.** La frase destacada inicia en el mismo azul del botón, así que la promesa del titular y la acción quedan conectadas visualmente.

**Riesgo y cómo controlarlo.** El azul es el color más usado por empresas de cloud y ciberseguridad, así que solo no diferencia. La diferenciación la aportan el logo multicolor, el fondo Órbitas y la tipografía monoespaciada.

## 3. Degradados oficiales

Existen dos degradados. Ninguno se usa en botones, bordes ni fondos de componentes.

### 3.1 `cosmic-gradient` (logo, intocable)

- **Uso exclusivo:** "verse" del wordmark y anillos del isotipo.
- **Valor:** `linear-gradient(135deg, #00FF87 0%, #60EFFF 50%, #8A2BE2 100%)`
- No se altera ni se reutiliza en otros textos.

### 3.2 `highlight-gradient` (frase destacada)

- **Uso:** una sola frase clave por pantalla, normalmente la promesa numérica del hero (por ejemplo, "Hasta 74% menos").
- **Valor:** `linear-gradient(135deg, #8CBFF9 0%, #B794F6 50%, #A855F7 100%)`
- **Tamaño mínimo:** 24 px en peso 700 u 800. Por debajo de eso se usa `#FFFFFF` sin degradado.
- Inicia en el color principal para unir visualmente la promesa con el botón de agendar.

```css
.text-highlight {
  background: linear-gradient(135deg, #8CBFF9 0%, #B794F6 50%, #A855F7 100%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}
```

## 4. Logotipo e identidad verbal

El logo no cambia. Archivos maestros: `logo_sin_fondo.svg` (isotipo) y `logo_completo_sin_fondo_soloNombre2.svg` (isotipo + wordmark).

### 4.1 Naming y construcción

- **Escritura correcta:** `Sooniverse` (solo la S en mayúscula).
- **Wordmark:** `Inter` ExtraBold 800, letter-spacing -2 px. "Sooni" en `#FFFFFF`; "verse" con `cosmic-gradient`.
- **Isotipo:** planeta con degradado `#2563EB` → `#4C1D95` → `#1E1B4B`, anillos inclinados -18° y tres nodos (verde, cian, violeta). No se recolorea.

### 4.2 Tagline oficial

- **Texto:** `ADVANCED TECH UNIVERSE`. Queda prohibido "PRIVATE AI PLATFORM" como descriptor general.
- **Estilo:** `JetBrains Mono`, 11–13 px, Bold 700, mayúsculas, letter-spacing 3 px en web (6.5 px en gran formato).
- **Color:** `#A0AEC6`.
- **Prefijo:** punto de 6 px en `#8CBFF9` a 8 px a la izquierda.

### 4.3 Uso

- Solo sobre `#090A17`, `#0F1526` o el fondo Órbitas. Nunca sobre fondos claros.
- Ancho mínimo del logo completo: 140 px en pantalla. Por debajo se usa solo el isotipo.
- Área de respeto: la altura del planeta en los cuatro lados.
- Prohibido: sombras, contornos, cambiar el degradado o usar el wordmark sin el isotipo en la navbar.

## 5. Tipografía y jerarquía

Dos familias: `Inter` (alternativa `Plus Jakarta Sans`) para prosa y títulos, y `JetBrains Mono` (alternativa `Fira Code`) para datos, métricas, badges y taglines.

| Nivel | Fuente | Tamaño | Peso | Tracking | Color |
| --- | --- | --- | --- | --- | --- |
| H1 (hero) | Inter | 56 px (móvil 36 px) | 800 | -1.5 px | `#FFFFFF` |
| H2 (sección) | Inter | 36 px (móvil 28 px) | 700 | -1 px | `#FFFFFF` |
| H3 (card) | Inter | 22 px | 600 | 0 | `#FFFFFF` |
| Body | Inter | 16 px, line-height 1.6 | 400 | 0 | `#A0AEC6` |
| Botón primario | Inter | 15 px | 700 | 0 | `#090A17` |
| Botón secundario | Inter | 15 px | 500 | 0 | `#EDF2FA` |
| Navegación | Inter | 14 px | 500 | 0 | `#A0AEC6`, hover `#EDF2FA` |
| Tagline | JetBrains Mono | 11–13 px, mayúsculas | 700 | 3 px | `#A0AEC6` |
| Badge | JetBrains Mono | 11 px, mayúsculas | 700 | 1 px | `#C9D6EA` |
| Métrica | JetBrains Mono | 24–48 px | 700 | 0 | `#FFFFFF` |
| Microcopy | JetBrains Mono | 11–12 px, mayúsculas | 500 | 1.5 px | `#7E8BA3` |

## 6. Sistema de fondo "Órbitas"

El fondo repite a gran escala la geometría del isotipo sobre `#090A17`, con capas por debajo del 20% de opacidad. Mezcla el azul cielo principal con toques violeta para conservar el carácter de universo.

| Capa | Elemento | Valores |
| --- | --- | --- |
| 1. Nebulosa | Tres resplandores radiales | `rgba(91, 33, 182, 0.32)` arriba a la derecha (88% / 14%); `rgba(140, 191, 249, 0.10)` al centro derecha (70% / 48%); `rgba(30, 27, 75, 0.7)` abajo a la izquierda |
| 2. Rejilla estelar | Puntos de 0.9 px cada 22 px | `#8CBFF9` al 15%, con máscara radial que se desvanece al alejarse de la nebulosa |
| 3. Órbitas | Tres elipses inclinadas -18° + planeta fantasma | Exterior `#8CBFF9` al 10%; media `#8CBFF9` al 16% punteada 2-6; interior `#A78BFA` al 14%; planeta `#1E1B4B` al 35% |
| Nodos | Tres puntos sobre las órbitas | `#D6E8FD`, `#EDF2FA` y `#B794F6`, 2.5–3 px, con halo del mismo color al 8–20% |
| Grano (opcional) | Ruido estático | Opacidad 1.5–2% |

### 6.1 Reglas

- Las órbitas van detrás de la zona sin texto (lado derecho del hero) y no cruzan el titular a más del 10% de opacidad.
- Ningún nodo usa cian ni verde.
- Animación permitida: parpadeo lento de los nodos (ciclo de 4 s, opacidad 1 → 0.45, desfasados 1.3 s). Nada más se mueve.
- Con `prefers-reduced-motion: reduce`, la animación se desactiva.
- Se construye con CSS y SVG inline, sin imágenes.

### 6.2 Código de referencia

```html
<section class="orbits">
  <svg class="orbits__layer" viewBox="0 0 660 600" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
    <defs>
      <pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse">
        <circle cx="11" cy="11" r="0.9" fill="#8CBFF9" opacity="0.15"/>
      </pattern>
      <radialGradient id="fade" cx="78%" cy="28%" r="65%">
        <stop offset="0%" stop-color="#fff"/><stop offset="100%" stop-color="#000"/>
      </radialGradient>
      <mask id="m"><rect width="660" height="600" fill="url(#fade)"/></mask>
    </defs>
    <rect width="660" height="600" fill="url(#dots)" mask="url(#m)"/>
    <g transform="translate(545,165) rotate(-18)" fill="none">
      <ellipse rx="300" ry="86" stroke="#8CBFF9" stroke-opacity="0.10"/>
      <ellipse rx="215" ry="62" stroke="#8CBFF9" stroke-opacity="0.16" stroke-dasharray="2 6"/>
      <ellipse rx="135" ry="39" stroke="#A78BFA" stroke-opacity="0.14"/>
      <circle r="44" fill="#1E1B4B" fill-opacity="0.35" stroke="#8CBFF9" stroke-opacity="0.10"/>
    </g>
    <g transform="translate(545,165) rotate(-18)">
      <circle cx="-212" cy="-12" r="9" fill="#8CBFF9" opacity="0.14"/>
      <circle class="node" cx="-212" cy="-12" r="3" fill="#D6E8FD"/>
      <circle cx="128" cy="13" r="8" fill="#FFFFFF" opacity="0.08"/>
      <circle class="node" style="animation-delay:1.3s" cx="128" cy="13" r="2.5" fill="#EDF2FA"/>
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
    radial-gradient(ellipse 45% 50% at 88% 14%, rgba(91, 33, 182, 0.32), transparent 70%),
    radial-gradient(ellipse 45% 45% at 70% 48%, rgba(140, 191, 249, 0.10), transparent 70%),
    radial-gradient(ellipse 50% 45% at 0% 100%, rgba(30, 27, 75, 0.7), transparent 70%),
    #090A17;
}
.orbits__layer { position: absolute; inset: 0; width: 100%; height: 100%; pointer-events: none; }
.orbits__content { position: relative; }
@keyframes twinkle { 0%, 100% { opacity: 1; } 50% { opacity: 0.45; } }
.node { animation: twinkle 4s ease-in-out infinite; }
@media (prefers-reduced-motion: reduce) { .node { animation: none; } }
```

## 7. Componentes de interfaz

Radio de esquina máximo 12 px. Ningún componente usa degradado de fondo.

### 7.1 Cards

- **Sobre fondo liso:** fondo `#0F1526`, borde 1 px `#1F2940`, radio 12 px, padding 16–24 px.
- **Sobre fondo Órbitas (glass):** fondo `rgba(15, 21, 38, 0.72)`, borde 1 px `#1F2940`, `backdrop-filter: blur(12px)`.
- **Hover (si es interactiva):** borde `#8CBFF9` al 50%, `translateY(-2px)`, transición `all 0.3s ease`.

### 7.2 Botones

| Tipo | Fondo | Borde | Texto | Hover |
| --- | --- | --- | --- | --- |
| Primario | `#8CBFF9` | ninguno | `#090A17`, Inter 700 | Fondo `#A8D0FB`, `translateY(-2px)`, sombra `0 0 24px rgba(140, 191, 249, 0.35)` |
| Secundario | `rgba(15, 21, 38, 0.5)` | 1 px `#1F2940` | `#EDF2FA` | Borde `#8CBFF9` |
| Navbar (agendar) | transparente | 1 px `#8CBFF9` | `#EDF2FA` | Fondo `#8CBFF9`, texto `#090A17` |

- Padding primario: 12 × 20 px, radio 10 px.
- Texto en *sentence case* y concreto: "Agendar reunión de 30 min", no "Contáctanos" ni "ENVIAR".
- Un solo botón primario por vista.

### 7.3 Badges

- Fondo `#1A2238`, texto `#C9D6EA`, `JetBrains Mono` 11 px, mayúsculas, letter-spacing 1 px, radio 6 px, padding 3 × 8 px.

### 7.4 Métricas y progreso

- Etiqueta en `#7E8BA3` 12 px sobre la cifra.
- Cifra en `JetBrains Mono` 700, `#FFFFFF`.
- Barra de progreso: pista `#1F2940`, relleno `#8CBFF9`, alto 6 px, radio 3 px.
- Gráficos de varias series: `#8CBFF9`, `#C9D6EA`, `#7E8BA3`, en ese orden.

### 7.5 Estado "en línea"

- Punto de 7 px `#8CBFF9` a la izquierda del texto de estado.

### 7.6 Enlaces y foco

- Enlaces dentro de texto: `#8CBFF9`, subrayado en hover. En la navegación se usan neutros.
- Foco de teclado: `outline: 2px solid #8CBFF9; outline-offset: 2px`. Nunca se elimina.

### 7.7 Brillo (glow)

- Solo en el hover del botón primario y en los nodos del fondo.
- Fórmula: `box-shadow: 0 0 24px rgba(140, 191, 249, 0.35)`.

## 8. Reglas para la landing page

Toda la landing existe para que un prospecto calificado agende la reunión exploratoria gratuita de 30 minutos.

### 8.1 Jerarquía del hero (de arriba abajo)

1. Navbar: logo completo a la izquierda; navegación en `#A0AEC6` y botón "Agendar" (tipo navbar) a la derecha.
2. Tagline `ADVANCED TECH UNIVERSE` en `#A0AEC6` con punto `#8CBFF9`.
3. H1 en blanco con una sola frase en `highlight-gradient` (la promesa numérica).
4. Body en `#A0AEC6`, máximo dos líneas: privacidad y costo fijo.
5. Botón primario "Agendar reunión de 30 min" + botón secundario "Ver cómo funciona".
6. Microcopy de calificación en mono `#7E8BA3`: `SIN COSTO · PARA EQUIPOS CON +US$2K/MES EN IA`.
7. Tres cards glass: privacidad (badge), ahorro (métrica en blanco con barra cielo) e infraestructura (estado en línea).

### 8.2 Reglas de conversión

- Todos los botones primarios llevan al mismo destino: el agendamiento.
- El botón primario es el único relleno azul cielo sólido visible en cada pantalla.
- El microcopy de calificación acompaña siempre al CTA principal, para filtrar curiosos antes de la reunión.
- Repetir el CTA al final de cada bloque largo (cómo funciona, precios, casos) sin cambiar su texto.
- El fondo Órbitas completo va solo en el hero y en el bloque final de CTA. Las secciones intermedias usan `#090A17` liso o solo la nebulosa.

## 9. Reglas para los aplicativos (chat y dashboard)

En pantallas de uso diario la prioridad es la lectura cómoda durante horas, así que el fondo y los acentos se reducen.

### 9.1 Fondo

- Solo la nebulosa y la rejilla estelar. Sin órbitas ni nodos animados detrás de datos o conversaciones.
- Paneles y barras laterales en `#0F1526` sólido, sin glass.

### 9.2 Estados funcionales

No son colores de marca: aparecen solo cuando hay algo que comunicar, en tamaño pequeño (iconos, texto de estado, bordes de aviso).

| Estado | HEX | Fondo de aviso | Contraste sobre `#0F1526` | Uso |
| --- | --- | --- | --- | --- |
| Activo / en línea | `#8CBFF9` | ninguno | 9.5:1 | Nodo GPU, servicio disponible |
| Éxito | `#4ADE80` | `rgba(74, 222, 128, 0.10)` | 10.4:1 | Operación completada, key creada |
| Error | `#F87171` | `rgba(248, 113, 113, 0.10)` | 6.6:1 | Fallo de petición, key revocada |
| Alerta | `#FBBF24` | `rgba(251, 191, 36, 0.10)` | 10.9:1 | Límite de concurrencia, cuota cercana |

### 9.3 Componentes específicos

- **Chat:** burbuja del usuario en `#1A2238` con texto `#EDF2FA`; respuesta del modelo sin burbuja, sobre el fondo, en `#EDF2FA`.
- **Dashboard:** fila seleccionada en `#1A2238` con borde izquierdo 2 px `#8CBFF9`; divisores `#1F2940`; API Keys y valores técnicos en `JetBrains Mono`.
- **Densidad:** body de 14 px en tablas y paneles; 16 px en el chat.
- **Botón primario** (crear key, enviar): mismo estilo que en la landing, uno por vista.

## 10. Tokens para desarrolladores

Fuente única de verdad para la landing y los aplicativos. Ningún componente debe usar un HEX fuera de esta lista.

```css
:root {
  /* Neutros */
  --sv-bg-base: #090A17;
  --sv-bg-surface: #0F1526;
  --sv-bg-glass: rgba(15, 21, 38, 0.72);
  --sv-border: #1F2940;
  --sv-badge-bg: #1A2238;
  --sv-badge-text: #C9D6EA;
  --sv-text-heading: #FFFFFF;
  --sv-text-primary: #EDF2FA;
  --sv-text-secondary: #A0AEC6;
  --sv-text-tertiary: #7E8BA3;

  /* Principal */
  --sv-primary: #8CBFF9;
  --sv-primary-hover: #A8D0FB;
  --sv-on-primary: #090A17;
  --sv-primary-soft: #D6E8FD;

  /* Ambientales (solo fondo y degradado) */
  --sv-nebula: rgba(91, 33, 182, 0.32);
  --sv-sky-glow: rgba(140, 191, 249, 0.10);
  --sv-void-indigo: rgba(30, 27, 75, 0.7);
  --sv-orbit-violet: #A78BFA;
  --sv-node-violet: #B794F6;

  /* Estados (solo aplicativos) */
  --sv-success: #4ADE80;
  --sv-error: #F87171;
  --sv-warning: #FBBF24;

  /* Degradados */
  --sv-gradient-logo: linear-gradient(135deg, #00FF87 0%, #60EFFF 50%, #8A2BE2 100%);
  --sv-gradient-highlight: linear-gradient(135deg, #8CBFF9 0%, #B794F6 50%, #A855F7 100%);

  /* Forma y movimiento */
  --sv-radius-card: 12px;
  --sv-radius-button: 10px;
  --sv-radius-badge: 6px;
  --sv-glow: 0 0 24px rgba(140, 191, 249, 0.35);
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
        space: { DEFAULT: '#090A17', surface: '#0F1526', border: '#1F2940', steel: '#1A2238' },
        ink: { heading: '#FFFFFF', primary: '#EDF2FA', secondary: '#A0AEC6', tertiary: '#7E8BA3', badge: '#C9D6EA' },
        sky: { DEFAULT: '#8CBFF9', hover: '#A8D0FB', soft: '#D6E8FD' },
        state: { success: '#4ADE80', error: '#F87171', warning: '#FBBF24' },
      },
      borderRadius: { card: '12px', button: '10px', badge: '6px' },
      boxShadow: { glow: '0 0 24px rgba(140, 191, 249, 0.35)' },
      fontFamily: {
        sans: ['Inter', 'Plus Jakarta Sans', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
      },
    },
  },
};
```

Nota: la clave `sky` reemplaza la paleta `sky` por defecto de Tailwind. Si el proyecto ya la usa, renombrarla (por ejemplo, `brand`).

## 11. Instrucción maestra para IA

Copiar este bloque al inicio de cualquier prompt que genere diseño, código o imágenes para Sooniverse.

```text
[INSTRUCCIÓN MAESTRA DE DISEÑO: SOONIVERSE v3.0]
Eres un diseñador frontend experto. Para la marca Sooniverse:
- Fondo absoluto #090A17; superficies #0F1526; bordes #1F2940. Nunca fondos claros.
- Color principal: azul cielo #8CBFF9, usado con moderación (máximo cuatro lugares por pantalla): botón primario con texto #090A17 (hover #A8D0FB), borde del botón "Agendar" de la navbar, barras de progreso, puntos de estado, enlaces en texto y foco.
- Texto: títulos y cifras #FFFFFF; texto principal #EDF2FA; cuerpo y tagline #A0AEC6; metadatos #7E8BA3.
- Badges: fondo #1A2238 con texto #C9D6EA.
- Prohibido usar cian #60EFFF o verde #00FF87 en la interfaz; solo existen dentro del logo.
- Los violetas (#5B21B6, #A78BFA, #B794F6, #A855F7) solo aparecen en el fondo Órbitas y en el degradado de la frase destacada. Nunca en componentes.
- El logo no se modifica: "Sooni" en #FFFFFF y "verse" con linear-gradient(135deg, #00FF87, #60EFFF, #8A2BE2).
- Una sola frase por pantalla puede usar linear-gradient(135deg, #8CBFF9, #B794F6, #A855F7), a 24 px o más.
- Ningún botón, borde ni card lleva degradado. Radio máximo 12 px.
- Fondo del hero: sistema "Órbitas" (nebulosa violeta y cielo, rejilla de puntos #8CBFF9, tres elipses a -18°, tres nodos sin cian), por debajo del 20% de opacidad.
- Tipografía: Inter para prosa y títulos; JetBrains Mono para datos, badges y taglines.
- Un solo botón primario por vista; en la landing siempre lleva a "Agendar reunión de 30 min".
- Tono sobrio, claro, confiable y de alta seguridad. Si el resultado parece una plantilla corporativa genérica o una web con neón por todas partes, descártalo y rehazlo.
```

### 11.1 Checklist de revisión

- [ ] Ningún cian ni verde fuera del logo (salvo el estado de éxito en aplicativos).
- [ ] Un solo relleno azul cielo sólido por pantalla (el botón primario).
- [ ] El azul cielo aparece en cuatro lugares o menos por pantalla.
- [ ] Ningún violeta en botones, cards, badges ni texto.
- [ ] Como máximo una frase con `highlight-gradient`.
- [ ] Todo el texto cumple al menos AA (4.5:1).
- [ ] Las órbitas no cruzan el titular y la animación respeta `prefers-reduced-motion`.
- [ ] El logo usa los SVG maestros sin modificar.
