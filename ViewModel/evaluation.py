import json
import os
import math
from search import Searcher

current_path = os.getcwd()
film_file_path = current_path + r'\scrapy\film_eval.json'
with open(film_file_path) as f:
    film_js = json.load(f)

search = Searcher()
print("FILM EVALUATION\n")
for key in film_js.keys():
    score = search.search_by_film_name(key)
    
    film_list = list(score)
    list_len = len(film_list)
    imdb_list = film_js[key]
    relevance_list = []
    
    count = 0
    while(count < len(score.keys())):
        film = list(score.keys())[count]
        if score[film] >= 15:
            relevance_list.append(3) 
            count += 1
        elif score[film] >= 7:
            relevance_list.append(2) 
            count += 1
        elif score[film] < 7:
            relevance_list.append(1) 
            count += 1
   
    num = 0
    for i in imdb_list:
        if i in film_list:
            num += 1
            
    n = 0
    total_num = 0
    t_p = 0
    for film in imdb_list:
        total_num += 1
        if film in film_list:
            n += 1
            t_p += n /total_num
            
    if relevance_list:
        # DCG@10
        dcg_10_counter = 0
        dcg_10 = 0.0
        if len(imdb_list) >= 10:
            while dcg_10_counter < 10:
                # if the film in imdb list is in system results
                if imdb_list[dcg_10_counter] in score.keys():
                    for i in range(len(score.keys())):
                        if imdb_list[dcg_10_counter] == list(score.keys())[i]:
                            if dcg_10_counter == 0:
                                dcg_10 = float(relevance_list[i])
                                dcg_10_counter += 1
                                break
                            else:
                                dcg_10 += float(relevance_list[i]) / math.log(dcg_10_counter + 1, 2)
                                dcg_10_counter += 1
                                break
                else:
                    dcg_10_counter += 1      
        else:
            while dcg_10_counter < len(imdb_list):
                # if the film in imdb list is in system results
                if imdb_list[dcg_10_counter] in score.keys():
                    for i in range(len(score.keys())):
                        if imdb_list[dcg_10_counter] == list(score.keys())[i]:
                            if dcg_10_counter == 0:
                                dcg_10 = float(relevance_list[i])
                                dcg_10_counter += 1
                                break
                            else:
                                dcg_10 += float(relevance_list[i]) / math.log(dcg_10_counter + 1, 2)
                                dcg_10_counter += 1
                                break
                else:
                    dcg_10_counter += 1      
            
                
                
        # iDCG@10
        idcg_10 = float(relevance_list[0])
        idcg_10_counter = 1
        # less than 10, others are filled by 0. (add nothing)
        if len(score.keys()) < 10:
            while idcg_10_counter < len(score.keys()):
                idcg_10 += float(relevance_list[idcg_10_counter]) / math.log(idcg_10_counter + 1, 2)
                idcg_10_counter += 1
        else:
            while idcg_10_counter < 10:
                idcg_10 += float(relevance_list[idcg_10_counter]) / math.log(idcg_10_counter + 1, 2)
                idcg_10_counter += 1
    else:
        print("PASS! NULL!")
            
    
    # nDCG@10 = DCG@10 / iDCG@10
    sum_ndcg_10 = 0.0
    if idcg_10 == 0:
        ndcg_10 = 0
    else:
        ndcg_10 = dcg_10 / idcg_10
    sum_ndcg_10 += float(ndcg_10)
    ndcg_10 = format(ndcg_10, '.3f')
            
    if num == 0:
        print("no common actor!!!")
    else:
        precision = format(num / list_len, ".3f")
        recall = format(num / len(imdb_list[0:20]), ".3f")
        ap = format(t_p / num, '.3f')

        # print(key)
        # print("precision: " + precision)
        # print("recall@20: " + recall)
        # print("ap: " + ap)
        print(ndcg_10)
        # print('\n')
        

