"""解析 vendor_boot.img 的 vendor ramdisk，导出其中的 .ko 并分析符号兼容性。"""
import struct, sys, os, gzip, io, re

VB = r'D:\venus_kernel\images\lineage-vendor_boot.img'
OUT = r'D:\venus_kernel\work\vndramdisk'
PAGE = 4096

d = open(VB, 'rb').read()
ver, page = struct.unpack_from('<II', d, 8)
ramdisk_size = struct.unpack_from('<I', d, 24)[0]
print('vendor_ramdisk_size', ramdisk_size)
rd = d[PAGE:PAGE + ramdisk_size]
print('first bytes', rd[:8].hex())

# 判断压缩格式
if rd[:2] == b'\x1f\x8b':
    raw = gzip.decompress(rd)
    print('gzip, uncompressed', len(raw))
elif rd[:4] == b'\x04\x22\x4d\x18':
    sys.exit('lz4 compressed - needs lz4 module')
else:
    raw = rd
    print('not gzip, treat as raw cpio', len(raw))

os.makedirs(OUT, exist_ok=True)
open(os.path.join(OUT, 'vendor_ramdisk.cpio'), 'wb').write(raw)


def cpio_entries(data):
    off = 0
    n = len(data)
    while off + 110 <= n:
        hdr = data[off:off+110]
        if hdr[:6] not in (b'070701', b'070702'):
            nxt = data.find(b'070701', off + 1, off + 4096)
            if nxt < 0:
                break
            off = nxt
            continue
        vals = [int(hdr[i:i+8], 16) for i in range(6, 110, 8)]
        filesize = vals[6]
        namesize = vals[11]
        name = data[off+110:off+110+namesize-1].decode('utf-8', 'replace')
        foff = (off + 110 + namesize + 3) & ~3
        content = data[foff:foff+filesize]
        yield name, content, foff
        if name == 'TRAILER!!!':
            break
        off = (foff + filesize + 3) & ~3


mods = []
for name, content, _ in cpio_entries(raw):
    if name.endswith('.ko'):
        mods.append((name, content))
print('modules found:', len(mods))
for name, content in mods[:15]:
    print('  ', name, len(content))

os.makedirs(os.path.join(OUT, 'modules'), exist_ok=True)
for name, content in mods:
    fn = os.path.join(OUT, 'modules', os.path.basename(name))
    open(fn, 'wb').write(content)
print('extracted to', os.path.join(OUT, 'modules'))
