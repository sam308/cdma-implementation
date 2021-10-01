import multiprocessing
import random
import time
import threading
from sender import *
from receiver import *
from channel import *
import constants


def getNextPowerof2(num):
    power = 1
    while(power < num):
        power *= 2
    return power


def buildWalshTable(length, i1,i2, j1,j2, isComplement):
    if length == 2:
        if not isComplement:
            wTable[i1][j1] = 1
            wTable[i1][j2] = 1
            wTable[i2][j1] = 1
            wTable[i2][j2] = -1
        else:
            wTable[i1][j1] = -1
            wTable[i1][j2] = -1
            wTable[i2][j1] = -1
            wTable[i2][j2] = 1
        
        return
    
    midi = (i1+i2)//2
    midj = (j1+j2)//2

    buildWalshTable(length/2, i1, midi, j1, midj, isComplement)
    buildWalshTable(length/2, i1, midi, midj+1, j2, isComplement)
    buildWalshTable(length/2, midi+1, i2, j1, midj, isComplement)
    buildWalshTable(length/2, midi+1, i2, midj+1, j2, not isComplement)

    return

def start(wTable):

    WHOC2RL = []
    RHOC2RL = []

    RHOS2C, WHOS2C = multiprocessing.Pipe()

    for i in range(constants.TOT_RECEIVER):
        readHead, writeHead = multiprocessing.Pipe()
        WHOC2RL.append(writeHead)
        RHOC2RL.append(readHead)


    senderList = []
    receiverList = []

    for i in range(constants.TOT_SENDER):
        sender = Sender(i, wTable[i], WHOS2C)
        senderList.append(sender)
    
    for i in range(constants.TOT_RECEIVER):
        receiver = Receiver(i, wTable, RHOC2RL[i])
        receiverList.append(receiver)
    
    channelObj = Channel(0, RHOS2C, WHOC2RL)

    
    senderProcess = []
    receiverProcess = []

    for i in range(len(senderList)):
        p = threading.Thread(name="Sender" + str(i+1),target=senderList[i].startSender)
        senderProcess.append(p)
    
    for i in range(len(receiverList)):
        p = threading.Thread(name="Receiver"+str(i+1), target=receiverList[i].startReceiver)
        receiverProcess.append(p)
    
    channelProcess = threading.Thread(name="ChannelProcess", target=channelObj.startChannel)

    channelProcess.start()
    for process in receiverProcess:
        process.start()

    for process in senderProcess:
        process.start()

    for process in senderProcess:
        process.join()

    for process in receiverProcess:
        process.join()
    channelProcess.join()
    

if __name__ == "__main__":
    print("!-----------------------------------CDMA IMPLEMENTATION---------------------------------------------------!")
    print("NETWORK CONFIGURATION:")
    print("TOTAL NUMBER OF SENDERS: {}".format(constants.TOT_SENDER))
    print("TOTAL NUMBER OF RECEIVERS: {}".format(constants.TOT_RECEIVER))
    print("!---------------------------------------------------------------------------------------------------------!")

    num = getNextPowerof2(constants.TOT_SENDER)
    wTable = [[0 for i in range(num)] for j in range(num)]

    if constants.TOT_SENDER >1: buildWalshTable(num, 0, num - 1, 0, num - 1, False)
    else: wTable = [1]
    
    print("THE GENERATED WALSH TABLE:")
    for i in range(constants.TOT_SENDER):
        for j in range(constants.TOT_SENDER):
            print(wTable[i][j], end = " ")
        print()
    print("!---------------------------------------------------------------------------------------------------------!")
    
    start(wTable)
