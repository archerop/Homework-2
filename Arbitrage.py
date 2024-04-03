from operator import itemgetter, attrgetter
liquidity = {
    ("tokenA", "tokenB"): (17, 10),
    ("tokenA", "tokenC"): (11, 7),
    ("tokenA", "tokenD"): (15, 9),
    ("tokenA", "tokenE"): (21, 5),
    ("tokenB", "tokenC"): (36, 4),
    ("tokenB", "tokenD"): (13, 6),
    ("tokenB", "tokenE"): (25, 3),
    ("tokenC", "tokenD"): (30, 12),
    ("tokenC", "tokenE"): (10, 8),
    ("tokenD", "tokenE"): (60, 25),
}

def getAmountOut(amountIn, reserveIn, reserveOut):
        amountInWithFee = amountIn*997
        numerator = amountInWithFee*reserveOut
        denominator = reserveIn*1000+amountInWithFee
        amountOut = numerator / denominator
        return amountOut

def getAmountIn(amountOut, reserveIn, reserveOut):
        numerator = reserveIn*amountOut*1000
        denominator = (reserveOut-amountOut)*997
        amountIn = (numerator / denominator)+1
        return amountIn

def DFS(start,end,visit,token,tokenamount,tmppath,path):
    tmppath+=start
    #visit[start]=1
    for key,value in token[start].items():
        if(key==end):
            reserveIn = 0
            reserveOut = 0
            if liquidity.get(("token"+start,"token"+key)):
                reserveIn = liquidity[("token"+start,"token"+key)][0]
                reserveOut = liquidity[("token"+start,"token"+key)][1]
            else:
                reserveIn = liquidity[("token"+key,"token"+start)][1]
                reserveOut = liquidity[("token"+key,"token"+start)][0]
            amountout=getAmountOut(tokenamount, reserveIn, reserveOut)
            path.append((tmppath,amountout))
        elif not visit.get(start+key):
        #elif not visit.get(key):
            reserveIn = 0
            reserveOut = 0
            if liquidity.get(("token"+start,"token"+key)):
                reserveIn = liquidity[("token"+start,"token"+key)][0]
                reserveOut = liquidity[("token"+start,"token"+key)][1]
            else:
                reserveIn = liquidity[("token"+key,"token"+start)][1]
                reserveOut = liquidity[("token"+key,"token"+start)][0]
            visit[start+key]=1
            visit[key+start]=1
            amountout=getAmountOut(tokenamount, reserveIn, reserveOut)
            DFS(key,end,visit,token,amountout,tmppath,path)
            visit.pop(start+key)
            visit.pop(key+start)
            #visit.pop(key)
    return

pathtokenamount=[]

def checkpath(path,tokenamount):
    for i in range(len(path)-1):
        reserveIn = 0
        reserveOut = 0
        if liquidity.get(("token"+path[i],"token"+path[i+1])):
            reserveIn = liquidity[("token"+path[i],"token"+path[i+1])][0]
            reserveOut = liquidity[("token"+path[i],"token"+path[i+1])][1]
        else:
            reserveIn = liquidity[("token"+path[i+1],"token"+path[i])][1]
            reserveOut = liquidity[("token"+path[i+1],"token"+path[i])][0]
        amountin=tokenamount
        amountout=getAmountOut(tokenamount, reserveIn, reserveOut)
        pathtokenamount.append((amountin,amountout))
        tokenamount=amountout
    return

token = {
    "A" : {},
    "B" : {},
    "C" : {},
    "D" : {},
    "E" : {},
}

path = []

for key, value in liquidity.items():
    #print(key)
    #print(value)
    token[key[0][5]].update({key[1][5]:value[1]/value[0]})
    token[key[1][5]].update({key[0][5]:value[0]/value[1]})
#print(token)
visit={}
DFS("B","B",visit,token,5,"",path)
#print(token)
path=sorted(path, key=itemgetter(1))
#print(path)
maxi=-1024
ans = []
for i in path:
    if(i[1]>maxi):
        maxi=i[1]
        ans=i
#print(ans)
print("path: ", end='')
for i in ans[0]:
    print("token"+i+"->", end='')
print("tokenB, balance="+str(ans[1]))
#print(path[-1:])
checkpath("BACEDCB",5)
print(pathtokenamount)
'''
final={}
while(path[-1]>1):
    inamount=path[-1]-path[-2]
    for i in len(path[-1][0]):
        tokenamount=
        if i+1<len(path[-1][0]):
            swap()
'''