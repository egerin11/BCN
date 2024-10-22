import random


class Packet:
    def __init__(self, group_number, com_port, data):
        self.data = data
        self.flag = group_number
        self.source_address = int(com_port[-1])
        self.destination_address = 0
        self.fcs = self.calculate_hamming_code(self.to_bits(self.data))

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

    @staticmethod
    def calculate_hamming_code(data_bits):
        m = len(data_bits)
        r = 0
        while (2 ** r) < (m + r + 1):
            r += 1

        code_bits = ['0'] * (m + r)
        j = 0
        for i in range(1, len(code_bits) + 1):
            if (i & (i - 1)) != 0:
                code_bits[i - 1] = data_bits[j]
                j += 1

        for i in range(r):
            pos = 2 ** i
            parity = 0
            for j in range(1, len(code_bits) + 1):
                if j & pos:
                    parity ^= int(code_bits[j - 1])
            code_bits[pos - 1] = str(parity)

        return ''.join(code_bits)

    @staticmethod
    def hamming_decode(code_bits):
        r = 0
        while (2 ** r) < len(code_bits):
            r += 1

        error_pos = 0
        for i in range(r):
            pos = 2 ** i
            parity = 0
            for j in range(1, len(code_bits) + 1):
                if j & pos:
                    parity ^= int(code_bits[j - 1])
            if parity != 0:
                error_pos += pos

        if error_pos:
            print(f"Ошибка в позиции {error_pos}. Исправляем...")
            code_bits = list(code_bits)
            code_bits[error_pos - 1] = '0' if code_bits[error_pos - 1] == '1' else '1'

        return ''.join(code_bits)

    @staticmethod
    def introduce_random_errors(data_bits, error_prob_1=0.6, error_prob_2=0.25):
        data_bits = list(data_bits)
        if random.random() < error_prob_1:
            pos = random.randint(0, len(data_bits) - 1)
            data_bits[pos] = '0' if data_bits[pos] == '1' else '1'
            print(f"Один бит изменен в позиции {pos}")
        if random.random() < error_prob_2:
            pos = random.randint(0, len(data_bits) - 1)
            data_bits[pos] = '0' if data_bits[pos] == '1' else '1'
            print(f"Второй бит изменен в позиции {pos}")
        return ''.join(data_bits)

    def get_packet_with_stuffing(self):
        packet_data = (
                self.to_bits(self.flag) +
                self.to_bits(self.source_address) +
                self.to_bits(self.destination_address) +
                self.to_bits(self.data) +
                self.fcs
        )

        stuffed_data = self.bit_stuffing(packet_data)
        return stuffed_data

    def get_packet_without_stuffing(self, stuffed_data):
        return self.bit_destuffing(stuffed_data)



