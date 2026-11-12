#!/bin/bash
set -o pipefail
source "$(dirname "$0")/env21.sh"
cd $W/src/sm8350-kernel
make O=$W/out ARCH=arm64 -j8 \
  HOSTCC="$HOSTCC" HOSTLD="$HOSTLD" HOSTAR="$HOSTAR" \
  CC="$CC" LD="$LD" AR="$AR" NM="$NM" OBJCOPY="$OBJCOPY" OBJDUMP="$OBJDUMP" STRIP="$STRIP" \
  Image
