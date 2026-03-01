import serial

ser = serial.Serial('COM6',9600,timeout=1)

print("Connected to COM6")

while True:

    encrypted = ser.read(100)

    if not encrypted:
        continue

    # Decrypt
    decrypted = bytearray()
    for b in encrypted:
        decrypted.append(b ^ 0x55)

    try:
        line = decrypted.decode(errors='ignore')
    except:
        continue

    # Find one packet
    start = line.find('<')
    end = line.find('\r\n')

    if start == -1 or end == -1:
        continue

    packet = line[start:end]

    if '*' not in packet:
        continue

    data_part, received_checksum = packet.split('*', 1)

    calc_checksum = 0
    for ch in data_part:
        calc_checksum ^= ord(ch)

    if f"{calc_checksum:02X}" == received_checksum:
        print("VALID:", data_part)
    else:
        print("CORRUPTED MESSAGE")