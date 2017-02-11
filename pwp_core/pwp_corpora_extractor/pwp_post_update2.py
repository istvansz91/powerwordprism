from pwp_core.pwp_data_resources import *

all_links_dict = read_topic_dict_from_file_as_link_dict(RESOURCES_PATH_LINKS, 'all_topic_links')
all_posts_dict = read_post_dict_from_file(RESOURCES_PATH_POSTS, 'corpora_posts_raw')

# Re-read the complete Topic where they were found to be inconsistent
print('Updating out-of-date Topics:')
mismatch_count_t = 0

update_missing_class = 'no'
# all_posts_dict.pop(WowClassesResources.WOW_C_DEATH_KNIGHT)
# all_posts_dict.pop(WowClassesResources.WOW_C_WARRIOR)
for wow_class in all_links_dict:
    mismatch_count = 1

    if update_missing_class == wow_class:
        print('> ' + wow_class + '\n==========================')
        print('Missing completely: ')
        print('Updating missing classes is enabled for ' + update_missing_class +
              '. Performing corpora extraction...')
        all_posts_dict[wow_class] = {}
    if wow_class not in all_posts_dict:
        if update_missing_class == 'no':
            # print('Updating missing classes is not enabled')
            pass
    else:
        print('> ' + wow_class + '\nExisting Topics: ' + str(len(all_posts_dict[wow_class])) + '/' + str(
            len(all_links_dict[wow_class])) + '\n==========================')
        for link in all_links_dict[wow_class]:
            if link not in all_posts_dict[wow_class]:
                # extract whole topic
                print('Whole Topic: [' + link + '] ' + all_links_dict[wow_class][link].topic_title + ' (' + str(
                    all_links_dict[wow_class][link].number_of_posts) + ')')
                all_posts_dict[wow_class][link] = WowTopicComplete(all_links_dict[wow_class][link], extract_topic(
                    all_links_dict[wow_class][link]))
                mismatch_count += 1
            else:
                topic_count = all_links_dict[wow_class][link].number_of_posts
                post_count = len(all_posts_dict[wow_class][link].post_list)
                if topic_count > post_count:
                    start_page = 1 + int(post_count / 20)
                    print('Updating [' + link + '] ' + all_posts_dict[wow_class][link].topic_title + ' (' + str(
                        topic_count) + '/' + str(
                        post_count) + ') start page ' + str(start_page) + '. Reducing existing topics to: ' + str(
                        (start_page - 1) * 20))
                    all_posts_dict[wow_class][link].post_list = all_posts_dict[wow_class][link].post_list[
                                                                :((start_page - 1) * 20)] + extract_topic(
                        all_posts_dict[wow_class][link].get_wow_topic(),
                        start_page)
                    post_count = len(all_posts_dict[wow_class][link].post_list)
                    all_posts_dict[wow_class][link].number_of_posts = post_count
                    if topic_count > post_count:
                        all_links_dict[wow_class][link].number_of_posts = post_count
                    mismatch_count += 1
                elif topic_count < post_count:
                    # refresh whole topic
                    print('Refresh Topic: [' + link + '] ' + all_links_dict[wow_class][link].topic_title + ' (' + str(
                        all_links_dict[wow_class][link].number_of_posts) + ')')
                    all_posts_dict[wow_class][link] = WowTopicComplete(all_links_dict[wow_class][link], extract_topic(
                        all_links_dict[wow_class][link]))
                    mismatch_count += 1

            # break
            if mismatch_count % 20 == 0:
                save_post_dict_to_file(RESOURCES_PATH_POSTS, 'corpora_posts_raw', all_posts_dict)
                save_topic_dict_to_file_as_dict(RESOURCES_PATH_LINKS, 'all_topic_links', all_links_dict)
                mismatch_count += 1
                print('Existing Topics: ' + str(len(all_posts_dict[wow_class])) + '/' + str(
                    len(all_links_dict[wow_class])))

    mismatch_count_t += mismatch_count
    save_post_dict_to_file(RESOURCES_PATH_POSTS, 'corpora_posts_raw', all_posts_dict)
    save_topic_dict_to_file_as_dict(RESOURCES_PATH_LINKS, 'all_topic_links', all_links_dict)

print('\nDONE Updating out-of-date Topics. A total of ' + str(mismatch_count_t) + ' topics were updated')

# Save changes
save_post_dict_to_file(RESOURCES_PATH_POSTS, 'corpora_posts_raw', all_posts_dict)
