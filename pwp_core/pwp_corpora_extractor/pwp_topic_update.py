from pwp_core.pwp_data_resources import *

corpora_dict = read_topic_dict_from_file(RESOURCES_PATH_LINKS, 'all_topic_links')

for wow_class in corpora_dict:
    print(wow_class + ': ')
    topic_scrape_update(WOW_TOPIC_URLS_DICT_EU[wow_class], corpora_dict[wow_class])

save_topic_dict_to_file(RESOURCES_PATH_LINKS, 'all_topic_links_u', corpora_dict)
