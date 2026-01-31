"""
硅基流动余额查询插件主文件
"""

from typing import ClassVar, List, Tuple, Type, Optional
import aiohttp

from src.common.logger import get_logger
from src.plugin_system import (
    BasePlugin,
    register_plugin,
    ComponentInfo,
    PlusCommand,
    CommandArgs,
    ChatType,
)
from src.plugin_system.base.component_types import PermissionNodeField
from src.plugin_system.base.config_types import ConfigField

logger = get_logger("SiliconFlowBalance")


class BalanceCommand(PlusCommand):
    """
    查询硅基流动余额命令
    """

    command_name: str = "余额"
    command_description: str = "查询 SiliconFlow (硅基流动) API 账户余额"
    command_aliases: ClassVar[list[str]] = ["siliconflow_balance", "sf余额", "硅基余额"]
    chat_type_allow = ChatType.ALL

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def execute(self, args: CommandArgs) -> tuple[bool, Optional[str], bool]:
        """
        执行查询余额命令
        """
        # 获取 API Key
        api_key = self.get_config("api.api_key", "")
        
        if not api_key:
            await self.send_text(
                "未配置 API Key\n"
                "请在 config/plugins/siliconflow_balance_plugin/config.toml 中设置 api_key"
            )
            return False, "未配置 API Key", True

        try:
            # 调用 SiliconFlow API 查询余额
            balance_info = await self._query_balance(api_key)
            
            if balance_info.get("success"):
                await self.send_text(balance_info.get("message", "查询成功"))
                return True, "余额查询成功", True
            else:
                await self.send_text(f"查询失败：{balance_info.get('error', '未知错误')}")
                return False, balance_info.get("error", "查询失败"), True

        except Exception as e:
            logger.error(f"查询余额时发生异常: {e}")
            await self.send_text(f"查询过程中发生错误：{str(e)}")
            return False, f"查询异常: {str(e)}", True

    async def _query_balance(self, api_key: str) -> dict:
        """
        调用 SiliconFlow API 查询余额
        
        Args:
            api_key: SiliconFlow API Key
            
        Returns:
            dict: 包含查询结果的字典
        """
        url = "https://api.siliconflow.cn/v1/user/info"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=30) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._format_balance_message(data)
                elif response.status == 401:
                    return {
                        "success": False,
                        "error": "API Key 无效或已过期，请检查配置"
                    }
                else:
                    error_text = await response.text()
                    return {
                        "success": False,
                        "error": f"API 返回错误 (状态码: {response.status}): {error_text}"
                    }

    def _format_balance_message(self, data: dict) -> dict:
        """
        格式化余额信息为可读的消息
        
        Args:
            data: API 返回的原始数据
            
        Returns:
            dict: 包含格式化消息的字典
        """
        try:
            # 解析 API 返回的数据
            user_data = data.get("data", {})
            
            # 获取余额信息（API 返回的是字符串，需要转换为浮点数）
            balance = float(user_data.get("balance", "0"))
            total_balance = float(user_data.get("totalBalance", "0"))
            charge_balance = float(user_data.get("chargeBalance", "0"))
            status = user_data.get("status", "unknown")
            
            # 格式化消息
            message = f"""SiliconFlow 账户余额

当前余额: {balance:.4f} 元
充值余额: {charge_balance:.4f} 元
总余额: {total_balance:.4f} 元

账户状态: {status}"""

            return {
                "success": True,
                "message": message,
                "raw_data": data
            }
            
        except Exception as e:
            logger.error(f"格式化余额信息时出错: {e}, 数据: {data}")
            return {
                "success": False,
                "error": f"解析余额数据失败: {str(e)}"
            }


@register_plugin
class SiliconFlowBalancePlugin(BasePlugin):
    """
    硅基流动余额查询插件主类
    """

    plugin_name: str = "siliconflow_balance_plugin"
    plugin_version: str = "1.0.0"
    plugin_author: str = "ikun两年半"
    plugin_description: str = "查询 SiliconFlow (硅基流动) API 账户余额"
    config_file_name: str = "config.toml"
    enable_plugin: bool = True
    dependencies: list[str] = []
    python_dependencies: list[str] = ["aiohttp"]

    config_schema: dict = {
        "api": {
            "api_key": ConfigField(
                type=str,
                default="",
                description="SiliconFlow API Key，从 https://cloud.siliconflow.cn/account/ak 获取"
            ),
        },
    }

    permission_nodes: list[PermissionNodeField] = [
        PermissionNodeField(
            node_name="query_balance",
            description="允许用户查询 SiliconFlow 余额"
        ),
    ]

    def get_plugin_components(self) -> list[tuple[ComponentInfo, type]]:
        """
        注册插件的所有功能组件
        """
        return [
            (BalanceCommand.get_plus_command_info(), BalanceCommand),
        ]
