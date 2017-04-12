from pwp_core.pwp_classification_resources import *
from pwp_core.pwp_file_processor import *

fn = get_latest_post_scores_filename(SENTI_ALG_VADER)
print(fn)
post_scores_dict = read_posts_by_tag_dict_from_file(RESOURCES_PATH_SCORES, fn)

# scores by year/month
# activity by year/month
post_scores_by_date = {}
activity_by_date_relevant = {}
activity_by_date_all = {}
c_cnt = 0
for wow_class in post_scores_dict:
    c_cnt += 1
    print('==== Processing: ' + wow_class + '(' + str(c_cnt) + '/' + str(len(post_scores_dict)) + ') ======')
    post_scores_by_date[wow_class] = {}
    activity_by_date_relevant[wow_class] = {}
    activity_by_date_all[wow_class] = {}
    for pt in post_scores_dict[wow_class]:
        print('= ' + pt + ' =')
        a_cnt = 0
        post_scores_by_date[wow_class][pt] = {}
        temp_scores_by_date = {}
        activity_by_date_relevant[wow_class][pt] = {}
        activity_by_date_all[wow_class][pt] = {}
        for auth in post_scores_dict[wow_class][pt]:
            a_cnt += 1
            for post_detail in post_scores_dict[wow_class][pt][auth]:
                d = get_date_from_string(post_detail.post_date)
                if d.year not in activity_by_date_all[wow_class][pt]:
                    activity_by_date_all[wow_class][pt][d.year] = {}
                if d.month not in activity_by_date_all[wow_class][pt][d.year]:
                    activity_by_date_all[wow_class][pt][d.year][d.month] = 1
                else:
                    activity_by_date_all[wow_class][pt][d.year][d.month] += 1

                if post_detail.post_score != 0.00:
                    # print(post_detail.post_date + ' = year: ' + str(d.year) + ', month: ' + str(
                    #     d.month) + ', score: ' + str(post_detail.post_score))
                    if d.year not in temp_scores_by_date:
                        temp_scores_by_date[d.year] = {}
                    if d.month not in temp_scores_by_date[d.year]:
                        temp_scores_by_date[d.year][d.month] = []
                        temp_scores_by_date[d.year][d.month].append(post_detail.post_score)

                    if d.year not in activity_by_date_relevant[wow_class][pt]:
                        activity_by_date_relevant[wow_class][pt][d.year] = {}
                    if d.month not in activity_by_date_relevant[wow_class][pt][d.year]:
                        activity_by_date_relevant[wow_class][pt][d.year][d.month] = 1
                    else:
                        activity_by_date_relevant[wow_class][pt][d.year][d.month] += 1

        # pprint(temp_scores_by_date)
        for y in temp_scores_by_date:
            post_scores_by_date[wow_class][pt][y] = {}
            for m in temp_scores_by_date[y]:
                score_array = numpy.array(temp_scores_by_date[y][m])
                sc = numpy.mean(score_array)
                if not math.isnan(sc):
                    post_scores_by_date[wow_class][pt][y][m] = sc
                else:
                    print('Found empty array for ' + wow_class + '/' + pt + '/' + str(y) + '/' + str(m))

# pprint(post_scores_by_date)
# pprint(activity_by_date_relevant)
# pprint(activity_by_date_all)

fn_post_scores_by_date = fn + '_by_date'
fn_activity_by_date_rel = fn.replace('post_scores', 'activity_relevant')
fn_activity_by_date_all = fn.replace('post_scores', 'activity_all')

save_to_json_file(RESOURCES_PATH_SCORES_BY_DATE, fn_post_scores_by_date, post_scores_by_date)
save_to_json_file(RESOURCES_PATH_SCORES_BY_DATE, fn_activity_by_date_rel, activity_by_date_relevant)
save_to_json_file(RESOURCES_PATH_SCORES_BY_DATE, fn_activity_by_date_all, activity_by_date_all)

print('>>> DONE <<<')
