import argparse
import os
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from os import cpu_count, makedirs
from pathlib import Path
from zipfile import ZipFile

# Types and docstrings
THRESHOLD = 0.5


class UnableToCountCores(BaseException):
    pass


class IncorrectNumberOfCores(BaseException):
    pass


class Unzipper:

    def __init__(self, zip_archive, path, threads):
        self._path = path
        self._zip_archive = zip_archive
        self.cpu = os.cpu_count()
        if threads is None and self.cpu is None:
            raise UnableToCountCores
        elif threads is None and self.cpu is not None:
            self.threads = min(self.cpu + 4, 32)
        else:
            self.threads = threads

    # save file to disk
    def save_file(self, data, filename):
        # create a path
        filepath = os.join(self._path, filename)
        # write to disk
        with open(filepath, 'wb') as file:
            file.write(data)


class MultiThreadUnzipper(Unzipper):

    # unzip files from an archive
    def unzip_files(self, handle, filenames):
        # unzip multiple files
        for filename in filenames:
            # unzip the file
            handle.extract(filename, self._path)

    # unzip a large number of files
    def unzip(self):
        # open the zip file
        with ZipFile(self._zip_archive, 'r') as handle:
            # list of all files to unzip
            files = handle.namelist()
            # determine chunksize
            chunksize = round(len(files) / self._threads)
            # start the thread pool
            with ThreadPoolExecutor(self._threads) as exe:
                # split the copy operations into chunks
                for i in range(0, len(files), chunksize):
                    # select a chunk of filenames
                    filenames = files[i:(i + chunksize)]
                    # submit the batch copy task
                    _ = exe.submit(self.unzip_files, handle, filenames)


class CombinedUnzipper(Unzipper):

    def __init__(self, zip_archive, path, processes, threads):
        super().__init__(path, zip_archive, threads)
        if processes is None and self.cpu is None:
            raise UnableToCountCores
        elif self.__processes is None and self.cpu is not None:
            self.__processes = self.cpu
        elif self.__processes is not None and self.cpu is None:
            self.__processes = processes
            print("Attention!!! Unable to count cores. Please enter correct \
                number, else it can lead to undefined behaviour.")
        elif self.__processes is not None and self.cpu is not None:
            if self.__processes > self.cpu:
                raise IncorrectNumberOfCores
            else:
                self.__processes = processes

    # unzip files from an archive
    def unzip_files(self, filenames):
        # open the zip file
        with ZipFile(self._zip_archive, 'r') as handle:
            # create a thread pool
            with ThreadPoolExecutor(self._threads) as exe:
                # unzip each file
                for filename in filenames:
                    # decompress data
                    data = handle.read(filename)
                    # save to disk
                    _ = exe.submit(self.save_file, data, filename)

    # unzip a large number of files
    def unzip(self):
        # create the target directory
        makedirs(self._path, exist_ok=True)
        # open the zip file
        with ZipFile(self._zip_archive, 'r') as handle:
            # list of all files to unzip
            files = handle.namelist()
        # determine chunksize
        chunksize = round(len(files) / self.__processes)
        # start the thread pool
        with ProcessPoolExecutor(self.__processes) as exe:
            # split the copy operations into chunks
            for i in range(0, len(files), chunksize):
                # select a chunk of filenames
                filenames = files[i:(i + chunksize)]
                # submit the batch copy task
                _ = exe.submit(self.unzip_files, filenames)


class Controller:
    def __init__(self, mode):
        self.mode = mode

    def calculate_compression(self):
        pass

    def get_compression(self):
        pass


def parse_args() -> Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('archive_path', metavar='path', type=Path)
    parser.add_argument('-p', '--n_proc', default=None, type=int,
                        help='Number of processes')
    parser.add_argument('-t', '--n_threads', default=None, type=int,
                        help='Number of threads for tasks in one process')
    parser.add_argument('-d', '--outdir', default=Path('./ZIP_unpack'),
                        type=Path, help='Output directory to put unpacked \
                            data')
    parser.add_argument('-m', '--mode', default=None,
                        type=str, help='Mode in which program should work:\
                            "mt" or "cmbd"')
    args = parser.parse_args()

    assert args.archive_path.exists(), f'{args.archive_path}'
    return args


def main():
    args = parse_args()
    if args.mode is None:
        compression = Controller(args.mode).get_compression()
        if compression > THRESHOLD:
            MultiThreadUnzipper(args.archive_path, args.outdir,
                                args.n_threads).unzip()
        elif compression <= THRESHOLD:
            CombinedUnzipper(args.archive_path, args.outdir, args.n_proc,
                             args.n_threads).unzip()
    elif args.mode == "mt":
        MultiThreadUnzipper(args.archive_path, args.outdir,
                            args.n_threads).unzip()
    elif args.mode == "cmbd":
        CombinedUnzipper(args.archive_path, args.outdir, args.n_proc,
                         args.n_threads).unzip()


# entry point
if __name__ == '__main__':
    main()
