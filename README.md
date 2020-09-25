# scan2book

OCR pipeline to create a single text file from scanned pages of books.


## Dependencies

- unpaper ([https://github.com/unpaper/unpaper](https://github.com/unpaper/unpaper))
- tesseract 4
- imagemagick


## Usage

```
    run.sh - Run OCR pipeline.

    USAGE:
        run.sh --directory <scan_directory> [--title <book_title>] [-j <threads>]

    OPTIONS:
        -d|--directory   * Input directory with scanned images
        -t|--title         Book title [default 'untitled']
        -j                 Number of threads [default: 2]
        -h|--help          This help

    EXAMPLE:
        run.sh --directory example/scan --title example
```


```bash
./run.sh --directory example/scan/ --title "book"
```


