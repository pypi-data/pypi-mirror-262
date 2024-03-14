# DVPLX Cli Converter
- A Cli Tool Coded In Python To Convert WoTB ( Dava ) SmartDLC DVPL File Based On LZ4 High Compression.

Usage :

    dvplx [-mode] [-keep-originals] [-path]

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

Running :

- python 3.10+ required!

```
$ git clone https://github.com/rifsxd/dvplx.git
```

```
$ cd dvplx/src/dvplx
```

```
$ py ./dvplx.py -h
```
