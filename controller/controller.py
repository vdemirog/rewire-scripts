import _thread
import threading
import json
import os
import subprocess
import time
import socket

def main():
    consumer="node9-13"
    producer="node9-21"
    content = subprocess.check_output("nc -l -p 7998", shell=True)
    content = content.decode('UTF-8')
    content = content.rstrip("\n")
    # Create a new thread
    try:
        _thread.start_new_thread( configureNodes, (consumer,producer,content) )
    except:
        print ("Error: unable to start thread")

def configureNodes(consumer,producer,content):
    ConsumerCS = CS()
    if not cached(content,ConsumerCS):
        namePath = findTheParth(consumer,producer)
        ipPathList = getIPlist(namePath)
        print(namePath)
        print(ipPathList)
        print("content: ")
        #print(type(content))
        print(content)
        for i in range(len(ipPathList)-1):
            print(ipPathList[i])
            #create face
            addfacecmd = "ndnaddface tcp4://%s"%ipPathList[i+1]
            registercmd = "ndnregister %s tcp4://%s"%(content, ipPathList[i+1])
            data = addfacecmd + "\n" +registercmd
            time.sleep(0.5)
            sendData(ipPathList[i],8000,data)
            print("data")
            print(data)
            #register content to the next face
            #registercmd = "ndnregister %s tcp4://%s"%(content, ipPathList[i+1])
            #sendData(ipPathList[i],8000,registercmd)
            #print("registercmd: ")
            #print(registercmd)
        ConsumerCS.add(content,10)
    #Send "clear to send message" to the consumer node
    time.sleep(0.5)
    sendData(ipPathList[0],7999,"cts")

def fperiod_set_remove(cs, item, fperiod):
    time.sleep(fperiod)
    cs.remove(item)

class CS(set):
    def add(self, item, fperiod):
        set.add(self, item)
        t = threading.Thread(target=fperiod_set_remove, args=(self, item, fperiod))
        t.start()

def cached(content,cs):
    if content in cs:
        return 1
    else:
        return 0


def findTheParth(consumer,producer):
    nodesInfo=getNodesInfo()
    nodesPath = []
    endNode = False
    nodesPath.append(consumer)
    consumerBMAC=getBMACFromNodesInfo(nodesInfo,consumer)
    producerBMAC=getBMACFromNodesInfo(nodesInfo,producer)
    consumerWMAC=getWMACFromNodesInfo(nodesInfo,consumer)
    producerWMAC=getWMACFromNodesInfo(nodesInfo,producer)
    originators = getNodeOriginators(consumerBMAC)
    while endNode == False:
        walking = False
        for i in originators:
            if i['orig_address']==producerWMAC and i['neigh_address']==producerWMAC:
                nodesPath.append(producer)
                walking = True
                endNode = True
                break
        if endNode == False:
            for i in originators:
                if i['orig_address']==producerWMAC:
                    nextHopWMAC=i['neigh_address']
                    nextHopName=getNodeNameFromWMAC(nodesInfo,nextHopWMAC)
                    nodesPath.append(nextHopName)
                    #print(nextHopName)
                    nextHopBMAC=getBMACFromNodesInfo(nodesInfo,nextHopName)
                    originators=getNodeOriginators(nextHopBMAC)
                    walking = True
                    break
        if walking == False:
            print("There is NOT path for this producer node")
            break
    return nodesPath
    
def getIPlist(namePath):
    ipPath = []
    nodesInfo=getNodesInfo()
    for i in namePath:
        nodeIP=getIPFromName(nodesInfo,i)
        ipPath.append(nodeIP)
    return ipPath


def getNodesInfo():
    file1 = open('nodesinfo', 'r')
    file1lines = file1.readlines()
    nodesinfo=[]
    for i in file1lines:
        i = i.replace('", "','" : "')
        i = i.replace(' },',' }')
        data = json.loads(i)
        content = list(data.values())[0]
        content = content.replace("'",'"')
        nodeinfo = json.loads(content)
        nodesinfo.append(nodeinfo)
    file1 .close()
    return nodesinfo

def getNodeOriginators(nodeBMAC):
    file2 = open('bestoriginators', 'r')
    file2lines = file2.readlines()
    originators = []
    for i in file2lines:
        #print(i)
        i = i.replace('", "','" : "')
        i = i.replace(' },',' }')
        #print(i)
        data = json.loads(i)
        if nodeBMAC in data:
             originators=data[nodeBMAC]
             originators = originators.replace("'",'"')
             originators = originators.replace('True','"True"')
             originators = json.loads(originators)
    #    print(data2['ip'])
    return originators
    file2 .close()

def getBMACFromNodesInfo(nodesInfo,nodeName):
    for i in nodesInfo:
        if i['name'] == nodeName:
             bMac=i["bmac"]
    return bMac

def getWMACFromNodesInfo(nodesInfo,nodeName):
    for i in nodesInfo:
        if i['name'] == nodeName:
             wMac=i["wmac"]
    return wMac

def getNodeNameFromWMAC(nodesInfo,wMAC):
    for i in nodesInfo:
        if i['wmac'] == wMAC:
             name=i["name"]
    return name

def getIPFromName(nodesInfo,nodeName):
    for i in nodesInfo:
        if i['name'] == nodeName:
             name=i["ip"]
    return name
    
#! /usr/bin/python3



def sendData(ip,port,data):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    try:
        s.connect((ip,port))
        s.send(data.encode())
    except socket.timeout:
        print("ERROR!!! - Failed to connect- Timeout raised and caught.")
    print (data)
    s.close ()




if __name__ == "__main__":
    while True:
        main()

