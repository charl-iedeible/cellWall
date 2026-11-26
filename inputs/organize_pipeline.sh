# pseudocode given to chatgpt:

# loop through each folder name in directory in variable 'species_abbr'
# use species_abbr to extract each case of the following and move into appropriate folder directory:
   # ~/Downloads/species_abbr_cdna.fa.bgz
   # ~/Downloads/species_abbr_pep.fa.bgz
   # ~/Downloads/species_abbr_genes.gff3.gz
# unpack .bgz and .gz with gunzip and gzip, respectively
# move compressed folders into junk directory



# result:

#!/usr/bin/env bash
#
# Organize downloaded genome annotation files into their species directories.
#
# Expected source files in ~/Downloads:
#   SPECIES_cdna.fa.bgz
#   SPECIES_pep.fa.bgz
#   SPECIES_genes.gff3.gz
#
# Decompressed files are written into ./SPECIES/.
# Original compressed files are moved into ./junk/.

set -euo pipefail

DOWNLOAD_DIR="${HOME}/Downloads"
JUNK_DIR="./junk"

mkdir -p "$JUNK_DIR"

# Map each compressed suffix to its decompressed output suffix.
file_types=(
    "cdna.fa.bgz:cdna.fa"
    "pep.fa.bgz:pep.fa"
    "genes.gff3.gz:genes.gff3"
)

missing_files=0
processed_files=0

# Iterate over directories in the current working directory.
for species_dir in */; do
    [[ -d "$species_dir" ]] || continue

    species_abbr="${species_dir%/}"

    # Do not process the archive directory.
    [[ "$species_abbr" == "junk" ]] && continue

    echo "Processing ${species_abbr}..."

    for file_type in "${file_types[@]}"; do
        compressed_suffix="${file_type%%:*}"
        output_suffix="${file_type#*:}"

        source_file="${DOWNLOAD_DIR}/${species_abbr}_${compressed_suffix}"
        output_file="${species_dir}${species_abbr}_${output_suffix}"
        temporary_file="${output_file}.tmp"

        if [[ ! -f "$source_file" ]]; then
            echo "  WARNING: Missing ${source_file}; skipping." >&2
            missing_files=$((missing_files + 1))
            continue
        fi

        echo "  Decompressing $(basename "$source_file")..."

        # gunzip -c supports both .gz and .bgz files and leaves the
        # compressed source untouched until decompression succeeds.
        if gunzip -c "$source_file" > "$temporary_file"; then
            mv "$temporary_file" "$output_file"
            mv "$source_file" "$JUNK_DIR/"
            processed_files=$((processed_files + 1))
        else
            rm -f "$temporary_file"
            echo "  ERROR: Could not decompress ${source_file}." >&2
            exit 1
        fi
    done
done

echo
echo "Pipeline organization complete."
echo "Files decompressed and organized: ${processed_files}"
echo "Expected files missing: ${missing_files}"

if (( missing_files > 0 )); then
    exit 1
fi
