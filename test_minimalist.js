const { chromium } = require('playwright-core');
const path = require('path');

(async () => {
  const browser = await chromium.launch({ channel: 'chrome', headless: true });
  const page = await browser.newPage({ viewport: { width: 1584, height: 396 }, deviceScaleFactor: 2 });
  await page.goto('file://' + path.resolve(__dirname, 'banner_linkedin_sooniverse.html'));
  await page.evaluate(() => document.fonts.ready);
  
  await page.evaluate(() => {
    // 1. Remove eyebrow, subline, flow, and CTA card
    document.querySelector('.eyebrow')?.remove();
    document.querySelector('.subline')?.remove();
    document.querySelector('.flow')?.remove();
    document.querySelector('.metric.m-cta')?.remove();
    
    // 2. Lockup
    document.querySelector('.lockup').style.top = '30px';
    document.querySelector('.lockup').style.left = '48px';
    const lockupSvg = document.querySelector('.lockup svg');
    lockupSvg.setAttribute('width', '68');
    lockupSvg.setAttribute('height', '68');
    document.querySelector('.wordmark').style.fontSize = '46px';
    document.querySelector('.site').style.fontSize = '22px';
    
    // 3. Content container
    const content = document.querySelector('.content');
    content.style.padding = '0 48px 0 424px';
    content.style.justifyContent = 'center';
    content.style.alignItems = 'flex-end';
    
    // 4. Headline
    const headline = document.querySelector('h1.headline');
    headline.style.marginTop = '0';
    headline.style.fontSize = '64px';
    headline.style.lineHeight = '1.05';
    headline.style.letterSpacing = '-2px';
    
    // 5. Metrics
    const metrics = document.querySelector('.metrics');
    metrics.style.marginTop = '22px';
    metrics.style.width = 'auto';
    metrics.style.gap = '20px';
    
    document.querySelectorAll('.metric').forEach(m => {
      m.style.padding = '14px 28px 14px 22px';
      m.style.gap = '18px';
      m.style.borderRadius = '14px';
    });
    
    document.querySelectorAll('.metric svg').forEach(s => {
      s.setAttribute('width', '48');
      s.setAttribute('height', '48');
    });
    
    document.querySelectorAll('.metric .n').forEach(n => {
      n.style.fontSize = '56px';
      n.style.letterSpacing = '-2px';
    });
    
    document.querySelectorAll('.metric .l').forEach(l => {
      l.style.fontSize = '16.5px';
      l.style.letterSpacing = '2.4px';
      l.style.lineHeight = '1.35';
    });
    
    // 6. CTA text under metrics
    const ctaText = document.createElement('div');
    ctaText.className = 'cta-line';
    ctaText.innerHTML = `
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#60EFFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="flex:none;filter:drop-shadow(0 0 6px rgba(96,239,255,.6))">
        <rect x="2" y="4" width="20" height="16" rx="2"/>
        <path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>
      </svg>
      <span class="cta-q" style="color:#00FF87;font-family:'JetBrains Mono',monospace;font-size:20px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;text-shadow:0 0 16px rgba(0,255,135,.45)">¿Listo para tu IA privada?</span>
      <span class="cta-call" style="color:#FFFFFF;font-weight:600;font-size:21px;letter-spacing:-.2px">Escríbeme:</span>
      <span class="cta-email" style="color:#60EFFF;font-family:'JetBrains Mono',monospace;font-size:22px;font-weight:700;letter-spacing:.5px;text-shadow:0 0 16px rgba(96,239,255,.55)">contacto@sooniverse.co</span>
    `;
    ctaText.style.marginTop = '20px';
    ctaText.style.display = 'flex';
    ctaText.style.alignItems = 'center';
    ctaText.style.gap = '12px';
    
    content.appendChild(ctaText);
  });

  const banner = await page.$('#banner');
  await banner.screenshot({ path: path.resolve(__dirname, 'test_minimalist_preview.png') });
  console.log('Minimalist preview generated successfully!');
  await browser.close();
})();
