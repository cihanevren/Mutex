from concurrent import futures
import logging
import grpc
import time
import random
import mutex_pb2
import mutex_pb2_grpc
import sys
STATUS = ["RELEASED", "WANTED", "HELD"]

requestList = set() # Pair of time and Processes ID
diary = list() # keeps record of messages
diary_proc = list() # keeps record of procs

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")


class RoucairolCarvalhoServer(mutex_pb2_grpc.RoucairolCarvalhoServicer):

    def CriticalSection(self, request, context):
        logging.info(f"STARTING CRITICALSECTION FUNCTION")

        # Create request tuple with request id and request timestamp
        requestTuple = (request.process_id, float(request.process_timestamp))

        # Add request tuple into request list
        requestList.add(requestTuple)

        logging.info(f"CURRENT REQUESTLIST {list(requestList)}")
        logging.info(f"ENDING CRITICALSECTION FUNCTION")

        return mutex_pb2.ResponseCS(status="WANTED")


    def CaniEnterNow(self, request, context):
        logging.info(f"STARTING CANIENTERNOW FUNCTION")
        # Find the request with the minimum timestamp in the requestlist
        min_timestamp_id = min(requestList, key = lambda t: t[1])[0]

        logging.info(f"ENDING CANIENTERNOW FUNCTION")
        if request.id == min_timestamp_id:
            return mutex_pb2.ResponseEnter(granted=1)
        else:
            return mutex_pb2.ResponseEnter(granted=0)


    def WriteToDiary(self, request, context):
        logging.info(f"STARTING WRITETODIARY FUNCTION")
        logging.info(f"MESSAGE FROM PROC {request.id} IS {request.line}")
        diary.append(request.line)
        diary_proc.append(request.id)

        logging.info(f"UPDATED THE DIARY WITH THE MESSAGE")
        logging.info(f"Diary ----->>> {diary}")
        to_remove = {t for t in requestList if t[0] == request.id}
        requestList.remove(list(to_remove)[0])
        logging.info(f"UPDATED REQUESTLIST {list(requestList)}")


        
        logging.info(f"ENDING WRITETODIARY FUNCTION")
        time.sleep(random.randint(1,7))
        return mutex_pb2.ResponseWrite(granted=1)


server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))

mutex_pb2_grpc.add_RoucairolCarvalhoServicer_to_server(RoucairolCarvalhoServer(), server)


# Start the server
server.add_insecure_port("[::]:50061")
server.start()

# Keep the server running
while True:
    try:
        print("Port is Listening...")
        time.sleep(86400)
    except KeyboardInterrupt:
        logging.info("<---SERVER IS INTERRUPTED FROM THE TERMINAL--->")
        logging.info(f"Registry of Critical Section Accesses : \n {diary_proc}")
        sys.exit()



 

