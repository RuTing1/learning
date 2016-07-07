import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import datetime
import copy
import csv

data = pd.read_csv('rating_matrix.csv')
name = pd.read_csv('name.csv', index_col='name')
user_id = pd.read_csv('user_id.csv', index_col='user_id')

# 获得各个用户的平均评分数据表 save_avg
avg_count = []
count = []
for i in data.axes[1]:
    data[i] = np.byte(copy.deepcopy(data[i]))
    sum_lie = 0
    count1 = 0
    for j in data[i]:
        if j == 0:
            count1 = count1 + 1
        else:
            sum_lie += j
    avg_lie = sum_lie / (24 - count1)
    count.append(24 - count1)
    avg_count.append(avg_lie)
save_avg = pd.DataFrame([data.axes[1], avg_count, count]).T
save_avg.rename(columns={0: 'user'}, inplace=True)
save_avg.rename(columns={1: 'avg_count'}, inplace=True)
save_avg.rename(columns={2: 'count'}, inplace=True)
save_avg = save_avg.set_index('user')

# 计算用户的相似度表 similarity
similarity = pd.DataFrame(index=data.axes[1])
for user_a in data.axes[1]:
    for user_b in data.axes[1]:
        similarity[user_b]=0

count =0
for user_a in data.axes[1]:
    for user_b in data.axes[1]:
        w_a_b_1_all = []
        w_a_2_all = []
        w_b_2_all = []
        for i in range(0, 24):
            # print(data[user_a].ix[i],data[user_b].ix[i])
            if (data[user_a].ix[i] != 0) & (data[user_b].ix[i] != 0):
                w_a = data[user_a].ix[i] - save_avg.ix[user_a].avg_count
                w_b = data[user_b].ix[i] - save_avg.ix[user_b].avg_count
                w_a_b_1 = w_a*w_b
                w_a_2 = w_a*w_a
                w_b_2 = w_b*w_b
                w_a_b_1_all.append(w_a_b_1)
                w_a_2_all.append(w_a_2)
                w_b_2_all.append(w_b_2)
        w_a_b = sum(w_a_b_1_all)/(sum(w_a_2_all)**0.5*sum(w_b_2_all)**0.5)
        similarity[user_b].ix[count] = w_a_b
    count = count + 1
print(similarity[:5])

# 输出用户top5相似用户及其similarity
similarity_five = pd.DataFrame(index=data.axes[1])
similarity_five['one'] = 0
similarity_five['second'] = 0
similarity_five['third'] = 0
similarity_five['forth'] = 0
similarity_five['fifth'] = 0

count_five = 0
for user_a in similarity.axes[1]:
    similarity_test = similarity.sort(columns=user_a,ascending=False)
    similarity_5 = similarity_test.index[1:6]
#     print(similarity_5)
    for i in range(1,6):
        similarity_five['one'].ix[count_five] = similarity_5[0]
        similarity_five['second'].ix[count_five]= similarity_5[1]
        similarity_five['third'].ix[count_five] = similarity_5[2]
        similarity_five['forth'].ix[count_five] = similarity_5[3]
        similarity_five['fifth'].ix[count_five]= similarity_5[4]
    count_five = count_five + 1

# 对每个user计算每个item的评分，并输出评分前三
user_item_pre = pd.read_csv('rating_matrix_0.csv',index_col = 'name')
for user in data.axes[1]:
    for i in range(0, 24):
        if (data[user].ix[i] == 0):
            one = similarity_five.ix['815'].one
            second = similarity_five.ix['815'].second
            third = similarity_five.ix['815'].third
            forth = similarity_five.ix['815'].forth
            fifth = similarity_five.ix['815'].fifth
            one_score = (data[one].ix[i] - save_avg.ix[one].avg_count)*similarity.ix[user][one]
            second_score = (data[second].ix[i] - save_avg.ix[second].avg_count)*similarity.ix[user][second]
            third_score = (data[third].ix[i] - save_avg.ix[third].avg_count)*similarity.ix[user][third]
            forth_score = (data[forth].ix[i] - save_avg.ix[forth].avg_count)*similarity.ix[user][forth]
            fifth_score = (data[fifth].ix[i] - save_avg.ix[fifth].avg_count)*similarity.ix[user][fifth]
            sum_w = similarity.ix[user][one]+similarity.ix[user][second]+similarity.ix[user][third]+similarity.ix[user][forth]+similarity.ix[user][fifth]
            # 计算user对item i 的打分
            user_item_pre[user].ix[i]= save_avg.ix[user].avg_count+ (one_score+second_score+third_score+forth_score+fifth_score)/sum_w
        else:
            user_item_pre[user].ix[i] = 0
        i = i + 1


# recommendation top-3 items for each user
user_recomd_item = pd.DataFrame(index=data.axes[1])
user_recomd_item['item_one'] = 'null'
user_recomd_item['item_two'] = 'null'
user_recomd_item['item_three'] = 'null'
# user_recomd_item
count_three = 0
for user in similarity.axes[1]:
    user_item_pre_test = user_item_pre.sort(columns=user,ascending=False)
    user_item_pre_3= user_item_pre_test.index[0:3]
#     print(similarity_5)
    for i in range(0,3):
        user_recomd_item['item_one'].ix[count_three] = user_item_pre_3[0]
        user_recomd_item['item_two'].ix[count_three]= user_item_pre_3[1]
        user_recomd_item['item_three'].ix[count_three] = user_item_pre_3[2]
    count_three = count_three + 1

print(user_recomd_item[:24])




