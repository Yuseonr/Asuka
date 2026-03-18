import discord
from aiohttp import web
from discord.ext import commands
from datetime import datetime, timezone


CRYPTO_LOGOS = {"BTC": "https://assets.coingecko.com/coins/images/1/large/bitcoin.png",}
BINANCE_LOGO = "https://upload.wikimedia.org/wikipedia/commons/5/57/Binance_Logo.png"

class SignalHandler(commands.Cog):
    """ Handle incoming signal for Asuka """

    def __init__(self, bot):
        self.bot = bot
        self.runner = None 
        self.site = None
    
    """ 
    How Asuka handle incoming signal 
    """
    async def handle_proses_signal(self, request : web.Request):
        try:

            data = await request.json()
            channel = self.bot.get_channel(self.bot.trading_channel_id)
            if channel:
                embed = self.createEmbed(self.parse(data))
                await channel.send(embed=embed)
                return web.Response(status=200)
            
        except Exception as e:
            return web.Response(status=500)

    """ 
    Asuka start web server and listen for incoming messages 
    """
    async def cog_load(self):
        app = web.Application()
        app.add_routes([web.post('/signal', self.handle_proses_signal)])
        self.runner = web.AppRunner(app)
        await self.runner.setup()
        self.site = web.TCPSite(self.runner, '127.0.0.1', 8080)
        await self.site.start()
        print("Started signal handler server on http://127.0.0.1:8080")

    """ 
    Asuka shutdown web server when cog is unloaded : no double server running 
    """
    async def cog_unload(self):
        if self.runner:
            await self.runner.cleanup()
            print("Shutdown signal handler server")

    #************************ Helper Function wok for parsing and shi ************************#
    
    def parse(self, data):
        pair = data.get("pair", "UNKNOWN")
        base_asset = next((pair[:-len(q)] for q in ["USDT", "BUSD", "USDC", "BTC", "ETH"] if pair.endswith(q)), pair)
        def parse_items(d):
            return {
                k.replace("Check", "").replace("_with_CalculatePoc", "").replace("Is", "").replace("_", " ").strip().title(): 
                "[TRUE]" in v 
                for k, v in d.items()
            }

        return {
            "pair": pair,
            "logo_url": CRYPTO_LOGOS.get(base_asset),
            "timeframe": data.get("timeframe", ""),
            "signal": data.get("signal", {}),
            "triggers": parse_items(data.get("triggers_met", {})),
            "context": parse_items(data.get("market_context", {}))
        }

    def createEmbed(self, parsed):
        sig = parsed["signal"]
        direction = sig.get("direction", "UNKNOWN").upper()
        is_bullish = direction == "BULLISH"
        color = discord.Color.green() if is_bullish else discord.Color.red()
        arrow = "🟢" if is_bullish else "🔴"
        
        ts = sig.get("timestamp")
        dt = datetime.fromtimestamp(ts / 1000, tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC") if ts else "Unknown"

        embed = discord.Embed(
            title=f"{parsed['pair']}  ·  {parsed['timeframe']}",
            description=f"### {arrow} **{direction}**\n`{sig.get('name', 'UNKNOWN')}`",
            color=color,
            timestamp=datetime.now(timezone.utc)
        )
        
        embed.set_author(name="Binance", icon_url=BINANCE_LOGO)
        
        if parsed.get("logo_url"):
            embed.set_thumbnail(url=parsed["logo_url"])

        def build_list(data_dict):
            if not data_dict:
                return "None"
            return "\n".join(f"{'🟢' if status else '🔴'} {k}" for k, status in data_dict.items())

        embed.add_field(name="Anchor", value=build_list(parsed["triggers"]), inline=True)
        embed.add_field(name="Context", value=build_list(parsed["context"]), inline=True)
        embed.set_footer(text=f"Signal fired at {dt}")
        
        return embed

async def setup(bot):
    await bot.add_cog(SignalHandler(bot))

""" 
PAYLOAD EXAMPLE HOLY SHIT I OVER COMPLICATE :

{
  "pair": "BTCUSDT",
  "timeframe": "15m",
  "signal": {
    "name": "BULLISH_TRAPPED_POC",
    "direction": "BULLISH",
    "timestamp": 1773742500000
  },
  "triggers_met": {
    "CheckCandleColor_GREEN": "[TRUE] Candle closed GREEN.",
    "CheckPocLocation_LOWER_with_CalculatePoc": "[TRUE] POC is in the LOWER wick."
  },
  "market_context": {
    "IsNewYorkSession": "[FALSE] Candle time (10:15 UTC) is outside the NY Session."
  },
  "candle": {
    "start_time": 1773742500000,
    "open": "73650.00",
    "high": "73812.70",
    "low": "73540.00",
    "close": "73718.40",
    "total_volume": "2684.311",
    "total_buy_volume": "1238.390",
    "total_sell_volume": "1445.921",
    "delta": "-207.531",
    "levels": {
      "73550.0": {
        "buy_volume": "4.877",
        "sell_volume": "99.450",
        "total_volume": "104.327",
        "delta": "-94.573"
      },
      "73600.0": {
        "buy_volume": "41.313",
        "sell_volume": "316.304",
        "total_volume": "357.617",
        "delta": "-274.991"
        },
      // ... rest of levls
    }
  }
}


"""