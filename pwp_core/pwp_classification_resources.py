from pwp_core.pwp_data_resources import *
import re
import sys
from nltk import sent_tokenize
import nltk.data
import numpy
from nltk.sentiment import vader
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import math
import datetime

nltk.data.path.append('D:/WS/MSc/TMP/nltk_data')


class WowOntoElement:
    def __init__(self, name, parent, children_list, lex_list):
        self.name = name
        self.parent = parent
        self.children_list = children_list
        self.lex_list = lex_list

    def __str__(self):
        parent_name = 'NONE'
        if self.parent is not None:
            parent_name = self.parent.name
        return self.name + ' (' + parent_name + ') \nchildren: ' \
               + str([t.name for t in self.children_list]) + '\nlex: ' \
               + str(self.lex_list)

    def get_top_parent(self):
        if self.parent is None:
            return self
        else:
            return self.parent.get_top_parent()

    def get_sub_parent(self):
        if self.parent is None:
            return None
        elif self.parent.parent is None:
            return self
        else:
            return self.parent.get_sub_parent()


def build_onto_recursive(pwp_onto, parent):
    result = []
    if parent is None:
        for e in pwp_onto:
            if 'subClassOf' not in [k for k, v in e.items()]:
                ch_list = []
                lex_list = []
                elem = WowOntoElement(e['@id'].replace('_', ' '), None, ch_list, lex_list)
                result.append(elem)
                if 'hasLexicalization' in [k for k, v in e.items()]:
                    elem.lex_list.extend([lexi['@value'].replace('_', ' ') for lexi in e['hasLexicalization']])
                elem.children_list = build_onto_recursive(pwp_onto, elem)
                # print(elem.name)
                # print(elem.children_list)
                # print(elem.lex_list)

                # print(str(elem))
    else:
        # print('parent = ' + parent.name)
        for e in pwp_onto:
            if 'subClassOf' in [k for k, v in e.items()] \
                    and e['subClassOf'][0]['@id'].replace('_', ' ') == parent.name:
                ch_list = []
                lex_list = []
                elem = WowOntoElement(e['@id'].replace('_', ' '), parent, ch_list, lex_list)
                result.append(elem)
                if 'hasLexicalization' in [k for k, v in e.items()]:
                    elem.lex_list.extend([lexi['@value'].replace('_', ' ') for lexi in e['hasLexicalization']])
                elem.children_list = build_onto_recursive(pwp_onto, elem)
                # if elem.lex_list is None:
                #     print(elem.name + '********** LEXI LIST IS NONE')
                # if elem.children_list is None:
                #     print(elem.name + '********** CHILDREN LIST IS NONE')
                # print(str(elem))
    if parent is None:
        print("\n>>> DONE CONSTRUCTING ONTOLOGY.")
    return result


def print_onto_recursive(onto, index):
    tab_ind = ''
    for i in range(index):
        tab_ind += '\t'
    print(tab_ind + onto.name + ' ' + str(onto.lex_list))
    index += 1
    for e in onto.children_list:
        print_onto_recursive(e, index)


def read_and_build_onto(file_name):
    pwp_onto = read_from_json_file(RESOURCES_PATH_ONTOLOGY, file_name)
    pwp_onto_struct = build_onto_recursive(pwp_onto, None)
    return pwp_onto_struct


def get_min_index_for_word(text, word):
    critMatch = re.search(r'\b' + word.lower() + r'\b', text.lower())
    if critMatch:
        return critMatch.start(), word
    else:
        return sys.maxsize, 'NONE'


def get_post_type_recursive(onto, post_body):
    # get index for current onto element
    current_index = (sys.maxsize, 'NONE')
    current_type = 'other'

    result = (current_index, current_type)

    if onto.name != 'Instance':
        # print('It is in ' + onto.name)
        crit_list = [onto.name] + onto.lex_list
        # print('Crit list: ' + str(crit_list))
        current_index = min([get_min_index_for_word(post_body, crit) for crit in crit_list], key=lambda t: t[0])
        current_type = onto.get_sub_parent().name
        result = (current_index, current_type)

        # if result[0] != sys.maxsize:
        #     print('Found: ' + onto.name + '@' + str(result[0]))

    for inst in onto.children_list:
        temp_result = get_post_type_recursive(inst, post_body)
        if temp_result[0][0] < result[0][0]:
            result = temp_result

    return result


def save_posts_by_tag_dict_to_file(path, file_name, post_dict):
    print('Saving posts to files ' + file_name + '_*.json')
    t_count = 0
    c_count = 0
    serializable_dict = {}
    for wow_class in post_dict:
        serializable_dict.clear()
        serializable_dict[wow_class] = post_dict[wow_class]
        temp_count = 0
        for pt in post_dict[wow_class]:
            for auth in post_dict[wow_class][pt]:
                serializable_dict[wow_class][pt][auth] = [
                    (pd.post_date, pd.post_author, pd.post_body, pd.post_type, pd.post_index, pd.post_score) for pd in
                    post_dict[wow_class][pt][auth]]
                temp_count += len(serializable_dict[wow_class][pt][auth])

        t_count += temp_count
        c_count += 1
        save_to_json_file(path, file_name + '_' + wow_class, serializable_dict, 'w')
        print('> ' + wow_class + ': ' + str(temp_count))
    print('Saved a total of ' + str(t_count) + ' posts for ' + str(
        c_count) + ' classes to file ' + path + file_name + '_*.json\n')


def read_posts_by_tag_dict_from_file(path, file_name):
    print('Reading posts from files ' + file_name + '_*.json')
    post_dict = {}
    t_count = 0
    c_count = 0
    for wow_class in WOW_TOPIC_URLS_DICT_EU:
        serializable_dict = read_from_json_file(path, file_name + '_' + wow_class)
        temp_count = 0
        if serializable_dict is not None:
            post_dict[wow_class] = serializable_dict[wow_class]
            for pt in serializable_dict[wow_class]:
                for auth in serializable_dict[wow_class][pt]:
                    post_dict[wow_class][pt][auth] = [WowPostDetail(p[0], p[1], p[2], p[3], p[4], p[5]) for p in
                                                      serializable_dict[wow_class][pt][auth]]
                    temp_count += len(post_dict[wow_class][pt][auth])
            t_count += temp_count
            c_count += 1
            print('> ' + wow_class + ': ' + str(temp_count))
    print('Read a total of ' + str(t_count) + ' posts for ' + str(
        c_count) + ' classes from file ' + path + file_name + '.json\n')
    return post_dict
