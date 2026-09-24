const { chromium } = require('playwright-core');
const path = require('path');
const fs = require('fs');

(async () => {
  console.log('=== EXPORTANDO HISTORIAS Y DESTACADAS DE INSTAGRAM (ACTUALIZADAS) ===');

  const baseDir = path.resolve(__dirname, 'export_historias_instagram');
  const historiasDir = path.join(baseDir, 'historias');
  const destacadasDir = path.join(baseDir, 'portadas_destacadas');

  // Limpiar historias previas para asegurar consistencia con el nuevo contenido
  if (fs.existsSync(historiasDir)) {
    fs.rmSync(historiasDir, { recursive: true, force: true });
  }
  fs.mkdirSync(historiasDir, { recursive: true });
  if (!fs.existsSync(destacadasDir)) fs.mkdirSync(destacadasDir, { recursive: true });

  const browser = await chromium.launch({
    channel: 'chrome',
    headless: true
  });

  const context = await browser.newContext({
    viewport: { width: 1080, height: 1920 },
    deviceScaleFactor: 1
  });

  const page = await context.newPage();
  const filePath = path.resolve(__dirname, 'historias_faq_instagram.html');
  console.log(`Cargando archivo: ${filePath}`);
  await page.goto(`file://${filePath}`, { waitUntil: 'networkidle' });

  // Esperar a que las fuentes web estén completamente listas
  await page.evaluate(async () => {
    await document.fonts.ready;
  });

  await page.waitForTimeout(600);

  // Asegurar que las zonas seguras estén totalmente ocultas y eliminadas
  await page.evaluate(() => {
    document.querySelectorAll('.st-safe').forEach(el => el.remove());
    document.querySelectorAll('.story').forEach(s => s.classList.remove('show-safe'));

    const stage = document.createElement('div');
    stage.id = 'export-stage';
    stage.style.position = 'fixed';
    stage.style.top = '0';
    stage.style.left = '0';
    stage.style.width = '1080px';
    stage.style.height = '1920px';
    stage.style.zIndex = '9999999';
    stage.style.overflow = 'hidden';
    stage.style.background = '#070A12';
    stage.style.display = 'none';
    document.body.appendChild(stage);
  });

  // Extraer dinámicamente todas las historias del DOM generado por DATA
  const storiesList = await page.evaluate(() => {
    const list = [];
    document.querySelectorAll('#groups .group').forEach((grp, gi) => {
      const groupNum = String(gi + 1).padStart(2, '0');
      const groupTitle = grp.querySelector('.group-hd h3')?.textContent?.trim() || `grupo_${gi+1}`;
      const groupSlug = groupTitle.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "").replace(/[^a-z0-9]+/g, '_').replace(/^_+|_+$/g, '');

      grp.querySelectorAll('.item').forEach((item, ii) => {
        const story = item.querySelector('.story');
        if (!story) return;
        const id = story.id;
        const idx = String(ii).padStart(2, '0');
        let title = '';
        if (story.classList.contains('cover')) {
          title = 'portada';
        } else {
          const q = story.querySelector('.st-q')?.textContent?.trim() || '';
          title = q.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "").replace(/[^a-z0-9]+/g, '_').replace(/^_+|_+$/g, '');
          if (title.length > 30) title = title.substring(0, 30).replace(/_+$/, '');
        }
        const filename = `${groupNum}_${idx}_${groupSlug}_${title}.png`;
        list.push({ id, filename, desc: `${groupTitle} - ${title}` });
      });
    });
    return list;
  });

  console.log(`\n--- Se detectaron ${storiesList.length} Historias completas a 1080x1920 px ---`);

  for (let idx = 0; idx < storiesList.length; idx++) {
    const item = storiesList[idx];
    const outPath = path.join(historiasDir, item.filename);

    await page.evaluate((id) => {
      const story = document.getElementById(id);
      if (!story) return;
      const stage = document.getElementById('export-stage');
      story._prevParent = story.parentElement;
      stage.appendChild(story);
      stage.style.display = 'block';
      story.style.position = 'absolute';
      story.style.top = '0';
      story.style.left = '0';
      story.style.transform = 'none';
    }, item.id);

    await page.waitForTimeout(80);

    const stageEl = await page.$('#export-stage');
    await stageEl.screenshot({
      path: outPath,
      type: 'png'
    });

    await page.evaluate((id) => {
      const story = document.getElementById(id);
      if (!story) return;
      story.style.position = 'absolute';
      story.style.top = '0';
      story.style.left = '0';
      story.style.transform = 'scale(.238888)';
      if (story._prevParent) {
        story._prevParent.appendChild(story);
      }
      document.getElementById('export-stage').style.display = 'none';
    }, item.id);

    const sz = (fs.statSync(outPath).size / 1024).toFixed(1);
    console.log(`[${idx + 1}/${storiesList.length}] ✓ ${item.filename} (1080x1920, ${sz} KB) - ${item.desc}`);
  }

  console.log(`\n--- Exportando Portadas de Destacadas Cuadradas 1:1 (1080 × 1080 px) ---`);

  const coverStories = [
    { id: 'st-1-0', squareFile: '01_destacada_que_es_1080x1080.png', name: 'Qué es' },
    { id: 'st-2-0', squareFile: '02_destacada_beneficios_1080x1080.png', name: 'Beneficios' },
    { id: 'st-3-0', squareFile: '03_destacada_faq_1080x1080.png', name: 'FAQ' }
  ];

  for (const cov of coverStories) {
    await page.evaluate((id) => {
      const story = document.getElementById(id);
      const stage = document.getElementById('export-stage');
      story._prevParent = story.parentElement;
      stage.appendChild(story);
      stage.style.display = 'block';
      story.style.position = 'absolute';
      story.style.top = '0';
      story.style.left = '0';
      story.style.transform = 'none';
    }, cov.id);

    await page.waitForTimeout(100);

    const squarePath = path.join(destacadasDir, cov.squareFile);
    await page.screenshot({
      path: squarePath,
      type: 'png',
      clip: { x: 0, y: 420, width: 1080, height: 1080 }
    });
    console.log(`✓ Portada 1:1 (${cov.name}): ${cov.squareFile} (1080x1080, ${(fs.statSync(squarePath).size / 1024).toFixed(1)} KB)`);

    await page.evaluate((id) => {
      const story = document.getElementById(id);
      story.style.position = 'absolute';
      story.style.top = '0';
      story.style.left = '0';
      story.style.transform = 'scale(.238888)';
      if (story._prevParent) story._prevParent.appendChild(story);
      document.getElementById('export-stage').style.display = 'none';
    }, cov.id);
  }

  // Círculos de destacada del HTML original (.cov .ring)
  const covRings = await page.$$('.covers .cov');
  const covNames = ['01_circulo_destacada_que_es.png', '02_circulo_destacada_beneficios.png', '03_circulo_destacada_faq.png'];
  for (let i = 0; i < covRings.length; i++) {
    const ring = await covRings[i].$('.ring');
    if (ring) {
      const ringPath = path.join(destacadasDir, covNames[i]);
      await ring.screenshot({
        path: ringPath,
        type: 'png',
        omitBackground: true
      });
      console.log(`✓ Círculo destacada: ${covNames[i]} (${(fs.statSync(ringPath).size / 1024).toFixed(1)} KB)`);
    }
  }

  await page.close();

  console.log(`\n--- Exportando Iconos Individuales Autónomos (L196-L221) en SVG y PNG Transparente ---`);

  // Definiciones completamente autónomas con gradientes embebidos en el propio SVG
  const standaloneSvgs = {
    planeta: `<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="-140 -140 280 280">
  <defs>
    <linearGradient id="p_lg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00FF87"/>
      <stop offset="50%" stop-color="#60EFFF"/>
      <stop offset="100%" stop-color="#8A2BE2"/>
    </linearGradient>
    <linearGradient id="p_lp" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#2563EB"/>
      <stop offset="45%" stop-color="#4C1D95"/>
      <stop offset="100%" stop-color="#1E1B4B"/>
    </linearGradient>
  </defs>
  <g transform="rotate(-18)">
    <path d="M -68,0 A 68,19 0 0,1 68,0" fill="none" stroke="url(#p_lg)" stroke-width="2.5" stroke-opacity=".35"/>
    <path d="M -92,0 A 92,26 0 0,1 92,0" fill="none" stroke="url(#p_lg)" stroke-width="11" stroke-opacity=".4"/>
    <path d="M -114,0 A 114,32 0 0,1 114,0" fill="none" stroke="url(#p_lg)" stroke-width="3.5" stroke-opacity=".3"/>
  </g>
  <circle r="46" fill="url(#p_lp)" stroke="#3B82F6" stroke-width="1.5" stroke-opacity=".5"/>
  <path d="M -45,12 Q 0,26 45,12" fill="none" stroke="#00FF87" stroke-width="1.5" stroke-opacity=".5"/>
  <g transform="rotate(-18)">
    <path d="M 68,0 A 68,19 0 0,1 -68,0" fill="none" stroke="url(#p_lg)" stroke-width="2.5" stroke-linecap="round"/>
    <path d="M 92,0 A 92,26 0 0,1 -92,0" fill="none" stroke="url(#p_lg)" stroke-width="11" stroke-linecap="round"/>
    <path d="M 92,0 A 92,26 0 0,1 -92,0" fill="none" stroke="#FFF" stroke-width="2" stroke-opacity=".85" stroke-linecap="round"/>
    <path d="M 114,0 A 114,32 0 0,1 -114,0" fill="none" stroke="url(#p_lg)" stroke-width="3.5" stroke-linecap="round"/>
  </g>
  <circle cx="-80" cy="-45" r="9" fill="#00FF87"/><circle cx="-80" cy="-45" r="4" fill="#FFF"/>
  <circle cx="104" cy="12" r="7.5" fill="#60EFFF"/>
  <circle cx="15" cy="58" r="8.5" fill="#8A2BE2"/><circle cx="15" cy="58" r="3" fill="#60EFFF"/>
</svg>`,

    beneficios: `<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 24 24" fill="none" stroke="#00FF87" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
  <path d="M12 2.4l2.5 1.5 2.9-.3 1 2.7 2.4 1.7-1 2.7 1 2.7-2.4 1.7-1 2.7-2.9-.3L12 21.6l-2.5-1.5-2.9.3-1-2.7-2.4-1.7 1-2.7-1-2.7 2.4-1.7 1-2.7 2.9.3z"/>
  <path d="M8.6 12.2l2.3 2.3 4.5-4.7"/>
</svg>`,

    faq: `<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 24 24" fill="none" stroke="#60EFFF" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="12" cy="12" r="9.3"/>
  <path d="M9.3 9.2a2.8 2.8 0 1 1 3.6 2.7c-.6.2-.9.7-.9 1.3v.6"/>
  <path d="M12 17.2h.01"/>
</svg>`
  };

  const iconFiles = [
    { key: 'planeta', svgName: 'icono_planeta.svg', pngName: 'icono_planeta.png' },
    { key: 'beneficios', svgName: 'icono_beneficios.svg', pngName: 'icono_beneficios.png' },
    { key: 'faq', svgName: 'icono_faq.svg', pngName: 'icono_faq.png' }
  ];

  for (const item of iconFiles) {
    const svgPath = path.join(destacadasDir, item.svgName);
    fs.writeFileSync(svgPath, standaloneSvgs[item.key], 'utf8');
    console.log(`✓ SVG autónomo guardado: ${item.svgName}`);
  }

  const renderContext = await browser.newContext({
    viewport: { width: 512, height: 512 },
    deviceScaleFactor: 2
  });
  const renderPage = await renderContext.newPage();

  for (const item of iconFiles) {
    const pngPath = path.join(destacadasDir, item.pngName);
    const htmlDoc = `<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  html, body { margin: 0; padding: 0; width: 512px; height: 512px; background: transparent; overflow: hidden; display: flex; align-items: center; justify-content: center; }
  svg { width: 440px; height: 440px; }
</style>
</head>
<body>
  ${standaloneSvgs[item.key]}
</body>
</html>`;
    await renderPage.setContent(htmlDoc, { waitUntil: 'load' });
    await renderPage.waitForTimeout(100);

    await renderPage.screenshot({
      path: pngPath,
      type: 'png',
      omitBackground: true
    });
    console.log(`✓ PNG transparente guardado: ${item.pngName} (${(fs.statSync(pngPath).size / 1024).toFixed(1)} KB)`);
  }

  const circleHighRes = [
    { key: 'planeta', name: '01_circulo_hd_que_es.png' },
    { key: 'beneficios', name: '02_circulo_hd_beneficios.png' },
    { key: 'faq', name: '03_circulo_hd_faq.png' }
  ];

  for (const item of circleHighRes) {
    const pngPath = path.join(destacadasDir, item.name);
    const htmlCircle = `<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  :root {
    --cosmic: linear-gradient(135deg, #00FF87 0%, #60EFFF 50%, #8A2BE2 100%);
  }
  html, body { margin: 0; padding: 0; width: 512px; height: 512px; background: transparent; overflow: hidden; display: flex; align-items: center; justify-content: center; }
  .ring {
    width: 460px; height: 460px; border-radius: 50%; padding: 10px;
    background: var(--cosmic);
    box-shadow: 0 0 50px rgba(96,239,255,.5);
    display: flex; align-items: center; justify-content: center;
  }
  .in {
    width: 100%; height: 100%; border-radius: 50%;
    background: radial-gradient(circle at center, #0F172A 0%, #070A12 100%);
    border: 3px solid rgba(96,239,255,.4);
    box-shadow: 0 0 40px rgba(96,239,255,.25) inset;
    display: flex; align-items: center; justify-content: center;
  }
  svg { width: 280px; height: 280px; }
</style>
</head>
<body>
  <div class="ring"><div class="in">${standaloneSvgs[item.key]}</div></div>
</body>
</html>`;
    await renderPage.setContent(htmlCircle, { waitUntil: 'load' });
    await renderPage.waitForTimeout(100);

    await renderPage.screenshot({
      path: pngPath,
      type: 'png',
      omitBackground: true
    });
    console.log(`✓ Círculo HD transparente: ${item.name} (${(fs.statSync(pngPath).size / 1024).toFixed(1)} KB)`);
  }

  await renderContext.close();
  await browser.close();
  console.log('\n=== Exportación de Instagram finalizada con éxito total. ===');
})();
