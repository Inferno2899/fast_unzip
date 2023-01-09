# Fast unzipper

Fast unzipper is a Python CLI tool you could use to effectively and fast unzip ZIP archives.

## When will it be helpful?

It proved to be useful working with huge amount of relatively small files for it distributes load among processes and threads to provide higher speeds than standard unzip.

However, should you need to unzip archive with only few files, that tool isn't probably for you because it won't be possible to distribute 1 or 2 files in archive among threads.

Moreover, changing threads(e.g. 8) when there are 8 files will lead to decrease in performance rather than profit in time.

Use it when it's possible to adequately split your files.


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install fast_unzip.

```bash
pip install fast_unzip
```

## Usage
It's compulsory you specify the archive PATH like this.

MacOS/Linux
```bash
python3 -m fast_unzip test.zip
```
Windows
```bash
python -m fast_unzip test.zip
```
Being started this way it will use standard mode which means it will decide automatically which mode to use depending on compression level of your archive.

Standard directory for unpacking is ./ZIP_unpack.
You can specify it with -d flag.
```bash
python -m fast_unzip test.zip -d ./../test
```

Nevertheless, you can specify number of processes and threads you want to start using -p and -t flags.
```bash
python3 -m fast_unzip test.zip -p 4 -t 10
```
Also, you can specify mode you want this tool to work. Maybe you know beforehand that compression level is low. You do it with -m flag.
```bash
python -m fast_unzip test.zip -m "mt"
```
## Recommendations
Though, it's possible to choose mode, number of threads and number of processes manually, it's highly unrecommended, because if will affect the performance.

Number of threads is chosen as `min(32, os.cpu_count())`.

Number of processes is chosen as `os.cpu_count()`.

For some reasons `os.cpu_count()` can fail to determine your system characteristics. This way you'll be given an error and you need to specify this arguments explicitly. I highly recommend you use formula from above.

If you try to enter more processes than `os.cpu_count()`
found you'll be given an error. You can either choose an appropriate number of processes or leave it to program to decide.

**!!! If it's impossible for `os.cpu_count()` to work and you enter inappropriate number of processes it will lead to undefined behaviour.**

If you know that archive you want to unpack is compressed less than 50% you can use `-m "cmbd"`, else `-m "mt"`. It will disable part of program doing analysis and increase performance.

Thank you for using our tool!

## License

[MIT](https://choosealicense.com/licenses/mit/)
