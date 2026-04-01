#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN_DIR="${HOME}/.local/bin"
APP_DIR="${HOME}/.local/share/applications"

mkdir -p "${BIN_DIR}" "${APP_DIR}"

install -m 0755 "${ROOT_DIR}/scripts/monster-cycle-tcc-profile" "${BIN_DIR}/monster-cycle-tcc-profile"
install -m 0755 "${ROOT_DIR}/scripts/monster-tcc-profile-manager" "${BIN_DIR}/monster-tcc-profile-manager"
install -m 0755 "${ROOT_DIR}/scripts/monster_tcc_common.py" "${BIN_DIR}/monster_tcc_common.py"
install -m 0644 "${ROOT_DIR}/desktop/monster-tcc-profile-manager.desktop" "${APP_DIR}/monster-tcc-profile-manager.desktop"

if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database "${APP_DIR}" >/dev/null 2>&1 || true
fi

echo "Installed scripts to ${BIN_DIR}"
echo "Installed desktop file to ${APP_DIR}"
echo
echo "Open 'Monster TCC Profile Manager' from the app grid or run:"
echo "  ${BIN_DIR}/monster-tcc-profile-manager"
