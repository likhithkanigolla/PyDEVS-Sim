#!/bin/bash

# Output directory for reports
OUTPUT_DIR="code_metrics_report"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
REPORT_DIR="${OUTPUT_DIR}/${TIMESTAMP}"
FINAL_REPORT="${REPORT_DIR}/complete_analysis.txt"
# Set the directory where Python files are located (or "." for current directory)
SOURCE_DIR="."

# Function to check if radon is installed
check_radon() {
    if ! command -v radon &> /dev/null; then
        echo "Radon is not installed. Installing now..."
        pip install radon
    fi
}

# Function to create directory structure

if [ ! -d "$REPORT_DIR" ]; then
  mkdir -p "$REPORT_DIR" || { echo "Failed to create report directory"; exit 1; }
fi


create_directories() {
    mkdir -p "${REPORT_DIR}"
    echo "Created report directory: ${REPORT_DIR}"
}

# Function to initialize CSV files with headers
initialize_csv_files() {
    # Complexity metrics CSV
    echo "File,Function,Complexity,Complexity_Score" > "${COMPLEXITY_CSV}"
    
    # Halstead metrics CSV
    echo "File,h1,h2,N1,N2,vocabulary,length,calculated_length,volume,difficulty,effort,time,bugs" > "${HALSTEAD_CSV}"
    
    # Raw metrics CSV
    echo "File,LOC,LLOC,SLOC,Comments,Single_comments,Multi,Blank,Comment_Ratio,Comment_SLOC_Ratio" > "${RAW_METRICS_CSV}"
    
    # Maintainability metrics CSV
    echo "File,Maintainability_Index" > "${MAINTAINABILITY_CSV}"
}

# Function to parse and store cyclomatic complexity
parse_complexity() {
    local file=$1
    local tmp_file="${REPORT_DIR}/tmp_cc.txt"
    
    echo "Running Radon CC for ${file}..."  # Debugging line
    radon cc "${file}" -a -s > "${tmp_file}"
    
    # Parse the complexity output and add to CSV
    while IFS= read -r line; do
        if [[ $line =~ ^[[:space:]]*F[[:space:]]([0-9]+):([0-9]+)[[:space:]]([^[:space:]]+)[[:space:]]-[[:space:]]([A-F])[[:space:]]\(([0-9]+)\) ]]; then
            local func="${BASH_REMATCH[3]}"
            local grade="${BASH_REMATCH[4]}"
            local score="${BASH_REMATCH[5]}"
            echo "${file},${func},${grade},${score}" >> "${COMPLEXITY_CSV}"
        fi
    done < "${tmp_file}"
    
    rm "${tmp_file}"
}

# Function to parse and store Halstead metrics
parse_halstead() {
    local file=$1
    local tmp_file="${REPORT_DIR}/tmp_hal.txt"
    
    echo "Running Radon Halstead for ${file}..."  # Debugging line
    radon hal "${file}" > "${tmp_file}"
    
    # Initialize variables
    local metrics=""
    
    # Read the metrics
    while IFS= read -r line; do
        if [[ $line =~ h1:[[:space:]]*([0-9.]+) ]]; then
            metrics="${BASH_REMATCH[1]}"
        elif [[ $line =~ h2:[[:space:]]*([0-9.]+) ]]; then
            metrics="${metrics},${BASH_REMATCH[1]}"
        elif [[ $line =~ N1:[[:space:]]*([0-9.]+) ]]; then
            metrics="${metrics},${BASH_REMATCH[1]}"
        elif [[ $line =~ N2:[[:space:]]*([0-9.]+) ]]; then
            metrics="${metrics},${BASH_REMATCH[1]}"
        elif [[ $line =~ vocabulary:[[:space:]]*([0-9.]+) ]]; then
            metrics="${metrics},${BASH_REMATCH[1]}"
        elif [[ $line =~ length:[[:space:]]*([0-9.]+) ]]; then
            metrics="${metrics},${BASH_REMATCH[1]}"
        elif [[ $line =~ calculated_length:[[:space:]]*([0-9.]+) ]]; then
            metrics="${metrics},${BASH_REMATCH[1]}"
        elif [[ $line =~ volume:[[:space:]]*([0-9.]+) ]]; then
            metrics="${metrics},${BASH_REMATCH[1]}"
        elif [[ $line =~ difficulty:[[:space:]]*([0-9.]+) ]]; then
            metrics="${metrics},${BASH_REMATCH[1]}"
        elif [[ $line =~ effort:[[:space:]]*([0-9.]+) ]]; then
            metrics="${metrics},${BASH_REMATCH[1]}"
        elif [[ $line =~ time:[[:space:]]*([0-9.]+) ]]; then
            metrics="${metrics},${BASH_REMATCH[1]}"
        elif [[ $line =~ bugs:[[:space:]]*([0-9.]+) ]]; then
            metrics="${metrics},${BASH_REMATCH[1]}"
        fi
    done < "${tmp_file}"
    
    if [ ! -z "$metrics" ]; then
        echo "${file},${metrics}" >> "${HALSTEAD_CSV}"
    fi
    
    rm "${tmp_file}"
}

