import contextlib

from errors import InputError
from bit_stream import BitOutStream
from bit_stream import BitInStream
import json


class Node:
    """
    用于存储码树的父类
    """

    def __init__(self, count=0, symbol=''):
        self.count = count
        self.symbol = symbol


class Branch(Node):
    """
    用于存储分支节点的类，不存储字节
    """

    def __init__(self, left, right, symbol=(), count=0):
        super().__init__(count, symbol)
        if not isinstance(left, Node) or not isinstance(right, Node):
            raise TypeError("You may get invalid Node format.")
        self.left = left
        self.right = right


class Leaf(Node):
    """
    用于存储字节的叶子节点的类
    """

    def __init__(self, word, count=0, symbol=()):
        super().__init__(count, symbol)
        self.word = word


class Tree(Node):
    """
    用于存储跟节点的类
    """
    def __init__(self, left, right, count=0, symbol=()):
        super().__init__(count, symbol)
        if not isinstance(left, Node) or not isinstance(right, Node):
            raise TypeError("You may get invalid Node format.")
        self.left = left
        self.right = right


def binary_search(key, array):
    """
    用于插入Leaf型前进行的word位置寻找
    :param key: word，bytes
    :param array: word_list, list
    :return: [flag, position]，flag=0表示已经存在，position表示插入位置
    """
    low = 0
    high = len(array) - 1
    while low <= high:
        mid = (low + high) // 2
        if key < array[mid].word:
            high = mid - 1
        elif key > array[mid].word:
            low = mid + 1
        else:
            return [0, mid]
    return [1, low]


def frequency_count(text):
    """
    用于统计词频的函数
    :param text: 文本字节，bytes
    :return: word list, list
    """
    result = [Leaf(256, count=1)]
    for word in text:
        flag, position = binary_search(word, result)
        if flag == 0:
            result[position].count += 1
        else:
            result.insert(position, Leaf(word, count=1))
    result.sort(key=lambda x: x.count, reverse=True)
    return result


def tree_build(word_list):
    """
    用于建成Huffman树的函数
    :param word_list: 应由frequency_count生成的列表，list
    :return: 一个Tree类型的结点，该结点应为一个根
    :raise inputError:输入空列表时报错
    """
    if len(word_list) == 0:
        raise InputError("No word!", "you input a empty word list!")
    if len(word_list) == 1:
        return Tree(word_list[0], Node())
    while len(word_list) != 2:
        a = word_list.pop()
        b = word_list.pop()
        c = Branch(a, b, count=a.count + b.count)
        word_list.insert(0, c)
        word_list.sort(key=lambda x: x.count, reverse=True)
        # position = binary_position(c, word_list)
        # word_list.insert(position, c)
    return Tree(word_list[0], word_list[1])


def symbol_add(node, dic):
    """
    为Huffman树完成编码
    :param dic: 码表，应当由调用者上传，并且为空,list
    :param node: 应当是一个Tree或Branch型
    :return: void.
    """
    node.left.symbol = node.symbol + (0,)
    if not isinstance(node.left, Leaf):
        symbol_add(node.left, dic)
    else:
        if dic[node.left.word] is not None:
            raise ValueError(
                "You are covering symbol of %d. Check your environment." % node.left.word)
        dic[node.left.word] = node.left.symbol
    node.right.symbol = node.symbol + (1,)
    if not isinstance(node.right, Leaf):
        symbol_add(node.right, dic)
    else:
        if dic[node.right.word] is not None:
            raise ValueError(
                "You are covering symbol of %d. Check your environment." % node.right.word)
        dic[node.right.word] = node.right.symbol


