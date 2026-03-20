# 网易云音乐 Agent Skills

基于 `ncm-cli` 的网易云音乐 AI Agent 技能包。

**温馨提示**：使用前请完成ncm-cli的安装（[安装指南](https://www.npmjs.com/package/@music163/ncm-cli)
）与入驻（[入驻指南](https://developer.music.163.com/st/developer/document?docId=9504d35aa41a47c6ac9830b2dbf48f94)），并完成配置。

## 技能概览

| 技能                      | 说明           | 触发场景        |
|-------------------------|--------------|-------------|
| ncm-cli-setup           | 安装配置 ncm-cli | 工具未安装时自动引导  |
| netease-music-cli       | 执行音乐操作       | 搜索、歌单管理、推荐等 |
| netease-music-assistant | 智能音乐助手       | 个性化推荐       |

三个技能的依赖关系：

```
netease-music-assistant（智能助手）
    │
    │  调用
    ▼
netease-music-cli（CLI 操作层）
    │
    │  依赖
    ▼
ncm-cli-setup（安装配置）
```

---

## 前置条件

ncm-cli 的所有命令调用依赖 API
Key。请先前往[网易云音乐开放平台](https://developer.music.163.com/st/developer/apply/account?type=INDIVIDUAL)完成入驻并申请
API Key（appId 和 privateKey），并在安装后通过 `ncm-cli configure` 完成配置。

---

## ncm-cli-setup

**安装和配置 ncm-cli 工具。**

- 环境要求：Node.js >= 18
- 安装方式：`npm install -g @music/ncm-cli`
- 安装后需执行 `ncm-cli configure` 完成配置
- 安装后需执行 `ncm-cli login` 完成登录授权

常见问题：

| 问题                           | 解决方法                     |
|------------------------------|--------------------------|
| `ncm-cli: command not found` | 检查 npm 全局 bin 是否在 PATH 中 |
| 登录超时                         | 重新执行 `ncm-cli login`     |

---

## netease-music-cli

**通过 ncm-cli 执行网易云音乐操作。**

核心能力：

- 搜索歌曲/歌单/专辑
- 歌单管理（创建、添加歌曲、查看）
- 获取每日推荐
- 查看用户信息

关键规则：

- 返回结果时提供可点击的链接（`https://music.163.com/#/song?id=<明文ID>`）
- 遇到未授权提示时自动执行 `ncm-cli login` 引导登录

---

## netease-music-assistant

**以模型判断为核心的智能音乐助手。**

触发条件：消息中包含"网易云"或"云音乐"，或用户表达听歌、推荐、偏好分析等意图。

### 核心能力

```
理解需求 → 分析偏好 → 制定搜索策略 → 执行搜索 → 筛选结果 → 语义化推荐 → 推送 + 可选建单
```

### 主要功能

**1. 偏好分析**

分析用户红心歌单，从多维度生成用户画像：

- 内容维度：曲风标签统计、情绪方向、语言偏好、代表艺人
- 时间维度：高频红心时段、周期规律
- 近期趋势：最近红心的偏好变化

**2. 智能推荐**

- 自动决策搜索类型（歌单/专辑/单曲或混合）
- 多关键词并行搜索（2~4 次），自动去重已推荐和已收藏内容
