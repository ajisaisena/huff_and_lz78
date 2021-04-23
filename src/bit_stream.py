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
