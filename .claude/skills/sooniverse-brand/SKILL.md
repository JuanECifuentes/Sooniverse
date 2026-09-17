---
name: sooniverse-brand
description: Reglas de identidad visual de Sooniverse (paleta, tipografía, componentes, micro-interacciones, tono verbal). Usar SIEMPRE antes de escribir o modificar HTML/CSS/plantillas/componentes visuales de este proyecto, o cualquier imagen/diagrama de marca — landing, CRM interno, correos, PDFs o brochures. Dispara con: "landing", "CRM", "dashboard", "plantilla", "email/correo HTML", "color", "botón", "tarjeta/card", "logo", "SVG", "diagrama", "estilo", "Tailwind", "identidad de marca", "branding".
---

# Identidad de marca — Sooniverse

Destilado de `conceptos/Manual_de_imagen_sooniverse.md`. Ante cualquier duda de diseño en este proyecto, estas reglas ganan sobre el instinto genérico de "landing SaaS bonita" — Sooniverse es oscura, de alto contraste, con acentos neón, nunca una plantilla corporativa clara.

## 1. Paleta (estricta — nunca fondos claros ni pasteles)

| Rol | Nombre | HEX | Token Tailwind (`tailwind.config.js`) |
|---|---|---|---|
| Fondo principal | Deep Space | `#070A12` | `deep` |
| Fondo secundario (cards, modales) | Cyber Surface | `#0F172A` | `surface` |
| Borde estructural | — | `#1E293B` | `border` |
| Texto principal | Pure White | `#FFFFFF` | — |
| Texto secundario | Slate Gray | `#94A3B8` | `slate` |
| Acento primario (IA) | Neon Green | `#00FF87` | `neon` |
| Acento secundario (infra) | Electric Cyan | `#60EFFF` | `cyan` |
| Acento terciario (seguridad) | Cosmic Violet | `#8A2BE2` | `violet` |

**Prohibido:** `#FFFFFF` o similares como fondo, cualquier pastel, cualquier plantilla que se vea "corporativa estándar" — si el resultado parece un sitio B2B genérico, descartar y rehacer con más contraste oscuro/neón.

### Gradiente oficial `cosmic-gradient`
`linear-gradient(135deg, #00FF87 0%, #60EFFF 50%, #8A2BE2 100%)` — único ángulo y stops permitidos para cualquier degradado de marca (texto, botones, bordes decorativos). Ya existe como `backgroundImage['cosmic-gradient']` en `tailwind.config.js` y como clase `.text-cosmic` (gradiente en texto) en el CSS inline de `landing.html`.

## 2. Tipografía

- **Prosa y títulos:** `Inter` (300–800), sans-serif. H1 hero: 56px/ExtraBold(800)/tracking -1.5px. H2 sección: 36px/Bold(700)/tracking -1px. H3 componente: 22px/SemiBold(600). Body: 16px/Regular(400)/line-height 1.6, color `slate`.
- **Datos, código, métricas, badges, taglines:** `JetBrains Mono`, 12–14px, SemiBold(600), UPPERCASE, letter-spacing 6px (clase `tracking-brand` = 6.5px ya definida). Color `neon` para badges/kickers.

## 3. Naming y tagline (verbal)

- Escritura exacta: **`Sooniverse`** (solo la S mayúscula).
- Logo partido por color, una sola tipografía (`Inter` ExtraBold 800): `Sooni` en blanco puro + `verse` en `cosmic-gradient`. Patrón HTML ya usado en `emails/base_email.html`: `<span style="color:#FFFFFF">Sooni</span><span class="text-cosmic">verse</span>`.
- Tagline oficial obligatorio: **`ADVANCED TECH UNIVERSE`** — JetBrains Mono, uppercase, bold(700), letter-spacing 6.5px, color `#00FF87`.
- **Prohibido** usar "PRIVATE AI PLATFORM" como descriptor general de la empresa.

## 4. Componentes UI

