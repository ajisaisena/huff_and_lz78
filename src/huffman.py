from errors import InputError


class Node:
    def __init__(self, count=0, symbol=''):
        self.count = count
        self.symbol = symbol


class Branch(Node):
    def __init__(self, left, right, symbol='', count=0):
        super().__init__(count, symbol)
        if not isinstance(left, Node) or not isinstance(right, Node):
            raise TypeError("You may get invalid Node format.")
        self.left = left
        self.right = right


class Leaf(Node):
    def __init__(self, word, count=0, symbol=''):
        super().__init__(count, symbol)
        self.word = word


class Tree(Node):
    def __init__(self, left, right, count=0, symbol=''):
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


def binary_position(key, array):
    """
    用于插入Branch型时的二分查找
    :param key: 需要插入的Branch, Branch
    :param array: word list, list
    :return: 位置，该函数设定新插入的Branch永远居前
    """
    low = 0
    high = len(array) - 1
    while low <= high:
        mid = (low + high) // 2
        if key.count < array[mid].count:
            high = mid - 1
        elif key.count > array[mid].count:
            low = mid + 1
        else:
            return mid
    return low


def frequency_count(text):
    """
    用于统计词频的函数
    :param text: 文本字节，bytes
    :return: word list, list
    """
    result = []
    for word in text:
        flag, position = binary_search(word, result)
        if flag == 0:
            result[position].count += 1
        else:
            result.insert(position, Leaf(word))
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
        position = binary_position(c, word_list)
        word_list.insert(position, c)
    return Tree(word_list[0], word_list[1])


def symbol_add(node, dic):
    """
    为Huffman树完成编码
    :param dic: 码表，应当由调用者上传，并且为空
    :param node: 应当是一个Tree或Branch型
    :return: void.
    """
    node.left.symbol = node.symbol + '0'
    if not isinstance(node.left, Leaf):
        symbol_add(node.left, dic)
    else:
        dic[node.left.word] = node.left.symbol
    node.right.symbol = node.symbol + '1'
    if not isinstance(node.right, Leaf):
        symbol_add(node.right, dic)
    else:
        dic[node.right.word] = node.right.symbol


def huffman_encoder(filename):
    with open(filename, 'rb') as f:
        text = f.read()
        if text == -1:
            raise ValueError("You are reading a empty file. Check the file name and try again later.")
    word_list = frequency_count(text)
    root = tree_build(word_list)
    code_dict = {}
    symbol_add(root, code_dict)

