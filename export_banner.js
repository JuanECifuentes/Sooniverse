const { chromium } = require('playwright-core');
const path = require('path');
const fs = require('fs');

(async () => {
  console.log('Launching Chrome...');
  const browser = await chromium.launch({
    channel: 'chrome',
    headless: true
  });

  const context = await browser.newContext({
    viewport: { width: 1584, height: 396 },
    deviceScaleFactor: 2
  });

  const page = await context.newPage();
  const filePath = path.resolve(__dirname, 'banner_linkedin_sooniverse.html');
  console.log(`Loading file: ${filePath}`);
  await page.goto(`file://${filePath}`, { waitUntil: 'networkidle' });

  // Wait for Google fonts to be fully rendered
  await page.evaluate(async () => {
    await document.fonts.ready;
  });

  // Short pause to guarantee gradients, noise filter, and SVGs are composited
  await page.waitForTimeout(500);

  const banner = await page.$('#banner');
  const outputPath = path.resolve(__dirname, 'banner_linkedin_sooniverse.png');
  await banner.screenshot({
    path: outputPath,
    type: 'png'
  });

  const stats = fs.statSync(outputPath);
  console.log(`Screenshot saved successfully: ${outputPath}`);
  console.log(`File size: ${(stats.size / 1024).toFixed(1)} KB`);

  await browser.close();
})();
