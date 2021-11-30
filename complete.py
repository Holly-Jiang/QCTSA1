import sys, time, os

from base.MyVF2 import MyVF2
from qct_tools.utils.FileUtils import FileUtils


def executeShellCommands(bashcommads):
    if os.path.isdir(bashcommads) or bashcommads.endswith('zip'):
        print('the commands is not execute: ', bashcommads)
        return
    file = open(bashcommads, 'r')
    line = file.readline().strip()
    while line != ' ' and line != '':
        os.system(line)
        line = file.readline()


def completeSingle(file_name, type: int, out_path):
    graphpath = 'graphDB/QX20.data'
    querypath = 'graphDB/ex2.my'
    outpath = 'graphDB/res_ex2.my'
    files = os.listdir('pre_ini_qx20/')
    outinipath = 'graphDB/ini_map_GQL.my'
    mappingpath = ''
    mappingpath = 'pre_ini_qx20/%s' % (file_name)
    querypath = 'pre_result/%s' % (file_name)
    outinipath = '%s/%s' % (out_path, file_name)
    iniwriter = open(outinipath, 'w+')
    graphset = FileUtils.loadGraphSetFromFile(graphpath, 'Graph ')
    queryset = FileUtils.loadGraphSetFromFile(querypath, 'Query ')
    mapping = FileUtils.loadDataSetFromFile(mappingpath, 'mapping ')
    if len(mapping) <= 0:
        os.system(
            'CISC/SubgraphComparing/build/matching/SubgraphMatching.out -d CISC/SubgraphComparing/test/sample_dataset/test_case_1.graph -q pre_result/%s  -filter DPiso -order GQL -engine LFTJ -num 100\n' % (
                file_name))

        mapping = FileUtils.loadDataSetFromFile(mappingpath, 'mapping ')
    maxMappingCount = 0
    mappingresult = dict()
    for i in range(len(mapping)):
        m = 0
        for j in range(len(mapping[i])):
            if mapping[i][j] - 99999 != 0:
                m += 1
        mappingresult['%d' % i] = m
        if m - maxMappingCount > 0:
            maxMappingCount = m
    vf2 = MyVF2()
    print('loading Done')
    for querygraph in queryset:
        stateset = vf2.dealData(graphset, querygraph, mappingresult, type, mapping)
        for i in range(len(stateset)):
            res = [20] * 20
            for j in range(len(stateset[i])):
                res[stateset[i][j]] = j
            iniwriter.write(str(res))
            iniwriter.write('\n')
    iniwriter.flush()
    iniwriter.close()
    print('----------------finish----------------')


def complete(type: int, out_path):
    graphpath = 'graphDB/QX20.data'
    querypath = 'graphDB/ex2.my'
    outpath = 'graphDB/res_ex2.my'
    files = os.listdir('pre_ini_qx20/')
    outinipath = 'graphDB/ini_map_GQL.my'
    mappingpath = ''
    bashcommand = 'shells/subgraph.sh'
    executeShellCommands(bashcommand)
    for file_name in files:
        print(file_name)
        mappingpath = 'pre_ini_qx20/%s' % (file_name)
        querypath = 'pre_result/%s' % (file_name)
        outinipath = '%s/%s' % (out_path, file_name)
        iniwriter = open(outinipath, 'w+')
        graphset = FileUtils.loadGraphSetFromFile(graphpath, 'Graph ')
        queryset = FileUtils.loadGraphSetFromFile(querypath, 'Query ')
        mapping = FileUtils.loadDataSetFromFile(mappingpath, 'mapping ')
        if len(mapping) <= 0:
            os.system(
                'CISC/SubgraphComparing/build/matching/SubgraphMatching.out -d CISC/SubgraphComparing/test/sample_dataset/test_case_1.graph -q pre_result/%s  -filter DPiso -order GQL -engine LFTJ -num 100\n' % (
                    file_name))

            mapping = FileUtils.loadDataSetFromFile(mappingpath, 'mapping ')
        maxMappingCount = 0
        mappingresult = dict()
        for i in range(len(mapping)):
            m = 0
            for j in range(len(mapping[i])):
                if mapping[i][j] - 99999 != 0:
                    m += 1
            mappingresult['%d' % i] = m
            if m - maxMappingCount > 0:
                maxMappingCount = m
        vf2 = MyVF2()
        print('loading Done')
        for querygraph in queryset:
            stateset = vf2.dealData(graphset, querygraph, mappingresult, type, mapping)
            for i in range(len(stateset)):
                res = [20] * 20
                for j in range(len(stateset[i])):
                    res[stateset[i][j]] = j
                iniwriter.write(str(res))
                iniwriter.write('\n')
        iniwriter.flush()
        iniwriter.close()
        print('----------------finish----------------')


if __name__ == '__main__':
    out_path = 'connect_ini_mapping_q20'
    type = 0
    if sys.argv[1] == 'connect':
        type = 0
    elif sys.argv[1] == 'degree':
        type = 1
        out_path = 'degree_ini_mapping_q20'
    else:
        print('please input the correct parameter [connect/degree]')
        sys.exit(-1)
    complete(type, out_path)
