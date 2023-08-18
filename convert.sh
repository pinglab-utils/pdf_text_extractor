#!/bin/bash

# src directory contains all pdfs for research papers
src_dir='data/'
# sink directory will contain all images from the research pdfs
sink_dir='images/'
# results directory to store the converted texts
res_dir='results/'

# As a check, create the proper directories if needed
if [ ! -d "$sink_dir" ]; then
    mkdir -p "$sink_dir"
fi

if [ ! -d "$res_dir" ]; then
    mkdir -p "$res_dir"
fi

# Now, go and actually convert these files into pngs
for file in "$src_dir"/*.pdf; do
    # Extract the filename without the extension
    filename=$(basename -- "$file")
    filename="${filename%.*}"
    # Try and convert the pdf into a png
    convert -density 300 "$file" -quality 100 "$sink_dir/$filename.png"
    # Determine conversion status
    if [ $? -eq 0 ]; then
        echo "Converted $file to PNG successfully."
    else
        echo "Failed to convert $file to PNG."
    fi
done