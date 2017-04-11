from pwp_core.pwp_classification_resources import *
from pwp_core.pwp_file_processor import *

# posts_dict = read_posts_by_tag_dict_from_file(RESOURCES_PATH_SCORES)
fn = get_latest_post_scores_filename(SENTI_ALG_VADER)
print(fn)
post_scores_dict = read_posts_by_tag_dict_from_file(RESOURCES_PATH_SCORES, fn)

cnt = 0
score_tag_dict = {}
for wow_class in post_scores_dict:
    score_tag_dict[wow_class] = {}
    for pt in post_scores_dict[wow_class]:
        print('Extracting from: ' + wow_class + '/' + pt)
        score_tag_dict[wow_class][pt] = []
        for auth in post_scores_dict[wow_class][pt]:
            if [p for p in post_scores_dict[wow_class][pt][auth] if p.post_score != 0.0]:
                cnt += 1
                p = post_scores_dict[wow_class][pt][auth][0]
                score_tag_dict[wow_class][pt].append((p.post_body, pt, p.post_score, p.post_index, 1, 1))
                if cnt % 100 == 0:
                    break
        if cnt % 100 != 0:
            found = cnt
            cnt = (int(cnt / 100) + 1) * 100
            found -= cnt - 100
            print('did not find 100 posts for ' + wow_class + '/' + pt + ', only ' + str(
                found) + '. Counter set to: ' + str(cnt))
        else:
            print('Counter: ' + str(cnt))

save_to_json_file(RESOURCES_PATH_CLASSIFICATION, 'samples_to_check2', score_tag_dict)
