"""
    ____          ____                __               __
   / __ \\ __  __ / __ \\ _____ ____   / /_ ___   _____ / /_
  / /_/ // / / // /_/ // ___// __ \\ / __// _ \\ / ___// __/
 / ____// /_/ // ____// /   / /_/ // /_ /  __// /__ / /_
/_/     \\__, //_/    /_/    \\____/ \\__/ \\___/ \\___/ \\__/
       /____/

Made With ❤️ By Ghoul & Marci
"""

from discord_webhook import DiscordEmbed, DiscordWebhook

from ..constants import EmbedConfig, UserInfo


class Webhook:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def send(self, content: str, module: str):
        webhook = DiscordWebhook(self.webhook_url)

        embed = DiscordEmbed(title=EmbedConfig.TITLE, color=EmbedConfig.COLOR)

        embed.add_embed_field(
            name="User",
            value=UserInfo.USERNAME,
            inline=True)
        embed.add_embed_field(name="IP", value=UserInfo.IP, inline=True)
        embed.add_embed_field(name="Module", value=module, inline=True)

        embed.set_timestamp()
        embed.set_description(content)

        embed.set_thumbnail(url=EmbedConfig.ICON)
        embed.set_footer(
            text=f"PythonProtector | {EmbedConfig.VERSION}",
            icon_url=EmbedConfig.ICON)

        webhook.add_embed(embed)

        webhook.execute()
