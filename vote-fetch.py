# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 23:16:00 2013

@author: richardkwo
"""

import imaplib
import email
import time
import matplotlib.pyplot as plt
import numpy as np


def getTextAndNumber(mailRaw):
    email_message_instance = email.message_from_string(mailRaw)
    maintype = email_message_instance.get_content_maintype()
    # mail text
    if maintype == 'multipart':
        for part in email_message_instance.get_payload():
            if part.get_content_maintype() == 'text':
                mailText = part.get_payload()
    elif maintype == 'text':
        mailText = email_message_instance.get_payload()
        # number from
    subjectLine = email_message_instance['From']
    fromNumber = subjectLine.split("\"")
    fromNumber = fromNumber[1]

    mailText = mailText.rstrip()
    mailText = mailText.split("\n")[0]
    mailText = mailText.rstrip()
    return mailText, fromNumber

def strSorted(L):
    L = [int(x) for x in L]
    L = sorted(L)
    L = [str(x) for x in L]
    return (L)

def fetchMail(mail, uid):
    result, data = mail.uid("fetch", uid, "(RFC822)")
    if result == "OK":
        return data[0][1]
    else:
        return None


def getSMSMails(mail):
    # search for unread sms mails    
    result, data = mail.uid('search', None, '(UNSEEN HEADER Subject "SMS from")')
    if result == 'OK':
        data = data[0]
        if data == "":
            return []
        uidList = data.split(" ")
        return uidList
    else:
        print result, "when searching for mails!"
        return []

def saveVoteCountFile(voteCountDict, voteCountFileName):
    fw = open(voteCountFileName, "w")
    for v in strSorted(voteCountDict.keys()):
        print >>fw, "%s\t%d" % (v, voteCountDict[v])
    fw.close()

def saveImgFile(voteCountDict, imgFileName):
    ind = np.arange(len(voteCountDict))
    width = 0.8
    fig, ax = plt.subplots()
    sortedKeys = strSorted(voteCountDict.keys())
    sortedVals = [voteCountDict[x] for x in sortedKeys]
    rects1 = ax.bar(ind, sortedVals, width, color='r', alpha=0.5)       
    # add some
    ax.set_ylim(0,max(10,int(1.2 * max(sortedVals))))
    ax.set_xlabel('Candidates')
    ax.set_ylabel('Votes')
    ax.set_title('Voting')
    ax.set_xticks(ind+width/2)
    ax.set_xticklabels(sortedKeys)
    plt.savefig(imgFileName)

def updateVotes(mail, votedNumbersDict, voteCountDict, votePatternDict, voteRecordFile):
    mail.list()
    mail.select("inbox")
    fw = open(voteRecordFile, "a")
    uidList = getSMSMails(mail)
    if len(uidList)==0:
        print "No new vote.\n"
        fw.close()
        return (0)
    else:
        print "UPDATED: %d new sms votes.\n" % (len(uidList))
        for uid in uidList:
            mailRaw = fetchMail(mail, uid)
            mailText, fromNumber = getTextAndNumber(mailRaw)
            '''            
            print "UID:", uid
            print "Text:", mailText
            print "Number:", fromNumber, "\n"
            '''
            foundFlag = False
            for voteKeyword in votePatternDict.keys():
                if voteKeyword in mailText:
                    if fromNumber in votedNumbersDict.keys():
                        # duplicate vote
                        print "Duplicate vote:", fromNumber
                        # not count
                        foundFlag = True
                        break
                    # a vote from a new number
                    try:
                        voteFor = votePatternDict[voteKeyword]
                    except:
                        print "Keyword undefined:", voteKeyword
                        break
                    # a valid vote
                    votedNumbersDict[fromNumber] = 1
                    try:
                        voteCountDict[voteFor] += 1
                    except:
                        voteCountDict[voteFor] = 1
                    print >>fw, "%s\t%s" % (fromNumber, voteFor)
                    # no more matching
                    foundFlag = True
                    break
            if not foundFlag:
                print "BAD vote from", fromNumber, ":", mailText
    
    fw.close()
    return (1)

def readVotePattern(votePatternFile):
    fr = open(votePatternFile)
    votePatternDict = {}
    for line in fr:
        line = line.rstrip()
        line = line.split("\t")
        if len(line)<2:
            continue
        else:
            voteStr = line[0]
            voteFor = line[1]
            votePatternDict[voteStr] = voteFor
    fr.close()
    
    return (votePatternDict)

if __name__ == "__main__":
    # initialize IMAP
    workingDir = "./"
    f = open("acc.info")
    accInfoList = []
    for line in f:
        accInfoList.append(line.rstrip())
    f.close()
    username = accInfoList[0]
    pswd = accInfoList[1]

    mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
    mail.login(username, pswd)
    mail.list()
    mail.select("inbox")
    
    # check freq
    waitTime = 15
    # initialize rules and containers
    votedNumbersDict = {}
    voteCountDict = {}
    voteeList = []
    votePatternDict= readVotePattern("vote-pattern.txt")
    for v in votePatternDict.values():
        if not (v in voteeList):
            voteeList.append(v)
            voteCountDict[v] = 0
    print "\nCandidates:"
    voteeList = strSorted(voteeList)
    for v in voteeList:
        print v
    print ""
    # read vote pattern file
    voteRecordFile = "vote-record.txt"
    while True:
        ccmd = raw_input("Record a new vote (N) or continue with record (C)? ")
        if ccmd=="C":
            fr = open(voteRecordFile, "r")
            for line in fr:
                line = line.rstrip()
                line = line.split("\t")
                if len(line)!=2:
                    continue
                fromNumber = line[0]
                voteFor = line[1]
                votedNumbersDict[fromNumber] = 1
                try:
                    voteCountDict[voteFor] += 1
                except:
                    voteCountDict[voteFor] = 1
            print "Continue counting with"
            for voteFor in strSorted(voteCountDict.keys()):
                print "%3s:%3d votes" % (voteFor, voteCountDict[voteFor])
            print "\n"
            fr.close()
            break
        elif ccmd=="N":
            # erase the vote record file
            fr = open(voteRecordFile, "w")
            fr.close()
            for voteFor in votePatternDict.values():
                voteCountDict[voteFor] = 0
            print "A new vote started.\n"
            break

    # start updating
    saveImgFile(voteCountDict, "voting-now.png")
    saveVoteCountFile(voteCountDict, "vote-count.txt")
    cnt = 1
    while True:
        cnt += 1
        rt = updateVotes(mail, votedNumbersDict, voteCountDict, votePatternDict, voteRecordFile)
        if rt==1:
            saveImgFile(voteCountDict, "voting-now.png")
            saveVoteCountFile(voteCountDict, "vote-count.txt")
            print ""
            for v in strSorted(voteCountDict.keys()):
                print "Candidate %3s : %3d" % (v, voteCountDict[v])
            print ""
                
        time.sleep(waitTime)

    mail.logout()