# NOTE: 这套脚本用 Debian clang 构建，产出的内核无法在 venus 上启动（缺 CFI，厂商模块加载失败）。
# 可用的构建方式见 .github/workflows/build-kernel.yml（AOSP clang + 原厂配置）。
#!/bin/bash
set -o pipefail
source "$(dirname "$0")/env21.sh"
cd $W/src/sm8350-kernel
make O=$W/out ARCH=arm64 -j8 \
  HOSTCC="$HOSTCC" HOSTLD="$HOSTLD" HOSTAR="$HOSTAR" \
  CC="$CC" LD="$LD" AR="$AR" NM="$NM" OBJCOPY="$OBJCOPY" OBJDUMP="$OBJDUMP" STRIP="$STRIP" \
  Image
