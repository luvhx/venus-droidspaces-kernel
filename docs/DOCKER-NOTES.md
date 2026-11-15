# Docker / 1Panel 在 venus 容器里的可用配置（2026-11-15）

## 结论

当前内核（`5.4.302-qgki-g7ede20c8692e`，v8 构建，**没有** `NF_TABLES` / `BRIDGE_NETFILTER`）
下，容器里的 Docker 可以正常跑，前提是把 iptables 切到 **legacy** 后端。

```bash
# 容器内
update-alternatives --set iptables  /usr/sbin/iptables-legacy
update-alternatives --set ip6tables /usr/sbin/ip6tables-legacy
systemctl restart docker
```

验证：

```text
docker version   -> client 29.9.3 / server 29.9.3
docker info      -> driver=overlayfs  cgroup=systemd/2  iptables=legacy
systemctl is-active docker -> active（enabled，开机自启）
```

## 为什么默认不行

Debian 12 的 `iptables` 默认指向 `iptables-nft`，而内核没编 `CONFIG_NF_TABLES`：

```
iptables v1.8.9 (nf_tables): Could not fetch rule set generation id: Invalid argument
failed to create NAT chain DOCKER
```

dockerd 因此直接退出。legacy 后端走 `IP_NF_IPTABLES` / `IP_NF_NAT`，这条路径内核是完整的。

## 缺失项与影响

| 缺的选项 | 影响 |
| --- | --- |
| `CONFIG_NF_TABLES` + `NFT_*` | 不能用 nft 后端（改 legacy 即可绕过） |
| `CONFIG_BRIDGE_NETFILTER` | 无 `br_netfilter`：日志有 `bridge-nf-call-iptables is disabled`；同一 bridge 内容器互访走 L2 正常，`-p` 端口映射走 nat DNAT 也正常；只是"对桥接流量做 iptables 过滤"这类场景不生效 |

## 内核侧的尝试（未成功，记录备查）

2026-11-15 用同一个 CI（AOSP clang r547379 + 原厂配置 + droidspaces kABI 补丁）编了三版：

| 变体 | 新增选项 | 结果 |
| --- | --- | --- |
| full | `NF_TABLES`+`NFT_*`+`BRIDGE_NETFILTER`+`IPVLAN`+`VXLAN`+xtables | ❌ 卡在开机 logo |
| brnf | `BRIDGE_NETFILTER`+`BRIDGE_VLAN_FILTERING`+`IPVLAN`+`VXLAN`+xtables | ❌ 同样卡住 |
| nft  | `NF_TABLES`+`NFT_*`+xtables | ❌ 同样卡住 |

已排除的因素：

- **不是体积问题**：把已知能开机的旧内核补零到同样 40,032,768 字节后刷入，能正常开机；
- **不是工具链问题**：三版与能开机的 v8 都是同一套 AOSP clang（r547379 / clang 20.0.0）；
- **不是 ABI/vermagic**：版本串都是 `5.4.302-qgki-g7ede20c8692e`，`__cfi_slowpath` 正常导出。

也就是说，**某个 netfilter 选项本身会让这台机器的引导卡死**（无 ramoops，拿不到 panic 日志）。
继续定位需要逐项二分（每轮 ~40 分钟构建 + 2 次重启），暂缓。

工作流里保留了 `brnf` / `nft` 两个矩阵变体（`.github/workflows/build-kernel.yml`），
以后要接着排可直接复用。当前出货内核仍是 v8（`boot-venus-droidspaces-v8.img`）。
