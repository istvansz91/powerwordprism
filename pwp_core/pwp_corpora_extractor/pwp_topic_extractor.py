from pwp_core.pwp_data_resources import *

current_class = WowClassesResources.WOW_C_HUNTER
current_class_url = WOW_TOPIC_URLS_DICT_EU[current_class]
print(current_class + ': ' + current_class_url)

for cc in sorted(WOW_TOPIC_URLS_EU)[4:]:
    # print(cc)
    current_class = cc[0]
    current_class_url = WOW_TOPIC_URLS_DICT_EU[current_class]
    print(current_class + ': ' + current_class_url)
    current_topic_list = topic_scrape(current_class_url)

    save_topic_dict_to_file(RESOURCES_PATH_LINKS, 'topic_links_' + current_class,
                            {current_class: current_topic_list})
