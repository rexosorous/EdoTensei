# standard python modules
from random import uniform
import urllib.request
from os import listdir
from enum import Enum
from asyncio import sleep

# dependencies
import arsenic
from bs4 import BeautifulSoup
import qasync
from PyQt5.QtWidgets import QFrame
from PyQt5.QtGui import QPixmap

# local modules
import gui.ninja_card_frame



class State(Enum):
    STOPPED = 0
    RUNNING = 1
    PAUSED = 2



class NinjaCard(QFrame, gui.ninja_card_frame.Ui_Frame):
    '''
    GUI cards used to represent ninja info

    Note:
        all instances of exp in args and attr are % values that have lvl included
        EX: lvl 5 @ 30% == 530% == 530

    Args:
        name (str)
        image_dir (str)
        exp (int)
        BL_name (str)
        BL_exp (int)

    Attributes:
        name (str)
        image_dir (str)
        ninja_exp_start (int)
        ninja_exp_curr (int)
        ninja_exp_gain (int)
        BL_name (str)
        BL_exp_start (int)
        BL_exp_curr (int)
        BL_exp_gain (int)
    '''
    def __init__(self, name: str, image_dir: str, exp: int, BL_name: str, BL_exp: int):
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

        self.BL_exp_curr = BL
        self.BL_exp_gain = self.BL_exp_curr - self.BL_exp_start
        self.bl_exp_curr_label.setText(f'Lv.{int(self.BL_exp_curr/100)}@{self.BL_exp_curr%100}%')
        self.bl_exp_gain_label.setText(f'+{self.BL_exp_gain}%')







