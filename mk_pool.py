import re

f = open('poetry.txt', encoding='UTF-8')
r = []
while 1:
    this = f.readline()
    this = re.split("，|。|？|！|：", this)
    # print(this)
    for thi in this:
        if len(thi) == 7 and '月' in thi:
            print(thi)
            c = input('要使用这个句子吗？')
            if c == 'y':
                r.append(thi)
                if len(r) == 100:
                    break

    if len(r) == 100:
        break

with open('./pool.txt', mode='w', encoding='UTF-8') as p:
    for _ in r:
        p.write(_ + '\n')
