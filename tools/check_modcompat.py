"""检查 vendor 模块的 vermagic / 依赖符号是否被我们编译的内核满足。"""
import struct, sys, os, glob, re

def read_elf(path):
    d = open(path, 'rb').read()
    assert d[:4] == b'\x7fELF', path
    assert d[4] == 2, 'not ELF64'
    e_shoff = struct.unpack_from('<Q', d, 0x28)[0]
    e_shentsize = struct.unpack_from('<H', d, 0x3A)[0]
    e_shnum = struct.unpack_from('<H', d, 0x3C)[0]
    e_shstrndx = struct.unpack_from('<H', d, 0x3E)[0]
    secs = []
    for i in range(e_shnum):
        off = e_shoff + i * e_shentsize
        name, typ, flags, addr, offset, size, link, info, align, entsize = struct.unpack_from('<IIQQQQIIQQ', d, off)
        secs.append(dict(name_off=name, type=typ, offset=offset, size=size, link=link, info=info, entsize=entsize))
    shstr = secs[e_shstrndx]
    shstrtab = d[shstr['offset']:shstr['offset']+shstr['size']]
    for s in secs:
        s['name'] = shstrtab[s['name_off']:shstrtab.find(b'\x00', s['name_off'])].decode()
    return d, secs


def get_section(d, secs, name):
    for s in secs:
        if s['name'] == name:
            return d[s['offset']:s['offset']+s['size']]
    return None


def symbols(d, secs):
    symtab = None
    strtab = None
    for i, s in enumerate(secs):
        if s['type'] == 2:  # SYMTAB
            symtab = s
            strtab = secs[s['link']]
            break
    if not symtab:
        return []
    out = []
    num = symtab['size'] // 24
    st = d[strtab['offset']:strtab['offset']+strtab['size']]
    for i in range(num):
        off = symtab['offset'] + i * 24
        name, info, other, shndx, value, size = struct.unpack_from('<IBBHQQ', d, off)
        nm = st[name:st.find(b'\x00', name)].decode('utf-8', 'replace')
        out.append(dict(name=nm, info=info, shndx=shndx, bind=info >> 4, typ=info & 0xf))
    return out


def modinfo(d, secs):
    blob = get_section(d, secs, '.modinfo')
    info = {}
    if not blob:
        return info
    for item in blob.split(b'\x00'):
        if b'=' in item:
            k, v = item.split(b'=', 1)
            info[k.decode()] = v.decode('utf-8', 'replace')
    return info


def main(moddir, sysmap):
    exported = set()
    for line in open(sysmap, encoding='utf-8', errors='replace'):
        parts = line.split()
        if len(parts) >= 3:
            exported.add(parts[2])
    print('System.map symbols:', len(exported))

    mods = sorted(glob.glob(os.path.join(moddir, '*.ko')))
    all_mod_syms = {}
    parsed = []
    for m in mods:
        d, secs = read_elf(m)
        syms = symbols(d, secs)
        defs = {s['name'] for s in syms if s['shndx'] != 0 and s['name']}
        all_mod_syms[os.path.basename(m)] = defs
        parsed.append((m, d, secs, syms, modinfo(d, secs)))

    missing_total = {}
    for m, d, secs, syms, mi in parsed:
        base = os.path.basename(m)
        undef = [s['name'] for s in syms if s['shndx'] == 0 and s['name'] and (s['bind'] != 2 or True)]
        other_defs = set()
        for k, v in all_mod_syms.items():
            if k != base:
                other_defs |= v
        missing = [u for u in undef if u not in exported and u not in other_defs]
        if missing:
            missing_total[base] = missing
        print('\n== %s ==' % base)
        print('  vermagic:', mi.get('vermagic'))
        print('  undef symbols: %d, missing in our kernel: %d' % (len(undef), len(missing)))
        if missing:
            print('  MISSING:', ', '.join(sorted(missing)[:20]))
    return missing_total


if __name__ == '__main__':
    main(r'D:\venus_kernel\work\vndramdisk\modules',
         r'D:\venus_kernel\ci\venus-kernel-line\k\System.map')
