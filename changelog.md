We optimized the code, and the existing results are slightly better than the data of the submitted paper.

1. The  updated artifact: that part of preprocessing is only done for circuits of small sizes (with the numbers of gates less than or equal to 10000); for large circuits, the preprocessing step merely prepares the data for the following step. The updated artifact is much faster. 

2. The updated artifact does not sort the candidate SWAP edges, so there will be randomness when selecting candidates with the same value. This randomness adds more possibilities to the circuit compilation, and it is possible to find a fewer solution for inserting the SWAP gate. The total number of inserted SWAP gates for 159 cases of submitted papers is 291161 in the file **./results/data/tsa/tsa**.  The new results are in the directory **./results/new/**.  The **tsa** results are consistent with the paper. 

3.  The file  **main.py**  is process the old statistics in the directory **./results/data/**, and the file  **main_new.py** process the new statistics in the directory **./results/new/**.  

4. We have updated the commands for processing statistical information for ease of use, such as

   ```
   python3 main.py [evalnum]  [TSA_cca_path]  [TSA_depth_path] [TSA_num_path]
   python3 main.py [evaldepth]  [TSA_cca_path]  [TSA_depth_path] [TSA_num_path]
   ```

5. The more details are in the file **Readme.txt**.

   