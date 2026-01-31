"""
硅基流动余额查询插件
用于查询 SiliconFlow API 账户余额
"""

from src.plugin_system.base.plugin_metadata import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="硅基流动余额查询",
    description="查询 SiliconFlow (硅基流动) API 账户余额的插件",
    usage="""
    使用 /余额 命令查询 SiliconFlow 账户余额。
    
    命令：
    - /余额 - 查询当前账户余额
    - /siliconflow_balance - 完整命令名
    - /sf余额 - 快捷别名
    - /硅基余额 - 中文别名
    
    配置：
    在 config/plugins/siliconflow_balance_plugin/config.toml 中设置 API Key
    """,
    author="ikun两年半",
    version="1.0.0",
    license="AGPL",
    keywords=["siliconflow", "硅基流动", "余额", "API"],
    categories=["工具"],
)
