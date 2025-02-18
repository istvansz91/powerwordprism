from bs4 import BeautifulSoup
from pprint import pprint
from urllib import request
import json
import time

RESOURCES_PATH_LINKS = 'Resources/Corpora/EU/Links/'
RESOURCES_PATH_POSTS = 'Resources/Corpora/EU/Posts/'
RESOURCES_PATH_SCORES = 'Resources/Corpora/EU/Scores/'
RESOURCES_PATH_SCORES_BY_DATE = 'Resources/Corpora/EU/Scores/ByDate/'
RESOURCES_PATH_ONTOLOGY = 'Resources/Ontology/'
RESOURCES_PATH_CLASSIFICATION = 'Resources/Corpora/EU/Classification/'
RESOURCES_PATH_ANNOTATIONS = 'Resources/Manual annotation/'


class WowClassesResources:
    def __init__(self):
        pass

    # links
    WOW_FORUM_ROOT_URL_EU = 'http://eu.battle.net'
    WOW_FORUM_ROOT_URL_US = 'http://us.battle.net'
    WOW_FORUM_MID_URL = '/forums/en/wow/'
    URL_PAGE_ATTRIBUTE = "?page="

    # WoW classes
    WOW_C_DEATH_KNIGHT = 'Death Knight'
    WOW_C_DEMON_HUNTER = 'Demon Hunter'
    WOW_C_DRUID = 'Druid'
    WOW_C_HUNTER = 'Hunter'
    WOW_C_MAGE = 'Mage'
    WOW_C_MONK = 'Monk'
    WOW_C_PALADIN = 'Paladin'
    WOW_C_PRIEST = 'Priest'
    WOW_C_ROGUE = 'Rogue'
    WOW_C_SHAMAN = 'Shaman'
    WOW_C_WARLOCK = 'Warlock'
    WOW_C_WARRIOR = 'Warrior'

    WOW_CLASS_LIST_EU = {WOW_C_DEATH_KNIGHT: "874789/",
                         WOW_C_DEMON_HUNTER: "19369494/",
                         WOW_C_DRUID: "874790/",
                         WOW_C_HUNTER: "874791/",
                         WOW_C_MAGE: "874792/",
                         WOW_C_MONK: "6038099/",
                         WOW_C_PALADIN: "874793/",
                         WOW_C_PRIEST: "874794/",
                         WOW_C_ROGUE: "874795/",
                         WOW_C_SHAMAN: "874796/",
                         WOW_C_WARLOCK: "874929/",
                         WOW_C_WARRIOR: "874930/"}

    WOW_CLASS_LIST_US = {WOW_C_DEATH_KNIGHT: "1012662/",
                         WOW_C_DEMON_HUNTER: "22813967/",
                         WOW_C_DRUID: "1012663/",
                         WOW_C_HUNTER: "1012664/",
                         WOW_C_MAGE: "1012760/",
                         WOW_C_MONK: "7379141/",
                         WOW_C_PALADIN: "1012668/",
                         WOW_C_PRIEST: "1012666/",
                         WOW_C_ROGUE: "1012667/",
                         WOW_C_SHAMAN: "1012669/",
                         WOW_C_WARLOCK: "1012670/",
                         WOW_C_WARRIOR: "1012759/"}

    class GameType:
        PVP_CRITERIA = ['pvp', '2v2', '3v3', '5v5', 'cc',
                        'AB', 'AV', 'BET', 'DR', 'Efc', 'EotS', 'FC', 'FR', 'FRR', 'IoC',
                        'LH', 'LM', 'Mid', 'MT', 'SW', 'Stags', 'SoTA', 'SSM', 'ST', 'TB',
                        'ToK', 'TP', 'TP', 'WG', 'WSG', 'WV', 'WW',
                        'arena', 'bg', 'rbg', 'warsong', 'flag', 'capture', 'fr', 'fc', 'ftw',
                        'duel', 'skirmish', 'lom', 'arathi', 'los', 'focus', 'nuke', 'poly',
                        'sheep', 'alterac', '2s', '3s', '5s', 'rated', 'rating', 'battleground',
                        'battle ground', 'nagrand', 'blade\'s edge', 'blades edge',
                        'tiger\'s peak', 'tigers peak', 'ashamane\'s fall', 'ashamanes fall',
                        'black rook hold', 'tol\'viron', 'tolviron', 'dalaran', 'ruins',
                        'championship', 'deepwind gorge', 'kotmogu', 'silvershard',
                        'twin peaks', 'gilneas', 'strand', 'ashran', 'gladiator', 'mmr',
                        'honor', 'prestige']
        PVE_CRITERIA = ['pve', 'heroic', 'mythic', 'mythic+', 'm+', 'scenario', 'boss', 'mobs',
                        'time-walk', 'time-walking'
                                     'RFC', 'VC', 'DM', 'WC', 'SFK', 'Stocks', 'Stockade', 'BFD', 'Gnomer',
                        'SH', 'SM', 'RFK', 'Mara', 'Ulda', 'DM', 'Warpwood', 'DM', 'East', 'Scholo',
                        'RFD', 'Strat', 'ZF', 'BRD', 'ST', 'AH', 'LBRS', 'UBRS', 'AQ', 'RAQ', 'MC',
                        'BWL', 'AQ40', 'TAQ', 'Ramps', 'BF', 'SP', 'UB', 'MT', 'AC', 'AS', 'Seth',
                        'Seth', 'Halls', 'SV', 'SH', 'Shatt', 'Halls', 'SL', 'Slabs', 'OH',
                        'DH', 'DK', 'Durn', 'Mech', 'Bot', 'Arc', 'BM', 'MgT', 'Terrace', 'MrT',
                        'HoR', 'Naxx', 'OS', 'Sarth', 'Vault', 'VoA', 'Maly',
                        'EoE', 'Uld', 'TC', 'ToC', 'TotC', 'ToGC', '(Heroic)', 'Ony',
                        'RS', 'Hal', 'ICC', 'UK', 'UTK', 'Nexus', 'Nex', 'AZN', 'AN', 'ANK',
                        'OLD', 'AKO', 'OK', 'DTK', 'VH', 'GD', 'HOS', 'Occ', 'HOL', 'UP', 'Culling',
                        'COS', 'Champ', 'ToC', 'FoS', 'PoS', 'TotT', 'BRC', 'SC', 'VP', 'LCoT', 'GB',
                        'HoO', 'H-DM', 'H-VC', 'H-SFK', 'ZA', 'ZG', 'ET', 'WoE', 'HoT', 'BH',
                        'BoT', 'TFW', 'BWD', 'FL', 'DS', 'SH', 'Scholo', 'TJS', 'SB', 'MP',
                        'SPM', 'GSS', 'SNT', 'MV', 'HoF', 'TES', 'ToT', 'SoO', 'BSM', 'Auch', 'SR',
                        'GD', 'SBG', 'EB', 'UBRS', 'HM', 'BF', 'BRF', 'HC', 'HFC', 'arc', 'VoW', 'MoS',
                        'CoS', 'EN', 'BRH', 'RtK', 'arc', 'ToV', 'VH', 'CoN', 'EoZ', 'NL', 'HoV', 'GR',
                        'DHT', 'DT']


