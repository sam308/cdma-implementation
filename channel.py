import multiprocessing
import threading
import constants

class Channel:
    def __init__(self, name, senderToChannel, channelToReceiver):
        self.name               = name
        self.senderToChannel    = senderToChannel
        self.channelToReceiver  = channelToReceiver
        self.channelData        = [0 for i in range(constants.TOT_SENDER)]  # channel data that needs to be distributed
        self.syncValue          = 0 # to keep track of the number of senders whose data has been read
        


    def channelizeData(self):
        while True:

            for i in range(constants.TOT_SENDER):
            
                data = []
                data = self.senderToChannel.recv()
                print("[CHANNEL: ] " + str(data)+" ...........")
              
                # update channel Data
                for i in range(len(data)):
                    self.channelData[i] += data[i] 
                
                self.syncValue += 1

                if self.syncValue == constants.TOT_SENDER:
                    # distribute over every receiver
                    for receiver in range(constants.TOT_RECEIVER):
                        self.channelToReceiver[receiver].send(self.channelData)
                        # reset self.value and channelData for next bit transfer
                        self.syncValue = 0
                        self.channelData = [0 for i in range(len(data))]
    
    
    def startChannel(self):
        
        t = threading.Thread(name="channel", target=self.channelizeData)
        t.start()
        t.join()
