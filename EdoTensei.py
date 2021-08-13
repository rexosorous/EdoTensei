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
        self.browser = None     # this is arsenic/webdriver and NOT gui
        self.ninjas = {}
        self.items = []     # items are NOT mats!!!
        self.state = State.STOPPED
        self.cooldown_time = [900, 1200]     # in seconds



    @qasync.asyncSlot()
    async def run(self):
        self.state = State.RUNNING
        self.browser = await arsenic.start_session(self.service, self.driver)
        await self.set_cookies()
        await self.login()
        await self.loop()



    @qasync.asyncSlot()
    async def set_cookies(self):
        await self.browser.get('https://www.ninjamanager.com')
        await self.browser.add_cookie(name='Arena_Settings', value='%7B%22SkipBattleAnim%22%3A%221%22%7D')
        await self.sleep_()



    @qasync.asyncSlot()
    async def login(self, account = None):
        await self.browser.get('https://www.ninjamanager.com/account/login')
        account = await util.get_account()
        
        username_field = await self.browser.wait_for_element(5, 'input[id="input-login"]')
        await self.sleep_()
        await username_field.send_keys(account['username'])

        password_field = await self.browser.get_element('input[id="input-password"]')
        await self.sleep_()
        await password_field.send_keys(account['password'])

        submit_button = await self.browser.get_element('input[id="login-nm-button"]')
        await self.sleep_()
        await submit_button.click()

        await self.browser.wait_for_element(5, 'div[class="top-menu__item-icon"]')
        await self.sleep_()



    @qasync.asyncSlot()
    async def loop(self):
        while True:
            await self.scrape()

            await self.arena_actions()
            await self.scrape()
            await self.cooldown()

            await self.world_actions()
            await self.scrape()
            await self.cooldown()



    @qasync.asyncSlot()
    async def scrape(self):
        await self.gather_gold_and_energy()
        await self.sleep_(1, 3)
        await self.gather_ninja_data()
        await self.sleep_()
        # await self.gather_equipment_data()
        # await self.sleep_()
        await self.gather_forge_data()
        await self.sleep_()
        await self.browser.get('https://www.ninjamanager.com')



    @qasync.asyncSlot()
    async def gather_gold_and_energy(self):
        raw_html = await self.browser.get_page_source()
        html = BeautifulSoup(raw_html, 'html.parser')
        gold = int(html.find('div', class_='js-header-gold').span.string.replace(',', ''))
        # send pyqtsignal to update gold in the gui
        # we probably don't need to save the energy in a global variable. we can probably just pass it on to the functions that need them



    @qasync.asyncSlot()
    async def gather_ninja_data(self):
        await self.browser.get('https://www.ninjamanager.com/myteam/ninjas')

        raw_html = await self.browser.get_page_source()
        html = BeautifulSoup(raw_html, 'html.parser')
        ninja_urls = ['https://www.ninjamanager.com/myteam/ninja/' + nin['data-tnid'] for nin in html.find_all('div', class_='c-ninja-box__card')]

        for url in ninja_urls:
            await self.sleep_()
            await self.browser.get(url)
            raw_html = await self.browser.get_page_source()
            html = BeautifulSoup(raw_html, 'html.parser')
            
            ninja_card = html.find('div', class_='m-ninja-details__column -c-squeezed').div
            id_ = ninja_card.find('div', class_='c-card -size-l  m-ninja-details__card')['data-tnid']
            img_url = 'https://www.ninjamanager.com' + ninja_card.find('div', class_='c-card__pic-inner').img['src'].replace('large', 'medium').replace('jpg', 'png')
            img_filename = img_url.split('/')[-1]
            name = img_filename[:-4].replace('-', ' ')
            lvl = int(ninja_card.find('span', class_='c-card__lvl-nr').string)
            try:
                exp = ninja_card.find('div', class_='c-exp__fill')['style']
                exp = int(exp[7:-2])
            except arsenic.errors.NoSuchElement:
                exp = 0
            ninja_exp = lvl*100 + exp

            BL_card = html.find('div', id='equipped-bloodline')
            try:
                BL_name = list(BL_card.find('div', class_='c-item__name').stripped_strings)[1]
                BL_lvl = BL_card.find('div', class_='c-item__name').em.string
                BL_lvl = int(BL_lvl[3:])
                try: 
                    BL_exp = BL_card.find('div', class_='c-exp__fill')['style']
                    BL_exp = int(BL_exp[7:-1])
                except arsenic.errors.NoSuchElement:
                    exp = 0
                BL_exp = BL_lvl*100 + BL_exp
            except:
                BL_name = 'No Bloodline'
                BL_exp = 0
            

            if img_filename not in os.listdir('images'):
                with open(f'images/{img_filename}', 'wb+') as file:
                        file.write(urllib.request.urlopen(img_url).read())

            if id_ not in self.ninjas:
                self.ninjas[id_] = DataStructures.Ninja(name, f'images/{img_filename}', ninja_exp, BL_name, BL_exp)
            else:
                self.ninjas[id_].update_exp(ninja=ninja_exp, BL=BL_exp)

            self.sigs.ninja_signal.emit(self.ninjas[name])
            
        await self.sleep_()
        


    @qasync.asyncSlot()
    async def gather_equipment_data(self):
        # this isn't for figuring out if you have the right equipment to use as a mat for forge,
        # this is to figure out if you obtained a dropped LW
        # perhaps this is redundant if we can figure out how to analyze the world win screen
        await self.browser.get('https://www.ninjamanager.com/myteam/equipment')
        
        raw_html = await self.browser.get_page_source()
        html = BeautifulSoup(raw_html, 'html.parser')
        self.items = [item_card.find('div', class_='c-item__name').string for item_card in html.find_all('div', class_='c-inventory-box')]



    @qasync.asyncSlot()
    async def gather_forge_data(self):
        # only a rough skeleton right now. does not interace with the DB yet as i have not designed that
        await self.browser.get('https://www.ninjamanager.com/forge')
        
        raw_html = await self.browser.get_page_source()
        html = BeautifulSoup(raw_html, 'html.parser')
        mat_area = html.find('div', id='material-list')
        materials = mat_area.find_all('div', class_='pc-forge-ingredient')

        for mat in materials:
            print(f"{mat.find('div', class_='c-item__amount').string}x {mat.find('div', class_='c-item__name').string}")



    @qasync.asyncSlot()
    async def arena_actions(self):
        await self.browser.get('https://www.ninjamanager.com/arena')
        await self.sleep_()

        our_rating_ele_outer = await self.browser.get_element('.header-team__details-rating')
        our_rating_ele = await our_rating_ele_outer.get_element('span')
        our_rating_str = await our_rating_ele.get_text()
        our_rating = int(our_rating_str.replace(',', ''))
        
        main_challenges = await self.browser.get_elements('.c-arena-box')
        for challenge in main_challenges:
            button = await challenge.get_element('.c-arena-box__challenge')
            rating_ele = await challenge.get_element('.c-arena-box__rating')
            rating_str = await rating_ele.get_text()
            rating = int(rating_str.replace(',', ''))
            rematch_ele = await button.get_element('span')
            rematch_str = await rematch_ele.get_text()
            rematch = False if rematch_str.lower() == 'fight' else True

            # if rating > our_rating and self.arena_wins_only:
                # continue
            
            if not rematch: # and self.arena_rematches_only:
                continue

            await button.click()
            await self.sleep_(3, 5)

            try:
                max_challenge_button = await self.browser.get_element('.c-overlay-message__close')
                await max_challenge_button.click()
                await self.sleep_(3, 5)
            except arsenic.errors.NoSuchElement:
                pass

        sidebar_challenges = await self.browser.get_elements('.m-sb-challenges__row')        
        for challenge in sidebar_challenges:
            # this is smart enough to 'know' when icons change
            button = await challenge.get_element('.m-sb-challenges__challenge')
            rating_ele = await challenge.get_element('.m-sb-challenges__rating')
            rating_str = await rating_ele.get_attribute('class')
            rating = True if '-result-win' in rating_str else False     # the other is -result-loss
            rematch_str = await button.get_attribute('class')
            rematch = True if '-icon-challenge-return' in rematch_str else False

            # if not rating and self.arena_wins_only:
            #     continue

            if not rematch: # and self.arena_rematches_only:
                continue

            await button.click()
            await self.sleep_(3, 5)

            try:
                max_challenge_button = await self.browser.get_element('.c-overlay-message__close')
                await max_challenge_button.click()
                await self.sleep_(3, 5)
            except arsenic.errors.NoSuchElement:
                pass



    @qasync.asyncSlot()
    async def world_actions(self):
        await self.do_world_mission('https://www.ninjamanager.com/world/area/the-sealed-world/mission/2')



    @qasync.asyncSlot()
    async def do_world_mission(self, url):
        await self.browser.get(url)
        
        mission_button = await self.browser.wait_for_element(5, f'div[data-url="{url[url.find(".com/")+4:]}"]')
        await self.sleep_(1, 3)
        await mission_button.click()
        await self.sleep_()
        
        skip_button = await self.browser.wait_for_element(5, 'div[class="pm-battle-buttons__skip  c-button -color-themed-yes -c-icon -width-auto  js-battle-skip"]')
        await self.sleep_(1, 3)
        await skip_button.click()
        await self.sleep_()

        raw_html = await self.browser.get_page_source()
        html = BeautifulSoup(raw_html, 'html.parser')
        for drop in html.find_all('div', class_='pm-battle-treasures__drop'):
            # it is not possible to get item id this way
            name = drop.find('div', class_='c-item__name').string
            success = True if '-status-done' in drop['class'] else False      # -status-failed or -status-done

        finish_button = await self.browser.wait_for_element(5, f'div[class=pm-battle-buttons__finish]')
        await self.sleep_(1, 3)
        await finish_button.click()



    @qasync.asyncSlot()
    async def cooldown(self):
        await self.sleep_(self.cooldown_time[0], self.cooldown_time[1])



    @qasync.asyncSlot()
    async def sleep_(self, min: int = 5, max: int = 8):
        # sleeps for a random amount of time between min and max
        await asyncio.sleep(uniform(min, max))


    @qasync.asyncSlot()
    async def shutdown(self):
        if self.state != State.STOPPED:
            print('shutting down')
            self.state = State.STOPPED
            await arsenic.stop_session(self.browser)