class WowTopic:
    def __init__(self, topic_link, topic_title, number_of_posts):
        self.topic_link = topic_link
        self.topic_title = topic_title
        self.number_of_posts = number_of_posts

    def __str__(self):
        return 'Topic (' + self.topic_link + ')' + ': ' + self.topic_title + ' [' + str(self.number_of_posts) + ']'


class WowPostDetail:
    def __init__(self, post_date, post_author, post_body, post_type='other', post_index=-1, post_score=0.0):
        self.post_date = post_date
        self.post_author = post_author
        self.post_body = post_body
        self.post_type = post_type
        self.post_index = post_index
        self.post_score = post_score

    def __str__(self):
        return 'Post (' + self.post_author + '@' + self.post_date + '@' + ')' \
               + ': ' + str(self.post_body[:100])


class WowPost(WowPostDetail):
    def __init__(self, wow_topic, wow_post_detail):
        super().__init__(wow_post_detail.post_date, wow_post_detail.post_author, wow_post_detail.post_body)
        self.wow_topic = wow_topic

    def __str__(self):
        return 'Post (' + self.post_author + '@' + self.post_date + '@' + self.wow_topic.topic_title + ')' \
               + ': ' + self.post_body[:100]


class WowTopicComplete(WowTopic):
    def __init__(self, wow_topic, post_list):
        super().__init__(wow_topic.topic_link, wow_topic.topic_title, wow_topic.number_of_posts)
        self.post_list = post_list

    def get_wow_topic(self):
        return WowTopic(self.topic_link, self.topic_title, self.number_of_posts)


