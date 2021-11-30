from builtins import range
import sys
import os
import time

from qct_tools.qct import QCT
from qct_tools.circuit_preprocess import get_initial_gql
from qct_tools.utils.FileUtils import FileUtils
from qct_tools.utils.PathUtil import PathUtil

if len(sys.argv) == 10:
    count = 0
    path = 'processed_data/'
    files = os.listdir(path)

    SIZE = sys.argv[2]
    start = time.time()
    forw = float(sys.argv[5])
    while forw < float(sys.argv[6]):
        delta = float(sys.argv[7])
        while delta < float(sys.argv[8]):
            out_file = ""
            type = 0
            ini_mapping_path = "connect_ini_mapping_q20"
            if sys.argv[3] == 'num':
                type = 0
                out_file += 'numcca'
            elif sys.argv[3] == 'depth':
                type = 1
                out_file += 'depth'
            elif sys.argv[3] == 'cca':
                type = 2
                out_file += 'ccanum'
            elif sys.argv[3] == 'numdep':
                type = 3
                out_file += 'numdep'
            else:
                print(
                    'Please input correct parameters : python run.py [[1 connect/degree] [2 small/medium/large/all] [3 num/depth/cca] [4 the output file prefix] [5 range_of_l_a] [6 range_of_l_a] [7 range of delta] [8 range of delta] [9 span of delta]')
                sys.exit(-1)
            if sys.argv[1] == 'connect':
                out_file += 'connect'
            elif sys.argv[1] == 'degree':
                ini_mapping_path = "degree_ini_mapping_q20"
                out_file += 'degree'
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
                    'Please input correct parameters : python run.py [[1 connect/degree] [2 small/medium/large/all] [3 num/depth/cca] [4 the output file prefix] [5 range_of_l_a] [6 range_of_l_a] [7 range of delta] [8 range of delta] [9 span of delta]')
                sys.exit(-1)
            out_file = '%s%s_forw_%.2f_delta_%.5f' % (SIZE, out_file, forw, delta)
            outpath = 'results/%s/%s' % (sys.argv[4], out_file)
            print("*********************Tabu search start********************")
            print('the initial mapping path: ', ini_mapping_path)
            print('the evaluation criterion: ', sys.argv[3])
            print('the number of look-ahead layers: ', forw)
            print('the attenuation factor: ', delta)
            print('the output file: %s' % (outpath))
            print('the generated circuit directory: results/circuits/%s/' % sys.argv[4])
            print("**********************************************")
            po = open(outpath, "w")
            print(forw, delta)
            pathUtil = PathUtil(20)
            graph = pathUtil.build_graph_QX20()
            dist = pathUtil.build_dist_table_tabu(graph.graph)
            count = 0
            print(len(files))
            for fileindex in range(len(files)):
                file_name=files[fileindex]
                ss = file_name.split('.')[0]
                min_swaps = 99999999
                in_start = time.time()
                min_index = -1
                min_time = 99999999
                count += 1
                current_path = 'processed_data/' + file_name
                if os.path.isdir(current_path) or current_path.endswith('zip'):
                    continue
                fu = FileUtils()
                fileResult = fu.readQasm(path=current_path)
                l = fileResult.n2gates
                if SIZE == 'small':
                    if l >= 100:
                        continue
                if SIZE == 'medium':
                    if l > 1000 or l < 100:
                        continue
                if SIZE == 'large':
                    if l <= 1000:
                        continue
                prefix = ''
                print('This is the %dth circuit: %s, consisting of %d 2-qubit gates' % (count, ss, l))
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
                    continue

                for i in range(len(initial_mapping.lolist)):
                    swaps = []
                    locations = initial_mapping.lolist[i].copy()
                    qubits = initial_mapping.qlist[i].copy()
                    qct = QCT()
                    OW = qct.originalSearch(layers_original, forw, delta, ss, graph, dist, locations, qubits, i,
                                            type, sys.argv[4],out_file)
                    if type >-1 :
                        IW = qct.improveSearch(layers_improve, forw, delta, ss, graph, dist, locations, qubits, i, type,
                                               sys.argv[4],out_file)
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
                'results/circuits/%s/original/%s_%s_%d.qasm'
                min_files = FileUtils.readQasm('results/circuits/%s/%s/%s_%s_%d.qasm' % (sys.argv[4],
                                                                                                prefix, out_file,ss,
                                                                                                min_index))
                compath = '%s_%s_%d.qasm' % (out_file,ss, min_index)
                os.system('find results/circuits/%s/*/%s_%s*.qasm ! -name %s -type f -exec rm -rf {} \;' % (
                    sys.argv[4], out_file,ss, compath))
                # print('find results/circuits/%s/*/%s_%.2f_%.5f*.qasm ! -name %s -type f -exec rm -rf {} \;'%(sys.argv[4], ss, forw, delta, compath))
                po.write('%s\n' % (ss))
                po.write('%s %d %d %d %d %d %lf %lf %f\n' % (prefix,
                                                             min_index, fileResult.ngates, min_files.ngates,
                                                             len(min_files.layers), min_swaps, forw, delta,
                                                             min_time))


                # print(
                #     'the minimal initial mapping index: %d\nthe ini gates number: %d\nthe output circuit inserted %d SWAP gates\nthe total gates number: %d\nthe 2-qubit gates number: %d\nthe depth of generated circuit: %d\nthe cost time: %d,\n' % (
                #         min_index, fileResult.ngates, min_swaps,min_files.ngates, min_files.n2gates, len(min_files.layers), min_time))
                po.flush()
            end = time.time()
            po.write('time:%f' % (end - start))
            po.flush()
            po.close()
            delta += float(sys.argv[9])
        forw += 1
else:
    print(
        'Please input correct parameters : python run.py [[1 connect/degree] [2 small/medium/large/all] [3 num/depth/cca] [4 the generated_circuit path] [5 range_of_l_a] [6 range_of_l_a] [7 range of delta] [8 range of delta] [9 span of delta]')
    sys.exit(-1)


