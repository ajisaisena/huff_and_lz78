from errors import InputError


def lz78_encode(in_stream, out_stream):
    """
    lz78 编码函数
    :param in_stream:输入字节流
    :param out_stream: 输出字节流
    :return: void
    """
    i = 0
    dic = {}
    text = in_stream.read()
    if text == -1:
        raise InputError('Input empty file', 'You input an empty file!!!')
    while i < len(text):
        if text[i:i + 1] not in dic.keys():
            dic[text[i:i + 1]] = len(dic) + 1
            out_stream.write(b'0' + text[i:i + 1])
            i += 1
        elif i == len(text) - 1:
            out_stream.write(bytes(str(dic[text[i:i + 1]]), encoding='utf-8'))
            i += 1
        else:
            for j in range(i + 1, len(text)):
                if text[i:j + 1] not in dic.keys():
                    dic[text[i:j + 1]] = len(dic) + 1
                    out_stream.write(
                        bytes(str(dic[text[i:j]]), encoding='utf-8') + text[j:j + 1])
                    i = j + 1
                    break
                elif j == len(text) - 1:
                    out_stream.write(
                        bytes(str(dic[text[i:j + 1]]), encoding='utf-8'))
                    i = j + 1


def lz78_decode(in_stream, out_stream):
    """
    lz78 解码函数
    :param in_stream:输入字节流
    :param out_stream: 输出字节流
    :return:
    """
    result = b''
    dic = {}
    i = 0
    text = in_stream.read()
    if text == -1:
        raise InputError('Input empty file', 'You input an empty file!!!')
    while i < len(text):
        j = i
        while text[i:i + 1].isdigit():
            i += 1
            if i == len(text) - 1:
                if not text[i:i + 1].isdigit():
                    break
                out_stream.write(dic[int(text[j:i + 1])])
                result += dic[int(text[j:i + 1])]
                return
            elif text[j:i] == b'0':
                break
            elif int(text[j:i]) not in dic.keys():
                i -= 1
                break
        num = text[j:i]
        if num == b'0':
            dic[len(dic) + 1] = text[i:i + 1]
        else:
            dic[len(dic) + 1] = dic[int(num)] + text[i:i + 1]
        out_stream.write(dic[len(dic)])
        result += dic[len(dic)]
        i += 1


def lz78_enc_set(filename, outname=None):
    """
    lz78 编码API
    :param filename: 文件名称
    :param outname: 输出文件名称
    :return: void
    """
    outfile = filename + '.enc' if outname is None else outname
    with open(filename, 'rb') as inp, open(outfile, 'wb') as out:
        lz78_encode(inp, out)


def lz78_dec_set(filename, outname=None):
    """
    lz78 解码API
    :param filename: 文件名称
    :param outname: 输出名称
    :return: void
    """
    if len(filename) < 4:
        raise ValueError("Program won't receive a file that is not extracted by this program.You may rename the "
                         "file. Change it back or at least end with '.enc'.")
    outfile = filename[:-4] + '.dec' if outname is None else outname
    with open(filename, 'rb') as inp, open(outfile, 'wb') as out:
        lz78_decode(inp, out)


def main():
    inp = open('draw.bmp', 'rb')
    out = open('draw.bmp.enc', 'wb')
    lz78_encode(inp, out)
    inp.close()
    out.close()
    ind = open('draw.bmp.enc', 'rb')
    oud = open('draw.bmp.dec', 'wb')
    lz78_decode(ind, oud)
    ind.close()
    oud.close()


if __name__ == '__main__':
    main()
