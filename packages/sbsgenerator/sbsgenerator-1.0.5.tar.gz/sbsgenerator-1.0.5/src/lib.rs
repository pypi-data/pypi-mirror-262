//! This module provides functionality for parsing VCF files and generating SBS data.
//!
//! The main function in this module is `parse_vcf_files`, which takes a list of VCF files,
//! a reference genome, and a context size as input. It reads the VCF files, collects the data,
//! reshapes it into a 2D array, and returns it as a numpy array.
//!
//! The module also provides helper functions for reading and processing the VCF files and
//! the associated byte files.
use numpy::PyArray;
use pyo3::prelude::*;
use pyo3::types::PyList;
use pyo3::Python;
use std::collections::HashMap;
use std::fs::File;
use std::io::{BufRead, BufReader, Read, Seek, SeekFrom, Write};

/// Parses VCF files and generates a NumPy array containing the parsed data.
///
/// # Arguments
///
/// * `py` - A Python interpreter session.
/// * `vcf_files` - A list of paths to VCF files.
/// * `ref_genome_path` - A string indicating the reference genome.
/// * `context` - An integer specifying the context size.
///
/// # Returns
///
/// A NumPy array containing the parsed data.
///
/// # Errors
///
/// Returns a Python error if there is an issue reading or parsing the VCF files.
#[pyfunction]
fn parse_vcf_files(
    py: Python,
    vcf_files: &PyList,
    ref_genome_path: &str,
    context: usize,
) -> PyResult<PyObject> {
    // All the collected data from the VCF files
    let all_data = read_and_collect_vcf_data(vcf_files, ref_genome_path, context)?;
    // Reshape the data into a 2D array
    let s = all_data.len();
    let t = if !all_data.is_empty() {
        all_data[0].len()
    } else {
        0
    };
    // Convert the data to Python objects
    let py_objects: Vec<PyObject> = all_data
        .into_iter()
        .flatten()
        .map(|x| x.to_object(py))
        .collect();
    // Convert it to a numpy array
    let np_array = PyArray::from_iter(py, py_objects.iter().map(|x| x.to_object(py)))
        .reshape([s, t])
        .unwrap();
    Ok(np_array.to_object(py))
}

/// Reads the contents of VCF files and collects the relevant data.
///
/// # Arguments
///
/// * `vcf_files` - A list of paths to VCF files.
/// * `ref_genome_path` - A string indicating the reference genome.
/// * `context` - An integer specifying the context size.
///
/// # Returns
///
/// A vector containing the collected data.
///
/// # Errors
///
/// Returns an I/O error if there is an issue reading the VCF files.
fn read_and_collect_vcf_data(
    vcf_files: &PyList,
    ref_genome_path: &str,
    context: usize,
) -> Result<Vec<Vec<String>>, PyErr> {
    let mut all_data = Vec::new();
    // Read and collect the data from each VCF file
    for vcf_file in vcf_files {
        let vcf_file_path: String = vcf_file.extract()?;
        let data = read_vcf_file_contents(&vcf_file_path)?;
        all_data.extend(data);
    }
    let genome_chromosome_indices = process_vcf_data(&all_data);
    update_all_data_based_on_indices(
        &mut all_data,
        &genome_chromosome_indices,
        ref_genome_path,
        context,
    )?;
    Ok(all_data)
}

/// Updates the collected data based on chromosome indices to include contextual information.
///
/// # Arguments
/// * `all_data` - Mutable reference to all collected data to be updated.
/// * `genome_chromosome_indices` - Mapping from genome and chromosome to indices in `all_data`.
/// * `ref_genome_path` - Path to the reference genome directory.
/// * `context` - Number of base pairs to include around the mutation for context.
///
/// # Returns
/// Ok if the update is successful, Err otherwise.
fn update_all_data_based_on_indices(
    all_data: &mut Vec<Vec<String>>,
    genome_chromosome_indices: &HashMap<String, HashMap<String, Vec<usize>>>,
    ref_genome_path: &str,
    context: usize,
) -> Result<(), PyErr> {
    let grand_total_indices: usize = genome_chromosome_indices
        .values()
        .map(|chromosomes_indices| {
            chromosomes_indices
                .values()
                .map(|indices| indices.len())
                .sum::<usize>()
        })
        .sum();
    let mut processed_indices_count = 0;
    let n = 1000; // Update frequency

    for (ref_genome, chromosomes_indices) in genome_chromosome_indices {
        for (chromosome, indices) in chromosomes_indices {
            for &index in indices {
                processed_indices_count += 1;
                update_progress(processed_indices_count, grand_total_indices, n);
                process_mutation_row(
                    index,
                    all_data,
                    ref_genome,
                    chromosome,
                    ref_genome_path,
                    context,
                )?;
            }
        }
    }
    println!();
    Ok(())
}

