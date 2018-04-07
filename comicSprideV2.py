#!/usr/bin/pyenv python
# -*- coding:utf-8 -*-

# ------------------------------------------------------ #
# --  the code is using for download comics from the  -- #
# --  http://www.omanhua.com/comic                    -- #
# ------------------------------------------------------ #

import re
import os
import urllib2
import urllib
import time

# get the html info for given website
def getHtml(url):
    page = urllib2.urlopen(url)
    html = page.read()
    return html

# get the file list for all images in this chapter
def getFileList(html):
    reg = 'var pVars = pVars(.+?)\n</script>'
    scriptReg = re.compile(reg, re.M)
    scripts = re.findall(scriptReg, html)
    script =scripts[0]

    reg2 = ':\[(".+?")\],'
    listNumsReg = re.compile(reg2)
    listNums = re.findall(listNumsReg, script)
    listNum = listNums[0]
    listNum = listNum.replace('\"', '')
    keyLists = re.split(',', listNum)

    reg3 = ',\'(jpg.+?)\'.split'
    infoReg = re.compile(reg3, re.M)
    infos = re.findall(infoReg, script)
    imagList = []
    if infos:
        infoList = re.split('\|', infos[0])
        print len(infoList)
        listDict = createDict(infoList)
        for key in keyLists:
            imagList.append(listDict[key])
    return imagList

# create dict for the url Information
def createDict(infoList):
    i = 0
    listDict = {}
    for info in infoList:
        if (i < 10):
            key = str(i)+'.0'
        elif (i < 36):
            key = chr(ord('a')+i - 10)+'.0'
        else:
            key = chr(ord('A')+i -36)+'.0'
        listDict[key] = info
        i = i + 1

    return listDict

# get the image url and download the picture
def getImagUrls(html):

    # this is the address for website store the picture
    # it should be change for different website
    baseImageUrl = "http://pic.fxdm.cc/tu/undefined/"
    downloadDir = '/Users/hxia/Pictures/comics'
    # TODO : should get the chapter and the name of comic in the upper webside
    # get the name of comic
    reg = '<h1><a href=".+?">(.+?)</a>'
    # reg = 'var pVars = pVars(.+?)\n</script>'
    titleReg = re.compile(reg, re.M)
    titleLists = re.findall(titleReg, html)
    comicName = titleLists[0]

    # get the chapter
    reg2 = '<h2>(.+?)</h2>'
    chapterReg = re.compile(reg2)
    chapterLists = re.findall(chapterReg, html)
    chapter = chapterLists[0]
    #print baseImageUrl + "/"+comicName+ "/" + chapter

    imagList =getFileList(html)
    imagUrls =[]
    page = 1
    for image in imagList:
        imageUrl = baseImageUrl + comicName + "/" + chapter+'/'+image+'.jpg'
        imagUrls.append(imageUrl)
        print imageUrl
        os.chdir(downloadDir)
        if not os.path.exists(comicName):
            os.mkdir(comicName)
        if not os.path.exists(comicName+"/"+chapter):
            os.mkdir(comicName+"/"+chapter)
        if page < 10:
            pageNum = '0' + str(page)
        else:
            pageNum = str(page)
        downLoadPath = comicName+"/"+chapter+"/page"+pageNum+".jpg"
        urllib.urlretrieve(imageUrl, downLoadPath)
        page = page + 1
    return imagUrls

# get the url for all the chapter
def getUrlsChapters(html):
    reg = '<li><a href=\'/.+?/.+?/(.+?)/\' title'
    chaptersReg = re.compile(reg, re.M)
    chaptersLists = re.findall(chaptersReg, html)
    # for chapter in chaptersLists:
    #    print chapter
    return chaptersLists

if __name__ == '__main__':
    # the start url is the main direction of the comics
    #  here is the '一人之下'
    mainUrl = "http://www.omanhua.com/comic/17521/"
    # the download dir
    mainDownloadDir = "/Users/hxia/Pictures/comic"
    # *************************************************************************** #
    # ** start from the latest chapter
    # ** format [startChapter, chapterNum, step]
    # ** ps: if set Number is -1 or bigger than all will download all
    # **     step be set 1 in general stand download from the newest chapter
    # **     if you want start from oldest chapter please set step is -1
    # ** Be Notice: 1 is stand the first chapter (no matter step is 1 or -1)
    # **            for positive step  1 is the newest chapter
    # **            for negative step  1 is the oldest chapter
    # ** Warning: do not set the start chapter is  0 it will be some mistake
    # *************************************************************************** #
    downloadRange = [1, 10, 1]

    htmlMain = getHtml(mainUrl)
    print htmlMain
    chaptersLists = getUrlsChapters(htmlMain)

    if downloadRange[2] > len(chaptersLists) or downloadRange[2] == -1:
        downloadRange[2] = len(chaptersLists)
    step = downloadRange[2]
    sign = step/abs(step)
    start = downloadRange[0] * sign - int(sign + 0.5)
    end = start + sign * downloadRange[1]
    for num in range(start, end, step):
        print chaptersLists[num]
        subUrl = mainUrl+chaptersLists[num]+'/'
        subHtml = getHtml(subUrl)
        getImagUrls(subHtml)
        print "the program will sleep 10 second "
        time.sleep(10)
