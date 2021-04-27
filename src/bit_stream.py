class BitOutStream:
    """
    为（huffman）编码使用的比特流类
    """

    def __init__(self, out):
        """
        输出比特流构造方法
        :param out: 输出字节流
        """
        self.output = out
        self.buff_len = 0
        self.buffer = 0

    def write(self, b):
        """
        输出字节流中二进制字节写入方法
        :param b: 写入的单比特
        :return: void
        """
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
        """
        字节流关闭方法
        :return: void
        """
        while self.buff_len != 0:
            self.write(0)
        self.output.close()


class BitInStream:
    """
    为(Huffman)解码实现的比特读入流
    """

    def __init__(self, inp):
        """
        比特读入流的构造方法
        :param inp: 输入字节流
        """
        self.inp = inp
        self.buffer = 0
        self.buff_len = 0

    def read(self):
        """
        比特流读入方法
        :return: void
        """
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
        """
        比特流中不读入EOF的写入方法
        :return: void
        """
        bit = self.read()
        if bit != -1:
            return bit
        else:
            raise EOFError(
                "The bit stream should be close before you reach EOF. You may change the file or use file that "
                "extracted by other program.")

    def close(self):
        """
        比特流关闭方法
        :return: void
        """
        self.inp.close()
        self.buffer = -1
        self.buff_len = 0
