"""
File: getgenes.py
Author: Jake Leyhr
GitHub: https://github.com/jakeleyhr/EZgenesynteny/
Date: March 2024
Description: Get list of genes upstream and downstream of gene of interest
"""
# Import dependencies
import re
import os
import sys
import time
import argparse
import configparser
import csv
from Bio import Entrez, SeqIO
from shutil import get_terminal_size
from collections import OrderedDict
from urllib.error import HTTPError
from .genevis import plot_genes
from .version_check import check_for_updates


# Function #1 - get gene record
def search_gene_info(species, gene_name):
    # Set email address if not already done
    config = configparser.ConfigParser()
    current_dir = os.path.dirname(__file__) # Get the directory path of the current script
    config_file_path = os.path.join(current_dir, 'config.ini') # Specify the path to config.ini relative to the script's directory
    if os.path.exists(config_file_path): # Check if the config file exists
        config.read(config_file_path)
    else:
        print("Config file not found:", config_file_path)

    Entrez.email = config.get('User', 'email')

    if not Entrez.email:
        Entrez.email = input(f"NCBI's Entrez system requests an email address to be associated with queries. \nPlease enter your email address: ")
        config.set('User', 'email', Entrez.email)
        # Write the config.ini file to the same directory as the script
        with open(config_file_path, 'w') as configfile:
            config.write(configfile)
        print(f"Email address set: '{Entrez.email}'. This will be used for all future queries. \nYou can change the saved email address using 'gbemail -update'")

    # Print run header
    terminalwidth = get_terminal_size()[0]
    nameswidth = len(f" ezgenesynteny: {species} {gene_name} ")
    leftindent = ((terminalwidth-nameswidth)//2)
    print("▒"*terminalwidth+
          "▒"*leftindent+ 
          f" ezgenesynteny: {species} {gene_name} "+ 
          "▒"*(terminalwidth-leftindent-nameswidth)+
          "▒"*terminalwidth)
    if '.' in species:
        species = species.split(". ", 1)[1]
    # Build the query - strict check on species name and gene name (also searches gene name synonyms)
    query = f"{species}[ORGN] AND {gene_name}[Gene Name] OR {gene_name}[Accession]"

    # Search Entrez Gene
    handle = Entrez.esearch(db="gene", term=query, retmode="xml")
    record = Entrez.read(handle)
    # print(f' Entrez record: {record}')

    # Fetch gene information from each record
    max_retries = 5
    retry_delay = 1  # You can adjust this delay as needed

    for retry in range(max_retries):
        try:
            if "IdList" in record and record["IdList"]:
                gene_id = record["IdList"][0]
                handle = Entrez.efetch(db="gene", id=gene_id, retmode="xml")
                gene_record = Entrez.read(handle)
                return gene_record
        except HTTPError as e:
            if retry < max_retries - 1:  # Retry if it's not the last attempt
                print(f"Attempt #{retry + 1} failed to obtain gene record due to HTTP error. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                raise  # If it's the last attempt, raise the exception

    return None


# Function #2 - process the gene record and extract relevant information
def process_gene_info(gene_info, record_id, start_adjust, end_adjust, species, gene_name, gene_oriented_adjustment):
    # Extract the relevant information
    if gene_info:
        print("Gene info:")
        gene_ref_name = gene_info[0]["Entrezgene_gene"]["Gene-ref"]["Gene-ref_locus"]
        print(f"Name: {gene_ref_name}")
        try:
            gene_ref_desc = gene_info[0]["Entrezgene_gene"]["Gene-ref"]["Gene-ref_desc"]
            print(f"Description: {gene_ref_desc}")
        except KeyError:
            print("Description: None available")
        try:
            synonyms = gene_info[0]["Entrezgene_gene"]["Gene-ref"]["Gene-ref_syn"]
            print(f"Synonyms: {synonyms}")
        except KeyError:
            print("Synonyms: None available")
        try:
            locus = gene_info[0]["Entrezgene_gene"]["Gene-ref"]["Gene-ref_maploc"]
            print(f"Locus: {locus}")
        except KeyError:
            print("Locus: None available")
        try:
            strandsign = gene_info[0]["Entrezgene_locus"][0]["Gene-commentary_seqs"][0]["Seq-loc_int"]["Seq-interval"]["Seq-interval_strand"]["Na-strand"].attributes['value']
            if strandsign == 'plus':
                strand = 'forward'
            elif strandsign == 'minus':
                strand = 'reverse'
            print(f"Strand: {strand}")
        except KeyError:
            print("Strand: None available")
            return
        
        #print(gene_info)
        print(f"\nUsing record {record_id}:")
        try: 
            org = gene_info[0]["Entrezgene_source"]["BioSource"]["BioSource_org"]["Org-ref"]["Org-ref_taxname"]
            common = gene_info[0]["Entrezgene_source"]["BioSource"]["BioSource_org"]["Org-ref"]["Org-ref_common"]
            print(f"Organism: {common} ({org})")
        except:
            pass
        try:
            assembly = gene_info[0]["Entrezgene_locus"][record_id]["Gene-commentary_label"]
            print(f"Assembly: {assembly}")
        except:
            pass
        try:
            accession_number = gene_info[0]["Entrezgene_locus"][record_id]["Gene-commentary_accession"]
            print(f"Accession: {accession_number}")
            start = (int(
                gene_info[0]["Entrezgene_locus"][record_id]["Gene-commentary_seqs"][0]
                ["Seq-loc_int"]["Seq-interval"]["Seq-interval_from"]
            ) + 1)
            end = (int(
                    gene_info[0]["Entrezgene_locus"][record_id]["Gene-commentary_seqs"][0]
                    ["Seq-loc_int"]["Seq-interval"]["Seq-interval_to"]
            ) + 1)  # "Gene-commentary_seqs" gives merged gene sequence, "Gene-commentary-products" gives transcripts
            length = end - start + 1

            print(f"Location: {start}:{end}")
            print(f"Length: {length}bp")
        except IndexError:
            print(f"ERROR: Record_ID #{record_id} not found. Try a different value")
            return # Force exit the function


        # For debugging - explore the file format:
        # Assuming gene_info is a dictionary, explore the format
        # record_directories(gene_info)
        # Assuming gene_info is a list with a single dictionary, explore the format
        # search_key_value(gene_info[0], 'Seq-interval_from')
        # Print the structure of gene_info[0]
        # explore_structure(gene_info[0]['Entrezgene_locus'])
        # explore_structure(gene_info[0])
    else:
        #species = species.split(". ", 1)[1]
        print(f"ERROR: No gene information found for {gene_name} in {species}. Check the names are correct.")
        return # Force exit the function
        #sys.exit()

    if gene_oriented_adjustment and strand == 'reverse':
        requested_start_position = start - end_adjust
        requested_end_position = end + start_adjust
    else:
        # Calculate region start and end based on the gene start and end coordinates +/- the user-provided adjustment values
        requested_start_position = start - start_adjust
        requested_end_position = end + end_adjust


    return accession_number, requested_start_position, requested_end_position, strand, gene_ref_name


has_run_before = False
# Function #3 - get list of genes and features in specified region
def get_genes_in_region(accession_number, requested_start_position, requested_end_position, X=False):
    global has_run_before
    quickhandle = Entrez.efetch(db="nuccore", id=accession_number, rettype="gb", retmode="text")
    quickrecord = SeqIO.read(quickhandle, "genbank")
    for feature in quickrecord.features:
        if feature.type == "source":
            source_str = str(feature.location)
            match = re.search(r"\[([<>]?\d+):([<>]?\d+[<>]?)\]\([+-]\)", source_str) # Look for location coordinates in particular format. '[<>]?' allows for < or >
            if match:
                chr_source_start = int(match.group(1).lstrip('<').lstrip('>')) + 1 # +1 to start only because of 0-based indexing in Entrez record (not present on NCBI website)
                chr_source_end = int(match.group(2).lstrip('<').lstrip('>'))
            break
    if requested_start_position > chr_source_end:
        print(f"\nERROR: {requested_start_position} is not a valid start coordinate, {accession_number} is only {chr_source_end}bp long")
        sys.exit()
    if requested_start_position < chr_source_start:
        print(f"\nWARNING: {requested_start_position} is not a valid start coordinate, changing to {chr_source_start}")
        requested_start_position = chr_source_start
    if requested_end_position > chr_source_end:
        print(f"\nWARNING: Input end coordinate {requested_end_position} is out of bounds, trimming to closest value: {chr_source_end}")
        requested_end_position = chr_source_end

    near_accession_left_lim = False
    near_accession_right_lim = False
    # By default, look upstream and downstream 1Mb of the specified region for genes and their features that could overlap with the specified region
    overhang = 0
    startdiff = overhang
    enddiff = overhang
    seqstart = requested_start_position - startdiff
    seqstop = requested_end_position + enddiff
    # Change this distance to fit smaller sequence records if needed, or if querying near the start or end of a sequence record
    if seqstart < chr_source_start:
        startdiff = startdiff - (chr_source_start - seqstart)
        seqstart = chr_source_start
        #print(f"new seq start: {seqstart}")
        #print(f"new startdiff: {startdiff}")
        near_accession_left_lim = True
    if seqstop > chr_source_end:
        enddiff = enddiff -(seqstop - chr_source_end)
        seqstop = chr_source_end
        #print(f"new seq stop: {seqstop}")
        #print(f"new enddiff: {enddiff}")
        near_accession_right_lim = True

    handle = Entrez.efetch(db="nuccore", id=accession_number, rettype="gbwithparts", retmode="text", seq_start=seqstart, seq_stop=seqstop)
    if has_run_before == False:
        print(f"\nParsing upstream genomic record ({seqstart}:{seqstop})...")
    else:
        print(f"\nParsing downstream genomic record ({seqstart}:{seqstop})...")
    starttime= time.time()
    record = SeqIO.read(handle, "genbank")
    handle.close()
    endtime= time.time()
    print(f"Record file parsed in {round(endtime - starttime, 1)} seconds")
    # Check if start and end coordinates are within range of sequence record
    for feature in record.features:
        if feature.type == "source":
            source_str = str(feature.location)
            match = re.search(r"\[([<>]?\d+):([<>]?\d+[<>]?)\]\([+-]\)", source_str) # Look for location coordinates in particular format. '[<>]?' allows for < or >
            if match:
                source_start = int(match.group(1).lstrip('<').lstrip('>')) + 1 # +1 to start only because of 0-based indexing in Entrez record (not present on NCBI website)
                source_end = int(match.group(2).lstrip('<').lstrip('>'))
            break
    #print(f"source start: {source_start}")
    #print(f"source end: {source_end}")
    #print(f"req start: {requested_start_position}")
    #print(f"req end: {requested_end_position}")
    accessions = record.annotations['accessions']
    # Find the element containing the ".." separator
    separator_element = next((elem for elem in accessions if ".." in elem), None)

    if separator_element:
        # Extract the numbers on either side of ".."
        abs_start_coord, abs_end_coord = map(int, separator_element.split('..'))
        abs_start_coord = abs_start_coord + overhang
        abs_end_coord = abs_end_coord - overhang
        #print("Start number:", abs_start_coord)
        #print("End number:  ", abs_end_coord)
        start = source_start + overhang
        end = source_end - overhang
    if separator_element and near_accession_right_lim:
        _, abs_end_coord = map(int, separator_element.split('..'))
        abs_end_coord = abs_end_coord - enddiff
        #print("abs_end_coord:  ", abs_end_coord)
        end = source_end - enddiff
        #print("end:  ", end)
    if separator_element and near_accession_left_lim:
        abs_start_coord, _ = map(int, separator_element.split('..'))
        abs_start_coord = abs_start_coord + startdiff
        #print("abs_start_coord:  ", abs_start_coord)
        start = source_start + startdiff
        #print("start:  ", start)
    if not separator_element:
        #print("Separator '..' not found in the list.")
        #add code here to get sequence length etc
        abs_start_coord = requested_start_position
        abs_end_coord = requested_end_position
        #print(abs_start_coord)
        #print(abs_end_coord)
        start = abs_start_coord
        end = abs_end_coord

    # Create a set to store gene names
    gene_names = []
    # Iterate through the features to find gene names
    for feature in record.features:
        if feature.type == "gene":
            try:
                gene_name = feature.qualifiers.get("gene", [])[0]
                gene_names.append(gene_name)
            except:
                pass

    # Prepare to collect genes and features
    genes_in_region = {}

    # Parse GenBank features to identify genes that overlap with specified sequence region
    for gene_name in gene_names:
        for feature in record.features:
            if feature.type == "CDS" and feature.qualifiers.get("gene", [])[0] == gene_name:
                #print(feature)
                location_str = str(feature.location)
                match = re.search(r"\[([<>]?\d+):([<>]?\d+[<>]?)\]\(([+-])\)", location_str) # Look for location coordinates in particular format. '[<>]?' allows for < or >
                if match:
                    gene_start = int(match.group(1).lstrip('<').lstrip('>')) + 1 # +1 to start only because of 0-based indexing in Entrez record (not present on NCBI website)
                    gene_end = int(match.group(2).lstrip('<').lstrip('>'))
                    strand = match.group(3)  # Extract strand direction
                    if gene_end < start:
                        continue
                    elif (
                        start <= gene_start <= end # Gene start inside region?
                        or start <= gene_end <= end # Gene end inside region?
                        or gene_start <= start <= end <= gene_end # Gene middle inside region?
                    ):
                        #print(feature)
                        #print(f'gene start: {gene_start}, gene end: {gene_end}')
                        #print(f'region start: {start}, region end: {end}')
                        try:
                            gene_name = feature.qualifiers["gene"][0]
                        except KeyError:
                            gene_name = feature.qualifiers["locus_tag"][0]

                        # Append gene name and strand direction to the dictionary
                        genes_in_region[gene_name] = strand
                else:
                    print("Location coordinates in unexpected format")
                    return # Force exit the function
                    #sys.exit()
    
    print(f"Genes in region: {genes_in_region}")
    has_run_before = True
    return genes_in_region


# Function #3.5 - simplify and reorder gene feature coordinates
def reorder_location(location_str):
    # Split the location string into features
    features = location_str.split(",")

    # Split each feature into pair of numbers (start and end coordinates) and convert to integers
    pairs = [tuple(map(int, feature.split(":"))) for feature in features]

    # Sort the pairs based on the leftmost value (start coordinate)
    ordered_pairs = sorted(pairs, key=lambda x: x[0])

    # Format the ordered pairs back into the desired string format e.g. "100:200, 300:400"
    ordered_location_str = ",".join([f"{int(left)+1}:{right}" for left, right in ordered_pairs]) # +1 to left(start) to account for 0-based numbering from Entrez record
    return ordered_location_str


def get_upstream_downstream_genes(species, gene_name, upstream, downstream):
    # Search for gene information
    gene_info = search_gene_info(species, gene_name)
    if not gene_info:
        print(f"No information found for gene {gene_name} in species {species}")
        return [], []

    # Process gene information
    accession_number, start, end, strand, gene_ref_name = process_gene_info(gene_info, record_id=0, start_adjust=0, end_adjust=0, species=species, gene_name=gene_name, gene_oriented_adjustment=False)

    # Define upstream and downstream regions
    upstream_start = max(0, start - upstream)
    downstream_end = end + downstream

    # Get genes in the upstream and downstream regions
    if strand == 'reverse':
        upstream_genes = get_genes_in_region(accession_number, end+1, downstream_end, X=False)
        upstream_genes = OrderedDict(upstream_genes) # Create an OrderedDict from the original dictionary
        upstream_genes = OrderedDict(reversed(list(upstream_genes.items()))) # Reverse
        downstream_genes = get_genes_in_region(accession_number, upstream_start, start-1, X=False)
        downstream_genes = OrderedDict(downstream_genes) # Create an OrderedDict from the original dictionary
        downstream_genes = OrderedDict(reversed(list(downstream_genes.items()))) # Reverse
        reverse = True
        genestrand = '+'
    else:
        upstream_genes = get_genes_in_region(accession_number, upstream_start, start-1, X=False)
        downstream_genes = get_genes_in_region(accession_number, end+1, downstream_end, X=False)
        reverse = False
        genestrand = '+'

    return upstream_genes, downstream_genes, gene_ref_name, genestrand, reverse


def collectgenes(species, gene_name, upgenes, downgenes):
    upstream = 1000000*upgenes
    downstream = 1000000*downgenes
    upstream_genes, downstream_genes, gene_ref_name, genestrand, reverse = get_upstream_downstream_genes(species, gene_name, upstream, downstream)

    # Get the first 10 entries
    upstream_genes = list(upstream_genes.items())[-upgenes:]
    # Get the last 10 entries
    downstream_genes = list(downstream_genes.items())[:downgenes]

    if reverse:
        upstream_genes = [(gene, '+' if strand == '-' else '-') for gene, strand in upstream_genes]
        downstream_genes = [(gene, '+' if strand == '-' else '-') for gene, strand in downstream_genes]

    # If the number of upstream genes is lacking, shift genes to the right to align target genes
    if len(upstream_genes) < upgenes:
        add = upgenes - len(upstream_genes)
    else:
        add = 0

    genes = upstream_genes

    gene_ref = {}
    gene_ref[gene_ref_name] = genestrand
    genes.extend(list(gene_ref.items()))

    genes.extend(downstream_genes)

    print(f"\n\nTrimming to max. {upgenes} upstream genes and max. {downgenes} downstream genes with {gene_ref_name} on forward strand:")
    print(f"{genes}\n")

    species_genes = {species: {"genes": [], "strand_directions": [], "gene_positions": []}}
    for idx, (gene, strand) in enumerate(genes, start=1):
        species_genes[species]["genes"].append(gene)
        species_genes[species]["strand_directions"].append(strand)
        species_genes[species]["gene_positions"].append(idx+add)

    #print(species_genes)
    return species_genes

def makecsv(species_genes, csvfilename, genenum):
    # Open a CSV file in write mode
    with open(f'{csvfilename}.csv', mode='w', newline='') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)
        # Write header
        writer.writerow(['Species'] + [f'Gene{i+1}' for i in range(genenum)])

        # Iterate over each species
        for species, data in species_genes.items():
            genes = data['genes']
            directions = data['strand_directions']
            positions = data['gene_positions']

            # Initialize an empty row
            row = [''] * genenum

            # Fill in the cells based on gene positions
            for gene, direction, position in zip(genes, directions, positions):
                #print(position)
                row[position - 1] = f"{gene} {direction}"

            # Write species and row data
            writer.writerow([species] + row)


def get_genes(species, gene_name, upgenes, downgenes, outputfilename, csvfilename, input_file=None):
    if outputfilename:
        # Find the index of the last period
        last_period_index = outputfilename.rfind('.')

        if last_period_index != -1:  # Check if a period was found
            imageformat = outputfilename[last_period_index + 1:]
        else:
            imageformat = 'pdf'
            outputfilename = f"{outputfilename}.pdf"
            print("Note: using PDF format for plot by default\n")

        if imageformat:
            if imageformat not in ["pdf", "eps", "png", "jpeg", "jpg", "pgf", "ps", "raw", "rgba", "svg", "svgz", "tif", "tiff", "webp"]:
                print(f"ERROR: Format '{imageformat}' is not supported plot format (supported formats: eps, jpeg, jpg, pdf, pgf, png, ps, raw, rgba, svg, svgz, tif, tiff, webp)")
                sys.exit()

    failed_lines=[]
    if input_file:
        species_genes_dict = {}
        with open(input_file, 'r') as file:
            for i, line in enumerate(file):
                if not line.strip():
                    continue
                parts = line.strip().split(',')
                if len(parts) == 2:
                    species_name = parts[0].strip()
                    gene = parts[1].strip()
                    if species_name not in species_genes_dict:
                        species_genes_dict[f"{i+1}. {species_name}"] = []
                    species_genes_dict[f"{i+1}. {species_name}"].append(gene)
                else:
                    print(f"Invalid format on line {i}: {line}")
                    failed_lines.append(line)
        species_list = list(species_genes_dict.keys())
        genes_list = [species_genes_dict[species] for species in species_list]
    else:
        species_list = species
        genes_list = [[gene_name] for _ in range(len(species))]  # Duplicate gene_name for each species

    print(species_list)
    print(genes_list)
    species_genes = {}
    failed_species = []
    start_time = time.time()
    for species_name, genes in zip(species_list, genes_list):
        for gene in genes:
            try:
                #if species_name not in species_genes:
                species_genes[species_name] = collectgenes(species_name, gene, upgenes, downgenes)
                #print(species_genes)
            except Exception:
                failed_species.append(species_name)

    end_time = time.time()
    if len(species_list) > 1:
        print(f"All completed in {round(end_time - start_time, 1)} seconds\n")
    else:
        print(f"Completed in {round(end_time - start_time, 1)} seconds\n")

    species_genes = {k: v[k] for k, v in species_genes.items()}

    reversed_data = dict(reversed(species_genes.items()))

    if outputfilename:
        species_genes_r = {species: species_genes[species] for species in reversed_data}
        plot_genes(species_genes_r, title=outputfilename, format=imageformat, upgenes=upgenes)
        print(f"Plot image saved as {outputfilename}")

    if csvfilename:
        genenum = upgenes + downgenes + 1
        makecsv(species_genes, csvfilename, genenum)
        print(f"CSV saved as {csvfilename}.csv")

    return failed_species, failed_lines


def main():
    check_for_updates()

    parser = argparse.ArgumentParser(description="Query the GenBank database with species and gene names \
                                     to obtain a list of genes upstream and downstream of the target gene.")

    parser.add_argument("-s", "--species", nargs='+', help="Species name(s) (e.g., 'Homo_sapiens' or 'Human')")
    parser.add_argument("-g", "--gene_name", help="Gene name (e.g. BRCA1 or brca1)")
    parser.add_argument("-up", "--upgenes", type=int, required=True, help="Number of upstream genes to search for")
    parser.add_argument("-down", "--downgenes", type=int, required=True, help="Number of downstream genes to search for")
    parser.add_argument("-plot", "--plotname", default=None, help="Output file name for the gene order plot")
    parser.add_argument("-csv", "--csvname", default=None, help="Output file name for the gene order CSV")
    parser.add_argument("-f", "--input_file", default=None, help="Path to a text file containing a list of species and genes")

    args = parser.parse_args()

    failed_species, failed_lines = get_genes(
        args.species,
        args.gene_name,
        args.upgenes,
        args.downgenes,
        args.plotname,
        args.csvname,
        args.input_file,
    )
    if len(failed_species) > 0:
        terminalwidth = get_terminal_size()[0]
        message = f" Failed to process species: {failed_species} "
        nameswidth = len(message)
        leftindent = ((terminalwidth-nameswidth)//2)
        print("\n" + 
              "!"*terminalwidth+
              "!"*leftindent+ 
              f"{message}"+ 
              "!"*(terminalwidth-leftindent-nameswidth)+
              "!"*terminalwidth)
    if len(failed_lines) > 0:
        terminalwidth = get_terminal_size()[0]
        message = f" Failed to process line: '{failed_lines}' "
        nameswidth = len(message)
        leftindent = ((terminalwidth-nameswidth)//2)
        print("\n" + 
              "!"*terminalwidth+
              "!"*leftindent+ 
              f"{message}"+ 
              "!"*(terminalwidth-leftindent-nameswidth)+
              "!"*terminalwidth)


if __name__ == '__main__':
    main()