from concurrent import futures
import logging
import grpc
import time
import random

# Import the generated classes
import mutex_pb2
import mutex_pb2_grpc

STATUS = ["RELEASED", "WANTED", "HELD"]

requestList = set() #Pair of time and Processes ID
msgList = [] #appends messages

def requestCS():
    pass



def enterCS():
    pass



def leaveCS():
    pass


class RoucairolCarvalhoServer(mutex_pb2_grpc.RoucairolCarvalhoServicer):

    def CriticalSection(self, request, context):
        reqTuple = (request.process_id, float(request.process_timestamp))
        requestList.add(reqTuple)
        print(request)
        print(f"THIS IS REQUESTLIST {list(requestList)}")

        
        
        return mutex_pb2.ResponseCS(status="WANTED")


    def CaniEnterNow(self, request, context):
        
        
        to_grant = min(requestList, key = lambda t: t[1])
        #to_grant = requestList[1]
        print("THIS IS TO GRANT NUMBER")
        print(to_grant[0])

        if request.id == to_grant[0]:
            return mutex_pb2.ResponseEnter(granted=1)
        else:
            return mutex_pb2.ResponseEnter(granted=0)


    def WriteToDiary(self, request, context):

        print(request.line, request.id)
        msgList.append(request.line)

        to_remove = {t for t in requestList if t[0] == request.id}
        requestList.remove(list(to_remove)[0])
        #requestList.remove(request.id)
        print(f"THIS IS REQUESTLIST {list(requestList)}")
        print(f"THIS IS MSGLIST {msgList}")

        time.sleep(random.randint(1,7))
        return mutex_pb2.ResponseWrite(granted=1)


server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))

mutex_pb2_grpc.add_RoucairolCarvalhoServicer_to_server(RoucairolCarvalhoServer(), server)


# Start the server
server.add_insecure_port("[::]:50061")
server.start()

# Keep the server running
while True:
  print("Port is Listening...")
  time.sleep(86400)
  #print(RoucairolCarvalhoServer.CriticalSection.request)

(1, 1672420864.0)
[(3, 1672420864.0), (1, 1672420864.0)]
[(3, 1672420864.0), (4, 1672420864.0), (1, 1672420864.0)]
[(3, 1672420864.0), (4, 1672420864.0)]
[(1, 1672420864.0), (4, 1672420864.0)]
[(1, 1672420864.0), (4, 1672420864.0)]



[(1, 1672421888.0), (4, 1672421888.0), (3, 1672421888.0)]
[(4, 1672421888.0), (3, 1672421888.0)]
[(1, 1672421888.0), (4, 1672421888.0), (3, 1672421888.0)]
[(4, 1672421888.0), (3, 1672421888.0)]
[(1, 1672421888.0), (4, 1672421888.0), (3, 1672421888.0)]
[(1, 1672421888.0), (3, 1672421888.0)]
### ONE THING TO NOTE WE DON"T UPDATE THE TIMESTAMPS


### ONE PROBLEM CLIENT 1 RUNS FOREVER

### IT WORKS BUT WE DON"T UPDATE THE TIMES