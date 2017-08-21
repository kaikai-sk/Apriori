#-*-coding:utf-8-*-

def loadDataSet():
    return [[1,3,4],[2,3,5],[1,2,3,5],[2,5]]

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
def apriori(dataSet,minSupport=0.5):
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
    #满足最小可信度要求的规则列表
    prunedH=[];
    for conseq in H:
        conf=supportData[freqSet]/supportData[freqSet-conseq]
        '''
        此处应该还有条件，就是要保证时序
       '''
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

if __name__=='__main__':
    dataSet = loadDataSet()
    L,supportData=apriori(dataSet);
    rules=generateRules(L,supportData)
    print rules


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