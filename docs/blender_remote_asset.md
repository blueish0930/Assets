# Blender 远程资产库本地构建

源资产目录是 `blender/assets`。远程资产库索引在本地生成。

## 配置

复制 env 示例 ，并把 `BLENDER_BIN` 改成本机 Blender 5.2+ 可执行文件：

```bash
cp tools/blender_remote_asset/.env.example tools/blender_remote_asset/.env
```

通用配置：

```bash
BLENDER_BIN="/path/to/blender"
ASSET_ROOT="blender/assets"
BUILD_ROOT="blender/assets"
```

常见路径示例：

```bash
# macOS app bundle
BLENDER_BIN="/Applications/Blender.app/Contents/MacOS/Blender"

# Linux 解压版
BLENDER_BIN="/opt/blender/blender"

# Windows, Git Bash
BLENDER_BIN="C:/Program Files/Blender Foundation/Blender 5.2/blender.exe"
```

`serve.sh` 会通过 `BLENDER_BIN` 自动读取 Blender 自带 Python，不需要单独配置 Python 路径
脚本使用 bash，可在 macOS、Linux、Windows Git Bash中运行；不要用 `sh tools/...` 执行

## 构建

```bash
bash tools/blender_remote_asset/build.sh
```

默认在 `blender/assets` 原位生成：

```bash
blender -b --factory-startup -c asset_listing generate blender/assets
```

这些生成物已被 Git 忽略：

```text
blender/assets/_asset-library-meta.json
blender/assets/_v1/
blender/assets/**/*_thumbnails/
```

如需隔离构建：

```bash
BUILD_ROOT=.build/blender_remote_asset bash tools/blender_remote_asset/build.sh
```

## 本地服务

```bash
bash tools/blender_remote_asset/serve.sh
```

Blender 远程资产库 URL：

```text
http://127.0.0.1:8000/
```

URL 必须指向包含 `_asset-library-meta.json` 的目录。
