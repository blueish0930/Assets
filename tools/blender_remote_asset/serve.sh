#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
ENV_FILE="${REMOTE_ASSET_ENV:-$SCRIPT_DIR/.env}"

USER_BLENDER_BIN_SET="${BLENDER_BIN+x}"
USER_BLENDER_BIN="${BLENDER_BIN-}"
USER_BLENDER_PYTHON_SET="${BLENDER_PYTHON+x}"
USER_BLENDER_PYTHON="${BLENDER_PYTHON-}"
USER_BUILD_ROOT_SET="${BUILD_ROOT+x}"
USER_BUILD_ROOT="${BUILD_ROOT-}"
USER_HTTP_BIND_SET="${HTTP_BIND+x}"
USER_HTTP_BIND="${HTTP_BIND-}"
USER_HTTP_PORT_SET="${HTTP_PORT+x}"
USER_HTTP_PORT="${HTTP_PORT-}"

if [[ -f "$ENV_FILE" ]]; then
  set -a
  # shellcheck disable=SC1090
  source "$ENV_FILE"
  set +a
fi

if [[ -n "$USER_BLENDER_BIN_SET" ]]; then BLENDER_BIN="$USER_BLENDER_BIN"; fi
if [[ -n "$USER_BLENDER_PYTHON_SET" ]]; then BLENDER_PYTHON="$USER_BLENDER_PYTHON"; fi
if [[ -n "$USER_BUILD_ROOT_SET" ]]; then BUILD_ROOT="$USER_BUILD_ROOT"; fi
if [[ -n "$USER_HTTP_BIND_SET" ]]; then HTTP_BIND="$USER_HTTP_BIND"; fi
if [[ -n "$USER_HTTP_PORT_SET" ]]; then HTTP_PORT="$USER_HTTP_PORT"; fi

BUILD_ROOT="${BUILD_ROOT:-blender/assets}"
HTTP_BIND="${HTTP_BIND:-127.0.0.1}"
HTTP_PORT="${HTTP_PORT:-8000}"
BLENDER_BIN="${BLENDER_BIN:-blender}"

if [[ -n "${BLENDER_PYTHON:-}" ]]; then
  PYTHON_BIN="$BLENDER_PYTHON"
else
  PYTHON_BIN="$("$BLENDER_BIN" -b --factory-startup --python-expr 'import sys; print("BLENDER_PYTHON_EXECUTABLE=" + sys.executable)' | sed -n 's/^BLENDER_PYTHON_EXECUTABLE=//p' | tail -n 1)"
fi

cd "$REPO_ROOT"

if [[ -z "$PYTHON_BIN" || ! -x "$PYTHON_BIN" ]]; then
  echo "Could not resolve Blender Python from: $BLENDER_BIN" >&2
  exit 1
fi

if [[ ! -f "$BUILD_ROOT/_asset-library-meta.json" ]]; then
  echo "Remote asset library metadata is missing: $BUILD_ROOT/_asset-library-meta.json" >&2
  echo "Run tools/blender_remote_asset/build.sh first." >&2
  exit 1
fi

echo "Serving $BUILD_ROOT"
echo "Using Python: $PYTHON_BIN"
echo "Blender remote asset library URL: http://$HTTP_BIND:$HTTP_PORT/"
exec "$PYTHON_BIN" -m http.server "$HTTP_PORT" --bind "$HTTP_BIND" --directory "$BUILD_ROOT"
