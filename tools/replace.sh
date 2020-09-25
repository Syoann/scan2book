#! /usr/bin/env bash

#
#   Remplacements systématiques
#


infile="$1"

sed -e 's/|//g' \
    -e 's/^[^A-Zaz ]\+— /— /g' \
    -e 's/\s\+$//g' \
    -e 's/\.\.\.\?/…/g' \
    -e 's/^\s*__ \?/— /g' \
    -e "s/’/'/g" \
    -e "s/''/'/g" \
    -e 's/>*»>*/»/g; s/>>/»/g' \
    -e "s/1l/il/g; s/Jl/Il/g; s/I]/Il/g; s/oe/œ/g; s/1'/l'/g" \
    -e '/^[[:space:]]*$/d' \
    "$infile" | \
tr '\n' '\r' | sed 's/\([a-zéè]\)\\r\([a-zéèê]\)/\1 \2/g' | tr '\r' '\n' | \
sed 's/\.\+…\.*/…/g; s/\.*…\.\+/…/g' | \
sed 's/\([\.\!\?…]\)[^a-zA-Z\.\?\!…»:]\+$/\1/g'
