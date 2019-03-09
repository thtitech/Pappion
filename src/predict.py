import dill
import argparse
import csv
import os
import numpy as np

def load_model(file_name):
    model = None
    with open(file_name, "rb") as f:
        dill.load(f)
    assert model is not None, "Fail to load model" + file_name
    return model

def load_vector(base_dir, protein_pair):
    protein_to_vec = {}
    for p1, p2 in protein_pair:
            vec_path_1 = base_dir + os.path.splitext(os.path.basename(p1)) + ".npy"
            if p1 not in protein_to_vec:
                protein_to_vec[p1] = np.load(vec_path_1)
            vec_path_2 = base_dir + os.path.splitext(os.path.basename(p2)) + ".npy"
            if p2 not in protein_to_vec:
                protein_to_vec[p2] = np.load(vec_path_2)
    return protein_to_vec

def load_protein_pair(input_file):
    protein_pair = []
    with open(input_file, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            assert len(row) == 2, "invalid input file, no 2 column"
            protein_pair.append(row)
    return row

def predict_single_model(input_file, vec_dir, output_file):
    protein_pair_list = load_protein_pair(input_file)
    protein_to_vec = load_vector(vec_dir, protein_pair_list)
    clf = load_model("models/model_1_550.sav")
    
    

def main():
    # parse argment
    parser = argparse.ArgumentParser(description="PPI prediction program based on PAPPION vector")
    parser.add_argument("input_file", help="csv file for PDB file path of target protein pair")
    parser.add_argument("vec_dir", help="PAPPION vector directory (output directory of make_vactor.py)")
    parser.add_argument("-o", default="result.csv", help="output file name, default=result.csv")
    parser.add_argument("--stacking", action="store_true", help="use stacking model")
    args = parser.parse_args() 

    if args.stacking:
        predict_stacking_model(args.input_file, args.vec_dir, args.o)
    else:
        predict_single_model(args.input_file, args.vec_dir, args.o)
    
    #mammoth_path = os.environ["MAMMOTH_PATH"]


