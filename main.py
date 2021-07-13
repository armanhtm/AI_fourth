import math
import re

# store bad comments
bad_comments = open('rt-polarity.neg', encoding='utf-8').readlines()
# store good comments
good_comments = open('rt-polarity.pos', encoding='utf-8').readlines()

bad_comments_final = []
good_comments_final = []


def remove_non_letter(text):
    text = re.sub("[^a-zA-Z0-9 -]+", "", text)
    text = text.replace('-', ' ')
    return text


for i in bad_comments:
    bad_comments_final.append(remove_non_letter(i))
for i in good_comments:
    good_comments_final.append(remove_non_letter(i))

bad_comments_lines = len(bad_comments_final)
good_comments_lines = len(good_comments_final)

bad_comments_test = []
good_comments_test = []

test_lines = math.floor(0.05 * (bad_comments_lines + good_comments_lines))

for i in range(test_lines):
    bad_comments_test.append(bad_comments_final[i])
    del bad_comments_final[i]
    good_comments_test.append(good_comments_final[i])
    del good_comments_final[i]


def calculate_number_of_word(list):
    counter = 0
    for i in list:
        counter += len(i.split())
    return counter


bad_comments_number = calculate_number_of_word(bad_comments_final)
good_comments_number = calculate_number_of_word(good_comments_final)


def calculate_occurrence(list, word):
    occurrence = 0
    for i in list:
        for j in i.split():
            if word == j:
                occurrence += 1
    return occurrence


def unigram(list, number):
    dict = {}
    for i in list:
        for j in i.split():
            if j not in dict:
                dict[j] = calculate_occurrence(list, j) / number
    return dict


bad_comments_unigram = unigram(bad_comments_final, bad_comments_number)
good_comments_unigram = unigram(good_comments_final, good_comments_number)


def calculate_occurrence_of_two_words(list, sentence):
    occurrence = 0
    for i in list:
        occurrence += i.count(sentence)
    return occurrence


def bigram(list, unigram_dict, word_num):
    dict = {}
    for i in list:
        temp = i.split()
        for i in range(len(temp) - 1):
            if temp[i] + ' ' + temp[i + 1] not in dict:
                # for start and end character
                if i == 0 or i == len(temp) - 1:
                    dict[temp[i]] = (unigram_dict[temp[i]] * word_num) / len(list)
                else:
                    dict[temp[i] + ' ' + temp[i + 1]] = calculate_occurrence_of_two_words(list, temp[i] + ' ' + temp[
                        i + 1]) / (unigram_dict[temp[i]] * word_num)

    dict[temp[0] + ' ' + temp[1]] = calculate_occurrence_of_two_words(list, temp[0] + ' ' + temp[1]) / (
            unigram_dict[temp[0]] * word_num)
    return dict


# bad_comments_bigram = bigram(bad_comments_final, bad_comments_unigram, bad_comments_number)
# good_comments_bigram = bigram(good_comments_final, good_comments_unigram, good_comments_number)


# def backoff(test_comments, unigram_dict, bigram_dict, text, x1, x2, x3, e):
#     sum = 1
#     string = text.split()
#     for i in range(len(string)):
#         if i == 0 or i == len(string) - 1:
#             if string[i] not in bigram_dict:
#                 unigram_counter = 1
#                 bigram_counter = 0
#             else:
#                 unigram_counter = 1
#                 bigram_counter = bigram_dict[string[i]]
#         else:
#             value = string[i] + ' ' + string[i + 1]
#             if value in bigram_dict and string[i] in unigram_dict:
#                 unigram_counter = unigram_dict[string[i]]
#                 bigram_counter = bigram_dict[value]
#             elif value in bigram_dict and string[i] not in unigram_dict:
#                 unigram_counter = 0
#                 bigram_counter = bigram_dict[value]
#             elif value not in bigram_dict and string[i] in unigram_dict:
#                 unigram_counter = unigram_dict[string[i]]
#                 bigram_counter = 0
#             else:
#                 unigram_counter = 0
#                 bigram_counter = 0
#         sum = sum * (x3 * bigram_counter + x2 * unigram_counter + x1 * e)
#
#     value = string[0] + ' ' + string[1]
#     if value in bigram_dict and string[0] in unigram_dict:
#         unigram_counter_specific = unigram_dict[string[0]]
#         bigram_counter_specific = bigram_dict[value]
#     elif value in bigram_dict and string[0] not in unigram_dict:
#         unigram_counter_specific = 0
#         bigram_counter_specific = bigram_dict[value]
#     elif value not in bigram_dict and string[0] in unigram_dict:
#         unigram_counter_specific = unigram_dict[string[0]]
#         bigram_counter_specific = 0
#     else:
#         unigram_counter_specific = 0
#         bigram_counter_specific = 0
#     sum = sum * (x3 * bigram_counter_specific + x2 * unigram_counter_specific + x1 * e)
#     return sum
#
#
# def accuracy_score_bigram(x1, x2, x3, e):
#     counter = 0
#     for i in bad_comments_test:
#         value1 = backoff(bad_comments_final, bad_comments_unigram, bad_comments_bigram, i, x1, x2, x3, e)
#         value2 = backoff(good_comments_final, good_comments_unigram, good_comments_bigram, i, x1, x2, x3, e)
#         if value1 > value2:
#             counter += 1
#     for i in good_comments_test:
#         value1 = backoff(bad_comments_final, bad_comments_unigram, bad_comments_bigram, i, x1, x2, x3, e)
#         value2 = backoff(good_comments_final, good_comments_unigram, good_comments_bigram, i, x1, x2, x3, e)
#         if value1 < value2:
#             counter += 1
#
#     return counter / (bad_comments_number + good_comments_number)
#

#output1 = accuracy_score(0.34, 0.33, 0.33, 0.2)
#print(output1)
def accuracy_score_unigram(string):
    temp = string.split()
    value1 = 1
    value2 = 1
    for i in temp:
        value1 = value1 * bad_comments_unigram[i]
        value2 = value2 * good_comments_unigram[i]
    if value1 > value2:
        return "filter this"
    else:
        return "not filter this"

print("ready to go\nenter your message")
while(1):
    string = input()
    if string == "!q":
        break
    string = remove_non_letter(string)
    print(accuracy_score_unigram(string))


