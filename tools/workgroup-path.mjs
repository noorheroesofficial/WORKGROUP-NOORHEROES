/**
 * NoorHeroes Cross-Platform Workgroup Root & Path Resolution Utility (Node.js ESM)
 * ==============================================================================
 * Provides dynamic, zero-hardcoding discovery of the WORKGROUP-NOORHEROES
 * repository root across Windows, Linux, and macOS.
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT_MARKER = '.workgroup-root';
const FALLBACK_MARKERS = ['PROJECT-CONTEXT.md', 'DEVELOPMENT-RULES.md'];
let cachedRoot = null;

/**
 * Dynamically discovers the absolute path of the WORKGROUP-NOORHEROES root.
 * @param {string} [startPath] Optional starting path for directory traversal.
 * @returns {string} Absolute normalized path to the workgroup root.
 */
export function getWorkgroupRoot(startPath) {
  // 1. Check environment variable override
  if (process.env.WORKGROUP_ROOT) {
    const envRoot = path.resolve(process.env.WORKGROUP_ROOT);
    if (fs.existsSync(path.join(envRoot, ROOT_MARKER))) {
      cachedRoot = envRoot;
      return envRoot;
    }
  }

  if (cachedRoot && !startPath) {
    return cachedRoot;
  }

  // 2. Ascend from startPath or current file location
  let current;
  if (startPath) {
    current = path.resolve(startPath);
  } else {
    const __filename = fileURLToPath(import.meta.url);
    current = path.dirname(path.resolve(__filename));
  }

  while (current) {
    if (fs.existsSync(path.join(current, ROOT_MARKER))) {
      cachedRoot = current;
      return current;
    }
    const allFallbacksExist = FALLBACK_MARKERS.every((marker) =>
      fs.existsSync(path.join(current, marker))
    );
    if (allFallbacksExist) {
      cachedRoot = current;
      return current;
    }
    const parent = path.dirname(current);
    if (parent === current) break;
    current = parent;
  }

  // 3. Fallback: ascend from process.cwd()
  let cwd = path.resolve(process.cwd());
  while (cwd) {
    if (fs.existsSync(path.join(cwd, ROOT_MARKER))) {
      cachedRoot = cwd;
      return cwd;
    }
    const parent = path.dirname(cwd);
    if (parent === cwd) break;
    cwd = parent;
  }

  throw new Error(
    "Could not determine WORKGROUP root. Ensure '.workgroup-root' exists at workgroup root or set WORKGROUP_ROOT env variable."
  );
}

/**
 * Resolves a path relative to the WORKGROUP root.
 * @param {...string} parts
 * @returns {string} Absolute resolved path.
 */
export function resolveWorkgroupPath(...parts) {
  const root = getWorkgroupRoot();
  return path.resolve(root, ...parts);
}

/**
 * Returns a POSIX-compliant relative path from workgroup root to target.
 * @param {string} targetPath
 * @returns {string} POSIX relative path.
 */
export function getRelativeWorkgroupPath(targetPath) {
  const root = getWorkgroupRoot();
  const rel = path.relative(root, path.resolve(targetPath));
  return rel.split(path.sep).join('/');
}

// Subsystem accessors
export function getBackendDir() {
  return resolveWorkgroupPath('NoorHeroes-Backend');
}

export function getAdminDir() {
  return resolveWorkgroupPath('noorheroes-admin');
}

export function getMobileDir() {
  return resolveWorkgroupPath('NoorHeroes');
}

export function getScreensDir() {
  return resolveWorkgroupPath('Screens');
}

// CLI usage
if (process.argv[1] && path.resolve(process.argv[1]) === path.resolve(fileURLToPath(import.meta.url))) {
  try {
    const root = getWorkgroupRoot();
    if (process.argv.length > 2) {
      console.log(resolveWorkgroupPath(...process.argv.slice(2)));
    } else {
      console.log(root);
    }
  } catch (err) {
    console.error(err.message);
    process.exit(1);
  }
}
