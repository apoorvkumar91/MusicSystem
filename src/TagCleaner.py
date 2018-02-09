import pandas as pd
import collections
import os
from nltk.stem import PorterStemmer
import operator
import matplotlib.pyplot as plt
import threading
import copy

stemCache = {}
class myThread(threading.Thread):
  def __init__(self,FileNumber,startime,endtime):
    threading.Thread.__init__(self)
    self.startime = startime
    self.endtime = endtime
    self.FileNumber = FileNumber

  def run(self):
    self.Retagger()
  
  def doStemming(self,w):
    return w
    if w in stemCache:
        return stemCache[w]
    stemmer = PorterStemmer()
    retVal = stemmer.stem(w)
    stemCache[w] = retVal
    return retVal

  def GetNewTag(self,inTag):
    i = inTag
    i = i.replace('[', '')
    i = i.replace(']', '')
    i = i.replace('u\'', '')
    i = i.replace('\'', '')
    i = i.replace(' ', '#')
    i = i.replace(',#', ' ')
    emptyTag = '$$NOTAG$$'
    if not len(i):
        return emptyTag

    i = i.lstrip().rstrip().lower()
    iList = i.split()
    newTaglist = []
    for t in set(iList):
        t = t.replace('#', ' ')
        tSubList = t.split()
        tSortedList = []
        for w in tSubList:
            tSortedList.append(self.doStemming(w))
        tSortedList.sort()
        newTag = " ".join(tSortedList)
        newTaglist.append(newTag)
    return "##".join(newTaglist)

  def tagCleaner(self,start_time,end_time):
    emptyTag = '$$NOTAG$$'
    base_directory = '/Users/sidverma/Desktop/IR/'
    os.chdir(base_directory)
    #merge two files
    df = pd.read_csv('FinalTagroomFile.csv')
    #start reading Tagscols
    tagsCol = df['tags']
    index = 0
    tags_list=[]
    print "Thread " + str(self.FileNumber) + "started"
    for i in tagsCol[start_time:end_time]:
        # if index == 20:
        #     print "Exitting!"
        #     df.to_csv('Final0-2999.csv')
        #     return
        #print "Initial Tag: ", i
        if index%1000 == 0:
            print '-------------------'
            print index, ' ', newTag  
            print '-------------------'

        if i == '[]' or (not isinstance(i, str)):
            tags_list.append(emptyTag)
            #df.set_value(index, 'Tags', emptyTag)
            index += 1
            continue
        else:
            newTag = self.GetNewTag(i)
            tags_list.append(newTag)
            #df.set_value(index, 'Tags', newTag)
            index += 1

    df2 = pd.DataFrame(
           data={"Tags": tags_list,
                 },columns=["Tags"])
    df2.to_csv("FinalTagCleaner" + str(self.FileNumber) + ".csv")
    return

  def mergCSV(self):
    base_directory = '/Users/sidverma/Desktop/IR/'
    os.chdir(base_directory)
    tags_list=[]
    df = pd.read_csv('FinalTagCleaner0.csv')
    df1 = pd.read_csv('FinalTagCleaner1.csv')
    df2 = pd.read_csv('FinalTagCleaner2.csv')
    df3 = pd.read_csv('FinalTagCleaner3.csv')
    df4 = pd.read_csv('FinalTagCleaner4.csv')
    df5 = pd.read_csv('FinalTagCleaner5.csv')
    tags_list = df['Tags']
    print len(tags_list)
    tags_list = tags_list.append(df1['Tags'])
    print len(tags_list)
    tags_list = tags_list.append(df2['Tags'])
    print len(tags_list)
    tags_list = tags_list.append(df3['Tags'])
    print len(tags_list)
    tags_list = tags_list.append(df4['Tags'])
    print len(tags_list)
    tags_list = tags_list.append(df5['Tags'])
    print len(tags_list)
    dfNew = pd.DataFrame(
           data={"Tags": tags_list,
                 },columns=["Tags"])
    dfNew.to_csv("FinalTagroomMerged.csv")

    splitList = []
    for i in tags_list:
        iList = i.split('##')
        for tg in iList:
            splitList.append(tg)

    return collections.Counter(splitList)

  def getTagFreqDict(self):
    # base_directory = '/Users/sidverma/Desktop/'
    # os.chdir(base_directory)
    # globalTags = []
    # df = pd.read_csv('Final0-2999.csv')
    # tagsCol = df['Tags']
    # index = 0
    # emptyTag = '$$NOTAG$$'
    # for i in tagsCol:
    #     iList = i.split()
    #     for t in iList:
    #         globalTags.append(t)
    # return collections.Counter(globalTagsList)
    
    df = pd.read_csv('FinalTagroomMerged.csv')
    #start reading Tagscols
    tagsCol = df['tags']
    index = 0
    tags_list=[]
    print "Thread " + str(self.FileNumber) + "started"
    for i in tagsCol[start_time:end_time]:
        if index%1000 == 0:
            print '-------------------'
            print index, ' ', newTag  
            print '-------------------'
        iList = i.split('##')
        for tg in iList:
            tags_list.append(tg)
        index += 1

  def Retagger(self):
    freqDict = self.mergCSV()
    print 'Done merg@'
    lists = sorted(freqDict.items(), key=operator.itemgetter(1), reverse = True)
    i = 0
    pop_tags = []
    for tup in lists:
        pop_tags.append(tup[0])
        i += 1
        if i == 1001:# if tup[1] < 1000:
            break
    pop_tags.pop(0)
    pop_tags.sort()
    print 'PopTags Len:: ',len(pop_tags)
    for i in pop_tags:
        print i
        print '-------------'
    print 'done'
    print 'start retaggin'
    base_directory = '/Users/sidverma/Desktop/IR/'
    os.chdir(base_directory)
    tags_list=[]
    df = pd.read_csv('FinalTagroomMerged.csv')
    final = pd.read_csv('Final.csv')
    tags_list = df['Tags']
    tags_list_New = []
    index = 0
    for i in tags_list:
        newStripTagVec = []
        iList = i.split('##')
        for tmplateTag in pop_tags:
            if tmplateTag in set(iList):
                newStripTagVec.append(1)
            else:
                newStripTagVec.append(0)
        print len(newStripTagVec)
        newStripTagStr = '$'.join(str(x) for x in newStripTagVec)
        tags_list_New.append(newStripTagStr)
    print 'done retagging list genrtr'
    for l in tags_list_New:
        if len(l) > 1000:
            print "Error"

    print "OK. Writing now...."
    my_df = pd.DataFrame()
    my_df['Songs'] = final.Songs    
    my_df['Tags'] = tags_list_New
    # dfNew = pd.DataFrame(
    #        data={"Tags": pd.Series(tags_list_New),
    #              },columns=["Tags"])
    my_df.to_csv("FinalTagroomMergedVecs.csv")
    print 'Done dona don'

    #self.getTagFreqDict(self.startime,self.endtime)
    #print 'cleaning Tags done'
    #freqDict = getTagFreqDict()
    #print len(freqDict)
    '''
    lists = sorted(freqDict.items(), key=operator.itemgetter(1), reverse = True)
    i = 0
    pop_tags = []
    for tup in lists:
        i += 1
        if i == 1000:# if tup[1] < 1000:
            break
    lists = lists[:i]
    f = open('poptags', 'w')
    for tu in lists :
        f.write(str(tu[0])+'\n')
    print 'done'
    f.close()
    '''

threads  =[]
threadscount = [5]
for itr in threadscount:
    threads.append(myThread(itr,itr*100000,(itr*100000)+84938))
print "It has started"
for itr in range(0,1):
    threads[itr].start()



# xTicks, y = zip(*lists) # unpack a list of pairs into two tuples
# #plt.figure(figsize = (90,30))
# x = xrange(len(lists))
# plt.xticks(x, xTicks, rotation=90)
# # plt.plot(x,y)
# plt.bar(x, y, color='b')
# plt.show()
# print 'done'