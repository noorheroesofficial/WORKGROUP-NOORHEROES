#!/usr/bin/env node

/**
 * NoorHeroes Archify Batch Visual-Check Runner
 * ============================================
 * Collects automated browser evidence (readability, containment across viewports,
 * dock/stage clearance, light/dark screenshots) for all generated HTML artifacts.
 */

import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const workgroupRoot = path.resolve(__dirname, '..');
const archifyBin = path.join(workgroupRoot, 'bin', 'archify.mjs');
const visualizationsDir = path.join(workgroupRoot, 'Architecture_Visualizations');
const generatedDir = path.join(visualizationsDir, 'generated');
const examplesDir = path.join(visualizationsDir, 'examples');

function discoverHtmlFiles(dir) {
  if (!fs.existsSync(dir)) return [];
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  const files = [];

  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      files.push(...discoverHtmlFiles(fullPath));
    } else if (
      entry.isFile() &&
      entry.name.endsWith('.html') &&
      !entry.name.endsWith('.visual-check.html')
    ) {
      files.push(fullPath);
    }
  }

  return files;
}

async function main() {
  const includeExamples = process.argv.includes('--include-examples') || process.argv.includes('--all');
  console.log('NoorHeroes Archify: Running visual check on delivered HTML artifacts...\n');

  const htmlFiles = [
    ...discoverHtmlFiles(generatedDir),
    ...(includeExamples ? discoverHtmlFiles(examplesDir) : []),
  ];

  if (htmlFiles.length === 0) {
    console.log('No HTML artifacts found to inspect. Run "npm run archify:build" first.');
    process.exit(0);
  }

  let totalPassed = 0;
  let totalSkipped = 0;
  let totalFailed = 0;

  for (const filePath of htmlFiles) {
    const relPath = path.relative(workgroupRoot, filePath);

    const result = spawnSync(process.execPath, [
      archifyBin,
      'visual-check',
      filePath,
      '--json',
    ], {
      cwd: workgroupRoot,
      encoding: 'utf8',
    });

    if (result.status === 0) {
      console.log(`[PASS] ${relPath} (containment, readability, captures verified)`);
      totalPassed += 1;
    } else if (result.status === 2) {
      console.warn(`[SKIPPED] ${relPath} (Chrome/Edge not available in environment)`);
      totalSkipped += 1;
    } else {
      console.error(`[FAIL] ${relPath}`);
      if (result.stdout) {
        try {
          const parsed = JSON.parse(result.stdout);
          if (parsed.error) console.error(`       -> ${parsed.error}`);
        } catch {
          console.error(result.stdout.trim());
        }
      }
      if (result.stderr) {
        console.error(result.stderr.trim());
      }
      totalFailed += 1;
    }
  }

  console.log(`\nVisual-check complete: ${totalPassed} passed, ${totalSkipped} skipped, ${totalFailed} failed.`);

  if (totalFailed > 0) {
    process.exit(1);
  }
}

main().catch((err) => {
  console.error(`Fatal error: ${err.message}`);
  process.exit(1);
});
