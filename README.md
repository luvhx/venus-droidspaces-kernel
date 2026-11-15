# 小米 11（venus）DroidSpaces 内核

适用于 **小米 11 / Mi 11（venus，SM8350，M2011K2C / M2011K2G）**。

推荐系统：**LineageOS 23.2 官方 nightly（Android 16）**  
内核：**Linux 5.4.302 QGKI**，已适配 DroidSpaces 所需的命名空间、cgroup、iptables/NAT、overlayfs 等，并**默认内置 SukiSU-Ultra**（`CONFIG_KSU=y`，无需 Magisk）。

## 资源下载

| 内容 | 链接 |
| --- | --- |
| LineageOS 23.2 ROM（2026-11-04） | [官方直链](https://mirrorbits.lineageos.org/full/venus/20261104/lineage-23.2-20261104-nightly-venus-signed.zip) · [FAU 镜像](https://ftp.fau.de/lineageos/full/venus/20261104/lineage-23.2-20261104-nightly-venus-signed.zip) · [dotsrc 镜像](https://mirrors.dotsrc.org/lineageos/full/venus/20261104/lineage-23.2-20261104-nightly-venus-signed.zip) |
| LineageOS 配套镜像（boot / vendor_boot / dtbo） | [boot.img](https://mirrors.dotsrc.org/lineageos/full/venus/20261104/boot.img) · [vendor_boot.img](https://mirrors.dotsrc.org/lineageos/full/venus/20261104/vendor_boot.img) · [dtbo.img](https://mirrors.dotsrc.org/lineageos/full/venus/20261104/dtbo.img) |
| LineageOS 设备页 / 安装教程 | [设备页](https://download.lineageos.org/devices/venus) · [安装教程](https://wiki.lineageos.org/devices/venus/install) |
| TWRP（3.7.0_11-0-venus） | [下载页](https://dl.twrp.me/venus/) · [官方说明](https://twrp.me/xiaomi/xiaomimi11.html) |
| SukiSU 管理器（v4.3.0-r2） | [APK 直链](https://github.com/SukiSU-Ultra/SukiSU-Ultra/releases/download/v4.3.0-r2/SukiSU_v4.3.0-r2_41150-release.apk) · [Releases](https://github.com/SukiSU-Ultra/SukiSU-Ultra/releases) |
| 本内核下载 | [Releases](https://github.com/luvhx/venus-droidspaces-kernel/releases/latest) |
| 启动失败排查包 | [v5.4.302-test](https://github.com/luvhx/venus-droidspaces-kernel/releases/tag/v5.4.302-test) · [TESTING.md](TESTING.md) |
| DroidSpaces | <https://github.com/ravindu644/Droidspaces-OSS/releases/latest> |

> ROM SHA-256：`ee286eb38b83c457fc105ded828605d3fe709eb52741f25439f7ad5ed0eae6ab`  
> ROM 大小：1,548,545,131 B

## 本内核产物

| 文件 | 用途 | SHA-256 |
| --- | --- | --- |
| `boot-venus-droidspaces.img` | fastboot 直刷 boot | `d251d848c0f9f390df567c417ea9f439f6d5401025b204af9c3fc40b97bf5d84` |
| `DroidSpaces-venus-5.4.302-kernel.zip` | TWRP / AK3 卡刷 | `0c54915a2ff6288af8c2baa92d43a464cf3d0f367ab31dffd01daae6bb9787cd` |
| `Image` | 原厂格式内核 | `5d337dcc241e9a5b4bd0fdb26541bb441e00d3fb11c3e19944268070da9f7f33` |

> **启动失败/进 fastboot？** 旧 `v5.4.302` Release 的 boot 镜像 AVB footer 已清零，部分机器会拒绝启动。请改用 [v5.4.302-test](https://github.com/luvhx/venus-droidspaces-kernel/releases/tag/v5.4.302-test) 里保留 AVB footer 的排查包，步骤见 [TESTING.md](TESTING.md)。

- 内核已内置 SukiSU-Ultra v4.3.0-r2，安装管理器 APK 即可获得 root，不需要 Magisk。
- boot 镜像基于官方 LineageOS 23.2 `boot.img`，只替换 kernel，ramdisk 逐字节不变。
- 内核版本：`5.4.302-qgki-g7ede20c8692e`，与官方 `vendor_boot` 模块的 `vermagic` 完全一致。
- 与 stock 配置做了 ABI 对比：13,435 个共同导出符号，CRC 不匹配 **0** 个。

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

首次开机完成后再刷本内核。

### 2. 刷本内核

**方式 A：fastboot（推荐，最简单）**

```bash
fastboot flash boot boot-venus-droidspaces.img
fastboot reboot
```

**方式 B：TWRP 卡刷（保留原 ramdisk）**

```bash
fastboot boot twrp-3.7.0_11-0-venus.img
```

进入 TWRP 后：`Advanced → Flash Current TWRP`，再刷：

```text
DroidSpaces-venus-5.4.302-kernel.zip
```

这个 zip 是 kernel-only，只替换内核，保留原 ramdisk 和其中已有的修改。

### 3. 装 SukiSU 管理器和 DroidSpaces

1. 安装 SukiSU 管理器 APK（[直链](https://github.com/SukiSU-Ultra/SukiSU-Ultra/releases/download/v4.3.0-r2/SukiSU_v4.3.0-r2_41150-release.apk)）。
2. 打开管理器，确认内核已内置 SukiSU；按提示授予 root。
3. 安装 DroidSpaces APK，授予 root。
4. 按 App 提示安装 backend，重启。
5. `Settings → Requirements → Check Requirements`。

> 本内核已内置 SukiSU，**不要再刷 Magisk 或 KernelSU**；同时装多个 root 方案会冲突。

预期：MUST 项全部通过；memory、swap、CPU 统计、user namespace 沙箱可用；`--cpus` 和 `--pids-limit` 会显示不可用（原因见下）。

## 说明与限制

- 本内核只匹配 **LineageOS 23.2 / 5.4.302 / 内核 commit `7ede20c8`**；刷到 22.2、其它 ROM 或 HyperOS 可能因模块 `vermagic`/CRC 不匹配而不开机。
- SukiSU 用 v4.3.0-r2 源码内置，并做了 5.4 兼容适配；`CONFIG_KPM` 关闭，`selinux_hide` 在 5.4 上不可用，管理器里部分高级功能可能显示不支持，普通 root 不受影响。
- 为保证 GKI 厂商模块能加载，没有开启 `CONFIG_CFS_BANDWIDTH` 和 `CONFIG_CGROUP_PIDS`，所以 `--cpus`、`--pids-limit` 不可用；其余 DroidSpaces 必需项均满足。
- boot 镜像的 AVB footer 已清零，只适用于已解锁 bootloader；不要重新锁 BL。
- 未在真机上实测。刷机有风险，务必先备份，并确认能刷回官方 `boot.img`。
- 如果刷完不开机：`fastboot flash boot 官方boot.img` 刷回，或用 TWRP 恢复备份。

## 编译

源码：<https://github.com/LineageOS/android_kernel_xiaomi_sm8350>（`lineage-23.2`）

```bash
source env21.sh
./build21.sh
```

详细配置和验证方法见 `config/` 与 `tools/check_kabi.sh`；SukiSU 集成使用 `drivers/kernelsu/`，配置为 `CONFIG_KSU=y`、`CONFIG_KSU_MANUAL_SU=y`。

---

## 实测结果（2026-11-15，真机 venus）

内核：`5.4.302-qgki-g7ede20c8692e`（构建时间 `Sat Nov 14 21:15:30 UTC 2026`），
`CONFIG_CFI_CLANG=y` + `CONFIG_LTO_CLANG=y` + droidspaces kABI padding 补丁。

`droidspaces check`（v7.2.0）：

- **MUST HAVE：全部 ✓**（root、PID/Mount/UTS/IPC namespace、pivot_root、/proc、/sys、Seccomp）
- **RECOMMENDED：全部 ✓**（epoll、signalfd、PTY、devpts、loop、ext4、cgroup v2、cgroup ns、new mount API、devtmpfs）
- **OPTIONAL：除 CPU 限制（CFS_BANDWIDTH）与进程限制（CGROUP_PIDS）外全部 ✓**（这两项会破坏 kABI，保持关闭）

容器实测：

```text
$ droidspaces start -n alpine -r /data/local/Droidspaces/rootfs/alpine --net=none
[+] Container started with PID 6258 ... OS: Alpine Linux v3.20
$ droidspaces -n alpine run -- /bin/sh -c 'uname -a; head -2 /etc/os-release'
Linux alpine 5.4.302-qgki-g7ede20c8692e #1 SMP PREEMPT Sat Nov 14 21:15:30 UTC 2026 aarch64 Linux
NAME="Alpine Linux"
ID=alpine
```

### 能开机的构建配方（关键）

之前几版内核"能编译但起不来"，根因是厂商模块（`msm_drm.ko`、`fts_touch_spi.ko`、`xiaomi_touch.ko` 等）
是 **CFI 编译**的，未定义符号里有 `__cfi_slowpath`；内核若不带 `CONFIG_CFI_CLANG` 就不导出该符号，
模块全部加载失败 → 卡在开机 logo。因此必须：

1. 用 **AOSP prebuilt clang**（本次为 `clang-r547379`，clang 20.0.0）而不是发行版 clang；
2. **保留原厂配置原样**：`CONFIG_LTO_CLANG=y`、`CONFIG_CFI_CLANG=y`、`CONFIG_SHADOW_CALL_STACK=y`；
3. 传 `-D__ANDROID_COMMON_KERNEL__`（LineageOS `build.config.common` 同样会传）；
4. 只额外加 droidspaces 选项与 venus 专用 kABI padding 补丁，`LOCALVERSION` 对齐 ROM 的 vermagic。

完整 CI 见 `.github/workflows/build-kernel.yml`（workflow v8），
构建产物用 `tools/repack-boot.py` 装回官方 `boot.img` 后 `fastboot flash boot` 即可。
