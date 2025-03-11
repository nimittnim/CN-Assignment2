from mininet.net import Mininet
from mininet.topo import Topo
from mininet.node import OVSController
import time
import os
import subprocess

def setup_topology():
    
    class CustomTopo(Topo):
        def build(self):
            s1 = self.addSwitch('s1')
            h1 = self.addHost('h1')
            h7 = self.addHost('h7')

            self.addLink(h1, s1)
            self.addLink(s1, h7)

    net = Mininet(topo=CustomTopo(), controller=OVSController)
    net.start()

    net.get('s1').cmd('ovs-ofctl add-flow s1 actions=normal')
    return net

def configure_tcp_options(host, nagle, delayed_ack):
 
    if nagle:
        host.cmd("sysctl -w net.ipv4.tcp_nodelay=0")
    else:
        host.cmd("sysctl -w net.ipv4.tcp_nodelay=1")

    if delayed_ack:
        host.cmd("sysctl -w net.ipv4.tcp_delack_min=100")
    else:
        host.cmd("sysctl -w net.ipv4.tcp_delack_min=0")

def analyze_pcap():
    if not os.path.exists("tcp_test.pcap") or os.path.getsize("tcp_test.pcap") == 0:
        print("[ERROR] No packets were captured. Check tcpdump settings!")
        return

    throughput = subprocess.getoutput("tshark -r tcp_test.pcap -q -z io,stat,10 | grep '<>'")
    goodput = int(subprocess.getoutput("tshark -r tcp_test.pcap -Y 'tcp.len > 0' | wc -l").strip().split('\n')[-1])

    # Count lost packets
    lost_packets = int(subprocess.getoutput("tshark -r tcp_test.pcap -Y 'tcp.analysis.lost_segment' 2>/dev/null | wc -l").strip().split('\n')[-1])


    # Count total TCP packets sent
    total_packets = int(subprocess.getoutput("tshark -r tcp_test.pcap -Y 'tcp' 2>/dev/null | wc -l").strip().split('\n')[-1])
    goodput = goodput/total_packets * 100
    

    # Calculate packet loss rate
    if total_packets > 0:
        packet_loss_rate = (lost_packets / total_packets) * 100
    else:
        packet_loss_rate = 0

    max_packet_size = subprocess.getoutput("tshark -r iperf_capture.pcap -T fields -e frame.len | sort -nr | head -1")
    
    print("Throughput:", throughput)
    print("Goodput (total data packets received):", goodput)
    print(f"Packet loss rate: {packet_loss_rate:.2f}%")
    print("Maximum packet size achieved:", max_packet_size)

def run_tcp_test(net, nagle, delayed_ack):

    server = net.get('h7')
    client = net.get('h1')

    configure_tcp_options(server, nagle, delayed_ack)
    configure_tcp_options(client, nagle, delayed_ack)

    # Get correct IP for h7
    server_ip = server.IP()

    # Start tcpdump on the correct interface
    server.cmd('tcpdump -i h7-eth0 port 5001 -w tcp_test.pcap &')
    time.sleep(3)  # Ensure tcpdump starts before traffic

    # Start iPerf Server
    server.cmd('iperf -s -p 5001 &')
    time.sleep(2)  # Ensure server starts

    # Start iPerf Client
    client.cmd(f'iperf -c {server_ip} -p 5001 -n 4K -b 320bps')

    time.sleep(120)  

    server.cmd('pkill iperf')
    time.sleep(2)
    server.cmd('pkill tcpdump')
    time.sleep(2)

    print("Test completed! Results saved to tcp_test.pcap.")
    analyze_pcap()

def cleanup():
    
    os.system('sudo pkill nc')
    os.system('sudo mn -c')

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3:
        print("Usage: python3 script.py <nagle: 0|1> <delayed_ack: 0|1>")
        sys.exit(1)

    nagle = bool(int(sys.argv[1]))
    delayed_ack = bool(int(sys.argv[2]))

    cleanup()
    net = setup_topology()
    run_tcp_test(net, nagle, delayed_ack)
    net.stop()
    cleanup()

