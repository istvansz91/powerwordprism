from pwp_core.pwp_data_resources import *

# Get all extracted topics
all_topic_links = read_topic_dict_from_file_as_link_dict(RESOURCES_PATH_LINKS, 'all_topic_links')

# Get all posts from the old format
old_posts_dict = read_from_json_file(RESOURCES_PATH_POSTS, 'complete_wow_class_posts_dict')
print(old_posts_dict.keys())

new_posts_dict = {}
for wow_class in old_posts_dict:
    print('Converting posts for: ' + wow_class + '(' + str(len(old_posts_dict[wow_class])) + ')')
    new_posts_dict[wow_class] = {}
    temp_post_struct = {}
    for post in old_posts_dict[wow_class]:
        if post[0] not in temp_post_struct:  # title
            temp_post_struct[post[0]] = [post]
        else:
            temp_post_struct[post[0]].append(post)

    for topic_title in temp_post_struct:
        topic_obj = [all_topic_links[wow_class][t] for t in all_topic_links[wow_class] if
                     all_topic_links[wow_class][t].topic_title == topic_title][0]
        if topic_obj is None:
            print('Topic title not found for ' + wow_class + ': ' + topic_title)
        for post in temp_post_struct[topic_title]:
            if topic_obj.topic_link not in new_posts_dict[wow_class]:
                new_posts_dict[wow_class][topic_obj.topic_link] = WowTopicComplete(topic_obj, [
                    WowPostDetail(post[1], post[2], post[3])])
            else:
                new_posts_dict[wow_class][topic_obj.topic_link].post_list.append(
                    WowPostDetail(post[1], post[2], post[3]))

print('Conversion done.\n')

save_post_dict_to_file(RESOURCES_PATH_POSTS, 'corpora_posts_raw', new_posts_dict)
new_posts_dict = read_post_dict_from_file(RESOURCES_PATH_POSTS, 'corpora_posts_raw')
#
# for wow_class in new_posts_dict:
#     print(wow_class + ': ')
#     for post in new_posts_dict[wow_class][:10]:
#         pprint(str(post))
