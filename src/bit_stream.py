class BitOutStream:
    def __init__(self, out):
        self.output = out
        self.buff_len = 0
        self.buffer = 0

    def write(self, b):
        if b not in (0, 1):
            raise ValueError("Bit should be 0 or 1")
        self.buffer = (self.buffer << 1) | b
        self.buff_len += 1
        if self.buff_len == 8:
            outs = bytes((self.buffer,))
            self.output.write(outs)
            self.buffer = 0
            self.buff_len = 0

    def close(self):
        while self.buff_len != 0:
            self.write(0)
        self.output.close()


class BitInStream:
    def __init__(self, inp):
        self.inp = inp
        self.buffer = 0
        self.buff_len = 0

    def read(self):
        if self.buffer == -1:
            return -1
        elif self.buff_len == 0:
            byte = self.inp.read(1)
            if len(byte) == 0:
                self.buffer = -1
                return -1
            self.buffer = byte[0]
            self.buff_len = 8
        self.buff_len -= 1
        return (self.buffer >> self.buff_len) & 1

    def read_without_EOF(self):
        bit = self.read()
        if bit != -1:
            return bit
        else:
            raise EOFError(
                "The bit stream should be close before you reach EOF. You may change the file or use file that "
                "extracted by other program.")

    def close(self):
        self.inp.close()
        self.buffer = -1
        self.buff_len = 0
