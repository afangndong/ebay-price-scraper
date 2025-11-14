import discord
from discord import Webhook, AsyncWebhookAdapter
import aiohttp

async def send_discord_notification(webhook_url, product):
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(webhook_url, adapter=AsyncWebhookAdapter(session))
        
        embed = discord.Embed(
            title="🎯 Günstigstes Produkt gefunden!",
            color=0x00ff00
        )
        embed.add_field(name="Produkt", value=product['title'], inline=False)
        embed.add_field(name="Preis", value=f"€{product['price']}", inline=True)
        embed.add_field(name="Platform", value=product['platform'], inline=True)
        embed.add_field(name="Link", value=product['link'], inline=False)
        
        await webhook.send(embed=embed)
