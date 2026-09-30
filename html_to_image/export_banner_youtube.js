const { chromium } = require('playwright-core');
const path = require('path');
const fs = require('fs');

(async () => {
  console.log('====================================================');
  console.log('  GENERANDO BANNER DE YOUTUBE PARA SOONIVERSE       ');
  console.log('  Especificaciones: 2048 × 1152 px (Mínimo oficial)  ');
  console.log('  Límite de peso YouTube: 6 MB                      ');
  console.log('====================================================\n');

  const outputDir = path.resolve(__dirname, 'export_banner_youtube');
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  console.log('1. Iniciando Chrome...');
  const browser = await chromium.launch({
    channel: 'chrome',
    headless: true
  });

  const context = await browser.newContext({
    viewport: { width: 2048, height: 1152 },
    deviceScaleFactor: 1
  });

  const page = await context.newPage();
  const filePath = path.resolve(__dirname, 'banner_youtube_sooniverse.html');
  console.log(`2. Cargando archivo HTML: ${filePath}`);
  await page.goto(`file://${filePath}`, { waitUntil: 'networkidle' });

  // Esperar a que las fuentes de Google (Inter, JetBrains Mono) estén cargadas
  await page.evaluate(async () => {
    await document.fonts.ready;
  });

  // Asegurar vista 100% limpia sin controles ni guías para la captura
  await page.evaluate(() => {
    const btnFull = document.getElementById('btnFull');
    if (btnFull) btnFull.click();

    const hdr = document.querySelector('.hdr');
    if (hdr) hdr.style.display = 'none';

    const controls = document.querySelector('.controls');
    if (controls) controls.style.display = 'none';

    const sims = document.querySelector('.sims');
    if (sims) sims.style.display = 'none';

    const banner = document.getElementById('banner');
    if (banner) {
      banner.classList.remove('show-guides');
    }

    const guides = document.querySelectorAll('.guides');
    guides.forEach(g => g.style.display = 'none');

    document.body.style.padding = '0';
    document.body.style.margin = '0';
    document.body.style.background = '#05070D';
  });

  // Breve pausa para asegurar renderizado perfecto de gradientes, noise y SVG
  await page.waitForTimeout(600);

  const bannerEl = await page.$('#banner');
  const box = await bannerEl.boundingBox();

  // 1. IMAGEN MÁSTER PARA SUBIR A YOUTUBE (2048 × 1152 px)
  const masterPathRoot = path.resolve(__dirname, 'banner_youtube_sooniverse.png');
  const masterPathFolder = path.join(outputDir, 'banner_youtube_master_2048x1152.png');

  console.log('3. Capturando imagen Máster 2048 × 1152 px...');
  await bannerEl.screenshot({
    path: masterPathRoot,
    type: 'png'
  });
  // Copia también dentro de la carpeta export_banner_youtube
  fs.copyFileSync(masterPathRoot, masterPathFolder);

  const statsMaster = fs.statSync(masterPathRoot);
  const sizeMasterMB = statsMaster.size / (1024 * 1024);
  const sizeMasterKB = statsMaster.size / 1024;
  console.log(`   ✓ Master guardado en: ${masterPathRoot}`);
  console.log(`   ✓ Tamaño: ${sizeMasterKB.toFixed(1)} KB (${sizeMasterMB.toFixed(2)} MB)`);
  if (sizeMasterMB <= 6) {
    console.log('   ✓ CUMPLE con el requisito de YouTube (menor a 6 MB)\n');
  } else {
    console.warn('   ⚠ ADVERTENCIA: Supera los 6 MB permitidos por YouTube.\n');
  }

  // 2. RECORTE DE VISTA EN ESCRITORIO (2048 × 338 px)
  console.log('4. Generando preview de Escritorio (2048 × 338 px)...');
  const deskPath = path.join(outputDir, 'banner_youtube_escritorio_2048x338.png');
  await page.screenshot({
    path: deskPath,
    type: 'png',
    clip: {
      x: box.x,
      y: box.y + 407,
      width: 2048,
      height: 338
    }
  });
  const statsDesk = fs.statSync(deskPath);
  console.log(`   ✓ Vista de Escritorio guardada: ${deskPath} (${(statsDesk.size / 1024).toFixed(1)} KB)\n`);

  // 3. RECORTE DE VISTA EN MÓVIL / ZONA SEGURA (1236 × 338 px)
  console.log('5. Generando preview de Móvil / Zona Segura (1236 × 338 px)...');
  const mobPath = path.join(outputDir, 'banner_youtube_movil_1236x338.png');
  await page.screenshot({
    path: mobPath,
    type: 'png',
    clip: {
      x: box.x + 406,
      y: box.y + 407,
      width: 1236,
      height: 338
    }
  });
  const statsMob = fs.statSync(mobPath);
  console.log(`   ✓ Vista Móvil guardada: ${mobPath} (${(statsMob.size / 1024).toFixed(1)} KB)\n`);

  await browser.close();

  console.log('====================================================');
  console.log('  ¡EXPORTACIÓN COMPLETADA CON ÉXITO!               ');
  console.log('====================================================');
  console.log(`Imagen principal lista para YouTube:`);
  console.log(`-> ${masterPathRoot}`);
})();
