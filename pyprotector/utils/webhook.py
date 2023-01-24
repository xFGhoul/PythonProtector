"""
	____          ____                __               __
   / __ \\ __  __ / __ \\ _____ ____   / /_ ___   _____ / /_
  / /_/ // / / // /_/ // ___// __ \\ / __// _ \\ / ___// __/
 / ____// /_/ // ____// /   / /_/ // /_ /  __// /__ / /_
/_/     \\__, //_/    /_/    \\____/ \\__/ \\___/ \\___/ \\__/
	   /____/

Made With ❤️ By Ghoul & Marci
"""
import io

from io import BytesIO
from PIL import Image, ImageGrab

from base64 import b64decode
from typing import Optional, List

from discord_webhook import DiscordEmbed, DiscordWebhook

from ..constants import EmbedConfig, LoggingInfo, UserInfo


class Webhook:
    def __init__(
            self,
            webhook_url: str,
            logs_path: Optional[str],
            screenshot: Optional[bool]) -> None:
        self.webhook_url: str = webhook_url
        self.logs_path: str = logs_path
        self.screenshot: bool = screenshot

    def TakeScreenshot(self) -> bytes:
        screenshot: Image = ImageGrab.grab(
            bbox=None,
            include_layered_windows=False,
            all_screens=True,
            xdisplay=None)

        screenshot_bytes_array: BytesIO = io.BytesIO()
        screenshot.save(screenshot_bytes_array, format="PNG")
        screenshot_bytes_array = screenshot_bytes_array.getvalue()
        return screenshot_bytes_array

    def DecryptLogs(self) -> bytes:
        with open(self.logs_path, "r") as logs_file:
            decrypted_logs_file = io.StringIO()
            lines: List[str] = logs_file.readlines()
            for line in lines:
                if not line.strip():
                    continue
                encrypted_message: str = line.split(" ")[4]
                encoded_message: bytes = b64decode(
                    encrypted_message.encode("latin1"))
                decrypted_message: str = LoggingInfo.CIPHER.decrypt(
                    encoded_message
                ).decode("utf-8")
                line: str = line.replace(
                    str(encrypted_message), str(decrypted_message))
                decrypted_logs_file.write(f"{line}\n")
            return decrypted_logs_file.getvalue()

    def send(self, content: str, module: str) -> None:
        webhook: DiscordWebhook = DiscordWebhook(
            self.webhook_url, rate_limit_retry=True
        )

        webhook.add_file(file=self.DecryptLogs(),
                         filename=f"{UserInfo.USERNAME}-[Security].log")

        embed: DiscordEmbed = DiscordEmbed(
            title=EmbedConfig.TITLE, color=EmbedConfig.COLOR
        )

        if self.screenshot:
            webhook.add_file(
                file=self.TakeScreenshot(),
                filename="screenshot.jpg")
            embed.set_image(url="attachment://screenshot.jpg")

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