/// Processes a specific index in the all_data vector based on the chromosome indices.
///
/// # Arguments
/// * `index` - The index in `all_data` to be processed.
/// * `all_data` - The collected data to be updated.
/// * `ref_genome` - The reference genome identifier.
/// * `chromosome` - The chromosome identifier.
/// * `ref_genome_path` - Path to the reference genome directory.
/// * `context` - Number of base pairs to include around the mutation for context.
///
/// # Returns
/// Ok if the mutation data at the specified index is successfully processed, Err otherwise.
fn process_mutation_row(
    index: usize,
    all_data: &mut Vec<Vec<String>>,
    ref_genome: &str,
    chromosome: &str,
    ref_genome_path: &str,
    context: usize,
) -> Result<(), PyErr> {
    if let Some(row) = all_data.get(index) {
        let total_path = format!("{}/{}/{}.txt", ref_genome_path, ref_genome, chromosome);
        let translate_complement = row[4].parse::<bool>().unwrap();
        let position = row[1].parse::<usize>().unwrap();
        let (left, right) =
            read_bytes_file_contents(&total_path, position, &context, translate_complement)?;
        let translated_reference = row[5].clone();
        let translated_alternate = row[6].clone();
        let new_mutation_type = format!(
            "{}[{}>{}]{}",
            left, translated_reference, translated_alternate, right
        );
        all_data[index] = vec![row[0].clone(), new_mutation_type]
            .iter()
            .map(|s| s.into())
            .collect();
    }
    Ok(())
}

/// Updates the progress of data processing to the console.
///
/// # Arguments
/// * `processed` - The number of items processed so far.
/// * `total` - The total number of items to process.
/// * `n` - The frequency of progress updates (e.g., update every `n` items).
///
/// Displays the current progress as a percentage of the total work done.
fn update_progress(processed: usize, total: usize, n: usize) {
    let current_percentage = (processed as f64 / total as f64 * 100.0).round() as usize;
    if processed % n == 0 || processed == total {
        print!(
            "\rProcessed: {}% ({}/{})",
            current_percentage, processed, total
        );
        std::io::stdout().flush().unwrap();
    }
}

/// Processes the collected VCF data to map genome and chromosomes to indices in the data vector.
///
/// # Arguments
/// * `all_data` - The collected data from VCF files.
///
/// # Returns
/// A mapping from reference genomes and chromosomes to indices in `all_data`.
fn process_vcf_data(all_data: &Vec<Vec<String>>) -> HashMap<String, HashMap<String, Vec<usize>>> {
    let mut genome_chromosome_indices: HashMap<String, HashMap<String, Vec<usize>>> =
        HashMap::new();
    let ref_genome_index = 2;
    let chromosome_index = 3;

    for (row_index, row) in all_data.iter().enumerate() {
        if let (Some(ref_genome), Some(chromosome)) =
            (row.get(ref_genome_index), row.get(chromosome_index))
        {
            genome_chromosome_indices
                .entry(ref_genome.clone())
                .or_default()
                .entry(chromosome.clone())
                .or_default()
                .push(row_index);
        }
    }

    genome_chromosome_indices
}

/// Reads the contents of a specified VCF file and collects relevant mutation data.
///
/// # Arguments
/// * `vcf_file` - The path to the VCF file to be read.
///
/// # Returns
/// A vector of vectors, where each inner vector contains strings representing collected mutation data.
///
/// # Errors
/// Returns an I/O error if the file cannot be read.
fn read_vcf_file_contents(vcf_file: &str) -> Result<Vec<Vec<String>>, std::io::Error> {
    let nucleotides = vec!["A", "C", "G", "T"];
    let translate_purine_to_pyrimidine: HashMap<char, char> =
        [('A', 'T'), ('G', 'C')].iter().cloned().collect();
    let translate_nucleotide: HashMap<char, char> =
        [('A', 'T'), ('C', 'G'), ('G', 'C'), ('T', 'A')]
            .iter()
            .cloned()
            .collect();
    let mut data = Vec::new();
    let file = File::open(vcf_file)
        .map_err(|_| pyo3::exceptions::PyIOError::new_err("Failed to open the VCF file"))?;
    for line in BufReader::new(file).lines() {
        let line = line.map_err(|_| {
            pyo3::exceptions::PyIOError::new_err("Error reading line from the VCF file")
        })?;
        let fields: Vec<&str> = line.split('\t').collect();

        if fields.len() >= 10 {
            let reference_genome = fields[3];
            let mutation_type = fields[4];
            let chromosome = fields[5];
            let reference_allele = fields[8];
            let alternate_allele = fields[9];

            let translated_alternate: String = if (reference_allele == "A"
                || reference_allele == "G")
                && nucleotides.contains(&alternate_allele)
            {
                alternate_allele
                    .chars()
                    .map(|c| *translate_nucleotide.get(&c).unwrap_or(&c))
                    .collect()
            } else {
                alternate_allele.to_string()
            };
            let translated_reference: String = reference_allele
                .chars()
                .map(|c| *translate_purine_to_pyrimidine.get(&c).unwrap_or(&c))
                .collect();
            let translate_complement = !(translated_alternate == alternate_allele);
            if (reference_genome == "GRCh37" || reference_genome == "GRCh38")
                && (mutation_type == "SNP" || mutation_type == "SNV")
                && nucleotides.contains(&alternate_allele)
                && (translated_reference != translated_alternate)
            {
                let position = fields[6].parse::<usize>().unwrap() - 1;
                let sample = format!("{}::{}", fields[0], fields[1]);
                data.push(vec![
                    sample,
                    position.to_string(),
                    reference_genome.to_string(),
                    chromosome.to_string(),
                    translate_complement.to_string(),
                    translated_reference,
                    translated_alternate,
                ]);
            }
        }
    }
    Ok(data)
}

