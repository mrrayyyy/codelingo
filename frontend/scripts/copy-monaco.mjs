import { mkdirSync } from "node:fs";
import { build } from "esbuild";
import { fileURLToPath } from "node:url";
const root = new URL("../", import.meta.url);
mkdirSync(new URL("public/monaco", root), { recursive: true });
// Rebuild from ESM so the patched DOMPurify dependency is included. Vendor min/
// distributions embed their own older dependency and cannot use npm overrides.
for (const [entry, output] of [["editor.api.js", "editor.js"], ["editor.worker.js", "editor.worker.js"]]) {
  await build({
    entryPoints: [fileURLToPath(new URL(`node_modules/monaco-editor/esm/vs/editor/${entry}`, root))],
    outfile: fileURLToPath(new URL(`public/monaco/${output}`, root)),
    bundle: true, minify: true, format: "iife", platform: "browser", target: "es2020",
    globalName: entry === "editor.api.js" ? "CodeLingoMonaco" : undefined,
    loader: { ".ttf": "file", ".woff": "file", ".woff2": "file" },
  });
}
