import argparse
import os
import sys
from zipfile import ZipFile

BUF_SIZE = 1024


# How to compare files in two zip file are totally same or not?
# https://stackoverflow.com/a/66540276/598057
def are_equivalent(filename1, filename2):
    """
    Compare two ZipFiles to see if they would expand into the same directory
    structure without actually extracting the files.
    """

    with ZipFile(filename1, "r") as zip1, ZipFile(filename2, "r") as zip2:
        # Index items in the ZipFiles by filename. For duplicate filenames, a
        # later item in the ZipFile will overwrite an ealier item; just like a
        # later file will overwrite an earlier file with the same name when
        # extracting.
        zipinfo1 = {info.filename: info for info in zip1.infolist()}
        zipinfo2 = {info.filename: info for info in zip2.infolist()}

        # Do some simple checks first
        # Do the ZipFiles contain the same the files?
        if zipinfo1.keys() != zipinfo2.keys():
            return False

        # Do the files in the archives have the same CRCs? (This is a 32-bit
        # CRC of the uncompressed item. Is that good enough to confirm the files
        # are the same?)
        if any(
            zipinfo1[name].CRC != zipinfo2[name].CRC for name in zipinfo1.keys()
        ):
            return False

        # Skip/omit this loop if matching names and CRCs is good enough.
        # Open the corresponding files and compare them.
        for name in zipinfo1.keys():
            # 'ZipFile.open()' returns a ZipExtFile instance, which has a
            # 'read()' method that accepts a max number of bytes to read.
            # In contrast, 'ZipFile.read()' reads all the bytes at once.
            with zip1.open(zipinfo1[name]) as file1, zip2.open(
                zipinfo2[name]
            ) as file2:
                while True:
                    buffer1 = file1.read(BUF_SIZE)
                    buffer2 = file2.read(BUF_SIZE)

                    if buffer1 != buffer2:
                        return False

                    if not buffer1:
                        break

        return True


main_parser = argparse.ArgumentParser()

main_parser.add_argument("lhs_file", type=str, help="")

main_parser.add_argument("rhs_file", type=str, help="")

args = main_parser.parse_args()

if not os.path.exists(args.lhs_file):
    print(  # noqa: T201
        "error: path does not exist: {}".format(args.lhs_file), file=sys.stderr
    )
    exit(1)
if not os.path.exists(args.rhs_file):
    print(  # noqa: T201
        "error: path does not exist: {}".format(args.rhs_file), file=sys.stderr
    )
    exit(1)

if not are_equivalent(args.lhs_file, args.rhs_file):
    print(  # noqa: T201
        "error: files {} and {} are not identical".format(
            args.lhs_file, args.rhs_file
        )
    )
    exit(1)
