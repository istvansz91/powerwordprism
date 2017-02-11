from pwp_core.pwp_classification_resources import *
from pwp_core.pwp_file_processor import *

posts_tagged_dict = read_posts_by_tag_dict_from_file(RESOURCES_PATH_CLASSIFICATION, 'corpora_by_tag')
auths_scored_dict = {}
post_types_scored_dict = {}

SENTI_ALG = SENTI_ALG_VADER

print('=== Applying sentiment analysis on all posts using ' + SENTI_ALG + ' ===')
print('===================================================================')
sid = SentimentIntensityAnalyzer()
SCORE_TRESHOLD = 0.5

for wow_class in posts_tagged_dict:
    print('\nProcessing ' + wow_class + '\n=======================')
    auths_scored_dict[wow_class] = {}
    post_types_scored_dict[wow_class] = {}
    for pt in posts_tagged_dict[wow_class]:
        auths_scored_dict[wow_class][pt] = {}

        total_post_count = sum([len(posts_tagged_dict[wow_class][pt][a]) for a in posts_tagged_dict[wow_class][pt]])
        print('>>> Processing ' + pt + '(' + str(total_post_count) + ' posts)')
        progress_post = 0
        progress_auth = 0
        for auth in posts_tagged_dict[wow_class][pt]:
            for p in posts_tagged_dict[wow_class][pt][auth]:
                # for each post
                post_sent_score = []
                for sent in p.post_body:
                    # for each sentence
                    if SENTI_ALG == SENTI_ALG_VADER:
                        post_sent_score.append(sid.polarity_scores(sent)['compound'])
                    elif SENTI_ALG == SENTI_ALG_SWN:
                        pass
                        # IMPLEMENT SWN Sentiment-analysis here.
                        # post_sent_score.append()
                if post_sent_score:
                    post_sent_score_array = numpy.array(post_sent_score)
                    sc = numpy.mean(post_sent_score_array)
                    if sc > SCORE_TRESHOLD or sc < -SCORE_TRESHOLD:
                        p.post_score = sc

                progress_post += 1
            auth_score_array = numpy.array(
                [post.post_score for post in posts_tagged_dict[wow_class][pt][auth] if post.post_score != 0.0])
            auth_sc = numpy.mean(auth_score_array)
            auths_scored_dict[wow_class][pt][auth] = 0.0
            if not math.isnan(auth_sc):
                auths_scored_dict[wow_class][pt][auth] = auth_sc
            progress_auth += 1
            if progress_auth % 250 == 0:
                print('\t\t\tProgress: ' + str(progress_post) + '/' + str(total_post_count))
        post_type_score_array = numpy.array(
            [auths_scored_dict[wow_class][pt][a] for a in auths_scored_dict[wow_class][pt] if
             auths_scored_dict[wow_class][pt][a] != 0.0])
        post_mean_sc = numpy.mean(post_type_score_array)
        post_types_scored_dict[wow_class][pt] = post_mean_sc

print('===================================================================')
print('=== DONE Applying Sentiment Analysis ===\n')

CURRENT_DATE = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

save_posts_by_tag_dict_to_file(RESOURCES_PATH_SCORES, get_file_name(SENTI_ALG, SCORE_POST_FILENAME, CURRENT_DATE),
                               posts_tagged_dict)
save_to_json_file(RESOURCES_PATH_SCORES, SENTI_ALG_VADER + '_' + CURRENT_DATE + '_complete_scores_by_author',
                  auths_scored_dict)
save_to_json_file(RESOURCES_PATH_SCORES, SENTI_ALG_VADER + '_' + CURRENT_DATE + '_complete_scores_by_post_type',
                  post_types_scored_dict)
