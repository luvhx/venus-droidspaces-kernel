# 启动失败排查包（venus）

主 Release `v5.4.302` 里的 `boot-venus-droidspaces.img` 曾把 AVB footer 清零，部分小米 ABL 会拒绝启动；同时 SukiSU 5.4 适配里修了一个 SELinux policy 锁问题。

请使用本测试 Release 里的镜像：

https://github.com/luvhx/venus-droidspaces-kernel/releases/tag/v5.4.302-test

## 文件

| 文件 | 用途 | SHA-256 |
| --- | --- | --- |
| `boot-venus-stock.img` | 官方 LineageOS 23.2 boot，先刷回恢复 | `6e3dd677b6729fa77b814bd899afe1137197e44678f341a3d29d924ea40a4956` |
| `boot-venus-sukisu-avb.img` | 修复版：保留 AVB footer + SukiSU + SELinux 锁修复 | `64a126bb4d4eeb995bf290cd275dc23281a415f73f16699e503f6015681ee827` |
| `boot-venus-nosukisu-avb.img` | 对照组：保留 AVB footer，无 SukiSU | `833c7426acf0409fa8685c99f8fa54cca6cdb77d28e13f0bf559eace6ea39a5f` |
| `DroidSpaces-venus-5.4.302-kernel-avb.zip` | TWRP/AK3 测试包，使用已修复的 SukiSU kernel | `90c890862e60e56d0ce54011d16306195ed19126682bae37f01114295e2619e6` |

## 步骤

### 1. 恢复

```bash
fastboot flash boot boot-venus-stock.img
fastboot reboot
```

确认能进 LineageOS。

### 2. 测试 SukiSU 修复版

```bash
fastboot flash boot boot-venus-sukisu-avb.img
fastboot reboot
```

### 3. 如果仍失败，测试无 SukiSU 对照

```bash
fastboot flash boot boot-venus-nosukisu-avb.img
fastboot reboot
```

判断：

- 无 SukiSU 能开机、SukiSU 不能：问题在 SukiSU 的 5.4 适配。
- 两个都不能开机：问题在 boot 打包/AVB 或 DroidSpaces 内核配置。

### 4. 抓日志

失败后临时启动 TWRP：

```bash
fastboot boot twrp-3.7.0_11-0-venus.img
adb shell "cat /sys/fs/pstore/console-ramoops* 2>/dev/null" > ramoops.txt
adb shell "cat /proc/last_kmsg 2>/dev/null" > last_kmsg.txt
adb shell "dmesg" > twrp-dmesg.txt
```

把 `ramoops.txt` / `last_kmsg.txt` 发到 Issue。

## 限制

- 只适用于已解锁 bootloader 的 LineageOS 23.2（5.4.302 / commit `7ede20c8`）。
- 测试包保留原厂 AVB footer，但 kernel 已换，签名本来就不再匹配；解锁状态下使用。
