import os
import threading
import zlib
from concurrent.futures import ThreadPoolExecutor
from dvplx.dvpl import DecompressDVPL, CompressDVPL, readDVPLFooter, DVPL_FOOTER_SIZE
from dvplx.color import Color

output_lock = threading.Lock()

def ConvertDVPLFiles(directory_or_file, config):
    success_count = 0
    failure_count = 0
    ignored_count = 0

    if os.path.isdir(directory_or_file):
        dir_list = os.listdir(directory_or_file)
        with ThreadPoolExecutor() as executor:
            future_results = []
            for dir_item in dir_list:
                future_results.append(executor.submit(ConvertDVPLFiles, os.path.join(directory_or_file, dir_item), config))
            for future in future_results:
                succ, fail, ignored = future.result()
                success_count += succ
                failure_count += fail
                ignored_count += ignored
    else:
        is_decompression = config.mode == "decompress" and directory_or_file.endswith(".dvpl")
        is_compression = config.mode == "compress" and not directory_or_file.endswith(".dvpl")

        ignore_extensions = config.ignore.split(",") if config.ignore else []
        should_ignore = any(directory_or_file.endswith(ext) for ext in ignore_extensions)

        if not should_ignore and (is_decompression or is_compression):
            file_path = directory_or_file
            try:
                with open(file_path, "rb") as f:
                    file_data = f.read()

                if is_compression:
                    processed_block = CompressDVPL(file_data)
                    new_name = file_path + ".dvpl"
                else:
                    processed_block = DecompressDVPL(file_data)
                    new_name = os.path.splitext(file_path)[0]

                with open(new_name, "wb") as f:
                    f.write(processed_block)

                if not config.keep_originals:
                    os.remove(file_path)

                success_count += 1
                if config.verbose:
                    with output_lock:
                        print(f"{Color.GREEN}\nFile{Color.RESET} {file_path} has been successfully {Color.GREEN}{'compressed' if is_compression else 'decompressed'}{Color.RESET} into {Color.GREEN}{new_name}{Color.RESET}")
            except Exception as e:
                failure_count += 1
                if config.verbose:
                    with output_lock:
                        print(f"{Color.RED}\nError{Color.RESET} processing file {file_path}: {e}")
        else:
            ignored_count += 1
            if config.verbose:
                with output_lock:
                    print(f"{Color.YELLOW}\nIgnoring{Color.RESET} file {directory_or_file}")

    return success_count, failure_count, ignored_count

def VerifyDVPLFiles(directory_or_file, config):
    success_count = 0
    failure_count = 0
    ignored_count = 0

    if os.path.isdir(directory_or_file):
        dir_list = os.listdir(directory_or_file)
        with ThreadPoolExecutor() as executor:
            future_results = []
            for dir_item in dir_list:
                future_results.append(executor.submit(VerifyDVPLFiles, os.path.join(directory_or_file, dir_item), config))
            for future in future_results:
                succ, fail, ignored = future.result()
                success_count += succ
                failure_count += fail
                ignored_count += ignored
    else:
        is_dvpl_file = directory_or_file.endswith(".dvpl")

        ignore_extensions = config.ignore.split(",") if config.ignore else []
        should_ignore = any(directory_or_file.endswith(ext) for ext in ignore_extensions)

        if not should_ignore and is_dvpl_file:
            file_path = directory_or_file
            try:
                with open(file_path, "rb") as f:
                    file_data = f.read()

                footer_data = readDVPLFooter(file_data)

                target_block = file_data[:-DVPL_FOOTER_SIZE]

                if len(target_block) != footer_data.compressed_size:
                    raise ValueError(Color.RED + "DVPLSizeMismatch" + Color.RESET)

                if zlib.crc32(target_block) != footer_data.crc32:
                    raise ValueError(Color.RED + "DVPLCRC32Mismatch" + Color.RESET)

                if config.verbose:
                    with output_lock:
                        print(f"{Color.GREEN}\nFile{Color.RESET} {file_path} has been successfully {Color.GREEN}verified.{Color.RESET}")

                success_count += 1
            except Exception as e:
                failure_count += 1
                if config.verbose:
                    with output_lock:
                        print(f"{Color.RED}\nError{Color.RESET} verifying file {file_path}: {e}")
        else:
            ignored_count += 1
            if config.verbose:
                with output_lock:
                    print(f"{Color.YELLOW}\nIgnoring{Color.RESET} file {directory_or_file}")

    return success_count, failure_count, ignored_count