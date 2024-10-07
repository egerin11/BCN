class Packet:
    def __init__(self, group_number, com_port, data):
        self.data = data
        self.flag = group_number
        self.source_address = int(com_port[-1])
        self.destination_address = 0
        self.fcs = 0

    @staticmethod
    def bit_stuffing(data):
        stuffed_data = []
        count = 0
        for bit in data:
            stuffed_data.append(bit)
            if bit == '1':
                count += 1
            else:
                count = 0
            if count == 5:
                stuffed_data.append('[0]')
                count = 0
        return ''.join(stuffed_data)

    @staticmethod
    def bit_destuffing(stuffed_data):
        destuffed_data = []
        count = 0
        i = 0
        while i < len(stuffed_data):
            if stuffed_data[i] == '[':
                i += 3
                continue
            bit = stuffed_data[i]
            destuffed_data.append(bit)
            if bit == '1':
                count += 1
            else:
                count = 0
            if count == 5:
                i += 1
                count = 0
            i += 1
        return ''.join(destuffed_data)

    @staticmethod
    def string_to_bits(s):
        return ''.join(format(ord(c), '08b') for c in s)

    @staticmethod
    def number_to_bits(n):
        return bin(n)[2:]

    @staticmethod
    def to_bits(data):
        if isinstance(data, str):
            return Packet.string_to_bits(data)
        elif isinstance(data, int):
            return Packet.number_to_bits(data)

    def get_packet_with_stuffing(self):
        packet_data = (
                self.to_bits(self.flag) +
                self.to_bits(self.source_address) +
                self.to_bits(self.destination_address) +
                self.to_bits(self.data) +
                self.to_bits(self.fcs)
        )

        stuffed_data = self.bit_stuffing(packet_data)
        return stuffed_data

    def get_packet_without_stuffing(self, stuffed_data):
        return self.bit_destuffing(stuffed_data)
