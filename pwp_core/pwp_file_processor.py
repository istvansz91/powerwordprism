from pwp_core.pwp_data_resources import *
from os import listdir
from os.path import isfile, join
import re
import datetime

SCORE_AUTH_FILENAME = 'complete_scores_by_author'
SCORE_PT_FILENAME = 'complete_scores_by_post_type'
SCORE_POST_FILENAME = 'post_scores'

SENTI_ALG_VADER = 'Vader'
SENTI_ALG_SWN = 'SWN'
SENTI_ALG = SENTI_ALG_VADER


def get_file_name(alg, file_name, timestamp_string=None):
    if timestamp_string is None:
        timestamp_string = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return alg + '_' + timestamp_string + '_' + file_name


def get_latest_post_scores_filename(alg):
    path = RESOURCES_PATH_SCORES
    score_files = [f for f in listdir(path) if
                   isfile(join(path, f)) and re.search(alg, f) and re.search(SCORE_POST_FILENAME, f)]
    latest_file = score_files[-1]
    for wc in sorted(WowClassesResources.WOW_CLASS_LIST_EU):
        latest_file = latest_file.replace(wc, '')
    latest_file = latest_file.replace('_.json', '')
    print('Latest file: ' + latest_file)
    return latest_file

    # my_path = 'Resources/Corpora/EU/Scores/'
    # score_auth_files = [f for f in listdir(my_path) if isfile(join(my_path, f))
    #                     and re.search(SCORE_AUTH_FN + ALGORITHM, f)]
    # LATEST_SCORE_AUTH_FN = score_auth_files[-1]
    # pprint(LATEST_SCORE_AUTH_FN)
    #
    # score_gt_files = [f for f in listdir(my_path) if isfile(join(my_path, f))
    #                   and re.search(SCORE_GT_FN + ALGORITHM, f)]
    # LATEST_SCORE_GT_FN = score_gt_files[-1]
    # pprint(LATEST_SCORE_GT_FN)
    #
    # scores_auth_meta = read_from_json_file(my_path, LATEST_SCORE_AUTH_FN.replace('.json', ''))
    # scores_gt_meta = read_from_json_file(my_path, LATEST_SCORE_GT_FN.replace('.json', ''))
    # scores_gt = scores_gt_meta['score']
    # scores_auth = scores_auth_meta['score']
    # pprint(scores_auth['Death Knight']['pve'][:10])
    # pprint(scores_gt)
