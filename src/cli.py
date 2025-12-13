import argparse
import json
import sys
from controllers import XMLController
from utils import file_io

parser = argparse.ArgumentParser(description="use XML editor in CLI mode")
commands =parser.add_subparsers(dest='command', help='Available functionalities',required=True)

verify_arg = commands.add_parser('verify', help= 'verify the structure of the XML provided')
verify_arg.add_argument('-i',"--input",required=True,type=str,help='Path to the input XML file')
verify_arg.add_argument('-o',"--output",required=False,type=str,help='Path to the output XML file')
verify_arg.add_argument('-f', "--fix", required=False, action='store_true', help='fix the XML file...')

format_arg = commands.add_parser('format', help= 'formatting the xml file to the standard format')
format_arg.add_argument('-i',"--input",required=True,type=str,help='Path to the input XML file')
format_arg.add_argument('-o',"--output",required=False,type=str,help='Path to the output XML file')

json_arg = commands.add_parser('json', help= 'transform the XMl file to a json format file')
json_arg.add_argument('-i',"--input",required=True,type=str,help='Path to the input XML file')
json_arg.add_argument('-o',"--output",required=False,type=str,help='Path to the output XML file')

mini_arg = commands.add_parser('mini', help= 'strip spaces in XML file')
mini_arg.add_argument('-i',"--input",required=True,type=str,help='Path to the input XML file')
mini_arg.add_argument('-o',"--output",required=False,type=str,help='Path to the output XML file')

compress_arg = commands.add_parser('compress', help= 'compressing XML file to specified destination')
compress_arg.add_argument('-i',"--input",required=True,type=str,help='Path to the input XML file')
compress_arg.add_argument('-o',"--output",required=False,type=str,help='Path to the output XML file')

decompress_arg = commands.add_parser('decompress', help= 'decompressing XML file to specified destination')
decompress_arg.add_argument('-i',"--input",required=True,type=str,help='Path to the input XML file')
decompress_arg.add_argument('-o',"--output",required=False,type=str,help='Path to the output XML file')


if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

editor = XMLController()
args = parser.parse_args()
if args.command == 'verify':
    if args.fix and args.output is None:
        print("invalid usage")

    if file_io.read_file(args.input)[0]:
        editor.set_xml_string(file_io.read_file(args.input)[1])
        editor.set_xml_string(editor.validate())
        ack = editor.format()
        if args.output is not None:
            file_io.write_file(args.output, ack)
        print(ack)
    else:
        print("invalid path")

if args.command == 'format':
    if file_io.read_file(args.input)[0]:
        editor.set_xml_string(file_io.read_file(args.input)[1])
        ack = editor.format()
        if args.output is not None:
            file_io.write_file(args.output,ack)
        print(ack)
    else:
        print("invalid file path")

if args.command == 'json':
    ack = file_io.read_file(args.input)
    if ack[0]:
        editor.set_xml_string(file_io.read_file(args.input)[1])
        bool_mes, _, json_data = editor.export_to_json()
        if bool_mes:
            if args.output is not None:
                with open(args.output, 'w', encoding='utf-8') as f:
                    json.dump(json_data, f, indent=2, ensure_ascii=False)
            else:
                print(f"json data format: \n\n{json_data}")
        else:
            print("invalid argument")

