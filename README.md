# 硅基流动余额查询插件

查询 SiliconFlow (硅基流动) API 账户余额的 MoFox-Core 插件。

## 功能

- 查询 SiliconFlow 账户余额
- 显示当前余额、充值余额和总余额

## 安装

1. 将本插件文件夹复制到 MoFox-Core 的插件目录
2. 重启机器人
3. 在配置文件中设置 API Key

## 配置

首次加载后，在 `config/plugins/siliconflow_balance_plugin/config.toml` 中配置：

```toml
[api]
api_key = "your-siliconflow-api-key"
```

API Key 可从 https://cloud.siliconflow.cn/account/ak 获取。

## 使用方法

在聊天中发送以下命令：

- `/余额` - 查询账户余额
- `/siliconflow_balance` - 完整命令
- `/sf余额` - 快捷别名
- `/硅基余额` - 中文别名

## 输出示例

```
SiliconFlow 账户余额

当前余额: 1234.5678 元
充值余额: 0.1145 元
总余额: 1234.6823 元

账户状态: normal
```

## 依赖

- aiohttp

## 作者

ikun两年半

## 许可证

AGPL