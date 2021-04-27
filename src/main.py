import argparse
import huffman
import lz78


def main():
    parser = argparse.ArgumentParser(description='Encode or decode files by huffman or lz78')
    prog = parser.add_mutually_exclusive_group(required=True)
    prog.add_argument('-eh', '--enchuff', help='Use Huffman Code to encode a file, need a file')
    prog.add_argument('-dh', '--dechuff',
                      help='Use Huffman Code to decode a file, need a .enc file and a .json table with the same name.')
    prog.add_argument('-el', '--enclz78', help='Use LZ78 to encode a file, need a file.')
    prog.add_argument('-dl', '--declz78', help='Use LZ78 to decode a file, need a file end with .enc')
    parser.add_argument('-o', '--out', help='spercify the output file name.')
    args = parser.parse_args()
    out = args.out
    if args.enchuff is not None:
        huffman.huff_enc_set(args.enchuff, out)
    elif args.dechuff is not None:
        huffman.huff_dec_set(args.dechuff, out)
    elif args.enclz78 is not None:
        lz78.lz78_enc_set(args.enclz78, out)
    elif args.declz78 is not None:
        lz78.lz78_dec_set(args.declz78, out)


if __name__ == '__main__':
    main()