WOW_TOPIC_URLS_EU = \
    [(c, WowClassesResources.WOW_FORUM_ROOT_URL_EU + WowClassesResources.WOW_FORUM_MID_URL + u)
     for c, u in WowClassesResources.WOW_CLASS_LIST_EU.items()]

WOW_TOPIC_URLS_DICT_EU = \
    {c: WowClassesResources.WOW_FORUM_ROOT_URL_EU + WowClassesResources.WOW_FORUM_MID_URL + u
     for c, u in WowClassesResources.WOW_CLASS_LIST_EU.items()}


# print(WOW_TOPIC_URLS_DICT_EU)


def get_page_content(url):
    attempt_number = 0
    while True:
        attempt_number += 1
        if attempt_number > 5:
            return None
        try:
            response = request.urlopen(url)
        except request.HTTPError as e:
            print('HTTPError = ' + str(e.code))
            continue
        except Exception as e:
            print(e)
            continue
        except e:
            print(e)
            continue
        html = response.read().decode('utf8')
        break
    return html


def topic_scrape(forum_url):
    all_links = []
    i = 1
    while True:
        html = get_page_content(forum_url + WowClassesResources.URL_PAGE_ATTRIBUTE + str(i))
        if html is None:
            return []
        bs_html = BeautifulSoup(html, "html.parser")

        all_link_elements = bs_html.find_all("a", class_="ForumTopic")
        # pprint(all_link_elements)
        link_count = len(all_link_elements)
        print(str(i) + ' ' + str(link_count))

        if link_count == 0:
            print('Exiting')
            break
        for a in all_link_elements:
            # print a
            title = a.find(class_='ForumTopic-title').get_text().strip()
            post_number = int(a.find(class_='ForumTopic-replies').get_text().strip())
            # print title
            all_links.append(WowTopic(a['href'], title, 1 + post_number))
        i += 1
        time.sleep(3)
    return all_links


def topic_scrape_update(forum_url, current_links):
    init_size = len(current_links)
    timeout = 3
    up_to_date_tresh = 200
    i = 1
    existing_link_count = 0
    while True:
        html = get_page_content(forum_url + WowClassesResources.URL_PAGE_ATTRIBUTE + str(i))
        if html is None:
            return []
        bs_html = BeautifulSoup(html, "html.parser")

        all_link_elements = bs_html.find_all("a", class_="ForumTopic")
        # pprint(all_link_elements)
        link_count = len(all_link_elements)
        print(str(i) + ' ' + str(link_count))

        if link_count == 0:
            print('Exiting')
            break
        for a in all_link_elements:
            link = a['href']
            # print a
            title = a.find(class_='ForumTopic-title').get_text().strip()
            post_number = int(a.find(class_='ForumTopic-replies').get_text().strip())
            # print title
            if link in current_links:
                if current_links[link].number_of_posts == (1 + post_number):
                    existing_link_count += 1
                else:
                    current_links[link].number_of_posts = 1 + post_number
            else:
                current_links.update({link: WowTopic(link, title, 1 + post_number)})
        if existing_link_count > up_to_date_tresh:
            print('Found ' + str(up_to_date_tresh) + ' existing links. Stopping further extraction')
            break
        i += 1
        time.sleep(timeout)
    read_diff = len(current_links) - init_size
    print('Updated given list with additional ' + str(read_diff) + ' topic links')
    return current_links


def extract_topic(wow_topic, start_page=None):
    topic_url_ending = wow_topic.topic_link
    pprint('[' + wow_topic.topic_title + '] (' + topic_url_ending + ')')
    post_list = []
    i = 1
    if start_page is not None:
        i = start_page
    while True:
        html = get_page_content(
            WowClassesResources.WOW_FORUM_ROOT_URL_EU + topic_url_ending + WowClassesResources.URL_PAGE_ATTRIBUTE + str(
                i))
        if html is None:
            return []
        bs_html = BeautifulSoup(html, "html.parser")

        all_topic_post_elements = bs_html.find_all("div", class_="TopicPost-content")
        # pprint(all_topic_post_elements)
        link_count = len(all_topic_post_elements)
        # print str(i) + ' ' + str(link_count)

        if link_count == 0:
            print('Exiting')
            break
        for element in all_topic_post_elements:
            # print a
            post_body = element.find(class_='TopicPost-bodyContent').get_text().strip()
            post_date = element.find("a", class_='TopicPost-timestamp')['data-tooltip-content']
            author_element = element.find("span", class_='Author-name')
            if author_element is not None:
                # post_author = '<UNKNOWN>'
                if author_element.a is not None:
                    post_author = author_element.a.get_text().strip()
                else:
                    post_author = author_element.get_text().strip()
                post_list.append(WowPostDetail(post_date, post_author, post_body))
        i += 1
        time.sleep(3)
    pprint('posts: ' + str(len(post_list)))
    return post_list


