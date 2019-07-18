# Joshua Sacher
# 12 Jul 2019

import csv
import itertools
import os
import requests
import time
import numpy as np
import pandas as pd

from Bio import AlignIO, Entrez, SeqIO
from Bio.Align.Applications import ClustalOmegaCommandline
from Bio.Alphabet import IUPAC
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

from flask import Flask, jsonify, redirect, render_template, request, send_file, session
from flask_session import Session

# Clustal Omega API connection
import clustalo
# Clustal Omega API options
options = {
    'email': 'jrsacher@broadinstitute.org',  # required
    'sequence': None,       # required
    'outfile': 'temp_out.aln',  # required
    'outfmt': 'clustal',
    'stype': 'protein',
    'title': 'identity_matrix',
    'guidetreeout': 'true',
    'dismatout': 'true',
    'dealign': 'false',
    'mbed': 'true',
    'mbediteration': 'true',
    'iterations': 0,
    'gtiterations': -1,
    'hmmiterations': -1,
    'order': 'aligned'
}

# Change email to not my personal one?
Entrez.email = 'jrsacher@broadinstitute.org'
Entrez.api_key = os.getenv('NCBI_KEY')

# Configure Flask
app = Flask(__name__)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/identity', methods=['GET'])
def identity():

    # Render form
    if request.method == 'GET':
        return render_template('identity.html')


@app.route('/matrix', methods=['GET', 'POST'])
def matrix():
    ''' Generates a protein identity matrix from UniProt IDs '''

    # Display matrix
    if request.method == 'GET':
        ident_matrix = pd.read_csv('identity_matrix.csv', index_col=0)
        return render_template('matrix.html', matrix=ident_matrix.to_html(table_id='matrix'))

    # Timer!
    start = time.time()

    # Get UniProt ids from website
    input_file = request.files.get('input_file')
    if input_file:
        input_file = input_file.read().decode('utf-8')
    input_text = request.form.get('input_text')
    if not input_file and not input_text:
        return render_template('error.html', message='no ids provided')

    uniprot_ids = []

    # File gets priority
    if input_file:
        uniprot_ids = input_file.split()
    else:
        uniprot_ids = input_text.split()

    if len(uniprot_ids) <= 1:
        return render_template('error.html', message='at least 2 ids required')

    seqs = []

    # Lookup proteins from NCBI using UniProt IDs
    for uniprot_id in uniprot_ids:
        with Entrez.efetch(db='protein', id=uniprot_id, retmode='text', rettype='fasta') as handle:
            records = SeqIO.parse(handle, 'fasta')
            # add SeqRecord objects to seqs list
            for seq in records:
                seq.annotations['uniprot'] = uniprot_id  # for later matching
                seqs.append(seq)
        time.sleep(0.25)

    # Setup dataframe to store identity results with 100 on the diagonals
    ident_matrix = pd.DataFrame(data=0, columns=uniprot_ids, index=uniprot_ids)
    for seq in seqs:
        ident_matrix.loc[seq.annotations['uniprot'], seq.annotations['uniprot']] = 100

    # Perform alignments using Clustal Omega
    for pair in itertools.combinations(seqs, 2):
        SeqIO.write(pair, 'temp_in.fasta', 'fasta')  # temporary input file
        clustalo.align(options)

        # Load in resulting alignment file
        try:
            alignment = AlignIO.read('temp_out.aln', 'clustal')
        except:
            return render_template('error.html', message='Error in alignment process. Please try again')

        # Make NumPy array for identity
        align_array = np.array([list(rec) for rec in alignment], np.character)

        # Calculate identity and store in matrix
        ident = 0
        for i in range(alignment.get_alignment_length()):
            if align_array[0, i] == align_array[1, i]:
                ident += 1

        row = pair[0].annotations['uniprot']
        col = pair[1].annotations['uniprot']

        # Change rounding precision?
        ident_pct = round((ident / alignment.get_alignment_length()) * 100)
        ident_matrix.loc[row, col] = ident_pct
        ident_matrix.loc[col, row] = ident_pct

    # print(ident_matrix)

    # Write matrix to csv file
    ident_matrix.to_csv('identity_matrix.csv')

    # Stop the timer
    stop = time.time()
    print(f'{len(uniprot_ids)} x {len(uniprot_ids)} matrix processed in {int((stop - start) // 60)}:{round((stop - start) % 60,3):06.6}')

    return render_template('matrix.html', matrix=ident_matrix.to_html(table_id='matrix'))

# Downloading through JS now
# @app.route('/download', methods=['POST'])
# def download():
#     try:
#         return send_file('identity_matrix.csv', attachment_filename='identity_matrix.csv')
#     except Exception as e:
#         return render_template('error.html', message=e)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
