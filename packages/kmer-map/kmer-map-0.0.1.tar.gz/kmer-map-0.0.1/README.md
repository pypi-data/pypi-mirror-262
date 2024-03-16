# Kmer Manifold Approximation and Projection (KMAP)
kmap is a package for visualizing kmers in 2D space. 

## Installation
```
conda create --name=kmap_test python=3.11
conda activate kmap_test
conda install anaconda::scipy
conda install anaconda::numpy
conda install anaconda::matplotlib
conda install anaconda::pandas
conda install anaconda::click
conda install anaconda::tomli-w
conda install anaconda::requests
conda install conda-forge::biopython
conda install bioconda::logomaker
pip install taichi

pip install kmer-map
```

## Example usage
The following code shows the typical workflow of the test data in `./tests/test.fa`
```
# step 0: preprocess input fast file
kmap preproc --fasta_file ./tests/test.fa --res_dir ./test 

# step 2: scanning for motifs 
kmap scan_motif --res_dir ./test --debug true

# step 3: visualize kmers
# now edit the "./test/config.toml" file, in the 3rd section "visualization"
# change "n_max_iter = 2500" to "n_max_iter = 100"  
kmap visualize_kmers --res_dir ./test --debug True
```

If you feel the consensus is `AATCGATAGC`, instead of `A[AATCGATAGC]GA` you can use the following commands. 
The motif logo for this consensus sequence is given by `./test/hamming_balls/logo.pdf`
```
kmap ex_hamball --res_dir ./test --conseq AATCGATAGC --return_type matrix --output_file ./test/hamming_balls/AATCGATAGC_cntmat.csv 
kmap draw_logo --cnt_mat_numpy_file ./test/hamming_balls/AATCGATAGC_cntmat.csv --output_fig_file ./test/hamming_balls/logo.pdf
```

Or if you want to change the number of maximum mutations to the consensus sequence `` to 3,
you can use the following commands to derive the motif. 
The motif logo for this consensus sequence is given by `./test/hamming_balls/logo.pdf`
```
kmap ex_hamball --res_dir ./test --conseq GTACGTAGGTCCTA --return_type matrix --max_ham_dist 3 --output_file ./test/hamming_balls/GTACGTAGGTCCTA_cntmat.csv 
kmap draw_logo --cnt_mat_numpy_file ./test/hamming_balls/GTACGTAGGTCCTA_cntmat.csv --output_fig_file ./test/hamming_balls/logo.pdf
```

[comment]: <> (Release commands)
[comment]: <> (python -m build) 
[comment]: <> (python3 -m twine upload --repository testpypi dist/*)