def extract_topic_update(topic_title_url_tuple):
    topic_url_ending = topic_title_url_tuple[0]
    topic_title = topic_title_url_tuple[1]
    pprint('[' + topic_title + '] (' + topic_url_ending + ')')
    all_posts = []
    i = 1
    while True:
        html = get_page_content(
            WowClassesResources.WOW_FORUM_ROOT_URL_EU + topic_url_ending + WowClassesResources.URL_PAGE_ATTRIBUTE + str(
                i))
        if html is None:
            return []
        bs_html = BeautifulSoup(html, "html.parser")

        all_topic_post_elements = bs_html.find_all("div", class_="TopicPost-content")
        # pprint(all_topic_post_elements)
        link_count = len(all_topic_post_elements)
        # print str(i) + ' ' + str(link_count)

        if link_count == 0:
            print('Exiting')
            break
        for element in all_topic_post_elements:
            # print a
            post_body = element.find(class_='TopicPost-bodyContent').get_text().strip()
            post_date = element.find("a", class_='TopicPost-timestamp')['data-tooltip-content']
            author_element = element.find("span", class_='Author-name')
            if author_element is not None:
                # post_author = '<UNKNOWN>'
                if author_element.a is not None:
                    post_author = author_element.a.get_text().strip()
                else:
                    post_author = author_element.get_text().strip()
                all_posts.append((topic_title, post_date, post_author, post_body))
        i += 1
        time.sleep(5)
    pprint('posts: ' + str(len(all_posts)))
    return all_posts


def save_to_json_file(path, file_name, content, mode='w'):
    with open(path + file_name + '.json', mode) as out_file:
        json.dump(content, out_file)


def read_from_json_file(path, file_name):
    try:
        with open(path + file_name + '.json', 'r') as in_file:
            return json.load(in_file)
    except FileNotFoundError as e:
        print('File not found (' + e.strerror + '), skipping read for: ' + path + file_name)


def save_topic_dict_to_file(path, file_name, topic_dict):
    serializable_dict = {}
    t_count = 0
    c_count = 0
    for wow_class in topic_dict:
        serializable_dict[wow_class] = [(t.topic_link, t.topic_title, t.number_of_posts) for t in topic_dict[wow_class]]
        t_count += len(serializable_dict[wow_class])
        c_count += 1
    save_to_json_file(path, file_name, serializable_dict, 'w')
    print('Saved a total of ' + str(t_count) + ' topic links for ' + str(
        c_count) + ' classes to file ' + path + file_name + '.json')


def save_topic_dict_to_file_as_dict(path, file_name, topic_dict):
    serializable_dict = {}
    t_count = 0
    c_count = 0
    for wow_class in topic_dict:
        serializable_dict[wow_class] = [(topic_dict[wow_class][t].topic_link, topic_dict[wow_class][t].topic_title,
                                         topic_dict[wow_class][t].number_of_posts) for t in topic_dict[wow_class]]
        t_count += len(serializable_dict[wow_class])
        c_count += 1
    save_to_json_file(path, file_name, serializable_dict, 'w')
    print('Saved a total of ' + str(t_count) + ' topic links for ' + str(
        c_count) + ' classes to file ' + path + file_name + '.json\n')


def read_topic_dict_from_file(path, file_name):
    serializable_dict = read_from_json_file(path, file_name)
    topic_dict = {}
    t_count = 0
    c_count = 0
    for wow_class in serializable_dict:
        topic_dict[wow_class] = [WowTopic(l, t, n) for (l, t, n) in serializable_dict[wow_class]]
        t_count += len(topic_dict[wow_class])
        c_count += 1
    print('Read a total of ' + str(t_count) + ' topic links for ' + str(
        c_count) + ' classes from file ' + path + file_name + '.json')
    return topic_dict


