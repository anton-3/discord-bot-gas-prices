from nextcord.ext import tasks, commands
from scraper import Scraper
from datetime import datetime

# cog that controls all bot functions
class Cog(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.checking = False # whether the bot is currently checking prices every check_interval min
        self.scrapers = [] # list of current stations getting prices checked
        self.update_ctx = None # the context to send price update messages in, is set in start

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Logged in as {self.client.user}')

    @commands.command()
    async def start(self, ctx):
        if self.checking == False:
            self.checking = True
            print('start')
            self.update_ctx = ctx
            self.scrape.start()
            await ctx.send('Price tracking started.')
        else:
            await ctx.send('Already running!')

    @commands.command()
    async def stop(self, ctx):
        if self.checking == True:
            self.checking = False
            print('stop')
            self.update_ctx = None
            self.scrape.stop()
            await ctx.send('Price tracking stopped.')
        else:
            await ctx.send('Already stopped!')

    @commands.command()
    async def list(self, ctx):
        response = ''
        for scraper in self.scrapers:
            response += f'{scraper.name}\n'

        if response == '':
            response = 'No gas stations added yet'
        await ctx.send(response)

    @commands.command()
    async def add(self, ctx, name=None, url=None):
        if name is None or url is None:
            await ctx.send('Missing argument(s)!')
            return
        if url in self.get_urls():
            await ctx.send('Already added!')
            return

        try:
            scraper = Scraper(name, url)
        except:
            await ctx.send('Invalid URL (or some kind of error happened idk)')
        else:
            self.scrapers.append(scraper)
            await ctx.send('Added')

    @commands.command()
    async def remove(self, ctx, url=None):
        if url is None:
            await ctx.send('URL needed!')
            return
        urls = self.get_urls()
        if url not in urls:
            await ctx.send('Invalid URL!')

        index = urls.index(url)
        self.scrapers.remove(index)
        await ctx.send('Removed')

    def get_urls(self):
        urls = []
        for scraper in self.scrapers:
            urls.append(scraper.url)
        return urls

    def get_time(self):
        return datetime.now().strftime('%H:%M:%S %m/%d/%y')

    @tasks.loop(minutes=5.0)
    async def scrape(self):
        if self.update_ctx is None or not self.client.is_ready():
            print('not ready yet')
            return

        for scraper in self.scrapers:
            old_prices = scraper.last_prices
            new_prices = scraper.get_prices()
            if old_prices == new_prices:
                print(f'Prices checked for {scraper.name} at {self.get_time()}, no changes')
            else:
                update = f'Price change for {scraper.name} at {self.get_time()}'
                print(update)
                print(new_prices)
                update += f'\nRegular: {new_prices["regular"]}'
                update += f'\nPremium: {new_prices["premium"]}'
                update += f'\nDiesel: {new_prices["diesel"]}'
                await self.update_ctx.send(update)

