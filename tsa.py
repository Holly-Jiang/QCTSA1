import os
import sys
import time

from processing import processingle
from complete import completeSingle
from qct_tools.circuit_preprocess import get_initial_gql
from qct_tools.qct import QCT
from qct_tools.utils.FileUtils import FileUtils
from qct_tools.utils.PathUtil import PathUtil

if len(sys.argv) == 7:
    start = time.time()
    forw = float(sys.argv[3])
    delta = float(sys.argv[4])
    p = sys.argv[5].split('/')
    filename = p[len(p) - 1].split('.')[0]
    out_file = ""
    processingle(sys.argv[5])
    ini_mapping_path = "connect_ini_mapping_q20"
    if sys.argv[2] == 'num':
        type = 0
        out_file += 'numcca'
    elif sys.argv[2] == 'depth':
        type = 1
        out_file += 'depthnum'
    elif sys.argv[2] == 'cca':
        type = 2
        out_file += 'ccanum'
    elif sys.argv[2] == 'numdep':
        type = 3
        out_file += 'numdepth'
    else:
        print(
        'Please input correct parameters : python tsa.py [[1 connect/degree] [2 num/depth/cca] [3 l_a] [4 delta] [5 input file path] [6 the output file prefix]')
        sys.exit(-1)
    if sys.argv[1] == 'connect':
        out_file += 'connect'
        completeSingle(filename, type, ini_mapping_path)
    elif sys.argv[1] == 'degree':
        ini_mapping_path = "degree_ini_mapping_q20"
        out_file += 'degree'
        completeSingle(filename, type, ini_mapping_path)
    elif sys.argv[1] == 'ga':
        ini_mapping_path = 'optm_ini'
        out_file += 'ga'
    elif sys.argv[1] == 'fidsl':
        ini_mapping_path = 'fidsl_ini'
        out_file += 'fidsl'
    elif sys.argv[1] == 'sabre':
        ini_mapping_path = 'sabre_ini'
        out_file += 'sabre'
    else:
        print(
        'Please input correct parameters : python tsa.py [[1 connect/degree] [2 num/depth/cca] [3 l_a] [4 delta] [5 input file path] [6 the output file prefix]')
        sys.exit(-1)
    count = 0
    outpath = 'results/%s/%s_%s_%s' % (sys.argv[6], out_file,forw,delta)
    print("*********************Tabu search start********************")
    print('the input file path: ', sys.argv[5])
    print('the initial mapping path: ', ini_mapping_path)
    print('the evaluation criterion: ', sys.argv[2])
    print('the number of look-ahead layers: ', sys.argv[3])
    print('the attenuation factor: ', sys.argv[4])
    print('the output path: ', outpath)

    po = open(outpath, "a+")
    pathUtil = PathUtil(20)
    graph = pathUtil.build_graph_QX20()
    dist = pathUtil.build_dist_table_tabu(graph.graph)
    ss = filename
    min_swaps = 99999999
    in_start = time.time()
    min_index = -1
    min_time = 99999999
    count += 1
    current_path = 'processed_data/' + filename+'.qasm'
    if os.path.isdir(current_path) or current_path.endswith('zip'):
        sys.exit('the path [%s] is valid!' % sys.argv[5])
    fu = FileUtils()
    fileResult = fu.readQasm(path=current_path)
    l = fileResult.n2gates
    prefix = ''
    print('the circuit: %s, consisting of %d 2-qubit gates' % ( ss, l))
    layers_original = []
    layers_improve = []
    for i in range(len(fileResult.layers)):
        ori = []
        imp = []
        for j in range(len(fileResult.layers[i])):
            ori.append(fileResult.layers[i][j])
            imp.append(fileResult.layers[i][j])
        layers_original.append(ori)
        layers_improve.append(imp)

    initial_mapping = get_initial_gql(ss, type, ini_mapping_path)
    if len(initial_mapping.lolist) <= 0:
        print('there no  initial mapping')
        sys.exit(-1)
    for i in range(len(initial_mapping.lolist)):
        swaps = []
        locations = initial_mapping.lolist[i].copy()
        qubits = initial_mapping.qlist[i].copy()
        qct = QCT()
        OW = qct.originalSearch(layers_original, forw,delta, ss, graph, dist, locations, qubits, i,
                                type,sys.argv[6],out_file)

        if type >-1 :
            IW = qct.improveSearch(layers_improve, forw, delta, ss, graph, dist, locations, qubits, i, type,
                                   sys.argv[6],out_file)
            if OW != None and IW != None:
                if (IW.min_swaps < OW.min_swaps):
                    if (min_swaps > IW.min_swaps):
                        min_swaps = IW.min_swaps
                        prefix = "improve"
                        min_index = IW.min_index
                        # print('%d %d %d'%(i, IW.min_swaps,min_swaps))
                else:
                    if (min_swaps > OW.min_swaps):
                        min_swaps = OW.min_swaps
                        prefix = "original"
                        min_index = OW.min_index
            else:
                print("IW: " + IW)
                print("OW: " + OW)
                if (IW != None and min_swaps > IW.min_swaps):
                    min_swaps = IW.min_swaps
                    prefix = "improve"
                    min_index = IW.min_index
                elif (OW != None and min_swaps > OW.min_swaps):
                    min_swaps = OW.min_swaps
                    prefix = "original"
                    min_index = OW.min_index
        else:
            min_swaps = OW.min_swaps
            prefix = "original"
            min_index = OW.min_index
        if min_swaps == 0:
            break

    in_end = time.time()
    min_time = in_end - in_start
    min_files = FileUtils.readQasm('results/circuits/%s/%s/%s_%s_%d.qasm' % (sys.argv[6],
                                                                                    prefix, out_file, ss,
                                                                                    min_index))
    po.write('%s\n' % (ss))
    po.write('%s %d %d %d %d %d %lf %lf %f\n' % (prefix,
                                         min_index, fileResult.ngates, min_files.ngates, len(min_files.layers),
                                         min_swaps,forw,delta,
                                         min_time))
    compath = '%s_%s_%d.qasm' % ( out_file,ss, min_index)
    os.system('find results/circuits/%s/*/%s_%s*.qasm ! -name %s -type f -exec rm -rf {} \;' % (
        sys.argv[6],  out_file, ss, compath))
    print(
        'the minimal initial mapping index: %d\nthe ini gates number: %d\nthe output circuit inserted %d SWAP gates\nthe total gates number: %d\nthe 2-qubit gates number: %d\nthe depth of generated circuit: %d\nthe cost time: %d,\n' % (
            min_index, fileResult.ngates, min_swaps,min_files.ngates, min_files.n2gates, len(min_files.layers), min_time))
    po.flush()
    end = time.time()
    po.write('time:%f\n' % (end - start))
    po.flush()
    po.close()
else:
    print(
        'Please input correct parameters : python tsa.py [[1 connect/degree] [2 num/depth/cca] [3 l_a] [4 delta] [5 input file path] [6 the output file prefix]')
    sys.exit(-1)