def read_topic_dict_from_file_as_link_dict(path, file_name):
    std_format_topic_dict = read_topic_dict_from_file(path, file_name)
    all_topics_dict = {}
    t_count = 0
    print('Started converting topic links to new dictionary...')
    for wow_class in std_format_topic_dict:
        all_topics_dict[wow_class] = {}
        count = 0

        for topic in std_format_topic_dict[wow_class]:
            count += 1
            all_topics_dict[wow_class][topic.topic_link] = topic
        t_count += count
        print(wow_class + ': ' + str(count))
    print('Done. Processed ' + str(t_count) + ' topic links')
    return all_topics_dict


def save_post_dict_to_file(path, file_name, post_dict):
    print('Saving posts to files ' + file_name + '_*.json')
    t_count = 0
    c_count = 0
    serializable_dict = {}
    for wow_class in post_dict:
        serializable_dict.clear()
        serializable_dict[wow_class] = {}
        serializable_dict[wow_class]['wow_class'] = wow_class

        # serializable_dict[wow_class]['links'] = {p: (post_dict[wow_class][p].topic_link,
        #                                              post_dict[wow_class][p].topic_title,
        #                                              post_dict[wow_class][p].number_of_posts) for p in
        #                                          post_dict[wow_class]}
        # serializable_dict[wow_class]['posts'] = {p: [(pd.post_date, pd.post_author, pd.post_body) for pd in
        #                                             post_dict[wow_class][p].post_list] for p in post_dict[wow_class]}
        serializable_dict[wow_class]['links'] = {}
        serializable_dict[wow_class]['posts'] = {}
        temp_count = 0
        for p in post_dict[wow_class]:
            serializable_dict[wow_class]['links'].update({p: (post_dict[wow_class][p].topic_link,
                                                              post_dict[wow_class][p].topic_title,
                                                              post_dict[wow_class][p].number_of_posts)})
            serializable_dict[wow_class]['posts'].update(
                {p: [(pd.post_date, pd.post_author, pd.post_body, pd.post_type, pd.post_index, pd.post_score) for pd in
                     post_dict[wow_class][p].post_list]})
            temp_count += len(serializable_dict[wow_class]['posts'][p])

        t_count += temp_count
        c_count += 1
        save_to_json_file(path, file_name + '_' + wow_class, serializable_dict, 'w')
        print('> ' + wow_class + ': ' + str(temp_count))
    print('Saved a total of ' + str(t_count) + ' posts for ' + str(
        c_count) + ' classes to file ' + path + file_name + '_*.json\n')


def read_post_dict_from_file(path, file_name):
    print('Reading posts from files ' + file_name + '_*.json')
    post_dict = {}
    t_count = 0
    c_count = 0
    for wow_class in WOW_TOPIC_URLS_DICT_EU:
        serializable_dict = read_from_json_file(path, file_name + '_' + wow_class)
        temp_count = 0
        if serializable_dict is not None:
            post_dict[wow_class] = {}
            for link in serializable_dict[wow_class]['posts']:
                topic_obj = WowTopic(serializable_dict[wow_class]['links'][link][0],
                                     serializable_dict[wow_class]['links'][link][1],
                                     serializable_dict[wow_class]['links'][link][2])
                post_list = []
                for p in serializable_dict[wow_class]['posts'][link]:
                    if len(p) == 3:
                        post_list.append(WowPostDetail(p[0], p[1], p[2]))
                    elif len(p) == 5:
                        post_list.append(WowPostDetail(p[0], p[1], p[2], p[3], p[4]))
                    elif len(p) == 6:
                        post_list.append(WowPostDetail(p[0], p[1], p[2], p[3], p[4], p[5]))

                # post_list = [WowPostDetail(d, a, b, t, i) for (d, a, b, t, i) in
                #              serializable_dict[wow_class]['posts'][link]]
                post_dict[wow_class].update({link: WowTopicComplete(topic_obj, post_list)})
                temp_count += len(post_dict[wow_class][link].post_list)
            t_count += temp_count
            c_count += 1
            print('> ' + wow_class + ': ' + str(temp_count))
    print('Read a total of ' + str(t_count) + ' posts for ' + str(
        c_count) + ' classes from file ' + path + file_name + '.json\n')
    return post_dict
