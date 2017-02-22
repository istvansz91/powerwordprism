from pwp_core.pwp_classification_resources import *

posts_tagged_dict = read_post_dict_from_file(RESOURCES_PATH_CLASSIFICATION, 'corpora_posts_tagged')

posts_by_tag_dict = {}

# {'pvp': {'Arena': [], 'Battleground': []},
#  'pve': {'Dungeon': [], 'Raid': []},
#  'other'}
print('=== Restructuring tagged posts according to their tags... ===')
print('=============================================================')
for wow_class in posts_tagged_dict:
    print('\nProcessing ' + wow_class + '\n==================')
    posts_by_tag_dict[wow_class] = {'Arena': {}, 'Battleground': {},
                                    'Dungeon': {}, 'Raid': {},
                                    'other': {}}
    inco_count = 0
    post_count = 0
    for link in posts_tagged_dict[wow_class]:
        for post in posts_tagged_dict[wow_class][link].post_list:
            if post.post_type not in posts_by_tag_dict[wow_class]:
                print('Inconsistent class found: ' + post.post_type + ' for:\n' + str(post))
                inco_count += 1
            else:
                if post.post_author not in posts_by_tag_dict[wow_class][post.post_type]:
                    posts_by_tag_dict[wow_class][post.post_type].update({post.post_author: []})
                post.post_body = sent_tokenize(post.post_body)
                posts_by_tag_dict[wow_class][post.post_type][post.post_author].append(post)
                post_count += 1

    print('Processed ' + str(post_count) + ' posts.')
    print('Found ' + str(inco_count) + ' inconsistent post tags.')
    print('Summary:')
    for pt in posts_by_tag_dict[wow_class]:
        cnt = sum([len(posts_by_tag_dict[wow_class][pt][l]) for l in posts_by_tag_dict[wow_class][pt]])
        print(pt + ': ' + str(cnt))

save_posts_by_tag_dict_to_file(RESOURCES_PATH_CLASSIFICATION, 'corpora_by_tag', posts_by_tag_dict)
posts_by_tag_dict = read_posts_by_tag_dict_from_file(RESOURCES_PATH_CLASSIFICATION, 'corpora_by_tag')

for pt in posts_by_tag_dict['Demon Hunter']:
    cnt = 0
    print(pt + ':')
    for link in posts_by_tag_dict['Demon Hunter'][pt]:
        print([str(p) for p in posts_by_tag_dict['Demon Hunter'][pt][link][:2]])
        cnt += 1
        if cnt == 5:
            break

