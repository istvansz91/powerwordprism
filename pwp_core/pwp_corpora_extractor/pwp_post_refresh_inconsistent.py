from pwp_core.pwp_data_resources import *

all_links_dict = read_topic_dict_from_file_as_link_dict(RESOURCES_PATH_LINKS, 'all_topic_links')
all_posts_dict = read_post_dict_from_file(RESOURCES_PATH_POSTS, 'corpora_posts_raw_u')


# Re-read the complete Topic where they were found to be inconsistent
print('Refreshing inconsistent Topics:')
mismatch_count_t = 0
for wow_class in all_posts_dict:
    print('> ' + wow_class + '\n==========================')
    mismatch_count = 0
    for link in all_posts_dict[wow_class]:
        topic_count = all_posts_dict[wow_class][link].number_of_posts
        post_count = len(all_posts_dict[wow_class][link].post_list)
        if topic_count < post_count:
            print('[' + link + '] ' + all_posts_dict[wow_class][link].topic_title)
            all_posts_dict[wow_class][link].post_list = extract_topic(all_posts_dict[wow_class][link].get_wow_topic(),
                                                                      1)
            mismatch_count += 1
    mismatch_count_t += mismatch_count

print('DONE Refreshing inconsistent Topics. A total of ' + str(mismatch_count_t) + ' topics were refreshed')

# Save changes
save_post_dict_to_file(RESOURCES_PATH_POSTS, 'corpora_posts_raw', all_posts_dict)