def huffman_encode(in_stream, table_stream, out_stream):
    """
    哈夫曼编码函数
    :param out_stream: 输出流
    :param table_stream: 码表流
    :param in_stream: 输入流
    :return:void
    """
    # if not is_std_out:
    text = in_stream.read()
    if text == -1:
        raise InputError(
            "You are reading a empty file. Check the file name and try again later.", "You input empty file")
    # else:
    #     text_str = in_stream.read(32 * 1024)
    #     text = bytes(text_str, encoding='utf-8')
    #     if text == -1:
    #         raise ValueError(
    #             "You are reading a empty stream. Check the file name and try again later.")
    word_list = frequency_count(text)
    root = tree_build(word_list)
    code_dict = [None] * 257
    symbol_add(root, code_dict)
    json.dump(code_dict, table_stream)
    with contextlib.closing(BitOutStream(out_stream)) as out:
        for word in text:
            if code_dict[word] is None:
                raise ValueError(
                    "You are trying to encode a word without huffman encoding.")
            for bit in code_dict[word]:
                out.write(bit)
        for bit in code_dict[256]:
            out.write(bit)


def rebuild_tree(in_stream):
    """
    解码部分重建树
    :param in_stream:输入流
    :return: 码树之根
    """
    heap = []
    origin = json.load(in_stream)
    for (i, symbol) in enumerate(origin):
        if symbol is not None:
            heap.append(Leaf(i, symbol=symbol))
    heap.sort(key=lambda x: x.symbol)
    heap.sort(key=lambda x: len(x.symbol))
    if len(heap) == 1:
        return Tree(heap[0], Node())
    while len(heap) != 2:
        a = heap.pop()
        b = heap.pop()
        if a.symbol[:-1] != b.symbol[:-1]:
            raise ValueError(
                "The Code may have something wrong. Have you changed or replaced it?")
        heap.append(Branch(b, a, a.symbol[:-1]))
        heap.sort(key=lambda x: x.symbol)
        heap.sort(key=lambda x: len(x.symbol))
    root = Tree(heap[0], heap[1])
    return root


def read(tree, stream):
    """
    解码用的读取和翻译函数
    :param tree: 码数之根
    :param stream: 字节流
    :return: 下一个读取到的字符
    """
    node = tree
    while True:
        temp = stream.read_without_EOF()
        if temp == 0:
            next_node = node.left
        elif temp == 1:
            next_node = node.right
        else:
            raise ValueError("Read File Error when we try to decode.")
        if isinstance(next_node, Leaf):
            return next_node.word
        elif isinstance(next_node, Branch):
            node = next_node
        else:
            raise TypeError("All node in the tree should be Branch or Leaf.")


def huffman_decode(in_stream, table_stream, out_stream):
    """
    huffman 解码函数
    :param in_stream:输入字节流
    :param table_stream: 码表字节流
    :param out_stream: 输出字节流
    :return: void
    """
    root = rebuild_tree(table_stream)
    with in_stream as inp, out_stream as out:
        stream = BitInStream(inp)
        while True:
            symbol = read(root, stream)
            if symbol == 256:
                break
            out.write(bytes((symbol,)))


def huff_enc_set(filename, out_name=None):
    """
    huffman编码API
    :param filename:文件名称
    :param out_name: 输出名称，默认filename.enc
    :return: void
    """
    # if not is_std_out:
    out_file = filename + '.enc' if out_name is None else out_name
    with open(filename, 'rb') as inp, open(filename + '.json', 'w') as table, open(out_file, 'wb') as out:
        huffman_encode(inp, table, out)
    # else:
    #     huffman_encode(sys.stdin, sys.stdout, sys.stdout, is_std_out=True)


def huff_dec_set(filename, out_name=None):
    """
    huffman解码API
    :param filename:文件名称
    :param out_name: 输出名称，默认filename[:-4].dec
    :return:
    """
    # if not is_std_out:
    if len(filename) < 4:
        raise ValueError("Program won't receive a file that is not extracted by this program.You may rename the "
                         "file. Change it back or at least end with '.enc'.")
    out_file = filename[:-4] + '.dec' if out_name is None else out_name
    json_file = filename[:-4] + '.json'
    with open(filename, 'rb') as inp, open(json_file, 'r') as table, open(out_file, 'wb') as out:
        huffman_decode(inp, table, out)


def main():
    huff_enc_set('draw.bmp')
    huff_dec_set('draw.bmp.enc')


if __name__ == '__main__':
    main()
