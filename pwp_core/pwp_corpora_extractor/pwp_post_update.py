from pwp_core.pwp_data_resources import *

all_links_dict = read_topic_dict_from_file_as_link_dict(RESOURCES_PATH_LINKS, 'all_topic_links')
all_posts_dict = read_post_dict_from_file(RESOURCES_PATH_POSTS, 'corpora_posts_raw_u')

tl = []
i = 0
while i <= 19:
    tl.append(i)
    i += 1

print(tl)
print(tl[0:10])
print(str(1 + int(len(tl) / 10)))
# Re-read the complete Topic where they were found to be inconsistent
print('Updating out-of-date Topics:')
mismatch_count_t = 0
for wow_class in all_posts_dict:
    print('> ' + wow_class + '\n==========================')
    mismatch_count = 0
    for link in all_posts_dict[wow_class]:
        topic_count = all_posts_dict[wow_class][link].number_of_posts
        post_count = len(all_posts_dict[wow_class][link].post_list)
        if topic_count > post_count:
            start_page = 1 + int(post_count / 10)
            print('[' + link + '] ' + all_posts_dict[wow_class][link].topic_title + ' (' + str(topic_count) + '/' + str(
                post_count) + ') start page ' + str(start_page))
            all_posts_dict[wow_class][link].post_list = all_posts_dict[wow_class][link].post_list[
                                                        :((start_page - 1) * 20)] + extract_topic(
                all_posts_dict[wow_class][link].get_wow_topic(),
                start_page)
            mismatch_count += 1
            break
    mismatch_count_t += mismatch_count

print('DONE Updating out-of-date Topics. A total of ' + str(mismatch_count_t) + ' topics were updated')

# Save changes
save_post_dict_to_file(RESOURCES_PATH_POSTS, 'corpora_posts_raw_u', all_posts_dict)
