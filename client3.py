import sys
import grpc
import time
import logging
import random
import mutex_pb2
import mutex_pb2_grpc

# Logging Configs
format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

# Set random seed
random.seed(3030)


# Create a gRPC channel to the server
channel = grpc.insecure_channel("localhost:50061")


# Create a stub for Roucairol Carlvalho Service
stub = mutex_pb2_grpc.RoucairolCarvalhoStub(channel)


class Process:
    # Init Function
    def __init__(self, proc_id, proc_timestamp, proc_state="RELEASED"):
        self.proc_id = proc_id
        self.proc_timestamp = proc_timestamp
        self.proc_state = proc_state

    # Request Function To Request Access to CS
    def RequestCS(self):
        time.sleep(3)

        # Send request to the server
        request = mutex_pb2.RequestCS(process_id = self.proc_id, process_timestamp = self.proc_timestamp)
        logging.info(f"Proc {self.proc_id}: SENT THE CS REQUEST")

        response = stub.CriticalSection(request)
        logging.info(f"Proc {self.proc_id}: RECEIVED THE CS RESPONSE")

        self.proc_state = response.status
        logging.info(f"Proc {self.proc_id}: UPDATED THE PROC STATE ----->>> {self.proc_state}")


        return self.proc_state        


    # Request Function to Enter the CS
    def RequestEnter(self):
        time.sleep(3)

        # Send Request to the server 
        request = mutex_pb2.RequestEnter(id = self.proc_id)
        logging.info(f"Proc {self.proc_id}: SENT THE ENTER REQUEST")


        # Receive responsse from the server
        response = stub.CaniEnterNow(request)
        logging.info(f"Proc {self.proc_id}: RECEIVED THE ENTER RESPONSE")


        # If response granted enter the CS
        if response.granted == 1:
            logging.info(f"Proc {self.proc_id}: I CAN ENTER NOW")

            # Change state to HELD since we are now in the CS
            self.proc_state = "HELD"
            logging.info(f"Proc {self.proc_id}: UPDATED THE PROC STATE ----->>> {self.proc_state}")


        # if response is not granted the process waits for the turn
        else:
            logging.info(f"Proc {self.proc_id}: I NEED TO WAIT FOR MY TURN")

            logging.info(f"Proc {self.proc_id}: THE PROC STATE ----->>> {self.proc_state}")


        return self.proc_state

    # Request Function to Write to the Diary
    def RequestWrite(self):
        # if state is HELD send WRITE request to the Server
        if self.proc_state == "HELD":
            line = f"Proc {self.proc_id} was here" #Message for the diary
            time.sleep(3)

            # Request to the server
            request = mutex_pb2.RequestWrite(id=self.proc_id, line=line)
            logging.info(f"Proc {self.proc_id}: SENT THE WRITE REQUEST")


            # Response from the server
            response = stub.WriteToDiary(request)
            logging.info(f"Proc {self.proc_id}: RECEIVED THE WRITE RESPONSE")

            # If response is granted change the state and update the time
            if response.granted == 1:
                logging.info(f"Proc {self.proc_id}: WRITE WAS SECCUSSFUL")

                self.proc_state = "RELEASED"
                self.proc_timestamp = str(time.time())
                logging.info(f"Proc {self.proc_id}: UPDATED THE PROC STATE ----->>> {self.proc_state}")

                logging.info(f"Proc {self.proc_id}: UPDATED THE PROC TIMESTAMP ----->>> {self.proc_timestamp}")

            else:
                logging.info(f"Proc {self.proc_id}: SOMETHING WENT WRONG")

# Create Process Instance
proc = Process(3, str(time.time()))

while True:
    try:
        # Add some randomness
        random_choice = random.choice([0,1])
        if random_choice == 1:

            if proc.proc_state != "HELD":
                # Run RequestCS
                proc.RequestCS()
                # Run RequestEnter
                proc.RequestEnter()
                # Run RequestWrite
                proc.RequestWrite()

            else:
                logging.info(f"PROC STATE IS EITHER WANTED OR HELD")
                break
        else:
            random_choice_sleep = random.randint(5,15)
            time.sleep(random_choice_sleep)
    except grpc.RpcError as e:
        logging.info("ERROR OCCURRED, CLIENT STOPPED")

        print("------------------------------------------")
        logging.info(f"ERROR DETAILS : {e.details()}")
        logging.info(f"ERROR CODE NAME : {e.code().name}")
        logging.info(f"ERROR CODE VALUE : {e.code().value}")
        print("------------------------------------------")
        
        sys.exit()

    except KeyboardInterrupt:
        logging.info("CLIENT IS INTERRUPTED FROM TERMINAL")
        sys.exit()