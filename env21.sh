export W="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export L=$W/toolchain21
export LD_LIBRARY_PATH=$L/usr/lib/aarch64-linux-gnu:$L/usr/lib/llvm-21/lib:$L/lib/aarch64-linux-gnu:$W/toolchain/usr/lib/aarch64-linux-gnu:$W/toolchain/usr/lib:$W/toolchain/lib/aarch64-linux-gnu:$W/toolchain/lib
export PATH=$L/usr/bin:$L/usr/lib/llvm-21/bin:$W/toolchain/usr/bin:$PATH
export ARCH=arm64
export CROSS_COMPILE=aarch64-linux-gnu-
export CC="clang-21 --sysroot=$W/toolchain/sysroot -B$W/toolchain/usr/lib/aarch64-linux-gnu -B$W/toolchain/usr/lib/gcc/aarch64-linux-gnu/12 -fuse-ld=lld -Wno-unused-command-line-argument"
export LD=ld.lld-21
export AR=llvm-ar-21
export NM=llvm-nm-21
export OBJCOPY=llvm-objcopy-21
export OBJDUMP=llvm-objdump-21
export STRIP=llvm-strip-21
export HOSTCC="clang-21 --sysroot=$W/toolchain/sysroot -B$W/toolchain/usr/lib/aarch64-linux-gnu -B$W/toolchain/usr/lib/gcc/aarch64-linux-gnu/12 -fuse-ld=lld -Wno-unused-command-line-argument"
export HOSTLD=ld.lld-21
export HOSTAR=llvm-ar-21
export M4=$W/toolchain/usr/bin/m4
export BISON_PKGDATADIR=$W/toolchain/usr/share/bison
export TMPDIR=$W/tmp
