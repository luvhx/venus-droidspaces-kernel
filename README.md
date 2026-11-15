# 灏忕背 11锛坴enus锛塂roidSpaces 鍐呮牳

閫傜敤浜?**灏忕背 11 / Mi 11锛坴enus锛孲M8350锛孧2011K2C / M2011K2G锛?*銆?

鎺ㄨ崘绯荤粺锛?*LineageOS 23.2 瀹樻柟 nightly锛圓ndroid 16锛?*  
鍐呮牳锛?*Linux 5.4.302 QGKI**锛屽凡閫傞厤 DroidSpaces 鎵€闇€鐨勫懡鍚嶇┖闂淬€乧group銆乮ptables/NAT銆乷verlayfs 绛夛紝骞?*榛樿鍐呯疆 SukiSU-Ultra**锛坄CONFIG_KSU=y`锛屾棤闇€ Magisk锛夈€?

## 璧勬簮涓嬭浇

| 鍐呭 | 閾炬帴 |
| --- | --- |
| LineageOS 23.2 ROM锛?026-11-04锛?| [瀹樻柟鐩撮摼](https://mirrorbits.lineageos.org/full/venus/20261104/lineage-23.2-20261104-nightly-venus-signed.zip) 路 [FAU 闀滃儚](https://ftp.fau.de/lineageos/full/venus/20261104/lineage-23.2-20261104-nightly-venus-signed.zip) 路 [dotsrc 闀滃儚](https://mirrors.dotsrc.org/lineageos/full/venus/20261104/lineage-23.2-20261104-nightly-venus-signed.zip) |
| LineageOS 閰嶅闀滃儚锛坆oot / vendor_boot / dtbo锛?| [boot.img](https://mirrors.dotsrc.org/lineageos/full/venus/20261104/boot.img) 路 [vendor_boot.img](https://mirrors.dotsrc.org/lineageos/full/venus/20261104/vendor_boot.img) 路 [dtbo.img](https://mirrors.dotsrc.org/lineageos/full/venus/20261104/dtbo.img) |
| LineageOS 璁惧椤?/ 瀹夎鏁欑▼ | [璁惧椤礭(https://download.lineageos.org/devices/venus) 路 [瀹夎鏁欑▼](https://wiki.lineageos.org/devices/venus/install) |
| TWRP锛?.7.0_11-0-venus锛?| [涓嬭浇椤礭(https://dl.twrp.me/venus/) 路 [瀹樻柟璇存槑](https://twrp.me/xiaomi/xiaomimi11.html) |
| SukiSU 绠＄悊鍣紙v4.3.0-r2锛?| [APK 鐩撮摼](https://github.com/SukiSU-Ultra/SukiSU-Ultra/releases/download/v4.3.0-r2/SukiSU_v4.3.0-r2_41150-release.apk) 路 [Releases](https://github.com/SukiSU-Ultra/SukiSU-Ultra/releases) |
| 鏈唴鏍镐笅杞?| [Releases](https://github.com/luvhx/venus-droidspaces-kernel/releases/latest) |
| 鍚姩澶辫触鎺掓煡鍖?| [v5.4.302-test](https://github.com/luvhx/venus-droidspaces-kernel/releases/tag/v5.4.302-test) 路 [TESTING.md](TESTING.md) |
| DroidSpaces | <https://github.com/ravindu644/Droidspaces-OSS/releases/latest> |

> ROM SHA-256锛歚ee286eb38b83c457fc105ded828605d3fe709eb52741f25439f7ad5ed0eae6ab`  
> ROM 澶у皬锛?,548,545,131 B

## 鏈唴鏍镐骇鐗?

