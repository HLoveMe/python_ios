# -*- coding: utf-8 -*-
import sys
import os
import re

main_path=''
# 得到工程信息
def projectmsg(target):
    filepaths=os.listdir(target)
    isPro=False
    isPod=False
    proName=''
    podFile=''
    for i in filepaths:
        if 'xcodeproj' in i:
            isPro=True
            proName=os.path.join(main_path,i.split('.')[0])
        if 'xcworkspace' in i:
            isPod=True
        if 'Podfile'==i:
            podFile = os.path.join(main_path, i)
    if not isPro:
        return (False,False,[],"","")
    return (isPro,isPod,[os.path.join(target,A) for A in filepaths if  '.' not in A],proName,podFile)
# 得到pod库
def podFramework(podFile):
    framework=[]
    with open(podFile ,'rt') as file:
        for i in file:
            if 'pod' in i:
                res = re.search(r"'[a-zA-Z]+'",i)
                if res:
                    framework.append(res.group())

    return  framework
# 计算长度

ignorepath=["lproj","xcassets"]
ignorepath2=[]
oneIgnore=[]  # 被忽略的文件夹
count=0
linecontainsuffix=['.h','.m','.mm','.c','.cpp','.hpp','.swift']
countDic=dict.fromkeys(linecontainsuffix,0)

def fileLine(filepath):
    (a,b) = os.path.splitext(filepath)
    if b not in linecontainsuffix:
        return
    countDic[b]=countDic[b]+1
    with open(filepath, 'rt') as file:
        while True:
            one = file.read(1024 * 1024)
            if not one:
                break
            else:
                global count
                count += one.count('\n')

def statisticCount(target):
    if target in ignorepath2:
        return
    list = os.listdir(target)
    for i in range(len(ignorepath)):
        one=ignorepath[i]
        if i>=2:
            global  oneIgnore
            j=i-2
            if len(oneIgnore[j])<=2:
                oneIgnore[j]=os.path.join(target,one)
        for k in list:
            if one in k:
                list.remove(k)

    for i in list:
        i = os.path.join(target,i)
        if os.path.isdir(i):
            statisticCount(i)
        if os.path.isfile(i):
            fileLine(i)


"""  
    Pods / lproj  / xcassets / Test / UItest 不做统计

    调用说明
        python thisPy target 多个不做统计文件夹名/路径 ...(如果有重名的 将以第一次为准)

example:
    python ios_lines_tatistics.py /Users/zhuzihao/Desktop/speedVideo/SpeedVideo  Other
log:
    工程名: SpeedVideo
    包含: .h,.m,.mm,.c,.cpp,.hpp,.swift 文件,共有行: 21442
    忽略的文件夹: ['/Users/zhuzihao/Desktop/speedVideo/SpeedVideo/DerivedData/Other']
    包含文件 .h        78 个
    包含文件 .swift    0 个
    包含文件 .m        77 个
    包含文件 .c        0 个
    包含文件 .cpp      0 个
    包含文件 .hpp      0 个
    包含文件 .mm       0 个

"""
if __name__=="__main__":
    args = sys.argv[1:]
    if len(args)<1:
        raise  Exception("指定相应参数")
    target = sys.argv[1:][0]
    if len(args)>=2:
        ignore=sys.argv[1:][1:]
        oneIgnore=['' for i in range(len(ignore))]
        for one in ignore:
            if os.path.isdir(one):
                ignorepath2.append(one)
            else:
                ignorepath.append(one)
    main_path=target
    if not os.path.exists(target):
        pass
    elif os.path.isfile(target):
        fileLine(target)
        print "统计的文件",str(count),"行"
    else:
        isPro, isPod, proDics,proName, podFile = projectmsg(target)
        if isPod:
            # 得到pod 加载的第三方
            frames = podFramework(podFile)
        if isPro:
            for i in proDics:
                # statisticCount(proDic)
                if "Tests" in i or "UITests" in i or "Pods" in i:
                    pass
                else:
                    if os.path.isdir(i):
                        statisticCount(i)
                    else:
                        fileLine(i)

        else:
            statisticCount(target)

        for i in range(5):
            print "\n"
        if isPro:
            print "工程名:", os.path.basename(proName)
            print "包含:",",".join(linecontainsuffix),'文件,共有行:',str(count)
            if len(args)>=2:
                print '忽略的文件夹:',oneIgnore
            if isPod:
                print "pod 第三方框架", ','.join(frames)
        else:
            print "统计的文件夹下",str(count),'行'

        for x,y in countDic.items():
            print "包含文件",x,''.join([" " for i in range(len(x),8)]),str(y),"个"