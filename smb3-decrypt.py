import pyshark

def extract_smb3_conversations(pcap_file):
    # Load pcap file
    cap = pyshark.FileCapture(pcap_file)
    smb2_packets = []
    smb_packets = []

    # TODO Instead of using a display filter, create a dictionary with all the pre cut filters so the below loops have less to grab
    for packet in cap:
        if hasattr(packet, 'smb2'):
            smb2_packets.append(packet)
        elif hasattr(packet, 'smb'):
            smb_packets.append(packet)
    session_ids_for_encrypted = {}
    auth_frames_for_encrypted = {}
    auth_packets = {}

    # Identify encrypted SMB traffic exists
    for packet in smb2_packets:
        if hasattr(packet.smb2, 'header_transform_flags_encrypted') and packet.smb2.header_transform_flags_encrypted == '1':
            if hasattr(packet.smb2, 'sesid'):
                session_ids_for_encrypted.setdefault(packet.smb2.sesid, []).append(packet.number)
                auth_frames_for_encrypted.setdefault(packet.smb2.auth_frame, []).append(packet.number)

    #Get the authentication packets for each encrypted SMB3 conversation
    for packet in smb2_packets:     
        if hasattr(packet.smb2, 'cmd') and packet.smb2.sesid in session_ids_for_encrypted:
            auth_packets.setdefault(packet.number, []).append(packet)

    
    return auth_packets

def main():
    pcap_file = 'example/pcap_psexec.pcapng'
    smb3_packets = extract_smb3_conversations(pcap_file)
    print(smb3_packets[0])
    # for packet in smb3_packets:
    #     print(packet)

if __name__ == '__main__':
    main()