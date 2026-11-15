# 小米 11（venus）DroidSpaces 内核

适用于 **小米 11 / Mi 11（venus，SM8350，M2011K2C / M2011K2G）**。

推荐系统：**LineageOS 23.2 官方 nightly（Android 16）**  
内核：**Linux 5.4.302 QGKI**，已适配 DroidSpaces 所需的命名空间、cgroup、iptables/NAT、overlayfs 等。

> **当前可用版本：[v5.4.302-v8](https://github.com/luvhx/venus-droidspaces-kernel/releases/tag/v5.4.302-v8)** ——
> 真机验证通过（`droidspaces check` 全绿、Alpine 容器可启停），见 [验证记录](docs/VERIFIED-2026-11-15.md)。
> 旧的 `v5.4.302` / `v5.4.302-test` 已标记为 pre-release，镜像会卡在开机 logo，请勿再刷。

## 资源下载

| 内容 | 链接 |
| --- | --- |
| 本内核（v8） | [Release](https://github.com/luvhx/venus-droidspaces-kernel/releases/tag/v5.4.302-v8) |
| 刷入与验证步骤 | [TESTING.md](TESTING.md) |
| 真机验证记录 | [docs/VERIFIED-2026-11-15.md](docs/VERIFIED-2026-11-15.md) |
| LineageOS 23.2 ROM（2026-11-04） | [官方直链](https://mirrorbits.lineageos.org/full/venus/20261104/lineage-23.2-20261104-nightly-venus-signed.zip) · [dotsrc 镜像](https://mirrors.dotsrc.org/lineageos/full/venus/20261104/lineage-23.2-20261104-nightly-venus-signed.zip) |
| LineageOS 配套镜像（boot / vendor_boot / dtbo） | [boot.img](https://mirrors.dotsrc.org/lineageos/full/venus/20261104/boot.img) · [vendor_boot.img](https://mirrors.dotsrc.org/lineageos/full/venus/20261104/vendor_boot.img) · [dtbo.img](https://mirrors.dotsrc.org/lineageos/full/venus/20261104/dtbo.img) |
| LineageOS 设备页 / 安装教程 | [设备页](https://download.lineageos.org/devices/venus) · [安装教程](https://wiki.lineageos.org/devices/venus/install) |
| DroidSpaces | <https://github.com/ravindu644/Droidspaces-OSS/releases/latest> |
| Magisk（拿 root） | <https://github.com/topjohnwu/Magisk/releases/latest> |

> ROM SHA-256：`ee286eb38b83c457fc105ded828605d3fe709eb52741f25439f7ad5ed0eae6ab`  
> ROM 大小：1,548,545,131 B

## 本内核产物（v8）

| 文件 | 用途 | SHA-256 |
| --- | --- | --- |
| `boot-venus-droidspaces-v8.img` | fastboot 直刷 boot | `a573f3a381cafce490479be066a90a04c10843746f2c42dcca1a66e06a323ba7` |
| `Image` | 原始内核，可自行 repack | `2b398a80ec6b5aaeae1f7a056b35627f5dbfe0028cce941a5233d1821c2bf2d9` |
| `venus-droidspaces-v8.config` | 构建实际使用的配置 | `ab5071343702fdb11e17bf073bf33fdf41ada749d7067c46b195e6c1043debce` |

- 内核版本：`5.4.302-qgki-g7ede20c8692e`，与 ROM `vendor_boot` 模块的 `vermagic` 完全一致。
- root 不在内核里：刷完后用 Magisk 对该 boot 镜像打补丁即可（见 TESTING.md）。

## 刷入方法

### 1. 先装 LineageOS 23.2

1. 解锁 bootloader，并确认手机已升级到 **Android 14 底层固件**（LineageOS 官方要求）。
2. 备份 `boot`、`persist`，电量保持 50% 以上。
3. 按 [官方安装教程](https://wiki.lineageos.org/devices/venus/install) 操作，核心步骤：

```bash
fastboot flash dtbo dtbo.img
fastboot flash vendor_boot vendor_boot.img
fastboot flash boot boot.img          # LineageOS recovery
fastboot reboot recovery
```

在 Recovery 里 **Factory reset → Format data**，然后：

```bash
adb sideload lineage-23.2-20261104-nightly-venus-signed.zip
```

首次开机完成后再刷本内核（必须是 `20261104` 这个版本，内核 commit 要对上 `7ede20c8`）。

### 2. 刷本内核

```bash
fastboot flash boot boot-venus-droidspaces-v8.img
fastboot reboot
```

### 3. 拿 root 并装 DroidSpaces

1. 安装 Magisk，用「安装 → 选择并补丁一个文件」对上面的 boot 镜像打补丁；
2. `fastboot flash boot magisk_patched-*.img`，重启后打开 Magisk 确认已安装；
3. 安装 DroidSpaces APK，授予 root，按提示安装 backend；
4. `Settings → Requirements → Check Requirements`。

预期：MUST / RECOMMENDED 全部通过；`--cpus`、`--pids-limit` 不可用（原因见下）。

## 说明与限制

- 本内核只匹配 **LineageOS 23.2 / 5.4.302 / 内核 commit `7ede20c8`**；刷到 22.2、其它 ROM 或 HyperOS 会因模块
  `vermagic`/CRC 不匹配而不开机。
- 为保证 GKI 厂商模块能加载，没有开启 `CONFIG_CFS_BANDWIDTH` 和 `CONFIG_CGROUP_PIDS`，所以 `--cpus`、
  `--pids-limit` 不可用；其余 DroidSpaces 必需项均满足。
- **必须用 AOSP prebuilt clang 编译并保留 `CONFIG_CFI_CLANG=y`**：厂商模块（`msm_drm.ko`、`fts_touch_spi.ko` 等）
  依赖 `__cfi_slowpath`，关掉 CFI 会全部加载失败、卡在开机 logo。构建配方见 [验证记录](docs/VERIFIED-2026-11-15.md)。
- 解锁 bootloader 才能刷；不要重新锁 BL。

## 编译

CI：`.github/workflows/build-kernel.yml`（AOSP clang + 原厂配置 + venus kABI padding 补丁），
产物用 `tools/repack-boot.py` 装回官方 `boot.img`。

源码：<https://github.com/LineageOS/android_kernel_xiaomi_sm8350>（`lineage-23.2`，commit `7ede20c8`）

> `env21.sh` / `build21.sh` 是早期用 Debian clang 的本地构建脚本，**产出的内核无法启动**，仅作历史参考。
