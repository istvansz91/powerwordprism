from pwp_core.pwp_data_resources import *

# Read topic Links for each Class, gather them in all_topic_links
# corpora_dict = {}
# for wow_class in WOW_TOPIC_URLS_DICT_EU:
#     class_dict = read_topic_dict_from_file(RESOURCES_PATH_LINKS, 'topic_links_' + wow_class)
#     corpora_dict.update(class_dict)
#
# save_topic_dict_to_file(RESOURCES_PATH_LINKS, 'all_topic_links', corpora_dict)

# Read all topic links, update them if necessary
corpora_dict = read_topic_dict_from_file_as_link_dict(RESOURCES_PATH_LINKS, 'all_topic_links')
# corpora_dict = read_topic_dict_from_file_as_link_dict(RESOURCES_PATH_LINKS, 'all_topic_links_u')

for wow_class in corpora_dict:
    print(wow_class + ': ')
    topic_scrape_update(WOW_TOPIC_URLS_DICT_EU[wow_class], corpora_dict[wow_class])

# save_topic_dict_to_file_as_dict(RESOURCES_PATH_LINKS, 'all_topic_links_u', corpora_dict)
save_topic_dict_to_file_as_dict(RESOURCES_PATH_LINKS, 'all_topic_links', corpora_dict)
