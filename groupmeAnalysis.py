import json
from collections import namedtuple
import datetime
import pandas as pd
import os

# some JSON:

def bin_f(x):
    if x.time() < datetime.time(1):
        return "00:00-00:59"
    elif x.time() < datetime.time(2):
        return "01:00-01:59"
    elif x.time() < datetime.time(3):
        return "02:00-02:59"
    elif x.time() < datetime.time(4):
        return "03:00-03:59"
    elif x.time() < datetime.time(5):
        return "04:00-04:59"
    elif x.time() < datetime.time(6):
        return "05:00-05:59"
    elif x.time() < datetime.time(7):
        return "06:00-06:59"
    elif x.time() < datetime.time(8):
        return "07:00-07:59"
    elif x.time() < datetime.time(9):
        return "08:00-08:59"
    elif x.time() < datetime.time(10):
        return "09:00-09:59"
    elif x.time() < datetime.time(11):
        return "10:00-10:59"
    elif x.time() < datetime.time(12):
        return "11:00-11:59"
    elif x.time() < datetime.time(13):
        return "12:00-12:59"
    elif x.time() < datetime.time(14):
        return "13:00-13:59"
    elif x.time() < datetime.time(15):
        return "14:00-14:59"
    elif x.time() < datetime.time(16):
        return "15:00-15:59"
    elif x.time() < datetime.time(17):
        return "16:00-16:59"
    elif x.time() < datetime.time(18):
        return "17:00-17:59"
    elif x.time() < datetime.time(19):
        return "18:00-18:59"
    elif x.time() < datetime.time(20):
        return "19:00-19:59"
    elif x.time() < datetime.time(21):
        return "20:00-20:59"
    elif x.time() < datetime.time(22):
        return "21:00-21:59"
    elif x.time() < datetime.time(23):
        return "22:00-22:59"
    else:
        return "23:00-23:59"

def customMessageDecoder(messageDict):
    return namedtuple('X', messageDict.keys())(*messageDict.values())

with open("transcriptAA.json", "r") as file:
    data = file.read()

messages = json.loads(data, object_hook=customMessageDecoder)

tempList = []
idList = []
for x in messages: 
    if x.user_id not in tempList:
        tempList.append(x.user_id)
        idList.append((x.name, x.user_id))

for y in idList:
    sentence = ""
    for x in messages:
        if x.user_id == y[1]:
            sentence += str(x.text) + " "
    wordList = sentence.split()
    temp = pd.Series(wordList).value_counts().sort_values(ascending=False)
    temp.to_csv('D:/GroupmeApp/wordFrq/' + str(y[0]) + ' Word Frequency.csv', encoding='utf-8', index=True)

sentence = ""
for x in messages: 
    sentence += str(x.text) + " "
    
wordList = sentence.split()

x = pd.Series(wordList).value_counts().sort_values(ascending=False)
x.to_csv('D:/GroupmeApp/wordFrq/Word Frequency.csv', encoding='utf-8', index=True)

likesRecived = []
seenUID = []

for x in messages:
    if x.user_id not in seenUID:
        seenUID.append(x.user_id)
        likesRecived.append((x.name, x.user_id, len(x.favorited_by)))
    else:
        for y in likesRecived:
            if y[1] == x.user_id:
                s = list(y)
                s[2] = s[2] + len(x.favorited_by)
                likesRecived[likesRecived.index(y)] = tuple(s)

likesRecived.sort(key=lambda tup: tup[2],reverse=True)

likesRecivedKeep = likesRecived

with open("D:/GroupmeApp/likes/likesRecived.csv", "w", encoding='utf-8') as file:
    file.write('Total Likes Recived\n')
    for y in likesRecived:
         file.write(str(y[0]) + "," + str(y[2]) + '\n')


likesGiven = []
seenUID = []
x1 = 0
for x in messages:
    for z in x.favorited_by:
        if z not in seenUID:
            seenUID.append(z)
            for p in idList:
                if z == p[1]:
                    likesGiven.append((p[0], z, 1))
        else:
            for y in likesGiven:
                if y[1] == z:
                    s = list(y)
                    s[2] = s[2] + 1
                    likesGiven[likesGiven.index(y)] = tuple(s)

likesGiven.sort(key=lambda tup: tup[2],reverse=True)

with open("D:/GroupmeApp/likes/likesGiven.csv", "w", encoding='utf-8') as file:
    file.write('Total Likes Given\n')
    for y in likesGiven:
        file.write((y[0]) + "," + str(y[2]) + '\n')

numPosts = []
seenUID = []
for x in messages:
    if x.user_id not in seenUID:
        seenUID.append(x.user_id)
        numPosts.append((x.name, x.user_id, 1))
    else:
        for y in numPosts:
            if y[1] == x.user_id:
                s = list(y)
                s[2] = s[2] + 1
                numPosts[numPosts.index(y)] = tuple(s)

numPosts.sort(key=lambda tup: tup[2],reverse=True)

numPostKeep = numPosts

#likePercent = []
#for x in numPostKeep:
#    likePercent.append((x[0],likesRecived[likesRecived.index(y)][2]/x[2]))
#    
#likePercent.sort(key=lambda tup: tup[1],reverse=True)

#with open("D:/GroupmeApp/likes/likePercent.csv", "w", encoding='utf-8') as file:
#    file.write('like Percent\n')
#    for y in likePercent:
#        file.write((y[0]) + "," + str(y[1]) + '\n')

with open("D:/GroupmeApp/posts/numPosts.csv", "w", encoding='utf-8') as file:
    file.write('Total Posts Made\n')
    for y in numPosts:
        file.write((y[0]) + "," + str(y[2]) + '\n')

timeList = []
#group activity time
for x in messages:
    time = datetime.datetime.fromtimestamp(x.created_at, datetime.timezone(datetime.timedelta(hours=-6)))
    timeList.append(bin_f(time))

x = pd.Series(timeList).value_counts().sort_index()
x.to_csv('D:/GroupmeApp/time/postTime.csv', encoding='utf-8', index=True)

    

