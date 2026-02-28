import can
import time
import random
import math
import sys

from PyQt5.QtCore import QObject, pyqtSignal, QThread

class CanSimHandler(QObject):
    message_received = pyqtSignal(list)  # Signal to emit the received position

    def __init__(self):
        super().__init__()
        self.reciever = None
        self.sender = None
        self.position = 0
        self.velocity = 300
        self.pipette_position_x = 0
        self.pipette_position_y = 0
        self.time_step = 0.01

        try:
            self.bus = can.Bus(interface='virtual', channel='vcan0', bitrate=500000, receive_own_messages=True)
            print("Virtual CAN bus initialized successfully!")
        except Exception as e:
            print(f"Error initializing virtual CAN bus: {e}")
            exit(1)

    def start_can_sim(self):
        """Function to start the CAN simulation."""
        if not self.reciever and not self.sender:
            print("Starting CAN simulation...")
            self.reciever = CANReceiveWorker(self.bus)
            self.reciever.message_received.connect(self.message_received)
            self.reciever.start()

            self.sender = CANSendWorker(self.bus, self.position, self.velocity, self.time_step, self.pipette_position_x, self.pipette_position_y)
            self.sender.start()

    def stop(self):
        """Stop the CAN simulation and clean up threads."""
        if self.reciever:
            self.reciever.stop()
            self.reciever = None
        if self.sender:
            self.sender.stop()
            self.position, self.velocity, self.pipette_position_x, self.pipette_position_y = self.sender.reagent_0_position, self.sender.velocity, self.sender.pipette_position_x, self.sender.pipette_position_y
            self.sender = None


class CANReceiveWorker(QThread):
    """Worker thread to receive CAN messages and emit signals."""
    message_received = pyqtSignal(list)  # Signal to emit the received position

    def __init__(self, bus):
        super().__init__()
        self.bus = bus
        self.running = True

        self.pipette_arbitration_id = 0x01
        self.reagent_0_arbitration_id = 0x02
        self.reagent_1_arbitration_id = 0x03
        self.sample_0_arbitration_id = 0x04
        self.sample_1_arbitration_id = 0x05
        self.sample_2_arbitration_id = 0x06
        

    def run(self):
        while self.running:
            message = self.bus.recv(timeout=1.0)
            if message is not None:
                arbitration_id = message.arbitration_id
                if arbitration_id == self.pipette_arbitration_id:
                    pipette_position_x = message.data[0] + message.data[1]*250
                    pipette_position_y = message.data[2] + message.data[3]*250
                    self.message_received.emit([arbitration_id, (pipette_position_x, pipette_position_y)])
                else:
                    position = message.data[0]
                    self.message_received.emit([arbitration_id, position])
                    


                # position = message.data[0]
                # pipette_position_x = message.data[1] + message.data[2]*250
                # pipette_position_y = message.data[3] + message.data[4]*250
                # # print(f"Received position: {position}")
                # self.message_received.emit([position, pipette_position_x, pipette_position_y])
            else:
                # print("No message received within timeout")
                pass

    def stop(self):
        self.running = False
        self.quit()
        self.wait()


class CANSendWorker(QThread):
    """Worker thread to send CAN messages."""
    def __init__(self, bus, position, velocity, time_step, pipette_position_x, pipette_position_y):
        super().__init__()
        self.bus = bus
        self.running = True
        self.reagent_0_position = position
        self.velocity = velocity
        self.time_step = time_step

        self.pipette_position_x = pipette_position_x
        self.pipette_position_y = pipette_position_y
        self.pipette_velocity = random.randint(200, 500)
        self.pipette_direction = random.randint(0, 360)

        self.reagent_1_position = 0
        self.sample_0_position = 0
        self.sample_1_position = 0
        self.sample_2_position = 0

        self.pipette_arbitration_id = 0x01
        self.reagent_0_arbitration_id = 0x02
        self.reagent_1_arbitration_id = 0x03
        self.sample_0_arbitration_id = 0x04
        self.sample_1_arbitration_id = 0x05
        self.sample_2_arbitration_id = 0x06


    def run(self):
        while self.running:
            self.reagent_0_position += self.velocity * self.time_step
            if self.reagent_0_position >= 200 or self.reagent_0_position <= 0:
                self.velocity = -self.velocity

            self.pipette_position_x += self.pipette_velocity * math.cos(math.radians(self.pipette_direction)) * self.time_step
            self.pipette_position_y += self.pipette_velocity * math.sin(math.radians(self.pipette_direction)) * self.time_step
            if self.pipette_position_x >= 800 or self.pipette_position_x <= 0 or self.pipette_position_y >= 600 or self.pipette_position_y <= 0:
                self.pipette_position_x = min(max(self.pipette_position_x, 0), 800)
                self.pipette_position_y = min(max(self.pipette_position_y, 0), 600)
                self.pipette_direction = random.randint(0, 360)
                self.pipette_velocity = random.randint(200, 500)

            pipette_x1 = int(self.pipette_position_x%250)
            pipette_x2 = int(self.pipette_position_x//250)
            pipette_y1 = int(self.pipette_position_y%250)
            pipette_y2 = int(self.pipette_position_y//250)

            # message = can.Message(
            #     arbitration_id=0x123,
            #     data=[int(self.reagent_1_position), int(pipette_x1), int(pipette_x2), int(pipette_y1), int(pipette_y2), 0x06, 0x07, 0x08],
            #     is_extended_id=False
            # )
            # try:
            #     self.bus.send(message)
            # except can.CanError as e:
            #     print(f"Failed to send message: {e}")

            message_pipette = can.Message(
                arbitration_id=self.pipette_arbitration_id,
                data=[int(pipette_x1), int(pipette_x2), int(pipette_y1), int(pipette_y2), 0x00, 0x00, 0x00, 0x00],
                is_extended_id=False
            )
            try:
                self.bus.send(message_pipette)
            except can.CanError as e:
                print(f"Failed to send message: {e}")

            message_reagent_0 = can.Message(
                arbitration_id=self.reagent_0_arbitration_id,
                data=[int(self.reagent_0_position), 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                is_extended_id=False
            )
            try:
                self.bus.send(message_reagent_0)
            except can.CanError as e:
                print(f"Failed to send message: {e}")

            message_reagent_1 = can.Message(
                arbitration_id=self.reagent_1_arbitration_id,
                data=[int(self.reagent_1_position), 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                is_extended_id=False
            )
            try:
                self.bus.send(message_reagent_1)
            except can.CanError as e:
                print(f"Failed to send message: {e}")

            message_sample_0 = can.Message(
                arbitration_id=self.sample_0_arbitration_id,
                data=[int(self.sample_0_position), 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                is_extended_id=False
            )
            try:
                self.bus.send(message_sample_0)
            except can.CanError as e:
                print(f"Failed to send message: {e}")

            message_sample_1 = can.Message(
                arbitration_id=self.sample_1_arbitration_id,
                data=[int(self.sample_1_position), 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                is_extended_id=False
            )
            try:
                self.bus.send(message_sample_1)
            except can.CanError as e:
                print(f"Failed to send message: {e}")

            message_sample_2 = can.Message(
                arbitration_id=self.sample_2_arbitration_id,
                data=[int(self.sample_2_position), 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                is_extended_id=False
            )
            try:
                self.bus.send(message_sample_2)
            except can.CanError as e:
                print(f"Failed to send message: {e}")

            time.sleep(self.time_step)

    def stop(self):
        self.running = False
        self.quit()
        self.wait()