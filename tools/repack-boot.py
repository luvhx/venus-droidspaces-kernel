#!/usr/bin/env python3
"""把任意 kernel Image 装回官方 LineageOS boot.img（header v3），并重新生成 AVB footer。

关键点：venus 的官方 boot.img 里，ramdisk 并不紧跟在（4K 对齐后的）kernel 后面，
而是再多留 3584 字节（0xE00）——本脚本会从官方镜像里把这个偏移自动测出来并复用，
否则产出的镜像虽然 header 合法，设备上却起不来。

用法:
    python repack-boot.py --boot lineage-boot.img --image Image --out boot-custom.img
"""
import argparse
import os
import struct
import subprocess
import sys

PAGE = 4096
HEADER_SIZE = 1580


def align(n, a=PAGE):
    return (n + a - 1) // a * a


def read_header(d):
    if d[:8] != b'ANDROID!':
        sys.exit('not an Android boot image: %r' % d[:8])
    kernel_size, ramdisk_size, os_version, header_size = struct.unpack_from('<IIII', d, 8)
    header_version, cmdline_size = struct.unpack_from('<II', d, 40)
    if header_version != 3:
        sys.exit('only header v3 supported, got %d' % header_version)
    return dn(kernel_size=kernel_size, ramdisk_size=ramdisk_size, os_version=os_version,
              header_size=header_size, header_version=header_version, cmdline_size=cmdline_size)


def dn(**kw):
    return kw


def find_ramdisk(d, kernel_size, ramdisk_size):
    """在核心里找 gzip 头，返回官方 ramdisk 起始偏移。"""
    start = PAGE + kernel_size
    i = d.find(b'\x1f\x8b\x08', start, start + 65536)
    if i < 0:
        i = start
    return i


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--boot', required=True, help='官方 boot.img（模板）')
    ap.add_argument('--image', required=True, help='新内核 Image')
    ap.add_argument('--out', required=True)
    ap.add_argument('--avbtool', default=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'avbtool.py'))
    ap.add_argument('--partition-size', type=int, default=201326592)
    ap.add_argument('--salt', default='9f2c1d7a6b3e40519c8d7f2a4e6b8c0d')
    ap.add_argument('--keep-avb', action='store_true',
                    help='不重算 AVB，直接沿用官方镜像尾部的 footer/vbmeta 字节（Magisk 式做法）')
    args = ap.parse_args()

    d = open(args.boot, 'rb').read()
    h = read_header(d)
    official_ramdisk_off = find_ramdisk(d, h['kernel_size'], h['ramdisk_size'])
    pad = official_ramdisk_off - align(PAGE + h['kernel_size'])
    ramdisk = d[official_ramdisk_off:official_ramdisk_off + h['ramdisk_size']]
    print('official kernel=%d ramdisk_off=%d extra_pad=%d' % (h['kernel_size'], official_ramdisk_off, pad))

    image = open(args.image, 'rb').read()
    new_ramdisk_off = align(PAGE + len(image)) + pad

    hdr = bytearray(PAGE)
    hdr[:8] = b'ANDROID!'
    struct.pack_into('<IIII', hdr, 8, len(image), len(ramdisk), h['os_version'], HEADER_SIZE)
    struct.pack_into('<I', hdr, 40, 3)
    struct.pack_into('<I', hdr, 44, 0)

    body = bytearray(max(new_ramdisk_off, PAGE + len(image)) + len(ramdisk))
    body[:PAGE] = hdr
    body[PAGE:PAGE + len(image)] = image
    body[new_ramdisk_off:new_ramdisk_off + len(ramdisk)] = ramdisk
    content = bytes(body)
    content += b'\x00' * (align(len(content)) - len(content))

    tmp = args.out + '.tmp'
    with open(tmp, 'wb') as f:
        f.write(content)
    print('new kernel=%d ramdisk_off=%d content=%d' % (len(image), new_ramdisk_off, len(content)))

    if args.keep_avb:
        # 沿用官方尾部（vbmeta + footer），只改前面的内容；hash 已不匹配，需解锁且关闭校验
        tail = d[len(content):]
        with open(tmp, 'ab') as f:
            f.write(tail)
        os.replace(tmp, args.out)
        print('written %s (kept official AVB tail, %d bytes)' % (args.out, os.path.getsize(args.out)))
        return

    subprocess.check_call([
        sys.executable, args.avbtool, 'add_hash_footer',
        '--image', tmp,
        '--partition_size', str(args.partition_size),
        '--partition_name', 'boot',
        '--hash_algorithm', 'sha256',
        '--salt', args.salt,
        '--rollback_index', '0',
    ])
    os.replace(tmp, args.out)
    print('written %s (%d bytes)' % (args.out, os.path.getsize(args.out)))


if __name__ == '__main__':
    main()
