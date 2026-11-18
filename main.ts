// World News One Image — make.fun entry for news-image-20261117.
//
// The entry is a program that writes one image to /output/entry.png.
// The image itself is the pre-rendered poster in this repository
// (entry.png, 1024x1024, drawn by draw_poster.py from verified reporting
// on 17 November 2026), so this program copies it there byte for byte.
// Node 22, standard library only, no network, deterministic: the same
// bytes go out on every run.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { join } from "node:path";

const source = new URL("./entry.png", import.meta.url);
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const target = join(outDir, "entry.png");

// Validate the image before copying: PNG signature, 1024x1024, <= 1 MiB.
const bytes = readFileSync(source);
if (bytes.length > 1024 * 1024) {
  throw new Error(`entry.png is ${bytes.length} bytes, over the 1 MiB cap`);
}
const pngSig = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!bytes.subarray(0, 8).equals(pngSig)) {
  throw new Error("entry.png is not a PNG file");
}
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width !== 1024 || height !== 1024) {
  throw new Error(`entry.png is ${width}x${height}, expected 1024x1024`);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(source, target);

// Confirm the copy is byte-identical to the source, so both grader runs
// see exactly the image this repository holds.
const copied = readFileSync(target);
if (!copied.equals(bytes)) {
  throw new Error("copied entry.png differs from the repository image");
}
const written = statSync(target).size;
console.log(`Wrote ${target} (${written} bytes, ${width}x${height}, verified)`);
