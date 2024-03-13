from copy import copy
# import json
from Bio.Seq import Seq
from geney.mutations.variant_utils import generate_mut_variant, Mutation, find_new_tts
from geney.utils import find_files_by_gene_name, reverse_complement, unload_pickle, unload_json
from geney.Fasta_segment import Fasta_segment
from pathlib import Path
import os
import re
import numpy as np
import subprocess
import joblib
from geney import config_setup

import pkg_resources
pssm_file_path = pkg_resources.resource_filename('geney.translation_initiation', 'resources/kozak_pssm.json')
model_state = pkg_resources.resource_filename('geney.translation_initiation', 'resources/tis_regressor_model.joblib')
PSSM = unload_json(pssm_file_path)
TREE_MODEL = joblib.load(model_state)


class Gene:
    def __init__(self, gene_name):
        self.gene_name = gene_name
        self.gene_id = ''
        self.rev = None
        self.chrm = ''
        self.gene_start = 0
        self.gene_end = 0
        self.transcripts = {}
        self.load_from_file(find_files_by_gene_name(config_setup['MRNA_PATH'] / 'protein_coding', gene_name))

    def __repr__(self):
        return f'Gene(gene_name={self.gene_name})'   #.format(gname=self.gene_name)

    def __len__(self):
        return len(self.transcripts)

    def __str__(self):
        return '{gname}, {ntranscripts} transcripts'.format(gname=self.gene_name, ntranscripts=self.__len__())

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    def __getitem__(self, index):
        return Transcript(list(self.transcripts.values())[index])

    def load_from_file(self, file_name):
        if not file_name.exists():
            raise FileNotFoundError(f"File '{file_name}' not found.")

        self.load_from_dict(dict_data=unload_pickle(file_name))
        return self

    def load_from_dict(self, dict_data=None):
        for k, v in dict_data.items():
            setattr(self, k, v)
        return self

    def generate_transcript(self, tid=None):
        if tid == None:
            tid = [k for k, v in self.transcripts.items() if v['primary_transcript']][0]
        return Transcript(self.transcripts[tid])

    def transcript(self, tid):
        if tid not in self.transcripts:
            raise AttributeError(f"Transcript '{tid}' not found in gene '{self.gene_name}'.")
        return self.generate_transcript(tid)