class EdoTensei:
    '''
    The webdriver bot. An instance of this should be created for each account.

    Notes:
        Only uses chromedriver
        Ideally, I would have made this work independently of PyQt and the rest of the app,
        but the integration is needed because of qasync and the use of signals

    Args:
        db (DBHandler)
        sigs (Signals)

    Attributes:
        service (arsenic.services.Chromedriver): required by arsenic, but should not be interacted with directly
        driver (arsenic.browser.Chrome): required by arsenic, but should not be interacted with directly
        browser (arsenic.session): this is what i should use to interact with the browser/webdriver
        db (DBHandler)
        sigs (Signals)
        ninjas (dict): ninja cards
        state (Enum): the current state the bot is in
        settings (dict)
    '''
    def __init__(self, db, sigs):
        # arsenic stuff
        self.service = arsenic.services.Chromedriver(binary='./drivers/chromedriver.exe')
        self.driver = arsenic.browsers.Chrome()
        self.browser = None     # this is arsenic/webdriver and NOT gui

        self.db = db
        self.sigs = sigs
        self.ninjas = dict()
        self.state = State.STOPPED
        self.settings = dict()



    @qasync.asyncSlot(dict)
    async def update_settings(self, settings: dict):
        self.settings = settings



    @qasync.asyncSlot()
    async def run(self):
        '''
        Starts the bot's main logic
        '''
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
    async def login(self):
        '''
        Logs in. Prefers using cookies if provided in settings, but will also work with username and password
        '''
        if self.settings['login_cookie'] and self.settings['login_cookie'] != 'OR INSTEAD OF USERNAME+PASSWORD, YOU CAN PUT YOUR LOGIN COOKIE HERE':
            # prefer using cookies over login info
            await self.browser.add_cookie(name='nm_al', value=self.settings['login_cookie'])
        else:
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

        await self.sleep_()
        await self.browser.get('https://www.ninjamanager.com/')
        team_name_area = await self.browser.wait_for_element(5, '.header-team__details-name')
        team_name_element = await team_name_area.get_element('span')
        team_name = await team_name_element.get_text()
        self.sigs.set_team_label.emit(team_name)
        await self.sleep_()



    @qasync.asyncSlot()
    async def loop(self):
        while True:
            self.sigs.update_loop_count.emit()
            await self.scrape()
            await self.arena_actions()
            await self.world_actions()



    @qasync.asyncSlot()
    async def scrape(self):
        await self.gather_gold()
        await self.sleep_(1, 3)
        await self.gather_ninja_data()
        await self.sleep_()
        await self.gather_forge_data()
        await self.sleep_()
        await self.browser.get('https://www.ninjamanager.com')
        await self.sleep_()



    @qasync.asyncSlot()
    async def gather_gold(self):
        raw_html = await self.browser.get_page_source()
        html = BeautifulSoup(raw_html, 'html.parser')
        gold = int(html.find('div', class_='js-header-gold').span.string.replace(',', ''))
        self.sigs.update_gold.emit(gold)



    @qasync.asyncSlot()
    async def gather_energy(self) -> dict[str, int]:
        raw_html = await self.browser.get_page_source()
        html = BeautifulSoup(raw_html, 'html.parser')
        arena_bar = html.find('div', class_='js-header-energy-arena') # header-team__bar header-team__bar-ae  c-bar -type-ae  js-header-energy-arena
        arena_energy = int(arena_bar.find('span', class_='c-bar__text-cur').string)
        world_bar = html.find('div', class_='js-header-energy-world')
        world_energy = int(world_bar.find('span', class_='c-bar__text-cur').string)

        return {'arena': arena_energy, 'world': world_energy}



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
            exp_area = ninja_card.find('div', class_='c-exp__fill')
            if exp_area:
                exp = int(exp_area['style'][7:-2])
            else:
                exp = 0
            ninja_exp = lvl*100 + exp

            BL_card = html.find('div', id='equipped-bloodline') # summons don't have this
            if BL_card:
                BL_stripped_strings = list(BL_card.find('div', class_='c-item__name').stripped_strings)
                if len(BL_stripped_strings) > 1:
                    BL_name = BL_stripped_strings[1]
                    BL_lvl = BL_card.find('div', class_='c-item__name').em.string
                    BL_lvl = int(BL_lvl[3:])
                    BL_exp_area = BL_card.find('div', class_='c-exp__fill')
                    if BL_exp_area:
                        BL_exp = int(BL_exp_area['style'][7:-1])
                    else:
                        BL_exp = 0
                    BL_exp = BL_lvl*100 + BL_exp
                else:
                    BL_name = 'No Bloodline'
                    BL_exp = 0
            else:
                BL_name = 'No Bloodline'
                BL_exp = 0


            if img_filename not in listdir('images'):
                with open(f'images/{img_filename}', 'wb+') as file:
                        file.write(urllib.request.urlopen(img_url).read())

            if id_ not in self.ninjas:
                self.ninjas[id_] = NinjaCard(name, f'images/{img_filename}', ninja_exp, BL_name, BL_exp)
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


        equipment_area = html.find('div', id='equipment-list')
        equipment = equipment_area.find_all('div', class_='pc-forge-ingredient')
        for equip in equipment:
            name = equip.find('div', class_='c-item__name').string
            self.db.update_quantity(name, 1)    # if you have multiple, it'll show up as multiple entires


        bloodlines_area = html.find('div', id='bloodlines-list')
        bloodlines = bloodlines_area.find_all('div', class_='pc-forge-ingredient')
        for bl in bloodlines:
            name_area = bl.find('div', class_='c-item__name')
            if name_area.find('em'):
                stripped_strings = list(name_area.stripped_strings)
                name = stripped_strings[1].replace('"', '')
                lvl = int(stripped_strings[0][stripped_strings[0].find('Lv.')+3:])
            else:
                name = name_area.string
                lvl = 0
            self.db.update_quantity(name, 1)


        ninjas_area = html.find('div', id='ninjas-list')
        ninjas = ninjas_area.find_all('div', class_='pc-forge-ingredient')
        for nin in ninjas:
            name = nin.find('div', class_='c-card__name').string
            if lvl := nin.find('span', class_='c-card__lvl-nr'):
                lvl = int(lvl.string)
            else:
                lvl = 0
            self.db.update_quantity(name, 1)

        self.sigs.update_item_quantities.emit()



    @qasync.asyncSlot()
    async def arena_actions(self):
        '''
        note: does not scan the sidebar challenges (the incoming and outgoing sections)
              because you cannot get a team's rating from them without scraping that team's link
              look for commits before Aug 21, 2021 to reference old logic for challenging sidebar teams
        '''
        # first check if we have enough energy to even do anything
        energy = await self.gather_energy()
        if energy['arena'] < 5:
            return

        await self.browser.get('https://www.ninjamanager.com/arena')
        await self.sleep_()

        our_rating_ele_outer = await self.browser.get_element('.header-team__details-rating')
        our_rating_ele = await our_rating_ele_outer.get_element('span')
        our_rating_str = await our_rating_ele.get_text()
        our_rating = int(our_rating_str.replace(',', ''))

        # instead of challenging as we traverse, we will collect the team's rating, rematch (bool), and button to make it easier to handle
        # doing it this way will allow us to sort all the challenges in one master list and order it however we like
        teams = list()      # list[dict[int, bool, arsenic.session.Element]]

        main_challenges = await self.browser.get_elements('.c-arena-box')
        for challenge in main_challenges:
            button = await challenge.get_element('.c-arena-box__challenge')
            rating_ele = await challenge.get_element('.c-arena-box__rating')
            rating_str = await rating_ele.get_text()
            rating = int(rating_str.replace(',', ''))
            rematch_ele = await button.get_element('span')
            rematch_str = await rematch_ele.get_text()
            rematch = False if rematch_str.lower() == 'fight' else True

            teams.append({
                'rating': rating,
                'rematch': rematch,
                'button': button
            })

        # decide which teams to battle
        if self.settings['arena_wins_only']:
            teams = [ele for ele in teams if ele['rating'] < our_rating]

        if self.settings['arena_rematches_only']:
            teams = [ele for ele in teams if ele['rematch']]

        # this sorts by rematches first and then by their rating
        # so no matter what the settings are, the bot will still try to:
        #   maximize energy efficiency (does rematches first)
        #   win as often as possible (challenges lower rated teams first)
        teams.sort(key=lambda data: (-data['rematch'], data['rating']))

        await self.send_arena_challenges([ele['button'] for ele in teams])

        await self.scrape()
        await self.cooldown()



    @qasync.asyncSlot()
    async def send_arena_challenges(self, buttons: list[arsenic.session.Element]):
        for btn in buttons:
            await btn.click()
            await self.sleep_(3, 5)

            # check to see if we ran out of energy or meached max challenges
            popup = await self.browser.get_elements('.c-overlay-message__close')    # get_elements does NOT raise a NoSuchElement exception if none are found
            if popup:
                button = popup[0]
                message_element = await self.browser.get_element('.c-overlay-message__text')
                message = await message_element.get_text()
                await button.click()
                await self.sleep_(3, 5)
                if message == 'Not enough energy!':
                    return

            # check for win or loss
            sent_challenges_area = await self.browser.get_element('#challenges-outgoing')
            latest_challenge = await sent_challenges_area.get_element('div')
            result_div = await latest_challenge.get_element('.m-sb-challenges__rating')
            class_attributes = await result_div.get_attribute('class')
            is_win = True if '-result-win' in class_attributes else False   # the other is -result-loss
            self.sigs.update_arena_stats.emit(is_win)



    @qasync.asyncSlot()
    async def world_actions(self):
        # INCOMPELTE!!
        # still need to implement the behavior modes!

        # first check if we have enough energy to even do anything
        energy = await self.gather_energy()
        if energy['world'] < 7:    # i think the most expensive mission is 7 energy
            return

        if 'http' in self.settings['mission_url']:
            await self.do_world_mission(self.settings['mission_url'])
        else:
            await self.do_world_mission(f'https://www.ninjamanager.com/world/area/{self.settings["mission_url"]}')

        await self.scrape()
        await self.cooldown()



    @qasync.asyncSlot()
    async def do_world_mission(self, url):
        await self.browser.get(url)
        await self.sleep_()

        mission_button = await self.browser.wait_for_element(5, f'div[data-url="{url[url.find(".com/")+4:]}"]')
        await self.sleep_(1, 3)
        await mission_button.click()
        await self.sleep_()

        # div[class="pm-battle-buttons__skip  c-button -color-themed-yes -c-icon -width-auto  js-battle-skip"]
        skip_button = await self.browser.wait_for_element(5, '.pm-battle-buttons__skip')
        await self.sleep_(1, 3)
        await skip_button.click()
        await self.sleep_()

        raw_html = await self.browser.get_page_source()
        html = BeautifulSoup(raw_html, 'html.parser')
        win_text = html.find('div', class_='pm-battle-matchup__title').string
        is_win = True if win_text == 'Victory' else False  # the other is Defeat
        self.sigs.update_world_stats.emit(is_win)
        for drop in html.find_all('div', class_='pm-battle-treasures__drop'):
            # it is not possible to get item id this way
            name = drop.find('div', class_='c-item__name').string
            success = True if '-status-done' in drop['class'] else False      # -status-failed or -status-done
            if success:
                self.sigs.update_items_gained.emit(name)

        finish_button = await self.browser.wait_for_element(5, f'.pm-battle-buttons__finish')
        await self.sleep_(1, 3)
        await finish_button.click()



    @qasync.asyncSlot()
    async def cooldown(self):
        await self.sleep_(self.settings['sleep_lower']*60, self.settings['sleep_upper']*60)



    @qasync.asyncSlot()
    async def sleep_(self, min: int = 5, max: int = 8):
        # sleeps for a random amount of time between min and max
        await sleep(uniform(min, max))



    @qasync.asyncSlot()
    async def shutdown(self):
        if self.state != State.STOPPED:
            print('shutting down')
            self.state = State.STOPPED
            await arsenic.stop_session(self.browser)