/// Reads a portion of a binary file and translates the bytes into characters based on a mapping.
///
/// # Arguments
///
/// * `file_path` - Path to the binary file.
/// * `start` - The starting position to read from.
/// * `end` - The ending position to read to.
///
/// # Returns
///
/// A tuple containing left and right strings.
///
/// # Errors
///
/// Returns an I/O error if there is an issue reading the file
fn read_bytes_file_contents(
    file_path: &str,
    position: usize,
    context: &usize,
    translate_complement: bool,
) -> Result<(String, String), std::io::Error> {
    let start = position.saturating_sub(*context / 2);
    let end = position + *context / 2 + 1;
    let mut file = File::open(file_path)
        .map_err(|_| pyo3::exceptions::PyIOError::new_err("Failed to open the bytes file"))?;
    file.seek(SeekFrom::Start(start as u64)).map_err(|_| {
        pyo3::exceptions::PyIOError::new_err("Error seeking to the specified position")
    })?;
    let bytes_to_read = end - start;
    let mut buffer = vec![0; bytes_to_read];
    file.read_exact(&mut buffer)
        .map_err(|_| pyo3::exceptions::PyIOError::new_err("Error reading data from the file"))?;

    let translation_mapping: HashMap<u8, char> = [
        (0, 'A'),
        (1, 'C'),
        (2, 'G'),
        (3, 'T'),
        (4, 'A'),
        (5, 'C'),
        (6, 'G'),
        (7, 'T'),
        (8, 'A'),
        (9, 'C'),
        (10, 'G'),
        (11, 'T'),
        (12, 'A'),
        (13, 'C'),
        (14, 'G'),
        (15, 'T'),
        (16, 'N'),
        (17, 'N'),
        (18, 'N'),
        (19, 'N'),
    ]
    .iter()
    .cloned()
    .collect();
    let middle_index = bytes_to_read / 2;
    let result: String = buffer
        .iter()
        .map(|&byte| translation_mapping.get(&byte).unwrap_or(&' ').to_owned())
        .collect();
    let final_result = if translate_complement {
        reverse_complement(&result)
    } else {
        result
    };
    let result_chars: Vec<char> = final_result.chars().collect();
    let left = result_chars[..middle_index].iter().collect::<String>();
    let right = result_chars[middle_index + 1..].iter().collect::<String>();

    Ok((left, right))
}

/// Generates the reverse complement of a nucleotide sequence.
///
/// # Arguments
/// * `nucleotide_str` - The nucleotide sequence for which to generate the reverse complement.
///
/// # Returns
/// A string representing the reverse complement of the input sequence.
fn reverse_complement(nucleotide_str: &str) -> String {
    let reversed = reverse_string(nucleotide_str);
    let complemented: String = reversed.chars().map(complement).collect();
    complemented
}

/// Reverses a string.
///
/// # Arguments
/// * `s` - The string to be reversed.
///
/// # Returns
/// The reversed string.
fn reverse_string(s: &str) -> String {
    s.chars().rev().collect()
}

/// Returns the complement of a given nucleotide.
///
/// # Arguments
/// * `nucleotide` - The nucleotide (A, T, C, or G) for which to find the complement.
///
/// # Returns
/// The complement nucleotide (A<>T, C<>G).
fn complement(nucleotide: char) -> char {
    match nucleotide {
        'A' => 'T',
        'T' => 'A',
        'G' => 'C',
        'C' => 'G',
        _ => nucleotide, // if not A, T, G, or C, return the same character
    }
}

/// A Python module implemented in Rust.
///
/// Exposes the `parse_vcf_files` function to Python.
#[pymodule]
fn sbsgenerator(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add("__version__", env!("CARGO_PKG_VERSION"))?;
    m.add_function(wrap_pyfunction!(parse_vcf_files, m)?)?;
    Ok(())
}