### Cards / contenedores
- Fondo `rgba(15, 23, 42, 0.8)` (surface con 80% opacidad si necesita traslucidez).
- Borde 1px sólido `#1E293B`.
- **Radio de esquina máximo 12px** — nunca más, nunca estilo "burbuja".
- `backdrop-filter: blur(12px)` en paneles flotantes (clase `.glass-panel` ya existe).

### Botón primario (CTA)
- Fondo `cosmic-gradient`. Texto `#070A12`, `Inter` Bold(700), UPPERCASE.
- **Micro-interacción obligatoria en hover:** `transform: translateY(-2px)` + `transition: all 0.3s ease` + aumento del resplandor de sombra. Ya implementada como `.btn-primary` en `landing.html` y como `.btn-email-primary` en los correos — replicar ese patrón, no reinventarlo.

### Botón secundario
- Fondo transparente, borde 1.5px sólido `#60EFFF`, texto `#FFFFFF`.

### Glow / resplandor neón
Fórmula fija para estados activos o elementos interactivos clave:
`filter: drop-shadow(0px 0px 12px rgba(96, 239, 255, 0.6))` (sustituir el color rgba por el acento correspondiente cuando el elemento no sea cyan — p. ej. `rgba(0,255,135,0.6)` para acentos neón, `rgba(239,68,68,0.6)` para elementos de riesgo/alerta).

### Grano / textura
Ruido digital estático sutil (opacidad 1.5–2%) sobre todo el fondo de pantalla. Ya implementado como `.noise-overlay` (SVG `feTurbulence` en data-URI) en `landing.html` y `base_internal.html` — reutilizar ese patrón, no crear una segunda capa de ruido.

## 5. Instrucción maestra (resumen operativo)

Al generar o modificar cualquier componente visual, CSS o imagen de Sooniverse: fondo absoluto `#070A12`, sin pasteles, sin fondos blancos, radio máximo 12px, logo con la división de color exacta, tono tecnológico/sofisticado/alto-contraste. Si el resultado parece una plantilla de negocio estándar, descartarlo y rehacerlo con más contraste oscuro y brillo neón controlado.

## 6. Nota operativa crítica — Tailwind está precompilado

`static/css/dist/tailwind.css` se genera con `npm run build` (`tailwindcss -i ./static/css/src/tailwind.css -o ./static/css/dist/tailwind.css --minify`) a partir de `tailwind.config.js`. **Cualquier clase utilitaria de Tailwind que no exista ya en el CSS compilado es un no-op silencioso** — no hay purga en desarrollo, hay purga real en el build de producción. Prueba viva del bug: `landing.html` usa `bg-cosmic` (línea ~356) que no es una utilidad definida (solo existe `backgroundImage['cosmic-gradient']`, o sea `bg-cosmic-gradient`) y no pinta nada.

**Regla práctica:** al escribir markup nuevo, usar solo clases Tailwind que ya aparezcan en algún `.html` del proyecto, o CSS propio dentro del bloque `<style>` inline de la plantilla (patrón ya usado en `landing.html`, `base_public.html`, `base_internal.html`). Si de verdad hace falta una utilidad nueva, hay que correr `npm run build` después — decirlo explícitamente si se depende de eso.

## 7. Dónde ya vive cada patrón (reutilizar, no reinventar)

| Patrón | Archivo |
|---|---|
| Paleta y tokens | `tailwind.config.js` |
| CSS de marca para la landing (botones, glow, glass-panel, ruido) | `apps/core/templates/core/landing.html` (bloque `<style>` inline) |
| CSS de marca para páginas internas/CRM | `apps/core/templates/core/base_internal.html`, `base_public.html` |
| Plantilla base de correo con header/footer de marca | `apps/core/templates/core/emails/base_email.html` |
| Ejemplo de diagrama SVG animado (SMIL + `flow-dash`/`pulse-glow`) | `svg_animado_ejemplo.html` (colores de este archivo son placeholders — recolorear siempre a la paleta de marca antes de usar) |
