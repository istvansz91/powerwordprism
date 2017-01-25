from pwp_core.pwp_data_resources import *

all_links_dict = read_topic_dict_from_file_as_link_dict(RESOURCES_PATH_LINKS, 'all_topic_links')

all_posts_dict = read_post_dict_from_file(RESOURCES_PATH_POSTS, 'corpora_posts_raw')

print('Checking for inconsistencies:')
mismatch_count = 0
for wow_class in all_posts_dict:
    print('> ' + wow_class)
    for link in all_posts_dict[wow_class]:
        if all_posts_dict[wow_class][link].number_of_posts < len(all_posts_dict[wow_class][link].post_list):
            print(' * Post number mismatch for topic: ' + link + ' [topic: ' + str(
                all_posts_dict[wow_class][link].number_of_posts) + '] vs [list size: ' +
                  str(len(all_posts_dict[wow_class][link].post_list)) + ']')
            mismatch_count += 1
            # all_posts_dict[wow_class][link].post_list = extract_topic(all_posts_dict[wow_class][link].get_wow_topic(),
            #                                                           1)
            # if all_posts_dict[wow_class][link].number_of_posts != len(all_posts_dict[wow_class][link].post_list):
            #     print(' *** ! INCONSISTENT after Update!')

print('DONE Checking for inconsistencies. Found ' + str(mismatch_count) + ' inconsistencies')
