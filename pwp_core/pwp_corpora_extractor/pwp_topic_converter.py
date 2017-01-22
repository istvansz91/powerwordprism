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
    new_topic_formats[wow_class] = [WowTopic(l, t) for (l, t) in old_topic_formats[wow_class]]
    print(wow_class + ' new: ' + str(len(new_topic_formats[wow_class])))
    print([str(t) for t in new_topic_formats[wow_class][:5]])

save_topic_dict_to_file(RESOURCES_PATH_LINKS, 'all_topic_links', new_topic_formats)
read_topic_dict_from_file(RESOURCES_PATH_LINKS, 'all_topic_links')
