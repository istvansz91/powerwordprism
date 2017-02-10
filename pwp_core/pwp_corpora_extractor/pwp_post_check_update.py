from pwp_core.pwp_data_resources import *

all_links_dict = read_topic_dict_from_file_as_link_dict(RESOURCES_PATH_LINKS, 'all_topic_links')

all_posts_dict = read_post_dict_from_file(RESOURCES_PATH_POSTS, 'corpora_posts_raw')

# Check the posts dictionary, that the number of posts for a topic matches the number read from the topic link
print('Checking for inconsistencies:')
mismatch_count_t = 0
out_of_date_t = 0
for wow_class in all_posts_dict:
    print('> ' + wow_class + ' topics:')
    mismatch_count = 0
    out_of_date = 0
    for link in all_posts_dict[wow_class]:
        topic_count = all_posts_dict[wow_class][link].number_of_posts
        post_count = len(all_posts_dict[wow_class][link].post_list)
        if topic_count < post_count:
            # print(' * Post number mismatch for topic: ' + link + ' [topic: ' + str(
            #     all_posts_dict[wow_class][link].number_of_posts) + '] vs [list size: ' +
            #       str(len(all_posts_dict[wow_class][link].post_list)) + ']')
            mismatch_count += 1
        elif topic_count > post_count:
            out_of_date += 1
    mismatch_count_t += mismatch_count
    out_of_date_t += out_of_date
    print('Out of date: ' + str(out_of_date) + '\tInconsistent: ' + str(mismatch_count))

print('DONE Checking for inconsistencies:\nFound a total of ' + str(
    out_of_date_t) + ' topics out of date.\nFound a total of ' + str(mismatch_count_t) + ' inconsistent topics.\n')

for wow_class in all_links_dict:
    if wow_class not in all_posts_dict:
        print('Missing completely: ' + wow_class)
    else:
        cnt = 0
        for link in all_links_dict[wow_class]:
            if link not in all_posts_dict[wow_class]:
                cnt += 1
        print('Missing ' + str(cnt) + ' topics from ' + wow_class)
