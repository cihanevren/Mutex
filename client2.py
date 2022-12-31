import grpc
import time

# Import the generated classes
import mutex_pb2
import mutex_pb2_grpc


class Process:
    def __init__(self, proc_id, proc_timestamp, proc_state="RELEASED"):
        self.proc_id = proc_id
        self.proc_timestamp = proc_timestamp
        self.proc_state = proc_state

proc = Process(2, time.time())

print("WE ACCESSED TO THE CLIENT")
# Create a gRPC channel to the server
channel = grpc.insecure_channel("localhost:50061")



# Create a stub for the traffic light service
stub = mutex_pb2_grpc.RoucairolCarvalhoStub(channel)


request = mutex_pb2.RequestCS(process_id = proc.proc_id, process_timestamp = proc.proc_timestamp)

print("WE SENT THE REQUEST")

response = stub.CriticalSection(request)

print("WE RECEIVED THE RESPONSE")

proc.proc_state = response.status

print(f"WE UPDATED THE PROC STATE ----->>> {proc.proc_state}")



time.sleep(20)
request2 = mutex_pb2.RequestEnter(id = proc.proc_id)

print("WE SENT THE REQUEST 2")

response2 = stub.CaniEnterNow(request2)

if response2.granted == 1:
    print("YES WE CAN ENTER NOW")
    proc.proc_state = "HELD"
    print(f"WE UPDATED THE PROC STATE ----->>> {proc.proc_state}")

else:
    print("WE NEED TO WAIT FOR OUR TURN")
    print(f"WE UPDATED THE PROC STATE ----->>> {proc.proc_state}")


if proc.proc_state == "HELD":
    line = f"Proc {proc.proc_id} was here"
    request3 = mutex_pb2.RequestWrite(line=line)
    print("WE SENT THE REQUEST 3")
    response3 = stub.WriteToDiary(request3)
    if response3.succeed == 1:
        print("WRITE WAS SUCCESSFUL")
    else:
        print("SOMETHING WENT WRONG")