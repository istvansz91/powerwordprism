from pwp_core.pwp_classification_resources import *

# Read existing corpora
posts_dict = read_post_dict_from_file(RESOURCES_PATH_POSTS, 'corpora_posts_raw')
print(posts_dict.keys())

# Read ontology
pwp_onto_struct = read_and_build_onto('PWPJson2')
print('\n****** ONTOLOGY TOP LEVEL STRUCTURE *******')
print([t.name for t in pwp_onto_struct])
print('*************\n')
instance_onto = pwp_onto_struct[0]
# print_onto_recursive(instance_onto, 0)

print('**********************************\nStarting classification of posts...\n**********************************')
# print(instance_onto)
# ['Arena', 'Battleground', 'Dungeon', 'Raid']
for wow_class in posts_dict:
    progress = 0
    total_topics = len(posts_dict[wow_class])
    print('Processing: ' + wow_class + '(' + str(total_topics) + ' topics)')
    for topic in posts_dict[wow_class]:
        progress += 1
        if progress % 250 == 0:
            print(str(progress) + '/' + str(total_topics))

        for post in posts_dict[wow_class][topic].post_list:
            index, post_type = get_post_type_recursive(instance_onto, post.post_body)
            post.post_type = post_type
            if index[0] != sys.maxsize:
                post.post_index = index
                # print(post.post_type + ': ' + str(post.post_index))
                # break
                # break

save_post_dict_to_file(RESOURCES_PATH_CLASSIFICATION, 'corpora_posts_tagged', posts_dict)
