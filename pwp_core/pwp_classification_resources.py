from pwp_core.pwp_data_resources import *
import re
import sys


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
        return critMatch.start()
    else:
        return sys.maxsize


def get_post_type_recursive(onto, post_body):
    # get index for current onto element
    current_index = sys.maxsize
    current_type = 'other'
    result = (current_index, current_type)

    if onto.name != 'Instance':
        # print('It is in ' + onto.name)
        crit_list = [onto.name] + onto.lex_list
        # print('Crit list: ' + str(crit_list))
        current_index = min([get_min_index_for_word(post_body, crit) for crit in crit_list])
        current_type = onto.get_sub_parent().name
        result = (current_index, current_type)

        # if result[0] != sys.maxsize:
        #     print('Found: ' + onto.name + '@' + str(result[0]))

    for inst in onto.children_list:
        temp_result = get_post_type_recursive(inst, post_body)
        if temp_result[0] < result[0]:
            result = temp_result

    return result
