from pwp_core.pwp_classification_resources import *
from pwp_core.pwp_file_processor import *

score_tag_dict = read_from_json_file(RESOURCES_PATH_ANNOTATIONS, 'Annotated samples')


def print_accuracy(result_name, cnt_total, cnt_good, cnt_good_senti, cnt_good_post_type):
    print('=== ' + result_name + ' === total entries: ' + str(cnt_total))
    print('= accuracy: ' + str(cnt_good) + '/' + str(cnt_total) + ' --> ' + '{0:.2f}'.format(
        cnt_good * 100 / cnt_total) + '%')
    print('= good sentiment: ' + str(cnt_good_senti) + '/' + str(
        cnt_total) + ' --> ' + '{0:.2f}'.format(cnt_good_senti * 100 / cnt_total) + '%')
    print('= good post type: ' + str(cnt_good_post_type) + '/' + str(
        cnt_total) + ' --> ' + '{0:.2f}'.format(
        cnt_good_post_type * 100 / cnt_total) + '%\n')


annotation_stats = {}

for wow_class in score_tag_dict:
    cnt_good_score = 0
    cnt_good_classif = 0
    cnt_good_entry = 0
    cnt_total_annotated = 0
    annotation_stats[wow_class] = {}
    for pt in score_tag_dict[wow_class]:
        ecnt_good_score = 0
        ecnt_good_classif = 0
        ecnt_good_entry = 0
        ecnt_total_annotated = 0
        for elem in score_tag_dict[wow_class][pt]:
            # pprint(elem)
            ecnt_total_annotated += 1
            # count wrong sentiment
            if elem[4] == 1:
                ecnt_good_score += 1
            # count wrong classification
            if elem[5] == 1:
                ecnt_good_classif += 1
            if elem[4] == 1 and elem[5] == 1:
                ecnt_good_entry += 1
        print_accuracy(wow_class + ' - ' + pt, ecnt_total_annotated, ecnt_good_entry, ecnt_good_score,
                       ecnt_good_classif)
        # [TOTAL, TOTAL_GOOD, TOTAL_GOOD_SENTI_SCORE, TOTAL_GOOD_POST_TYPE]
        annotation_stats[wow_class][pt] = [ecnt_total_annotated, ecnt_good_entry, ecnt_good_score, ecnt_good_classif]
        cnt_total_annotated += ecnt_total_annotated
        cnt_good_score += ecnt_good_score
        cnt_good_classif += ecnt_good_classif
        cnt_good_entry += ecnt_good_entry
    print_accuracy('=================\n' + wow_class + ' - Overall: ', cnt_total_annotated, cnt_good_entry,
                   cnt_good_score, cnt_good_classif)

save_to_json_file(RESOURCES_PATH_ANNOTATIONS, 'annotation_analysis_result', annotation_stats)