# Function to parse and store raw metrics
parse_raw_metrics() {
    local file=$1
    local tmp_file="${REPORT_DIR}/tmp_raw.txt"
    
    echo "Running Radon Raw for ${file}..."  # Debugging line
    radon raw "${file}" > "${tmp_file}"
    
    # Initialize variables
    local loc=""
    local lloc=""
    local sloc=""
    local comments=""
    local single=""
    local multi=""
    local blank=""
    local comment_ratio=""
    local comment_sloc_ratio=""
    
    while IFS= read -r line; do
        if [[ $line =~ LOC:[[:space:]]*([0-9]+) ]]; then
            loc="${BASH_REMATCH[1]}"
        elif [[ $line =~ LLOC:[[:space:]]*([0-9]+) ]]; then
            lloc="${BASH_REMATCH[1]}"
        elif [[ $line =~ SLOC:[[:space:]]*([0-9]+) ]]; then
            sloc="${BASH_REMATCH[1]}"
        elif [[ $line =~ Comments:[[:space:]]*([0-9]+) ]]; then
            comments="${BASH_REMATCH[1]}"
        elif [[ $line =~ Single[[:space:]]comments:[[:space:]]*([0-9]+) ]]; then
            single="${BASH_REMATCH[1]}"
        elif [[ $line =~ Multi:[[:space:]]*([0-9]+) ]]; then
            multi="${BASH_REMATCH[1]}"
        elif [[ $line =~ Blank:[[:space:]]*([0-9]+) ]]; then
            blank="${BASH_REMATCH[1]}"
        elif [[ $line =~ \(C[[:space:]]+%[[:space:]]+L\):[[:space:]]*([0-9]+)% ]]; then
            comment_ratio="${BASH_REMATCH[1]}"
        elif [[ $line =~ \(C[[:space:]]+%[[:space:]]+S\):[[:space:]]*([0-9]+)% ]]; then
            comment_sloc_ratio="${BASH_REMATCH[1]}"
        fi
    done < "${tmp_file}"
    
    if [ ! -z "$loc" ]; then
        echo "${file},${loc},${lloc},${sloc},${comments},${single},${multi},${blank},${comment_ratio},${comment_sloc_ratio}" >> "${RAW_METRICS_CSV}"
    fi
    
    rm "${tmp_file}"
}

# Function to parse and store maintainability index
parse_maintainability() {
    local file=$1
    local mi=$(radon mi "${file}" | grep -oE "${file} - [A-F]")
    
    if [ ! -z "$mi" ]; then
        echo "${file},${mi}" >> "${MAINTAINABILITY_CSV}"
    fi
}

# Function to write section header
write_header() {
    echo -e "\nAnalysis for: $1" >> "${FINAL_REPORT}"
    echo "================================================" >> "${FINAL_REPORT}"
}

# Function to analyze a specific Python file
analyze_file() {
    local file=$1
    write_header "${file}"
    
    # Cyclomatic Complexity
    echo -e "\nCyclomatic Complexity Analysis:" >> "${FINAL_REPORT}"
    parse_complexity "${file}"
    
    # Halstead Metrics
    echo -e "\nHalstead Metrics Analysis:" >> "${FINAL_REPORT}"
    parse_halstead "${file}"
    
    # Raw Metrics
    echo -e "\nRaw Metrics Analysis:" >> "${FINAL_REPORT}"
    parse_raw_metrics "${file}"
    
    # Maintainability Index
    echo -e "\nMaintainability Index Analysis:" >> "${FINAL_REPORT}"
    parse_maintainability "${file}"
}

# Start the analysis process
check_radon
create_directories
initialize_csv_files

echo "Starting analysis..."

# Ensure Python files exist in the source directory (recursive search)
find "${SOURCE_DIR}" -name "*.py" | while read -r file; do
    analyze_file "${file}"
done

echo "Analysis complete. Reports saved to ${REPORT_DIR}"
