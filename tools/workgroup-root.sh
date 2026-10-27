#!/usr/bin/env bash
# NoorHeroes Cross-Platform Workgroup Root Resolver (POSIX Bash for Linux & macOS)
# Dynamically discovers WORKGROUP root directory without hardcoding any user or machine paths.

set -euo pipefail

# 1. Check environment variable override
if [[ -n "${WORKGROUP_ROOT:-}" ]] && [[ -f "${WORKGROUP_ROOT}/.workgroup-root" ]]; then
    cd "${WORKGROUP_ROOT}" && pwd -P
    exit 0
fi

# 2. Ascend from script location
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd -P)"
DIR="${SCRIPT_DIR}"

while [[ "${DIR}" != "/" && -n "${DIR}" ]]; do
    if [[ -f "${DIR}/.workgroup-root" ]] || { [[ -f "${DIR}/PROJECT-CONTEXT.md" ]] && [[ -f "${DIR}/DEVELOPMENT-RULES.md" ]]; }; then
        echo "${DIR}"
        exit 0
    fi
    DIR="$(dirname "${DIR}")"
done

# 3. Fallback: ascend from current working directory
DIR="$(pwd -P)"
while [[ "${DIR}" != "/" && -n "${DIR}" ]]; do
    if [[ -f "${DIR}/.workgroup-root" ]] || { [[ -f "${DIR}/PROJECT-CONTEXT.md" ]] && [[ -f "${DIR}/DEVELOPMENT-RULES.md" ]]; }; then
        echo "${DIR}"
        exit 0
    fi
    DIR="$(dirname "${DIR}")"
done

echo "Error: Could not locate WORKGROUP root (.workgroup-root missing)" >&2
exit 1
