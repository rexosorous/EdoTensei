# standard python modules
from random import uniform
import urllib.request
import os
from enum import Enum

#dependencies
import arsenic
from bs4 import BeautifulSoup
import qasync
from PyQt5.QtWidgets import QFrame
from PyQt5.QtGui import QPixmap

# local modules
import asyncio
import utilities as util
import gui.ninja_card_frame



class State(Enum):
    STOPPED = 0
    RUNNING = 1
    PAUSED = 2



class Ninja_Card(QFrame, gui.ninja_card_frame.Ui_Frame):
    def __init__(self, name: str, image_dir: str, exp: int, BL_name: str, BL_exp: int):
        # big note. changes here don't have to be 'updated' for it to reflect in the gui
        super().__init__()
        self.setupUi(self)
        self.name = name
        self.image_dir = image_dir
        self.ninja_exp_start = exp
        self.ninja_exp_curr = exp
        self.ninja_exp_gain = 0
        self.BL_name = BL_name
        self.BL_exp_start = BL_exp
        self.BL_exp_curr = BL_exp
        self.BL_exp_gain = 0

        self.init_labels()



    def init_labels(self):
        self.image.setPixmap(QPixmap(f'./{self.image_dir}'))
        self.ninja_name_label.setText(self.name)
        self.ninja_exp_curr_label.setText(f'Lv.{int(self.ninja_exp_curr/100)}@{self.ninja_exp_curr%100}%')
        self.ninja_exp_gain_label.setText(f'+{self.ninja_exp_gain}%')
        self.bl_name_label.setText(self.BL_name)
        self.bl_exp_curr_label.setText(f'Lv.{int(self.BL_exp_curr/100)}@{self.BL_exp_curr%100}%')
        self.bl_exp_gain_label.setText(f'+{self.BL_exp_gain}%')


    def update_exp(self, ninja: int, BL: int):
        self.ninja_exp_curr = ninja
        self.ninja_exp_gain = self.ninja_exp_curr - self.ninja_exp_start
        self.ninja_exp_curr_label.setText(f'Lv.{int(self.ninja_exp_curr/100)}@{self.ninja_exp_curr%100}%')
        self.ninja_exp_gain_label.setText(f'+{self.ninja_exp_gain}%')

        self.BL_exp_curr = ninja
        self.BL_exp_gain = self.BL_exp_curr - self.BL_exp_start
        self.bl_exp_curr_label.setText(f'Lv.{int(self.BL_exp_curr/100)}@{self.BL_exp_curr%100}%')
        self.bl_exp_gain_label.setText(f'+{self.BL_exp_gain}%')







