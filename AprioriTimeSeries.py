#-*-coding:utf-8-*-
from pandas import *

def loadSolidDataSet():
    return [[1,3,4],[2,3,5],[1,2,3,5],[2,5]]

def loadDataSet(filePath):
    file = open(filePath)
    lineIndex=0
    retList=[]
    while 1:
        lines = file.readlines()
        if not lines:
            break
        for line in lines:
            if lineIndex==0:
                lineIndex+=1;
                continue
            lineIndex+=1;
            retList.append(line.strip().split(','))
    return retList

'''
    构建C1,大小为1的所有获选项集的集合
'''
def createC1(dataSet):
    C1=[]
    for transaction in dataSet:
        for item in transaction:
            if(not [item] in C1):
                C1.append([item])
    C1.sort();
    #冰冻的集合，用户不可更改它
    return map(frozenset,C1);

'''
    生成Lk
'''
def scanD(D,Ck,minSupport):
    ssCnt={}
    for tid in D:
        for can in Ck:
            if(can.issubset(tid)):
                if correspondToTimeSeriesFrozenset(can,tid)==True:
                    if(not ssCnt.has_key(can)):
                        ssCnt[can]=1;
                    else:
                        ssCnt[can]+=1;
    numItems=float(len(D))
    retList=[];
    supportData={}
    for key in ssCnt:
        support=ssCnt[key]/numItems;
        if(support>=minSupport):
            retList.insert(0,key)
        supportData[key]=support;
    return retList,supportData

'''
 通过对Lk-1进行组合 creates Ck
'''
def aprioriGen(Lk,k):
    retList=[]
    lenLk=len(Lk)

    for i in range(lenLk):
        for j in range(i+1,lenLk):
            L1=list(Lk[i])[:k-2]
            L2=list(Lk[j])[:k-2]
            if(L1==L2):
                retList.append(Lk[i] | Lk[j])
    return retList

'''
    生成所有的频繁项集，及其对应的支持度
'''
def apriori(dataSet,minSupport=0.35):
    C1=createC1(dataSet);
    D=map(set,dataSet)
    L1,supportData=scanD(D,C1,minSupport)
    L=[L1]
    k=2;
    while(len(L[k-2])>0):
        Ck=aprioriGen(L[k-2],k)
        Lk,supK=scanD(D,Ck,minSupport)
        supportData.update(supK)
        L.append(Lk)
        k+=1;
    return L,supportData

def generateRules(L,supportData,minConf=0.7):
    bigRuleList=[]
    for i in range(1,len(L)):
        for freqSet in L[i]:
            H1=[frozenset([item]) for item in freqSet]
            if i>1:
                rulesFromConseq(freqSet,H1,supportData,bigRuleList,minConf)
            else:
                calcConf(freqSet,H1,supportData,bigRuleList,minConf)
    return bigRuleList

'''
    对规则进行评估
'''


def calcConf(freqSet, H, supportData, br1, minConf=0.7):
    #print 'supportData:',supportData
    #满足最小可信度要求的规则列表
    prunedH=[];
    for conseq in H:
        #print 'debug info:',supportData[freqSet],
        #conf=supportData[freqSet]/supportData[freqSet-conseq]
        conf=supportData.get(freqSet,0)/supportData.get(freqSet-conseq,10000000000000000)
        if conf>=minConf:
            print freqSet-conseq,'---->',conseq,'conf:',conf
            br1.append((freqSet-conseq,conseq,conf))
            prunedH.append(conseq)
    return prunedH

'''
    生成候选规则集
'''
def rulesFromConseq(freqSet, H, supportData, br1, minConf=0.7):
    m=len(H[0])
    if(len(freqSet)>m+1):
        Hmp1=aprioriGen(H,m+1)
        Hmp1=calcConf(freqSet,Hmp1,supportData,br1,minConf)
        if(len(Hmp1)>1):
            rulesFromConseq(freqSet,Hmp1,supportData,br1,minConf)

'''
    检测一个频繁项集，是否符合时序关系
'''
def correspondToTimeSeriesFrozenset(freqSet, dataSet):
    index=-1;
    preIndex=-1;
    for item in freqSet:
            if item in dataSet:
                index=list(dataSet).index(item);
                if index<=preIndex:
                    return False
                preIndex=index
            else:
                continue
    return True;



'''
    检测一个频繁项集，是否符合时序关系
'''
def correspondToTimeSeriesList(freqSet, dataSet):
    index=-1;
    preIndex=-1;
    for item in freqSet:
        for line in dataSet:
            if item in line:
                index=line.index(item);
                if index>preIndex:
                    return True
                preIndex=index
            else:
                continue
    return False;

'''
    根据时序关系删减规则
'''
def pruneRules(rules,dataSet):
    prunedIndexList=[]
    index=0
    for item in rules:
        line=list(item[0])+list(item[1])
        if False==correspondToTimeSeriesList(line,dataSet):
            prunedIndexList.append(index)
        index+=1
    prunedIndexList.reverse();
    print prunedIndexList
    for index in prunedIndexList:
        rules.remove(index)
    return rules

if __name__=='__main__':
    filePath = 'C:\\Users\\shankai\\Desktop\\trace_input.csv_sk.csv';
    dataSet=loadDataSet(filePath)
    L,supportData=apriori(dataSet,minSupport=0.01);
    rules=generateRules(L,supportData,minConf=0.1);
    print rules.__len__()
    #print rules
    # rules=pruneRules(rules,dataSet)
    # print '-------------------------------------------------------------------------------------------------'
    # print rules.__len__()
    # print rules


    # dataSet=loadSolidDataSet();
    # L,supportData=apriori(dataSet,minSupport=0.5)
    # rules=generateRules(L,supportData,minConf=0.5)
    # print rules

    # dataSet = loadDataSet()
    # L,supportData=apriori(dataSet);
    # print L[0]
    # print L[1]
    # print L[2]
    # print L[3]

    # dataSet = loadDataSet()
    # C1 = createC1(dataSet)
    # print C1
    # D = map(set, dataSet)
    # print D
    # L1,supportData0 = scanD(D, C1, 0.5)
    # print L1