// Convertit un fichier HTML en PDF A4 avec Chromium (Playwright global).
// Usage : node tres-fute/outils/html-vers-pdf.mjs <entree.html> <sortie.pdf>
import { createRequire } from 'module';
import { execSync } from 'child_process';
import path from 'path';

const require = createRequire(import.meta.url);
const racineGlobale = execSync('npm root -g').toString().trim();
const { chromium } = require(path.join(racineGlobale, 'playwright'));

const [, , entree, sortie] = process.argv;
if (!entree || !sortie) {
  console.error('Usage : node html-vers-pdf.mjs <entree.html> <sortie.pdf>');
  process.exit(1);
}
const navigateur = await chromium.launch();
const page = await navigateur.newPage();
await page.goto('file://' + path.resolve(entree));
await page.pdf({ path: sortie, format: 'A4', printBackground: true, preferCSSPageSize: true });
await navigateur.close();
