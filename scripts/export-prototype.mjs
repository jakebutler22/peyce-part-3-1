// Export the built design as one offline HTML artifact, without a service.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const dist = path.join(root, 'frontend/dist');
let html = fs.readFileSync(path.join(dist, 'index.html'), 'utf8');
const script = html.match(/<script[^>]+src="([^"]+)"[^>]*><\/script>/);
const style = html.match(/<link[^>]+href="([^"]+\.css)"[^>]*>/);
if (!script || !style) throw new Error('Expected built Vite script and stylesheet');
const dataURL = filename => {
  const file = path.join(dist, filename.replace(/^\//, ''));
  const mime = filename.endsWith('.png') ? 'image/png' : 'font/ttf';
  return `data:${mime};base64,${fs.readFileSync(file).toString('base64')}`;
};
let js = fs.readFileSync(path.join(dist, script[1].slice(1)), 'utf8');
let css = fs.readFileSync(path.join(dist, style[1].slice(1)), 'utf8');
js = js.replaceAll('/assets/bow.png', dataURL('/assets/bow.png')).replaceAll('/assets/balloon.png', dataURL('/assets/balloon.png'));
css = css.replace(/url\((['"]?)(\/assets\/fonts\/[^)'" ]+)\1\)/g, (_, quote, filename) => `url("${dataURL(filename)}")`);
// Callback replacements preserve literal dollar sequences in compiled Vue code.
html = html.replace(script[0], () => `<script type="module">${js.replaceAll('</script', '<\\/script')}</script>`).replace(style[0], () => `<style>${css}</style>`);
const licenses = ['dmsans', 'playfairdisplay'].map(family => fs.readFileSync(path.join(dist, 'assets/fonts', family, 'OFL.txt'), 'utf8')).join('\n\n').split(/\r?\n/).map(line => line.trimEnd()).join('\n');
html = html.replace('<head>', () => `<head><!-- Peyce Part 3.1 offline design prototype. Scripted, fictional, no persistence or monitoring. --><script type="text/plain" id="font-licenses">\n${licenses}\n</script>`);
const destination = path.join(root, 'submissions/3.1/prototype.html');
fs.writeFileSync(destination, html);
console.log(`Offline prototype exported: ${path.relative(root, destination)} (${Buffer.byteLength(html)} bytes)`);