| 鏂囦欢 | 鐢ㄩ€?| SHA-256 |
| --- | --- | --- |
| `boot-venus-droidspaces.img` | fastboot 鐩村埛 boot | `d251d848c0f9f390df567c417ea9f439f6d5401025b204af9c3fc40b97bf5d84` |
| `DroidSpaces-venus-5.4.302-kernel.zip` | TWRP / AK3 鍗″埛 | `0c54915a2ff6288af8c2baa92d43a464cf3d0f367ab31dffd01daae6bb9787cd` |
| `Image` | 鍘熷巶鏍煎紡鍐呮牳 | `5d337dcc241e9a5b4bd0fdb26541bb441e00d3fb11c3e19944268070da9f7f33` |

> **鍚姩澶辫触/杩?fastboot锛?* 鏃?`v5.4.302` Release 鐨?boot 闀滃儚 AVB footer 宸叉竻闆讹紝閮ㄥ垎鏈哄櫒浼氭嫆缁濆惎鍔ㄣ€傝鏀圭敤 [v5.4.302-test](https://github.com/luvhx/venus-droidspaces-kernel/releases/tag/v5.4.302-test) 閲屼繚鐣?AVB footer 鐨勬帓鏌ュ寘锛屾楠よ [TESTING.md](TESTING.md)銆?

- 鍐呮牳宸插唴缃?SukiSU-Ultra v4.3.0-r2锛屽畨瑁呯鐞嗗櫒 APK 鍗冲彲鑾峰緱 root锛屼笉闇€瑕?Magisk銆?
- boot 闀滃儚鍩轰簬瀹樻柟 LineageOS 23.2 `boot.img`锛屽彧鏇挎崲 kernel锛宺amdisk 閫愬瓧鑺備笉鍙樸€?
- 鍐呮牳鐗堟湰锛歚5.4.302-qgki-g7ede20c8692e`锛屼笌瀹樻柟 `vendor_boot` 妯″潡鐨?`vermagic` 瀹屽叏涓€鑷淬€?
- 涓?stock 閰嶇疆鍋氫簡 ABI 瀵规瘮锛?3,435 涓叡鍚屽鍑虹鍙凤紝CRC 涓嶅尮閰?**0** 涓€?

## 鍒峰叆鏂规硶

### 1. 鍏堣 LineageOS 23.2

1. 瑙ｉ攣 bootloader锛屽苟纭鎵嬫満宸插崌绾у埌 **Android 14 搴曞眰鍥轰欢**锛圠ineageOS 瀹樻柟瑕佹眰锛夈€?
2. 澶囦唤 `boot`銆乣persist`锛岀數閲忎繚鎸?50% 浠ヤ笂銆?
3. 鎸?[瀹樻柟瀹夎鏁欑▼](https://wiki.lineageos.org/devices/venus/install) 鎿嶄綔锛屾牳蹇冩楠わ細

```bash
fastboot flash dtbo dtbo.img
fastboot flash vendor_boot vendor_boot.img
fastboot flash boot boot.img          # LineageOS recovery
fastboot reboot recovery
```

鍦?Recovery 閲?**Factory reset 鈫?Format data**锛岀劧鍚庯細

```bash
adb sideload lineage-23.2-20261104-nightly-venus-signed.zip
```

棣栨寮€鏈哄畬鎴愬悗鍐嶅埛鏈唴鏍搞€?

### 2. 鍒锋湰鍐呮牳

**鏂瑰紡 A锛歠astboot锛堟帹鑽愶紝鏈€绠€鍗曪級**

```bash
fastboot flash boot boot-venus-droidspaces.img
fastboot reboot
```

**鏂瑰紡 B锛歍WRP 鍗″埛锛堜繚鐣欏師 ramdisk锛?*

```bash
fastboot boot twrp-3.7.0_11-0-venus.img
```

杩涘叆 TWRP 鍚庯細`Advanced 鈫?Flash Current TWRP`锛屽啀鍒凤細

```text
DroidSpaces-venus-5.4.302-kernel.zip
```

杩欎釜 zip 鏄?kernel-only锛屽彧鏇挎崲鍐呮牳锛屼繚鐣欏師 ramdisk 鍜屽叾涓凡鏈夌殑淇敼銆?

### 3. 瑁?SukiSU 绠＄悊鍣ㄥ拰 DroidSpaces

1. 瀹夎 SukiSU 绠＄悊鍣?APK锛圼鐩撮摼](https://github.com/SukiSU-Ultra/SukiSU-Ultra/releases/download/v4.3.0-r2/SukiSU_v4.3.0-r2_41150-release.apk)锛夈€?
2. 鎵撳紑绠＄悊鍣紝纭鍐呮牳宸插唴缃?SukiSU锛涙寜鎻愮ず鎺堜簣 root銆?
3. 瀹夎 DroidSpaces APK锛屾巿浜?root銆?
4. 鎸?App 鎻愮ず瀹夎 backend锛岄噸鍚€?
5. `Settings 鈫?Requirements 鈫?Check Requirements`銆?

> 鏈唴鏍稿凡鍐呯疆 SukiSU锛?*涓嶈鍐嶅埛 Magisk 鎴?KernelSU**锛涘悓鏃惰澶氫釜 root 鏂规浼氬啿绐併€?

棰勬湡锛歁UST 椤瑰叏閮ㄩ€氳繃锛沵emory銆乻wap銆丆PU 缁熻銆乽ser namespace 娌欑鍙敤锛沗--cpus` 鍜?`--pids-limit` 浼氭樉绀轰笉鍙敤锛堝師鍥犺涓嬶級銆?

## 璇存槑涓庨檺鍒?

- 鏈唴鏍稿彧鍖归厤 **LineageOS 23.2 / 5.4.302 / 鍐呮牳 commit `7ede20c8`**锛涘埛鍒?22.2銆佸叾瀹?ROM 鎴?HyperOS 鍙兘鍥犳ā鍧?`vermagic`/CRC 涓嶅尮閰嶈€屼笉寮€鏈恒€?
- SukiSU 鐢?v4.3.0-r2 婧愮爜鍐呯疆锛屽苟鍋氫簡 5.4 鍏煎閫傞厤锛沗CONFIG_KPM` 鍏抽棴锛宍selinux_hide` 鍦?5.4 涓婁笉鍙敤锛岀鐞嗗櫒閲岄儴鍒嗛珮绾у姛鑳藉彲鑳芥樉绀轰笉鏀寔锛屾櫘閫?root 涓嶅彈褰卞搷銆?
- 涓轰繚璇?GKI 鍘傚晢妯″潡鑳藉姞杞斤紝娌℃湁寮€鍚?`CONFIG_CFS_BANDWIDTH` 鍜?`CONFIG_CGROUP_PIDS`锛屾墍浠?`--cpus`銆乣--pids-limit` 涓嶅彲鐢紱鍏朵綑 DroidSpaces 蹇呴渶椤瑰潎婊¤冻銆?
- boot 闀滃儚鐨?AVB footer 宸叉竻闆讹紝鍙€傜敤浜庡凡瑙ｉ攣 bootloader锛涗笉瑕侀噸鏂伴攣 BL銆?
- 鏈湪鐪熸満涓婂疄娴嬨€傚埛鏈烘湁椋庨櫓锛屽姟蹇呭厛澶囦唤锛屽苟纭鑳藉埛鍥炲畼鏂?`boot.img`銆?
- 濡傛灉鍒峰畬涓嶅紑鏈猴細`fastboot flash boot 瀹樻柟boot.img` 鍒峰洖锛屾垨鐢?TWRP 鎭㈠澶囦唤銆?

## 缂栬瘧

婧愮爜锛?https://github.com/LineageOS/android_kernel_xiaomi_sm8350>锛坄lineage-23.2`锛?

```bash
source env21.sh
./build21.sh
```

璇︾粏閰嶇疆鍜岄獙璇佹柟娉曡 `config/` 涓?`tools/check_kabi.sh`锛汼ukiSU 闆嗘垚浣跨敤 `drivers/kernelsu/`锛岄厤缃负 `CONFIG_KSU=y`銆乣CONFIG_KSU_MANUAL_SU=y`銆?

---

## 瀹炴祴缁撴灉锛?026-11-15锛岀湡鏈?venus锛?
鍐呮牳锛歚5.4.302-qgki-g7ede20c8692e`锛堟瀯寤烘椂闂?`Sat Nov 14 21:15:30 UTC 2026`锛夛紝
`CONFIG_CFI_CLANG=y` + `CONFIG_LTO_CLANG=y` + droidspaces kABI padding 琛ヤ竵銆?
`droidspaces check`锛坴7.2.0锛夛細

- **MUST HAVE锛氬叏閮?鉁?*锛坮oot銆丳ID/Mount/UTS/IPC namespace銆乸ivot_root銆?proc銆?sys銆丼eccomp锛?- **RECOMMENDED锛氬叏閮?鉁?*锛坋poll銆乻ignalfd銆丳TY銆乨evpts銆乴oop銆乪xt4銆乧group v2銆乧group ns銆乶ew mount API銆乨evtmpfs锛?- **OPTIONAL锛氶櫎 CPU 闄愬埗锛圕FS_BANDWIDTH锛変笌杩涚▼闄愬埗锛圕GROUP_PIDS锛夊鍏ㄩ儴 鉁?*锛堣繖涓ら」浼氱牬鍧?kABI锛屼繚鎸佸叧闂級

瀹瑰櫒瀹炴祴锛?
```text
$ droidspaces start -n alpine -r /data/local/Droidspaces/rootfs/alpine --net=none
[+] Container started with PID 6258 ... OS: Alpine Linux v3.20
$ droidspaces -n alpine run -- /bin/sh -c 'uname -a; head -2 /etc/os-release'
Linux alpine 5.4.302-qgki-g7ede20c8692e #1 SMP PREEMPT Sat Nov 14 21:15:30 UTC 2026 aarch64 Linux
NAME="Alpine Linux"
ID=alpine
```

### 鑳藉紑鏈虹殑鏋勫缓閰嶆柟锛堝叧閿級

涔嬪墠鍑犵増鍐呮牳"鑳界紪璇戜絾璧蜂笉鏉?锛屾牴鍥犳槸鍘傚晢妯″潡锛坄msm_drm.ko`銆乣fts_touch_spi.ko`銆乣xiaomi_touch.ko` 绛夛級
鏄?**CFI 缂栬瘧**鐨勶紝鏈畾涔夌鍙烽噷鏈?`__cfi_slowpath`锛涘唴鏍歌嫢涓嶅甫 `CONFIG_CFI_CLANG` 灏变笉瀵煎嚭璇ョ鍙凤紝
妯″潡鍏ㄩ儴鍔犺浇澶辫触 鈫?鍗″湪寮€鏈?logo銆傚洜姝ゅ繀椤伙細

1. 鐢?**AOSP prebuilt clang**锛堟湰娆′负 `clang-r547379`锛宑lang 20.0.0锛夎€屼笉鏄彂琛岀増 clang锛?2. **淇濈暀鍘熷巶閰嶇疆鍘熸牱**锛歚CONFIG_LTO_CLANG=y`銆乣CONFIG_CFI_CLANG=y`銆乣CONFIG_SHADOW_CALL_STACK=y`锛?3. 浼?`-D__ANDROID_COMMON_KERNEL__`锛圠ineageOS `build.config.common` 鍚屾牱浼氫紶锛夛紱
4. 鍙澶栧姞 droidspaces 閫夐」涓?venus 涓撶敤 kABI padding 琛ヤ竵锛宍LOCALVERSION` 瀵归綈 ROM 鐨?vermagic銆?
瀹屾暣 CI 瑙?`.github/workflows/build-kernel.yml`锛坵orkflow v8锛夛紝
鏋勫缓浜х墿鐢?`tools/repack-boot.py` 瑁呭洖瀹樻柟 `boot.img` 鍚?`fastboot flash boot` 鍗冲彲銆?
