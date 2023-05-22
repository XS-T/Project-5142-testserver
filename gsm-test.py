import serial
import time

ser = serial.Serial('/dev/ttyS0', baudrate=9600, timeout=1)
time.sleep(1)


def send_sms(number, message):
    ser.write('AT+CMGF=1\r\n'.encode())  # Set SMS mode to text
    time.sleep(1)
    ser.write('AT+CMGS="{}"\r\n'.format(number).encode())
    time.sleep(1)
    ser.write('{}\r\n'.format(message).encode())
    time.sleep(1)
    ser.write(bytes([26]))  # Send Ctrl+Z to indicate the end of the message
    time.sleep(1)


def receive_sms():
    ser.write('AT+CMGF=1\r\n'.encode())  # Set SMS mode to text
    time.sleep(1)
    ser.write('AT+CMGL="ALL"\r\n'.encode())  # List all received messages
    time.sleep(1)
    response = ser.readlines()

    messages = []
    for i in range(len(response)):
        if '+CMGL:' in response[i].decode():
            index = int(response[i].decode().split(',')[0].split(':')[1])
            message = response[i + 1].decode().strip()
            sender = response[i + 2].decode().strip().split(',')[1].strip().strip('"')
            timestamp = response[i + 2].decode().strip().split(',')[3].strip().strip('"')
            messages.append({'index': index, 'sender': sender, 'timestamp': timestamp, 'message': message})

    return messages


def answer_call():
    ser.write('ATA\r\n'.encode())  # Answer the incoming call
    time.sleep(1)
    print('Call answered')


def hangup_call():
    ser.write('ATH\r\n'.encode())  # Hang up the call
    time.sleep(1)
    print('Call hung up')


# Example usage
send_sms('phone_number', 'Hello, this is a test message!')

received_messages = receive_sms()
for message in received_messages:
    print('Sender: {}'.format(message['sender']))
    print('Timestamp: {}'.format(message['timestamp']))
    print('Message: {}'.format(message['message']))
    print('---')

answer_call()
time.sleep(10)  # Call duration
hangup_call()

ser.close()
