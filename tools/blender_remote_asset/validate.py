#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path


def parse_args() -> argparse.Namespace:
    args = sys.argv[1:]
    if "--" in args:
        args = args[args.index("--") + 1 :]

    parser = argparse.ArgumentParser(
        description="Validate generated Blender remote asset library files."
    )
    parser.add_argument("build_root", help="Generated remote asset library root")
    parser.add_argument("--source", help="Optional source asset root to compare against")
    return parser.parse_args(args)


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def rel_files(root: Path) -> set[str]:
    return {
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if path.is_file()
    }


def generated_pattern_files(root: Path) -> set[str]:
    files: set[str] = set()
    for path in [
        root / "_asset-library-meta.json",
        root / "_v1" / "asset-index.json",
    ]:
        if path.is_file():
            files.add(path.relative_to(root).as_posix())

    version_dir = root / "_v1"
    if version_dir.is_dir():
        files.update(
            path.relative_to(root).as_posix()
            for path in version_dir.rglob("*")
            if path.is_file()
        )

    for thumbnail_dir in root.rglob("*_thumbnails"):
        if not thumbnail_dir.is_dir():
            continue
        files.update(
            path.relative_to(root).as_posix()
            for path in thumbnail_dir.rglob("*")
            if path.is_file()
        )
    return files


def file_kind(path: str) -> str:
    name = Path(path).name
    if name.startswith(".") and name.count(".") == 1:
        return name
    return Path(path).suffix.lower() or "[noext]"


def main() -> int:
    ns = parse_args()
    build_root = Path(ns.build_root).resolve()
    source_root = Path(ns.source).resolve() if ns.source else None

    meta_path = build_root / "_asset-library-meta.json"
    index_path = build_root / "_v1" / "asset-index.json"
    page_paths = sorted((build_root / "_v1").glob("assets-*.json"))

    missing = [path for path in [meta_path, index_path] if not path.is_file()]
    if not page_paths:
        missing.append(build_root / "_v1" / "assets-*.json")

    if missing:
        for path in missing:
            print(f"Missing generated file: {path}", file=sys.stderr)
        return 1

    meta = load_json(meta_path)
    index = load_json(index_path)
    pages = [load_json(path) for path in page_paths]

    generated_files: set[str] = set()
    if source_root and source_root.is_dir() and source_root != build_root:
        source_files = rel_files(source_root) - generated_pattern_files(source_root)
        generated_files = rel_files(build_root) - source_files
    else:
        generated_files = generated_pattern_files(build_root)

    generated_exts = Counter(file_kind(path) for path in generated_files)
    generated_dirs = Counter(path.split("/", 1)[0] for path in generated_files)
    webp_count = sum(1 for path in build_root.rglob("*.webp") if path.is_file())

    print("Remote asset library validation")
    print(f"- build_root: {build_root}")
    print(f"- meta: {meta_path.relative_to(build_root)}")
    print(f"- index: {index_path.relative_to(build_root)}")
    print(f"- pages: {len(page_paths)}")
    print(f"- webp thumbnails: {webp_count}")

    if isinstance(index, dict):
        for key in ["asset_count", "file_count", "catalog_count", "page_count"]:
            if key in index:
                print(f"- {key}: {index[key]}")

    if generated_files:
        print("- generated-only files by extension:")
        for ext, count in sorted(generated_exts.items()):
            print(f"  {ext}: {count}")

        print("- generated-only top-level paths:")
        for dirname, count in sorted(generated_dirs.items()):
            print(f"  {dirname}: {count}")

    # Keep parsed objects alive until after validation so malformed JSON fails above.
    _ = (meta, index, pages)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
