import grpc
import time
import logging

# Import the generated classes
import mutex_pb2
import mutex_pb2_grpc

# Logging Configs
format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

# Process Class
class Process:
    def __init__(self, proc_id, proc_timestamp, proc_state="RELEASED"):
        self.proc_id = proc_id
        self.proc_timestamp = proc_timestamp
        self.proc_state = proc_state

# Create Process Instance
proc = Process(1, str(time.time()))


# Create a gRPC channel to the server
channel = grpc.insecure_channel("localhost:50061")


# Create a stub for the traffic light service
stub = mutex_pb2_grpc.RoucairolCarvalhoStub(channel)

#Request Function To Request Access to CS
def RequestCS(process):
    time.sleep(3)

    # Send request to the server
    request = mutex_pb2.RequestCS(process_id = process.proc_id, process_timestamp = process.proc_timestamp)
    logging.info(f"Proc {process.proc_id}: SENT THE CS REQUEST")

    response = stub.CriticalSection(request)
    logging.info(f"Proc {process.proc_id}: RECEIVED THE CS RESPONSE")

    process.proc_state = response.status
    logging.info(f"Proc {process.proc_id}: UPDATED THE PROC STATE ----->>> {process.proc_state}")


    return process.proc_state

# Request Function to Enter the CS
def RequestEnter(process):
    time.sleep(3)

    # Send Request to the server 
    request = mutex_pb2.RequestEnter(id = process.proc_id)
    logging.info(f"Proc {process.proc_id}: SENT THE ENTER REQUEST")


    # Receive responsse from the server
    response = stub.CaniEnterNow(request)
    logging.info(f"Proc {process.proc_id}: RECEIVED THE ENTER RESPONSE")


    # If response granted enter the CS
    if response.granted == 1:
        logging.info(f"Proc {process.proc_id}: I CAN ENTER NOW")

        # Change state to HELD since we are now in the CS
        process.proc_state = "HELD"
        logging.info(f"Proc {process.proc_id}: UPDATED THE PROC STATE ----->>> {process.proc_state}")


    # if response is not granted the process waits for the turn
    else:
        logging.info(f"Proc {process.proc_id}: I NEED TO WAIT FOR MY TURN")

        logging.info(f"Proc {process.proc_id}: THE PROC STATE ----->>> {process.proc_state}")


    return process.proc_state

# Request Function to Write to the Diary
def RequestWrite(process):
    # if state is HELD send WRITE request to the Server
    if process.proc_state == "HELD":
        line = f"Proc {process.proc_id} was here" #Message for the diary
        time.sleep(3)

        # Request to the server
        request = mutex_pb2.RequestWrite(id=process.proc_id, line=line)
        logging.info(f"Proc {process.proc_id}: SENT THE WRITE REQUEST")


        # Response from the server
        response = stub.WriteToDiary(request)
        logging.info(f"Proc {process.proc_id}: RECEIVED THE WRITE RESPONSE")

        # If response is granted change the state and update the time
        if response.granted == 1:
            logging.info(f"Proc {process.proc_id}: WRITE WAS SECCUSSFUL")

            process.proc_state = "RELEASED"
            process.proc_timestamp = str(time.time())
            logging.info(f"Proc {process.proc_id}: UPDATED THE PROC STATE ----->>> {process.proc_state}")

            logging.info(f"Proc {process.proc_id}: UPDATED THE PROC TIMESTAMP ----->>> {process.proc_timestamp}")

        else:
            logging.info(f"Proc {process.proc_id}: SOMETHING WENT WRONG")


while True:

    if proc.proc_state != "HELD":
        # Run RequestCS
        RequestCS(proc)
        # Run RequestEnter
        RequestEnter(proc)
        # Run RequestWrite
        RequestWrite(proc)

    else:

        logging.info(f"PROC STATE IS EITHER WANTED OR HELD")

        break

### LOGGINGS
### RANDOM FUNCTION


###PUt all functinos in the class
###create clientcreator to run the classes in it

