import grpc
import time
import random
# Import the generated classes
import mutex_pb2
import mutex_pb2_grpc

# Process Class
class Process:
    def __init__(self, proc_id, proc_timestamp, proc_state="RELEASED"):
        self.proc_id = proc_id
        self.proc_timestamp = proc_timestamp
        self.proc_state = proc_state

# Create Process Instance
proc = Process(3, str(time.time()))


# Create a gRPC channel to the server
channel = grpc.insecure_channel("localhost:50061")


# Create a stub for the traffic light service
stub = mutex_pb2_grpc.RoucairolCarvalhoStub(channel)

#Request Function To Request Access to CS
def RequestCS(process):
    time.sleep(3)

    # Send request to the server
    request = mutex_pb2.RequestCS(process_id = process.proc_id, process_timestamp = process.proc_timestamp)
    print("WE SENT THE CS REQUEST")
    response = stub.CriticalSection(request)
    print("WE RECEIVED THE CS RESPONSE")
    process.proc_state = response.status
    print(f"WE UPDATED THE PROC STATE ----->>> {process.proc_state}")

    return process.proc_state

# Request Function to Enter the CS
def RequestEnter(process):
    time.sleep(3)

    # Send Request to the server 
    request = mutex_pb2.RequestEnter(id = process.proc_id)
    print("WE SENT THE ENTER REQUEST")

    # Receive responsse from the server
    response = stub.CaniEnterNow(request)
    print("WE RECEIVED THE ENTER RESPONSE")

    # If response granted enter the CS
    if response.granted == 1:
        print("YES WE CAN ENTER NOW")
        # Change state to HELD since we are now in the CS
        process.proc_state = "HELD"
        print(f"WE UPDATED THE PROC STATE ----->>> {process.proc_state}")

    # if response is not granted the process waits for the turn
    else:
        print("WE NEED TO WAIT FOR OUR TURN")
        print(f"WE UPDATED THE PROC STATE ----->>> {process.proc_state}")

    return process.proc_state

# Request Function to Write to the Diary
def RequestWrite(process):
    # if state is HELD send WRITE request to the Server
    if process.proc_state == "HELD":
        line = f"Proc {process.proc_id} was here" #Message for the diary
        time.sleep(3)

        # Request to the server
        request = mutex_pb2.RequestWrite(id=process.proc_id, line=line)
        print("WE SENT THE WRITE REQUEST")

        # Response from the server
        response = stub.WriteToDiary(request)
        print("WE RECEIVED THE WRITE RESPONSE")

        # If response is granted change the state and update the time
        if response.granted == 1:
            print("WRITE WAS SUCCESSFUL")
            process.proc_state = "RELEASED"
            process.proc_timestamp = str(time.time())
            print(f"WE UPDATED THE PROC STATE ----->>> {process.proc_state}")
            print(f"WE UPDATED THE PROC TIMESTAMP ----->>> {process.proc_timestamp}")
        else:
            print("SOMETHING WENT WRONG")

while True:

    if proc.proc_state != "HELD":
        
        RequestCS(proc)

        RequestEnter(proc)

        RequestWrite(proc)

    else:

        print("PROC STATE IS EITHER WANTED OR HELD")
        break

# if proc.proc_state == "HELD":
#     line = f"Proc {proc.proc_id} was here"
#     request3 = mutex_pb2.RequestWrite(line=line)
#     print("WE SENT THE REQUEST 3")
#     response3 = stub.WriteToDiary(request3)
#     if response3.succeed == 1:
#         print("WRITE WAS SUCCESSFUL")
#     else:
#         print("SOMETHING WENT WRONG")


####if succeed leave CS
####pop it out from the list
####the one leaving the cs need to send that the other one can enter the cs

### it can only request if the status is not wanted or not held
### write them as functions first 