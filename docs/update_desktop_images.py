# -*- coding: utf-8 -*-
"""
扫描 docs/Desktop 下的图片，按"拍摄日期(文件名)或文件修改时间"取最新的一张，
更新 index.html 里 EMBEDDED_STATE.desktopImages（按最新在前排序），
使新建节点默认图片路径 = Desktop/最新图片。

用法: python update_desktop_images.py
"""
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = HERE if os.path.isfile(os.path.join(HERE, 'index.html')) else os.path.join(HERE, 'docs')
DESK = os.path.join(DOCS, 'Desktop')
HTML = os.path.join(DOCS, 'index.html')

EXTS = ('.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp')

def file_sort_key(full, fn):
    # 只看文件实际修改时间，不解析文件名里的日期
    return os.path.getmtime(full)

def main():
    if not os.path.isdir(DESK):
        print('Desktop 目录不存在:', DESK)
        return
    items = []
    for fn in os.listdir(DESK):
        if fn.lower().endswith(EXTS):
            full = os.path.join(DESK, fn)
            items.append((file_sort_key(full, fn), fn))
    items.sort(reverse=True)
    rel = [fn for _, fn in items]
    if not rel:
        print('Desktop 下没有找到图片')
        return
    s = open(HTML, encoding='utf-8').read()
    new_arr = '"desktopImages":[' + ','.join('"%s"' % x.replace('\\', '/') for x in rel) + ']'
    if '"desktopImages":' not in s:
        print('HTML 中未找到 desktopImages 字段')
        return
    s2 = re.sub(r'"desktopImages":\[.*?\]', new_arr, s, count=1)
    open(HTML, 'w', encoding='utf-8').write(s2)
    print('已更新 %d 张图片，按最新在前排序。' % len(rel))
    print('新建节点默认图片路径 =', rel[0])

if __name__ == '__main__':
    main()
