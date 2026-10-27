#!/usr/bin/env node

/**
 * NoorHeroes Archify Batch Delivery Runner
 * ========================================
 * Compiles and delivers standalone interactive HTML diagrams from source JSON
 * specifications into Architecture_Visualizations/generated/<type>/ and examples/.
 */

import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const workgroupRoot = path.resolve(__dirname, '..');
const archifyBin = path.join(workgroupRoot, 'bin', 'archify.mjs');
const visualizationsDir = path.join(workgroupRoot, 'Architecture_Visualizations');
const sourceDir = path.join(visualizationsDir, 'source');
const generatedDir = path.join(visualizationsDir, 'generated');
const examplesDir = path.join(visualizationsDir, 'examples');

const TYPES = new Set(['architecture', 'workflow', 'sequence', 'dataflow', 'lifecycle']);

function discoverJsonFiles(dir) {
  if (!fs.existsSync(dir)) return [];
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  const files = [];

  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      files.push(...discoverJsonFiles(fullPath));
    } else if (entry.isFile() && entry.name.endsWith('.json') && !entry.name.endsWith('.visual-check.json')) {
      files.push(fullPath);
    }
  }

  return files;
}

function resolveDiagramType(filePath) {
  try {
    const content = JSON.parse(fs.readFileSync(filePath, 'utf8'));
    if (content.diagram_type && TYPES.has(content.diagram_type)) {
      return content.diagram_type;
    }
  } catch {
    // Fall back to filename/directory inference
  }

  const filename = path.basename(filePath);
  for (const type of TYPES) {
    if (filename.includes(`.${type}.`)) return type;
  }

  const parentDir = path.basename(path.dirname(filePath));
  if (TYPES.has(parentDir)) return parentDir;

  return null;
}

function determineOutputPath(sourcePath, diagramType) {
  const filename = path.basename(sourcePath, '.json');
  const isExample = sourcePath.includes(path.sep + 'examples' + path.sep);

  if (isExample) {
    return path.join(examplesDir, `${filename}.html`);
  }

  const targetSubdir = path.join(generatedDir, diagramType);
  fs.mkdirSync(targetSubdir, { recursive: true });
  return path.join(targetSubdir, `${filename}.html`);
}

async function main() {
  console.log('NoorHeroes Archify: Building all architecture visualization artifacts...\n');

  const jsonFiles = [
    ...discoverJsonFiles(sourceDir),
    ...discoverJsonFiles(examplesDir),
  ];

  if (jsonFiles.length === 0) {
    console.log('No JSON specifications found to build.');
    process.exit(0);
  }

  let totalBuilt = 0;
  let totalFailed = 0;

  for (const filePath of jsonFiles) {
    const relSource = path.relative(workgroupRoot, filePath);
    const diagramType = resolveDiagramType(filePath);

    if (!diagramType) {
      console.warn(`[SKIP] Could not determine diagram type for: ${relSource}`);
      continue;
    }

    const outputPath = determineOutputPath(filePath, diagramType);
    const relOutput = path.relative(workgroupRoot, outputPath);

    const result = spawnSync(process.execPath, [
      archifyBin,
      'deliver',
      diagramType,
      filePath,
      outputPath,
      '--quality',
      'showcase',
      '--json',
    ], {
      cwd: workgroupRoot,
      encoding: 'utf8',
    });

    if (result.status === 0) {
      console.log(`[DELIVERED] (${diagramType}) ${relSource} -> ${relOutput}`);
      totalBuilt += 1;
    } else {
      console.error(`[FAIL] (${diagramType}) ${relSource}`);
      if (result.stdout) {
        try {
          const parsed = JSON.parse(result.stdout);
          const errors = parsed.composition?.issues || parsed.diagnostics || [];
          for (const err of errors) {
            console.error(`       -> [${err.code || 'error'}] ${err.message}`);
          }
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

  console.log(`\nBuild complete: ${totalBuilt} delivered, ${totalFailed} failed.`);

  if (totalFailed > 0) {
    process.exit(1);
  }
}

main().catch((err) => {
  console.error(`Fatal error: ${err.message}`);
  process.exit(1);
});
