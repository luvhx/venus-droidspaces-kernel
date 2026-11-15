# 刷入与验证（v8 内核，2026-11-15 真机验证）

> 这个版本已在真机（venus / M2011K2C，LineageOS 23.2 `20261104`）上跑通 DroidSpaces，
> requirements 全绿，Alpine 容器可正常启停。详见 [`docs/VERIFIED-2026-11-15.md`](docs/VERIFIED-2026-11-15.md)。

## 前提

- 小米 11（venus），bootloader 已解锁
- 系统：LineageOS 23.2 `20261104-NIGHTLY-venus`（Android 16，底层 Android 14 固件）
  - 官方镜像：<https://mirrorbits.lineageos.org/full/venus/20261104/>
  - 内核 commit 必须对应 `7ede20c8`，否则厂商模块 vermagic/CRC 对不上
- `boot.img` 备份：官方 `boot.img` 就是本仓库 repack 用的模板

## 方式 A：直接刷（推荐）

```bash
fastboot flash boot boot-venus-droidspaces-v8.img
fastboot reboot
```

刷完后再用 Magisk 拿 root：

1. 安装 Magisk（≥ v31.1）；
2. Magisk → 安装 → 选择并补丁一个文件 → 选刚刷入的 boot 镜像（或仓库里的 `boot-venus-droidspaces-v8.img`）；
3. 把生成的 `magisk_patched-*.img` 用 `fastboot flash boot` 刷入；
4. 重启，打开 Magisk 确认已安装。

## 方式 B：从 `Image` 自行组装

```bash
python tools/repack-boot.py --boot boot.img --image Image --out boot-custom.img
fastboot flash boot boot-custom.img
```

`repack-boot.py` 会自动复用官方 boot.img 的布局（kernel 与 ramdisk 的偏移、AVB footer 重算）。

## 安装 DroidSpaces

1. 安装 [DroidSpaces v7.2.0 APK](https://github.com/ravindu644/Droidspaces-OSS/releases/latest)；
2. 打开 App，授予 root，按提示安装 backend（会装成 Magisk 模块 `droidspaces`）；
3. `Settings → Requirements → Check Requirements`，或命令行：

```bash
su -c '/data/local/Droidspaces/bin/droidspaces check'
```

预期：MUST / RECOMMENDED 全绿；OPTIONAL 里只有 **CPU limit** 与 **Process limit** 为 ✗
（`CONFIG_CFS_BANDWIDTH` / `CONFIG_CGROUP_PIDS` 会破坏 kABI，故意关闭，`--cpus` 与 `--pids-limit` 不可用）。

## 跑一个容器

```bash
# rootfs 可以是任意 Linux rootfs 目录（这里用 Alpine minirootfs 解压）
su -c '/data/local/Droidspaces/bin/droidspaces start -n alpine -r /data/local/Droidspaces/rootfs/alpine --net=host'
su -c '/data/local/Droidspaces/bin/droidspaces -n alpine run -- /bin/sh -c "uname -a"'
su -c '/data/local/Droidspaces/bin/droidspaces stop -n alpine'
```

> 注意 `-n` 要写在子命令**前面**。

## 出问题怎么回退

```bash
fastboot flash boot boot.img      # 官方 boot，随时可回
fastboot reboot
```

## 常见卡在 MI 标志的原因（经验）

| 现象 | 原因 |
| --- | --- |
| 内核编译成功、刷入后卡 MI 标志 | 用了发行版 clang 并关掉 `CONFIG_CFI_CLANG` → 厂商模块缺 `__cfi_slowpath`，全部加载失败 |
| 同上 | 版本串多一个 `+`（工作树脏）→ vermagic 与 ROM 模块不一致 |
| 同上 | 缺少 `-D__ANDROID_COMMON_KERNEL__` |
| 开机后没有显示/触摸 | 同上，`msm_drm.ko` / `fts_touch_spi.ko` 没加载 |