class Transcript:
    def __init__(self, d=None):
        self.transcript_id = None
        self.transcript_start = None
        self.transcript_end = None
        self.transcript_biotype = None
        self.acceptors, self.donors = [], []
        self.TIS, self.TTS = None, None
        self.transcript_seq, self.transcript_indices = '', []
        self.rev = None
        self.chrm = ''
        self.pre_mrna = ''
        self.orf = ''
        self.protein = ''
        self.log = ''
        if d:
            self.load_from_dict(d)

    def __repr__(self):
        return 'pre_mRNA(transcript_id={tid})'.format(tid=self.transcript_id)

    def __len__(self):
        return len(self.transcript_seq)

    def __str__(self):
        return 'Transcript {tid}, Transcript Type: ' \
               '{protein_coding}'.format(
                tid=self.transcript_id, protein_coding=self.transcript_biotype)

    def __eq__(self, other):
        return self.transcript_seq == other.transcript_seq

    def __contains__(self, subvalue):
        if isinstance(subvalue, str):
            return subvalue in self.transcript_seq
        elif isinstance(subvalue, int):
            return subvalue in self.transcript_indices
        else:
            print(
                "Pass an integer to check against the span of the gene's coordinates or a string to check against the "
                "pre-mRNA sequence.")
            return False

    def __copy__(self, other):
        return copy(self)

    @property
    def constructor(self):
        core_attributes = ['transcript_id', 'transcript_start', 'transcript_end', 'transcript_biotype', 'acceptors', 'donors', 'TIS', 'TTS', 'rev', 'chrm']
        return {k: v for k, v in self.__dict__.items() if k in core_attributes}

    def load_from_dict(self, data):
        for k, v in data.items():
            setattr(self, k, v)
        self.__arrange_boundaries()
        self.generate_mature_mrna(inplace=True)
        return self

    @property
    def exons(self):
        return list(zip(self.acceptors, self.donors))

    def set_exons(self, boundaries):
        self.acceptors, self.donors = boundaries['acceptors'], boundaries['donors']
        self.__arrange_boundaries()
        return self

    @property
    def introns(self):
        return list(zip([v for v in self.donors if v != self.transcript_end], [v for v in self.acceptors if v != self.transcript_start]))

    def __exon_coverage_check(self):
        if sum([abs(a-b) + 1 for a, b in self.exons]) == len(self):
            return True
        else:
            return False
    @property
    def exons_pos(self):
        temp = self.exons
        if self.rev:
            temp = [(b, a) for a, b in temp[::-1]]
        return temp
    @property
    def mrna_indices(self):
        temp = [lst for lsts in [list(range(a, b+1)) for a, b in self.exons_pos] for lst in lsts]
        return sorted(temp, reverse=self.rev)

    def __arrange_boundaries(self):
        self.acceptors.append(self.transcript_start)
        self.donors.append(self.transcript_end)
        self.acceptors = list(set(self.acceptors))
        self.donors = list(set(self.donors))
        self.acceptors.sort(reverse=self.rev)
        self.donors.sort(reverse=self.rev)
        return self

    def positive_strand(self):
        if self.rev:
            return reverse_complement(self.transcript_seq)
        else:
            return self.transcript_seq

    def __pos2sense(self, mrna, indices):
        if self.rev:
            mrna = reverse_complement(mrna)
            indices = indices[::-1]
        return mrna, indices

    def pull_pre_mrna_pos(self):
        fasta_obj = Fasta_segment()
        if self.rev:
            return fasta_obj.read_segment_endpoints(config_setup['CHROM_SOURCE'] / f'chr{self.chrm}.fasta', self.transcript_end,
                                                                   self.transcript_start)
        else:
            return fasta_obj.read_segment_endpoints(config_setup['CHROM_SOURCE'] / f'chr{self.chrm}.fasta', self.transcript_start,
                                                                   self.transcript_end)

    def generate_pre_mrna_pos(self, mutations=[]):
        seq, indices = self.pull_pre_mrna_pos()
        for mutation in mutations:
            mutation = Mutation(mutation)
            seq, indices, _, _ = generate_mut_variant(seq, indices, mut=mutation)

        self.pre_mrna, _ = self.__pos2sense(seq, indices)
        return seq, indices

    def generate_pre_mrna(self, mutations=[], inplace=True):
        pre_mrna, pre_indices = self.__pos2sense(*self.generate_pre_mrna_pos(mutations))
        self.pre_mrna = pre_mrna
        if inplace:
            return self
        return pre_mrna

    def generate_mature_mrna_pos(self, mutations=[]):
        mature_mrna, mature_indices = '', []
        pre_seq, pre_indices = self.generate_pre_mrna_pos(mutations)
        for i, j in self.exons_pos:
            rel_start, rel_end = pre_indices.index(i), pre_indices.index(j)
            mature_mrna += pre_seq[rel_start:rel_end + 1]
            mature_indices.extend(pre_indices[rel_start:rel_end + 1])
        return mature_mrna, mature_indices

    def generate_mature_mrna(self, mutations=[], inplace=True):
        if inplace:
            self.transcript_seq, self.transcript_indices = self.__pos2sense(*self.generate_mature_mrna_pos(mutations))
            return self
        return self.__pos2sense(*self.generate_mature_mrna_pos(mutations))

    def generate_protein(self, inplace=True):
        rel_start = self.transcript_indices.index(self.TIS)
        rel_end = self.transcript_indices.index(self.TTS)
        orf = self.transcript_seq[rel_start:rel_end + 1 + 3]
        protein = str(Seq(orf).translate()).replace('*', '')
        if inplace:
            self.orf = orf
            self.protein = protein
            return self
        return protein

    def generate_translational_boundaries(self):
        if self.TIS not in self.transcript_indices or self.transcript_seq[self.transcript_indices.index(self.TIS):self.transcript_indices.index(self.TIS)+3] != 'ATG':
            new_tis = TISFInder(self.transcript_seq, self.transcript_indices)
            self.log += f' TIS for transcript reacquired: {self.TIS} --> {new_tis}.'
            self.TIS = new_tis
        self.TTS = find_new_tts(self.transcript_seq, self.transcript_indices, self.TIS)
        return self



