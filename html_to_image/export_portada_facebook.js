const { chromium } = require('playwright-core');
const path = require('path');
const fs = require('fs');

(async () => {
  console.log('--- EXPORTANDO PORTADAS DE FACEBOOK ---');

  const outputDir = path.resolve(__dirname, 'export_portada_facebook');
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  const browser = await chromium.launch({
    channel: 'chrome',
    headless: true
  });

  // Usamos deviceScaleFactor: 1 para las medidas exactas
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1400 },
    deviceScaleFactor: 1
  });

  const page = await context.newPage();
  const filePath = path.resolve(__dirname, 'portada_facebook_sooniverse.html');
  console.log(`Cargando archivo: ${filePath}`);
  await page.goto(`file://${filePath}`, { waitUntil: 'networkidle' });

  // Esperar a que las fuentes de Google estén completamente listas
  await page.evaluate(async () => {
    await document.fonts.ready;
  });

  // Asegurar vista a 100% (sin escala de zoom out) y sin guías
  await page.evaluate(() => {
    const bU = document.getElementById('btnFull');
    if (bU) bU.click();

    // Eliminar o esconder cualquier texto de control, títulos y encabezados de la página
    const hdr = document.querySelector('.hdr');
    if (hdr) hdr.style.display = 'none';
    const controls = document.querySelector('.controls');
    if (controls) controls.style.display = 'none';

    // Ocultar guías por seguridad
    const cover = document.getElementById('cover');
    if (cover) cover.classList.remove('show-guides');
    const guides = document.querySelectorAll('.guides');
    guides.forEach(g => g.style.display = 'none');

    // Ocultar los textos que indican el tamaño en las simulaciones (h3 y p)
    document.querySelectorAll('.sim h3, .sim p').forEach(el => el.style.display = 'none');

    // Quitar padding o fondos extras en las cajas de simulación para captura limpia
    document.querySelectorAll('.sim').forEach(sim => {
      sim.style.padding = '0';
      sim.style.background = 'transparent';
      sim.style.border = 'none';
    });
  });

  // Pausa breve para renderizado de gradientes, filtros y SVGs
  await page.waitForTimeout(600);

  // 1. DIMENSIÓN 1: Portada completa / Master (1640 × 924 px)
  const coverEl = await page.$('#cover');
  const pathMaster = path.join(outputDir, 'portada_facebook_master_1640x924.png');
  await coverEl.screenshot({
    path: pathMaster,
    type: 'png'
  });
  const statsMaster = fs.statSync(pathMaster);
  console.log(`✓ Master (1640x924) guardada: ${pathMaster} (${(statsMaster.size / 1024).toFixed(1)} KB)`);

  // 2. DIMENSIÓN 2: Escritorio (820 × 312 px)
  const winDesk = await page.$('.win.desktop');
  const pathDesk = path.join(outputDir, 'portada_facebook_escritorio_820x312.png');
  await winDesk.screenshot({
    path: pathDesk,
    type: 'png'
  });
  const statsDesk = fs.statSync(pathDesk);
  console.log(`✓ Escritorio (820x312) guardada: ${pathDesk} (${(statsDesk.size / 1024).toFixed(1)} KB)`);

  // 3. DIMENSIÓN 3: Móvil (640 × 360 px)
  const winMob = await page.$('.win.mobile');
  const pathMob = path.join(outputDir, 'portada_facebook_movil_640x360.png');
  await winMob.screenshot({
    path: pathMob,
    type: 'png'
  });
  const statsMob = fs.statSync(pathMob);
  console.log(`✓ Móvil (640x360) guardada: ${pathMob} (${(statsMob.size / 1024).toFixed(1)} KB)`);

  // 4. VERSIÓN EXTRA HD: Recorte de Escritorio a alta resolución (1640 × 624 px)
  // En Facebook desktop, los 150px de arriba y abajo se recortan de los 924px (924 - 300 = 624px)
  const pathDeskHD = path.join(outputDir, 'portada_facebook_escritorio_1640x624_hd.png');
  const coverBox = await coverEl.boundingBox();
  if (coverBox) {
    await page.screenshot({
      path: pathDeskHD,
      type: 'png',
      clip: {
        x: coverBox.x,
        y: coverBox.y + 150,
        width: 1640,
        height: 624
      }
    });
    const statsDeskHD = fs.statSync(pathDeskHD);
    console.log(`✓ Escritorio HD (1640x624) guardada: ${pathDeskHD} (${(statsDeskHD.size / 1024).toFixed(1)} KB)`);
  }

  await browser.close();
  console.log('Exportación de Facebook finalizada exitosamente.');
})();
