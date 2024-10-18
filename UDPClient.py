import sys, time
from socket import *
# Get the server hostname and port as command line arguments
argv = sys.argv
host = argv[1]
port = argv[2]
timeout = 1 # in second
times = []
# Create UDP client socket
# Note the use of SOCK_DGRAM for UDP datagram packet
clientsocket = socket(AF_INET, SOCK_DGRAM)
# Set socket timeout as 1 second
clientsocket.settimeout(timeout)
# Command line argument is a string, change the port into integer
port = int(port)
# Sequence number of the ping message
ptime = 0
# Ping for 10 times
packets_sent = 0
packets_received = 0

while ptime < 10:
    ptime += 1
    # Format the message to be sent
    data = "Ping " + str(ptime) + " " + time.asctime()
    try:
        # Sent time
        RTTb = time.time()
        
        # Send the UDP packet with the ping message
        clientsocket.sendto(data.encode(),(host, port))
        packets_sent += 1
        # Receive the server response
        message, address = clientsocket.recvfrom(1024)
        packets_received += 1
        # Received time
        RTTa = time.time()
        calc_RTT = (RTTa - RTTb)
        times.append(calc_RTT)
        # Display the server response as an output
        print("Reply from " + address[0] + ": " + message.decode())
        # Round trip time is the difference between sent and received time
        print("RTT: " + str(calc_RTT))
    except:
        # Server does not response
        # Assume the packet is lost
        print ("Request timed out.")
    continue
packet_loss = 100 - ((packets_received / packets_sent)*100)
print("\nPacket statistics for", (host),":")
print("Packets: Sent =", (packets_sent),", Received =", (packets_received),", Loss =", (packet_loss),"%")
#print("packets received: ", (packets_received))
if not times:
    print("Error. No RTTs entered.")
else:
    print("Approximate RTTs in milliseconds:")
    print("Minimum =", round(min(times)*1000, 4),"ms, Maximum =", round(max(times)*1000, 4),"ms, Average =", round((sum(times) / len(times))*1000, 4),"ms")
#    print("max RTT: ", round(max(times), 6))
#    print("average RTT: ", round((sum(times) / len(times)), 6))
#packet_loss = 100 - ((packets_received / packets_sent)*100)
#print("packet loss percentage: ", packet_loss , "%")

# Close the client socket
clientsocket.close()