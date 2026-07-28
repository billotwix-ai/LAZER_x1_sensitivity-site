import re
from scapy.all import rdpcap, TCP, UDP

# ==========================================
# CONFIGURATION
# ==========================================
PCAP_FILE = "your_capture.pcap"       # Change this to your actual PCAP file name
OUTPUT_FILE = "extracted_game_info.txt" # The text file where results will be saved

# Known signatures based on your project details
JWT_REGEX = re.compile(r'(eyJ[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_=]*)')

def extract_info_from_pcap(pcap_path, output_path):
    print(f"[*] Loading and analyzing {pcap_path}... (This might take a moment)")
    
    try:
        # Load all packets from the PCAP file
        packets = rdpcap(pcap_path)
    except Exception as e:
        print(f"[-] Error reading PCAP file: {e}")
        return

    extracted_tokens = set()
    extracted_messages = []
    
    packet_count = 0
    
    for packet in packets:
        packet_count += 1
        
        # We only care about network packets that carry actual data payloads (TCP or UDP)
        if packet.haslayer(TCP) or packet.haslayer(UDP):
            payload = bytes(packet[TCP].payload if packet.haslayer(TCP) else packet[UDP].payload)
            
            if not payload:
                continue

            # Try decoding the raw bytes into a readable string (ignoring errors for binary data)
            try:
                payload_text = payload.decode('utf-8', errors='ignore')
            except Exception:
                continue

            # 1. Search for potential JWT Token signatures (starting with eyJ)
            tokens = JWT_REGEX.findall(payload_text)
            for token in tokens:
                # Ensure it's long enough to be a real token structure
                if len(token) > 50 and token not in extracted_tokens:
                    extracted_tokens.add(token)

            # 2. Search for plain text clues (e.g., custom protocol text strings)
            # You can customize these keywords based on what you typed in the chat
            keywords = ["bearer", "token", "uid", "clan"]
            for keyword in keywords:
                if keyword in payload_text.lower():
                    # Record the packet number, the matching keyword, and printable text context
                    clean_text = "".join([c if 32 <= ord(c) < 127 else "." for c in payload_text]).strip()
                    extracted_messages.append(f"[Packet #{packet_count}] Found '{keyword}': {clean_text}")

    # ==========================================
    # SAVE THE RESULTS TO A TEXT FILE
    # ==========================================
    print(f"[*] Analysis complete. Saving results to {output_path}...")
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("=== EXTRACTED SESSION TOKENS ===\n")
        if extracted_tokens:
            for token in extracted_tokens:
                f.write(f"Token: {token}\n\n")
                print(f"[+] Found Token fragment: {token[:20]}...")
        else:
            f.write("No unencrypted JWT tokens found.\n\n")

        f.write("\n=== POTENTIAL PLAIN-TEXT MESSAGES / DATA ===\n")
        if extracted_messages:
            for msg in extracted_messages:
                f.write(f"{msg}\n")
                print(f"[+] Found keyword reference in packet log.")
        else:
            f.write("No matching plain-text game strings found. Traffic might be fully encrypted.\n")

    print(f"[+] Done! All results saved directly to '{output_path}'.")

if __name__ == "__main__":
    extract_info_from_pcap(PCAP_FILE, OUTPUT_FILE)