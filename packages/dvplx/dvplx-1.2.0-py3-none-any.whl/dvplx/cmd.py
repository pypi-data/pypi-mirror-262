import os
import argparse
import time
from dvplx.converter import ConvertDVPLFiles, VerifyDVPLFiles
from dvplx.color import Color

class Meta:
    NAME = 'DVPLX'
    VERSION = '1.2.0'
    DATE = '13/03/2024'
    DEV = 'RifsxD'
    REPO = 'https://github.com/rifsxd/dvplx'
    WEB = 'https://rxd-mods.xyz'
    INFO = 'A CLI Tool Coded In Python To Convert WoTB ( Dava ) SmartDLC DVPL File Based On LZ4 High Compression.'

def ParseCommandLineArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mode", help="mode can be 'compress' / 'decompress' / 'help' (for an extended help guide).")
    parser.add_argument("-k", "--keep-originals", action="store_true", help="keep original files after compression/decompression.")
    parser.add_argument("-v", "--verbose", action="store_true", help="shows verbose information for all processed files.")
    parser.add_argument("-p", "--path", help="directory/files path to process. Default is the current directory.")
    parser.add_argument("-i", "--ignore", default="", help="Comma-separated list of file extensions to ignore during compression.")
    args = parser.parse_args()

    if not args.mode:
        parser.error("No mode selected. Use '--help' for usage information")

    if not args.path:
        args.path = os.getcwd()

    return args

def PrintHelpMessage():
    print('''dvplx [-mode] [-keep-originals] [-path]

    • mode can be one of the following:

        compress: compresses files into dvpl.
        decompress: decompresses dvpl files into standard files.
        verify: verify compressed dvpl files to determine valid compression.
        help: show this help message.

    • flags can be one of the following:

        --keep-originals: flag keeps the original files after compression/decompression.
        --path: specifies the directory/files path to process. Default is the current directory.
        --ignore: specifies comma-separated file extensions to ignore during compression.
        --verbose: shows verbose information for all processed files.

    • usage can be one of the following examples:

        $ dvplx --mode help

        $ dvplx --mode decompress --path /path/to/decompress/compress

        $ dvplx --mode compress --path /path/to/decompress/compress

        $ dvplx --mode decompress --keep-originals -path /path/to/decompress/compress

        $ dvplx --mode compress --keep-originals -path /path/to/decompress/compress

        $ dvplx --mode decompress --path /path/to/decompress/compress.yaml.dvpl

        $ dvplx --mode compress --path /path/to/decompress/compress.yaml

        $ dvplx --mode decompress --keep-originals --path /path/to/decompress/compress.yaml.dvpl

        $ dvplx --mode dcompress --keep-originals --path /path/to/decompress/compress.yaml

        $ dvplx --mode compress --path /path/to/decompress --ignore .exe,.dll

        $ dvplx --mode compress --path /path/to/decompress --ignore exe,dll

        $ dvplx --mode compress --path /path/to/decompress --ignore test.exe,test.txt
    ''')

def PrintElapsedTime(elapsed_time):
    if elapsed_time < 1:
        print(f"\nProcessing took {Color.GREEN}{int(elapsed_time * 1000)} ms{Color.RESET}\n")
    elif elapsed_time < 60:
        print(f"\nProcessing took {Color.YELLOW}{int(elapsed_time)} s{Color.RESET}\n")
    else:
        print(f"\nProcessing took {Color.RED}{int(elapsed_time / 60)} min{Color.RESET}\n")

def main():
    print(f"\n{Color.BLUE}• Name:{Color.RESET} {Meta.NAME}")
    print(f"{Color.BLUE}• Version:{Color.RESET} {Meta.VERSION}")
    print(f"{Color.BLUE}• Commit:{Color.RESET} {Meta.DATE}")
    print(f"{Color.BLUE}• Dev:{Color.RESET} {Meta.DEV}")
    print(f"{Color.BLUE}• Repo:{Color.RESET} {Meta.REPO}")
    print(f"{Color.BLUE}• Web:{Color.RESET} {Meta.WEB}")
    print(f"{Color.BLUE}• Info:{Color.RESET} {Meta.INFO}\n")

    start_time = time.time()
    config = ParseCommandLineArgs()

    try:
        if config.mode in ["compress", "decompress"]:
            success_count, failure_count, ignored_count = ConvertDVPLFiles(config.path, config)
            print(f"\n\n{Color.GREEN}{config.mode.upper()} FINISHED{Color.RESET}. Successful conversions: {Color.GREEN}{success_count}{Color.RESET}, Failed conversions: {Color.RED}{failure_count}{Color.RESET}, Ignored conversions: {Color.YELLOW}{ignored_count}{Color.RESET}")
        elif config.mode == "verify":
            success_count, failure_count, ignored_count = VerifyDVPLFiles(config.path, config)
            print(f"\n\n{Color.GREEN}VERIFY FINISHED{Color.RESET}. Successful verifications: {Color.GREEN}{success_count}{Color.RESET}, Failed verifications: {Color.RED}{failure_count}{Color.RESET}, Ignored files: {Color.YELLOW}{ignored_count}{Color.RESET}")
        elif config.mode == "help":
            PrintHelpMessage()
        else:
            raise ValueError("Incorrect mode selected. Use '--help' for information.")
    except Exception as e:
        print(f"\n\n{Color.RED}{config.mode.upper()} FAILED{Color.RESET}: {e}\n")

    elapsed_time = time.time() - start_time
    PrintElapsedTime(elapsed_time)

if __name__ == "__main__":
    main()
