from bluetooth import*
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
pin_to_circuit = 7
server_sock = BluetoothSocket(RFCOMM)
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)
uuid = "00001101-0000-1000-8000-00805f9b34f4"
advertise_service(server_sock, "ApplePi",
                  service_id = uuid,
                  service_classes = [uuid, SERIAL_PORT_CLASS],
                  profiles = [SERIAL_PORT_PROFILE],
                 )


# light acquisition function
def rc_time (pin_to_circuit):
  count = 0
 
  #Output on the pin for 
  GPIO.setup(pin_to_circuit, GPIO.OUT)
  GPIO.output(pin_to_circuit, GPIO.LOW)
  time.sleep(.1)

  #Change the pin back to input
  GPIO.setup(pin_to_circuit, GPIO.IN)
 
  #Count until the pin goes high
  while (GPIO.input(pin_to_circuit) == GPIO.LOW):
    count += 1

  return count

while True:
    print ("Waiting for connection on RFCOMM")
    client_sock, client_info = server_sock.accept()

    print ("Accepted connection from: ", client_info)
    try:
        data = client_sock.recv(1024)
        if len(data) == 0: break
        print ("received [%s]" % data)


        # get the light value from the light sensor
        light= rc_time(pin_to_circuit)
        # set data = the value something like str(lightValue) + '!'

        
        data = str(light)+ '!'

        client_sock.send(data)
        print ("sending [%s]" % data)

    except IOError:
        pass

    except KeyboardInterrupt:
        print ("disconnected")
        client_sock.close()
        server_sock.close()
        print ("all done!")
        break
