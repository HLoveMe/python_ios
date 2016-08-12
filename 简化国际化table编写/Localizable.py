# -*- coding: utf-8 -*-
import os
import sys
import re

def get_source_path(path):
    paths = os.listdir(path)
    for one in paths:
        dir = os.path.join(path,one)
        if os.path.isfile(dir):
            pass
        else:
            if one=="Localizable":
                return dir
            source = get_source_path(dir)
            if None != source:
                return source

def update(texts,paths):
    for one in paths:
        path = os.path.join(one,"Localizable.strings")
        if os.path.exists(path):
            with open(path,'w') as file:
                for line in texts:
                    result = re.search(r'.+=.+', line)
                    if result:
                        if "Base.lproj" in one or "en.lproj" in one:
                            en = line.split("=")[0]
                            content = en+"="+en+";\n"
                            file.write(content)
                        else:
                            print "only englisg zh"
                            break
                    else:
                        file.write(line)
                        
"""
    python aa.py  oc工程目录

    1:创建工程 中多语言文件
    2:在国际化内容特别多时 修改也特别麻烦
       您只需要 修改对应中文文件（Localizable.strings(Chinese(Simplified))）
    3：该文件会根据中文文件  来修改英文(Localizable.string(English))和Base(Localizable.string(Base))
        example:
            中文:   "OK"="好的";
            en :   "OK"="OK";
            Base:  "OK"="OK";
        并保持注释不变
"""

if __name__=="__main__":
    path =  sys.argv[1]
    if os.path.isdir(path):
        path = get_source_path(path)
        print "得到的国际化文件夹,",path
        names = os.listdir(path)
        if names.__contains__("zh-Hans.lproj"):
            one = os.path.join(os.path.join(path,"zh-Hans.lproj"),"Localizable.strings")
            names.remove("zh-Hans.lproj")
            texts=[]
            with open(one,'rt') as file:
                line = file.readline()
                while not line=="":
                    texts.append(line)
                    line=file.readline()
            update(texts,[os.path.join(path,i) for i in names])
        else:
            pass
