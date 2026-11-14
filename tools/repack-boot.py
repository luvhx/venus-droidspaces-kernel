#!/usr/bin/env python3
"""把任意 kernel Image 装回官方 LineageOS boot.img（header v3），并重新生成 AVB footer。

用法:
    python repack-boot.py --boot lineage-boot.img --image Image --out boot-custom.img \
                          --avbtool tools/avbtool.py

注意: boot.img 的 ramdisk 必须来自同一版本的 LineageOS 官方镜像（20261104）。
"""
import argparse
import os
import struct
import subprocess
import sys

PAGE = 4096
HEADER_SIZE = 1580  # boot image header v3 固定 1580 字节，占用第一页


def read_header(d):
    magic = d[:8]
    if magic != b'ANDROID!':
        sys.exit('not an Android boot image: %r' % magic)
    kernel_size, ramdisk_size, os_version, header_size = struct.unpack_from('<IIII', d, 8)
    header_version, cmdline_size = struct.unpack_from('<II', d, 40)
    if header_version != 3:
        sys.exit('only header v3 supported, got %d' % header_version)
    return dict(kernel_size=kernel_size, ramdisk_size=ramdisk_size, os_version=os_version,
                header_size=header_size, header_version=header_version, cmdline_size=cmdline_size)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--boot', required=True, help='官方 boot.img（提供 header + ramdisk）')
    ap.add_argument('--image', required=True, help='新内核 Image')
    ap.add_argument('--out', required=True)
    ap.add_argument('--avbtool', default=os.path.join(os.path.dirname(__file__), 'avbtool.py'))
    ap.add_argument('--partition-size', type=int, default=201326592)
    ap.add_argument('--salt', default='6c6f76652d76656e75732d64726f69647370616365732d'[:32])
    args = ap.parse_args()

    d = open(args.boot, 'rb').read()
    h = read_header(d)
    ramdisk = d[PAGE + h['kernel_size']:PAGE + h['kernel_size'] + h['ramdisk_size']]
    image = open(args.image, 'rb').read()

    # header v3: magic + kernel_size + ramdisk_size + os_version + header_size + reserved[4] + header_version + cmdline_size
    hdr = bytearray(PAGE)
    hdr[:8] = b'ANDROID!'
    struct.pack_into('<IIII', hdr, 8, len(image), len(ramdisk), h['os_version'], HEADER_SIZE)
    struct.pack_into('<I', hdr, 40, 3)
    struct.pack_into('<I', hdr, 44, 0)

    body = bytes(hdr) + image
    body += b'\x00' * ((PAGE - len(body) % PAGE) % PAGE)
    body += ramdisk
    body += b'\x00' * ((PAGE - len(body) % PAGE) % PAGE)

    tmp = args.out + '.tmp'
    with open(tmp, 'wb') as f:
        f.write(body)
    print('kernel=%d ramdisk=%d content=%d' % (len(image), len(ramdisk), len(body)))

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
