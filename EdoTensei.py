# standard python modules
from time import sleep
from random import uniform
import urllib.request
import os
from enum import Enum

#dependencies
import arsenic
from bs4 import BeautifulSoup
import qasync

# local modules
import DataStructures
import asyncio
import logging
import structlog
import utilities as util



class State(Enum):
    STOPPED = 0
    RUNNING = 1
    PAUSED = 2



class EdoTensei:
    def __init__(self, sigs):
        self.sigs = sigs
        self.service = arsenic.services.Chromedriver(binary='./drivers/chromedriver.exe')
        self.driver = arsenic.browsers.Chrome()
        self.browser = None
        self.ninjas = {}
        self.items = []
        self.state = State.STOPPED
        self.suppress_logs()


    def suppress_logs(self):
        # this suppresses the excessive amount of logs printed to console/stdout
        logger = logging.getLogger('arsenic')
        def logger_factory():
            return logger
        structlog.configure(logger_factory=logger_factory)
        logger.setLevel(logging.WARNING)


    @qasync.asyncSlot()
    async def run(self):
        self.state = State.RUNNING
        self.browser = await arsenic.start_session(self.service, self.driver)
        await self.login()
        await self.loop()



    @qasync.asyncSlot()
    async def login(self, account = None):
        await self.browser.get('https://www.ninjamanager.com/account/login')
        account = await util.get_account()
        
        username_field = await self.browser.wait_for_element(5, 'input[id=input-login]')
        await self.sleep_(2, 5)
        await username_field.send_keys(account['username'])

        password_field = await self.browser.get_element('input[id=input-password]')
        await self.sleep_(2, 5)
        await password_field.send_keys(account['password'])

        submit_button = await self.browser.get_element('input[id=login-nm-button]')
        await self.sleep_(2, 5)
        await submit_button.click()

        await self.browser.wait_for_element(5, 'div[class=top-menu__item-icon]')
        await self.sleep_(2, 5)



    @qasync.asyncSlot()
    async def loop(self):
        while True:
            await self.scrape()

            # await self.arena_actions()
            # await self.scrape()
            # await self.cooldown()

            # await self.world_actions()
            # await self.scrape()
            # await self.cooldown()
            break



    @qasync.asyncSlot()
    async def scrape(self):
        await self.gather_ninja_data()
        await self.sleep_(3, 7)
        # self.gather_equipment_data()
        # await self.sleep_(3, 7)
        # self.gather_forge_data()
        # await self.sleep_(3, 7)



    @qasync.asyncSlot()
    async def gather_ninja_data(self):
        await self.browser.get('https://www.ninjamanager.com/myteam/ninjas')

        raw_html = await self.browser.get_page_source()
        html = BeautifulSoup(raw_html, 'html.parser')
        ninja_urls = ['https://www.ninjamanager.com/myteam/ninja/' + nin['data-tnid'] for nin in html.find_all('div', class_='c-ninja-box__card')]

        for url in ninja_urls:
            await self.sleep_(2, 5)
            await self.browser.get(url)
            raw_html = await self.browser.get_page_source()
            html = BeautifulSoup(raw_html, 'html.parser')
            
            ninja_card = html.find('div', class_='m-ninja-details__column -c-squeezed').div
            img_url = 'https://www.ninjamanager.com' + ninja_card.find('div', class_='c-card__pic-inner').img['src'].replace('large', 'medium').replace('jpg', 'png')
            img_filename = img_url.split('/')[-1]
            name = img_filename[:-4].replace('-', ' ')
            lvl = int(ninja_card.find('span', class_='c-card__lvl-nr').string)
            try:
                exp = ninja_card.find('div', class_='c-exp__fill')['style']
                exp = int(exp[7:-2])
            except arsenic.errors.NoSuchElement:
                exp = 0

            bl_card = html.find('div', id='equipped-bloodline')
            try:
                bl_name = list(bl_card.find('div', class_='c-item__name').stripped_strings)[1]
                bl_lvl = bl_card.find('div', class_='c-item__name').em.string
                bl_lvl = int(bl_lvl[3:])
                try: 
                    bl_exp = bl_card.find('div', class_='c-exp__fill')['style']
                    bl_exp = int(bl_exp[7:-1])
                except arsenic.errors.NoSuchElement:
                    exp = 0
            except:
                bl_name = 'No Bloodline'
                bl_lvl = 0
                bl_exp = 0

            if img_filename not in os.listdir('images'):
                with open(f'images/{img_filename}', 'wb+') as file:
                        file.write(urllib.request.urlopen(img_url).read())

            if name not in self.ninjas:
                self.ninjas[name] = DataStructures.Ninja(name, f'images/{img_filename}', lvl*100+exp, bl_name, bl_lvl*100+bl_exp)
            else:
                self.ninjas[name].exp = lvl*100 + exp
                self.ninjas[name].bl_exp = bl_lvl*100 + exp

            self.sigs.ninja_signal.emit(self.ninjas[name])
            
        await self.sleep_(2, 5)
        


    # @qasync.asyncSlot()
    # async def gather_equipment_data(self):
    #     await self.browser.get('https://www.ninjamanager.com/myteam/equipment')
        
    #     raw_html = await self.browser.get_page_source()
    #     html = BeautifulSoup(raw_html, 'html.parser')
    #     self.items = [item_card.find('div', class_='c-item__name').string for item_card in html.find_all('div', class_='c-inventory-box')]


    # @qasync.asyncSlot()
    # async def gather_forge_data(self):
    #     await self.browser.get('https://www.ninjamanager.com/forge')
        
    #     raw_html = await self.browser.get_page_source()
    #     html = BeautifulSoup(raw_html, 'html.parser')
    #     with open('output.html', 'w+') as file:
    #         file.write(raw_html)



    # @qasync.asyncSlot()
    # async def arena_actions(self):
    #     await self.browser.get('https://www.ninjamanager.com/arena')
        
    #     raw_html = await self.browser.get_page_source()
    #     html = BeautifulSoup(raw_html, 'html.parser')
    #     with open('output.html', 'w+') as file:
    #         file.write(raw_html)



    # @qasync.asyncSlot()
    # async def world_actions(self):
    #     await self.browser.get('https://www.ninjamanager.com/forge')
        
    #     raw_html = await self.browser.get_page_source()
    #     html = BeautifulSoup(raw_html, 'html.parser')
    #     with open('output.html', 'w+') as file:
    #         file.write(raw_html)



    # @qasync.asyncSlot()
    # async def cooldown(self):
    #     # self.clock = 0
    #     # while self.clock < self.delay:
    #     #     sleep(1)
    #     #     self.clock += 1
    #     #     self.cooldown.emit(self.clock)
    #     # self.clock = 0
    #     pass



    @qasync.asyncSlot()
    async def sleep_(self, min: int, max: int):
        # sleeps for a random amount of time between min and max
        await asyncio.sleep(uniform(min, max))



    # @qasync.asyncSlot()
    # async def set_delay(self, new_delay):
    #     self.delay = new_delay


    async def shutdown(self):
        if self.browser:
            print('shutting down')
            self.state == State.STOPPED
            await self.browser.close()