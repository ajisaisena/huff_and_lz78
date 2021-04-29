import argparse
import textwrap

import huffman
import lz78


def cli():
    """
    命令行设计函数
    :return: void
    """
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=textwrap.dedent('''\
         Encode or decode files by huffman or lz78
         --------------------------------
         Examples:
            python main.py -eh draw.bmp #使用huffman编码对draw.bmp进行压缩
            python main.py -dh draw.bmp.enc -o draw.bmp.dec -t draw.json #对draw.bmp.enc进行huffman解码，输出为draw.bmp.dec,码表为draw.json
            python main.py -el draw.bmp # 使用lz78编码对draw.bmp进行压缩
            python main.py -dl draw.bmp.enc #对draw.bmp.enc进行解码，默认输出为draw.bmp.dec
         '''))
    prog = parser.add_mutually_exclusive_group(required=True)
    prog.add_argument('-eh', '--enchuff',
                      help='Use Huffman Code to encode a file, need a file')
    prog.add_argument('-dh', '--dechuff',
                      help='Use Huffman Code to decode a file, need a .enc file and a .json table with the same name.')
    prog.add_argument('-el', '--enclz78',
                      help='Use LZ78 to encode a file, need a file.')
    prog.add_argument(
        '-dl', '--declz78', help='Use LZ78 to decode a file, need a file end with .enc')
    parser.add_argument(
        '-o', '--out', help='spercify the output file name. The defalt is filename[:-4].dec')
    parser.add_argument(
        '-t', '--table', help='spercify the code table file.The defalt is filename.json')
    args = parser.parse_args()
    out = args.out
    table = args.table
    if args.enchuff is not None:
        huffman.huff_enc_set(args.enchuff, table, out)
    elif args.dechuff is not None:
        huffman.huff_dec_set(args.dechuff, table, out)
    elif args.enclz78 is not None:
        lz78.lz78_enc_set(args.enclz78, out)
    elif args.declz78 is not None:
        lz78.lz78_dec_set(args.declz78, out)


def main():
    cli()


if __name__ == '__main__':
    main()