class EdoTensei:
    def __init__(self, db, sigs, account: str):
        # arsenic stuff
        self.service = arsenic.services.Chromedriver(binary='./drivers/chromedriver.exe')
        self.driver = arsenic.browsers.Chrome()
        self.browser = None     # this is arsenic/webdriver and NOT gui

        self.db = db
        self.sigs = sigs
        self.ninjas = dict()
        self.state = State.STOPPED
        self.settings = util.load_settings(account)



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
        # prefer using cookies over login info
        if self.settings['login_cookie'] and self.settings['login_cookie'] != 'OR INSTEAD OF USERNAME+PASSWORD, YOU CAN PUT YOUR LOGIN COOKIE HERE':
            await self.browser.add_cookie(name='nm_al', value=self.settings['login_cookie'])
            await self.sleep_()
            await self.browser.get('https://www.ninjamanager.com/myteam')
            await self.browser.wait_for_element(5, 'div[class="top-menu__item-icon"]')
            await self.sleep_()
            return

        # if a cookie is not present in settings.json, use the username and password
        await self.browser.get('https://www.ninjamanager.com/account/login')
        
        username_field = await self.browser.wait_for_element(5, 'input[id="input-login"]')
        await self.sleep_()
        await username_field.send_keys(self.settings['username'])

        password_field = await self.browser.get_element('input[id="input-password"]')
        await self.sleep_()
        await password_field.send_keys(self.settings['password'])

        submit_button = await self.browser.get_element('input[id="login-nm-button"]')
        await self.sleep_()
        await submit_button.click()

        await self.browser.wait_for_element(5, 'div[class="top-menu__item-icon"]')
        await self.sleep_()



    @qasync.asyncSlot()
    async def loop(self):
        while True:
            self.sigs.update_loop_count.emit()
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
        await self.gather_gold_and_energy()
        await self.sleep_(1, 3)
        await self.gather_ninja_data()
        await self.sleep_()
        await self.gather_forge_data()
        await self.sleep_()
        await self.browser.get('https://www.ninjamanager.com')



    @qasync.asyncSlot()
    async def gather_gold_and_energy(self):
        raw_html = await self.browser.get_page_source()
        html = BeautifulSoup(raw_html, 'html.parser')
        gold = int(html.find('div', class_='js-header-gold').span.string.replace(',', ''))
        self.sigs.update_gold.emit(gold)



    @qasync.asyncSlot()
    async def gather_ninja_data(self):
        await self.browser.get('https://www.ninjamanager.com/myteam/ninjas')

        raw_html = await self.browser.get_page_source()
        html = BeautifulSoup(raw_html, 'html.parser')
        ninja_urls = ['https://www.ninjamanager.com/myteam/ninja/' + nin['data-tnid'] for nin in html.find_all('div', class_='c-ninja-box__card')]
        self.sleep_()

        for url in ninja_urls:
            await self.browser.get(url)
            await self.sleep_()
            raw_html = await self.browser.get_page_source()
            html = BeautifulSoup(raw_html, 'html.parser')
            
            ninja_card = html.find('div', class_='m-ninja-details__column -c-squeezed').div
            id_ = ninja_card['data-tnid']
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
                self.ninjas[id_] = Ninja_Card(name, f'images/{img_filename}', ninja_exp, BL_name, BL_exp)
                self.sigs.add_ninja_card.emit(self.ninjas[id_])
            else:
                self.ninjas[id_].update_exp(ninja=ninja_exp, BL=BL_exp)
            
        await self.sleep_()



    @qasync.asyncSlot()
    async def gather_forge_data(self):
        await self.browser.get('https://www.ninjamanager.com/forge')
        
        raw_html = await self.browser.get_page_source()
        html = BeautifulSoup(raw_html, 'html.parser')
        mat_area = html.find('div', id='material-list')
        materials = mat_area.find_all('div', class_='pc-forge-ingredient')

        for mat in materials:
            name = mat.find('div', class_='c-item__name').string
            quantity = int(mat.find('div', class_='c-item__amount').string)
            self.db.update_quantity(name, quantity)
            


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

            await self.send_arena_challenge(button)

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

            await self.send_arena_challenge(button)



    @qasync.asyncSlot()
    async def send_arena_challenge(self, button):
        await button.click()
        await self.sleep_(3, 5)

        try: # attempt to click the button that pops up if you've reached max challenges against an opponent
            max_challenge_button = await self.browser.get_element('.c-overlay-message__close')
            await max_challenge_button.click()
            await self.sleep_(3, 5)
        except arsenic.errors.NoSuchElement:
            # this is expected behavior
            # check for win or loss
            sent_challenges_area = await self.browser.get_element('#challenges-outgoing')
            latest_challenge = await sent_challenges_area.get_element('div')
            class_attributes = await latest_challenge.get_attribute('class')
            is_win = True if '-result-win' in class_attributes else False   # the other is -result-loss
            self.sigs.update_arena_stats.emit(is_win)



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
        win_text = html.find('div', class_='pm-battle-matchup__title').string
        is_win = True if win_text == 'Victory' else False  # the other is Defeat
        self.sigs.update_world_stats(is_win)
        for drop in html.find_all('div', class_='pm-battle-treasures__drop'):
            # it is not possible to get item id this way
            name = drop.find('div', class_='c-item__name').string
            success = True if '-status-done' in drop['class'] else False      # -status-failed or -status-done
            if success:
                self.sigs.update_items_gained.emit(name)

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