def TISFInder(seq, index=None):
    '''
    Predicts the most likely start (TIS) and end (TTS) positions in a mature mRNA sequence.

    Parameters:
    var_seq (str): Mature mRNA sequence of a transcript with unknown TIS/TTS.
    var_index (list): Index coverage of the mRNA sequence.
    nstart (str): ORF of a mature reference sequence including start codon.
    istart (list): ORF index coverage of the reference sequence.

    Returns:
    tuple: A tuple containing the predicted relative positions of the start and end codons (TIS and TTS).
    '''

    start_codon_positions = [i for i in range(len(seq) - 2) if seq[i:i + 3] == 'ATG']
    if len(start_codon_positions) == 0:
        if index is None:
            return 0
        else:
            return index[0]

    kozak_scores = [calculate_kozak_score(seq, pos, PSSM) for pos in start_codon_positions]
    corresponding_end_codons = [get_end_codon(seq, pos) for pos in start_codon_positions]
    folding_scores = [calculate_folding_energy(seq, pos) for pos in start_codon_positions]
    # titer_scores = [calculate_titer_score(seq, pos) for por in start_codon_positions]

    input_X = np.array([kozak_scores, corresponding_end_codons, folding_scores]).transpose() #, titer_scores])
    scores = TREE_MODEL.predict(input_X)
    max_pos = np.argmax(scores)
    rel_start_pos = start_codon_positions[max_pos]

    if index is None:
        return rel_start_pos
    else:
        return index[rel_start_pos]


def calculate_kozak_score(seq, position, PSSM):
    """
    Calculates the Kozak score for a 9-nucleotide segment of a sequence,
    starting 3 nucleotides before the given position.

    Parameters:
    seq (str): The full nucleotide sequence.
    position (int): The relative position in the sequence to target for scoring.
    PSSM (np.array): Position-specific scoring matrix for Kozak sequence scoring.

    Returns:
    float: The calculated Kozak score, or None if the segment is not of valid length.

    Raises:
    ValueError: If the position is not valid within the sequence.
    """

    # Validate position for a valid 9-nucleotide segment
    if not 6 <= position < len(seq) - 9:
        return 0
        # raise ValueError("Position does not allow for a valid 9-nucleotide segment extraction.")

    # Extract the 9-nucleotide segment
    segment = seq[position - 6:position + 9]

    # Calculate score using list comprehension
    try:
        score = np.prod([PSSM[nucleotide][i] + 1 for i, nucleotide in enumerate(segment)])
    except KeyError as e:
        raise ValueError(f"Invalid nucleotide in sequence: {e}")

    return score

def calculate_folding_energy(seq, position, front_margin=20, back_margin=10):
    """
    Calculates the folding energy of a nucleotide sequence using ViennaRNA's RNAfold tool.

    Parameters:
    sequence (str): The nucleotide sequence for which folding energy is to be calculated.

    Returns:
    float: The folding energy of the sequence, or None if an error occurs.
    """

    segment = seq[max(0, position-front_margin):min(position+back_margin, len(seq))]

    try:
        # Call RNAfold with the sequence
        process = subprocess.run(['RNAfold'], input=segment, text=True, capture_output=True)

        # Capture the output
        output = process.stdout
        # Regular expression to find the folding energy
        match = re.search(r'\((\s*[-+]?\d*\.\d+)\)', output)
        if match:
            return float(match.group(1))

    except Exception as e:
        print(f"An error occurred: {e}")
        return 0


def get_end_codon(seq, start_position):
    """
    Finds the position of the first in-frame stop codon in a nucleotide sequence starting from a specified position.

    Parameters:
    seq (str): The nucleotide sequence.
    start_position (int): The relative position in the sequence to start searching for the stop codon.

    Returns:
    int: The relative position of the first in-frame stop codon after the start position.
         Returns -1 if no stop codon is found.
    """

    # Define stop codons
    stop_codons = ['TAG', 'TGA', 'TAA']

    # Check for each triplet (codon) in the sequence starting from start_position
    for i in range(start_position, len(seq) - 2, 3):
        codon = seq[i:i + 3]
        if codon in stop_codons:
            return i - start_position

    # Return -1 if no stop codon is found
    return 0


def calculate_titer_score(seq, pos):
    return 0
