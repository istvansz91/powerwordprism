from pwp_core.pwp_data_resources import *

# old format of topic dictionary is:
# dict[WOW_C_*] = [(Link, Title), (Link, Title), ...]
old_topic_formats = {}
old_topic_formats_DK = read_from_json_file(RESOURCES_PATH_LINKS, 'corpora_topic_links_'
                                           + WowClassesResources.WOW_C_DEATH_KNIGHT)
old_topic_formats.update(old_topic_formats_DK)
old_topic_formats_DH = read_from_json_file(RESOURCES_PATH_LINKS, 'corpora_topic_links_'
                                           + WowClassesResources.WOW_C_DEMON_HUNTER)
old_topic_formats.update(old_topic_formats_DH)
old_topic_formats_DR = read_from_json_file(RESOURCES_PATH_LINKS, 'corpora_topic_links_'
                                           + WowClassesResources.WOW_C_DRUID)
old_topic_formats.update(old_topic_formats_DR)
# print(old_topic_formats.keys())

new_topic_formats = {}
for wow_class in old_topic_formats:
    print(wow_class + ' old: ' + str(len(old_topic_formats[wow_class])))
    new_topic_formats[wow_class] = [WowTopic(l, t, 1) for (l, t) in old_topic_formats[wow_class]]
    print(wow_class + ' new: ' + str(len(new_topic_formats[wow_class])))
    print([str(t) for t in new_topic_formats[wow_class][:5]])

save_topic_dict_to_file(RESOURCES_PATH_LINKS, 'all_topic_links', new_topic_formats)
read_topic_dict_from_file(RESOURCES_PATH_LINKS, 'all_topic_links')

all_old_posts = read_from_json_file(RESOURCES_PATH_POSTS, 'complete_wow_class_posts_dict')
# print(all_old_posts.keys())
all_old_posts_count = {}

for wow_class in new_topic_formats:
    if wow_class in all_old_posts:
        for topic in new_topic_formats[wow_class]:
            same_topic_posts = [p for p in all_old_posts[wow_class] if p[0] == topic.topic_title]
            topic.number_of_posts = len(same_topic_posts)

save_topic_dict_to_file(RESOURCES_PATH_LINKS, 'all_topic_links_c', new_topic_formats)
read_topic_dict_from_file(RESOURCES_PATH_LINKS, 'all_topic_links_c')

for wow_class in new_topic_formats:
    print([str(t) for t in new_topic_formats[wow_class][:5]])
