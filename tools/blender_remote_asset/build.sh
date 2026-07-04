#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
ENV_FILE="${REMOTE_ASSET_ENV:-$SCRIPT_DIR/.env}"

USER_BLENDER_BIN_SET="${BLENDER_BIN+x}"
USER_BLENDER_BIN="${BLENDER_BIN-}"
USER_ASSET_ROOT_SET="${ASSET_ROOT+x}"
USER_ASSET_ROOT="${ASSET_ROOT-}"
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
if [[ -n "$USER_ASSET_ROOT_SET" ]]; then ASSET_ROOT="$USER_ASSET_ROOT"; fi
if [[ -n "$USER_BUILD_ROOT_SET" ]]; then BUILD_ROOT="$USER_BUILD_ROOT"; fi
if [[ -n "$USER_HTTP_BIND_SET" ]]; then HTTP_BIND="$USER_HTTP_BIND"; fi
if [[ -n "$USER_HTTP_PORT_SET" ]]; then HTTP_PORT="$USER_HTTP_PORT"; fi

BLENDER_BIN="${BLENDER_BIN:-blender}"
ASSET_ROOT="${ASSET_ROOT:-blender/assets}"
BUILD_ROOT="${BUILD_ROOT:-blender/assets}"

cd "$REPO_ROOT"

clean_generated_files() {
  local root="$1"

  rm -f "$root/_asset-library-meta.json"
  rm -rf "$root/_v1"
  find "$root" -type d -name '*_thumbnails' -prune -exec rm -rf {} +
}

if [[ ! -d "$ASSET_ROOT" ]]; then
  echo "Asset root does not exist: $ASSET_ROOT" >&2
  exit 1
fi

if [[ "$BUILD_ROOT" == "" || "$BUILD_ROOT" == "/" || "$BUILD_ROOT" == "." ]]; then
  echo "Refusing unsafe BUILD_ROOT: $BUILD_ROOT" >&2
  exit 1
fi

if [[ "$BUILD_ROOT" == "$ASSET_ROOT" ]]; then
  TARGET_ROOT="$ASSET_ROOT"
  echo "Generating remote asset library in place: $TARGET_ROOT"
  clean_generated_files "$TARGET_ROOT"
else
  TARGET_ROOT="$BUILD_ROOT"
  echo "Preparing build root: $TARGET_ROOT"
  rm -rf "$TARGET_ROOT"
  mkdir -p "$TARGET_ROOT"
  rsync -a --delete \
    --exclude '_asset-library-meta.json' \
    --exclude '_v1/' \
    --exclude '*_thumbnails/' \
    "$ASSET_ROOT/" "$TARGET_ROOT/"
  clean_generated_files "$TARGET_ROOT"
fi

echo "Using Blender: $BLENDER_BIN"
"$BLENDER_BIN" --version | sed -n '1,8p'

"$BLENDER_BIN" -b --factory-startup -c asset_listing generate "$TARGET_ROOT"

"$BLENDER_BIN" -b --factory-startup --python "$SCRIPT_DIR/validate.py" -- "$TARGET_ROOT" --source "$ASSET_ROOT"

echo
echo "Build complete: $TARGET_ROOT"
echo "Local URL after serve.sh: http://${HTTP_BIND:-127.0.0.1}:${HTTP_PORT:-8000}/"
