#! /usr/bin/env bash

function usage(){
    prog=$(basename $0)
    echo "
    $prog - Run OCR pipeline.

    USAGE:
        $prog --directory <scan_directory> [--title <book_title>] [-j <threads>]

    OPTIONS:
        -d|--directory   * Input directory with scanned images
        -t|--title         Book title [default 'untitled']
        -j                 Number of threads [default: 2]
        -h|--help          This help

    EXAMPLE:
        $prog --directory example/scan --title example
"
}


title="untitled"
threads=2

readonly OPTIONS=d:t:j:h
readonly LONGOPTIONS=directory:,title:,help

PARSED=$(getopt --options=$OPTIONS --longoptions=$LONGOPTIONS --name "$0" -- "$@")

if [[ $? -ne 0 ]]; then
    exit 1
fi

eval set -- "$PARSED"

while true; do
    case "$1" in
        -d|--directory)
            directory="$2"; shift 2 ;;
        -t|--title)
            title="$2"; shift 2 ;;
        -j)
            threads="$2"; shift 2 ;;
        -h|--help)
            usage
            exit 0 ;;
        --)
            shift
            break ;;
        *)
            exit 3 ;;
    esac
done

if [[ -z $directory ]]; then
    usage
    exit 1
fi

snakemake -j "$threads" -s tools/Snakefile --config title=$title --config directory=$directory
