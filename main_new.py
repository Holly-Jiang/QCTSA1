# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import math
import os, sys


# Press the green button in the gutter to run the script.
def read_tabu_files(path):
    if path == '':
        print('the path \'%s\' is not exist' % path)
    map = dict()
    f = open(path, "r")
    while True:
        str = f.readline().strip()
        line = f.readline().strip()
        if not line:
            break
        if line.__eq__(''):
            break
        list1 = list()
        arr = line.split(' ')
        for i in range(len(arr)):
            if i > 0:
                list1.append(float(arr[i]))
            else:
                list1.append(arr[i])
        map['%s' % str] = list1
    return map


def read_tabu_files1(path):
    if path == '':
        print('the path \'%s\' is not exist' % path)
    map = dict()
    f = open(path, "r")
    while True:
        str = f.readline().strip()
        line = f.readline().strip()
        if not line:
            break
        if line.__eq__(''):
            break
        list1 = list()
        arr = line.split(' ')
        for i in range(len(arr)):
            list1.append(float(arr[i]))
        map['%s' % str] = list1
    return map


def read_sabre_files(path):
    map = dict()
    f = open(path, "r")
    res = list()
    while True:
        str = f.readline().strip()
        line = f.readline().strip()
        if not line:
            break
        if line.__eq__(''):
            break
        list1 = list()
        arr = line.split(' ')
        list1.append(float(arr[0]))
        list1.append(float(arr[1]))
        list1.append(float(arr[2]))
        map[str] = list1
    return map


def readOptm(path):
    map = dict()
    f = open(path, "r")
    res = list()
    key = ''
    while True:
        line = f.readline().strip()
        if not line:
            break
        if line.__eq__(''):
            break
        list1 = list()
        arr = line.split(' ')
        if len(arr) == 4:
            list1.append(float(arr[0]))
            list1.append(float(arr[1]))
            list1.append(float(arr[2]))
            list1.append(float(arr[3]))
            res.append(list1)
        elif len(arr) == 5:
            list1.append(float(arr[0]))
            list1.append(float(arr[1]))
            list1.append(float(arr[2]))
            list1.append(float(arr[3]))
            list1.append(float(arr[4]))
            res.append(list1)
        else:
            if (res != None and len(res) > 0):
                map[key] = res
                res = list()
            key = line
    return map


def read_topgraph_files(path):
    if path == '':
        print('the path \'%s\' is not exist' % path)
    map = dict()
    f = open(path, "r")
    while True:
        str = f.readline().strip()
        line = f.readline().strip()
        if not line:
            break
        if line.__eq__(''):
            break
        list1 = list()
        arr = line.split(' ')
        if not float(arr[0]).__eq__(9999999):
            list1.append(float(arr[0]))
            list1.append(float(arr[1]))
            map['%s' % str] = list1
    return map


def selectTheBestResultFromFiles(path):
    files = os.listdir(path)
    mingatesum = 999999999
    mingatename = ''
    for file in files:
        map = read_tabu_files('%s/%s' % (path, file))
        gatesum = 0
        it1 = map.keys()
        # if len(it1)!=159:
        #     continue
        for k1 in it1:
            gatesum += map.get(k1)[5]
        if gatesum < mingatesum:
            mingatesum = gatesum
            mingatename = file
        # print('%s %s %s %f'%(file,file[30:],file[19:23], math.log(gatesum,10)))
        print('%s %d' % (file, gatesum))
    print("the minimal file is [[%s]], consisting of [[%d]] gates. " % (mingatename, mingatesum))


def selectTheMinimalDepthFromFiles(path, name):
    po = open(name, "w")
    files = os.listdir(path)
    res = dict()
    mapu = read_tabu_files('./results/example')
    it = mapu.keys()
    gatesum = 0

    print(
        '[Minimal mapping index] [Number of 2-qubit gates of the initial circuit]  [Depth of the generated circuit] \n[Number of SWAP inserted] [Number of look-ahead layers] [Attenuation factor] [Runtime] ')
    for k in it:
        res['%s' % k] = mapu.get(k)
        for file in files:
            map = read_tabu_files('%s\%s' % (path, file))
            it1 = map.keys()
            for k1 in it1:
                if k1.__eq__(k):
                    if res['%s' % k][4] > map.get(k1)[4]:
                        res['%s' % k] = map.get(k1)
                    break

        if res['%s' % k][4] != 999999999:
            gatesum += res['%s' % k][4]
            key = '%s' % k
            print(key)
            po.write('%s\n' % k)
            for i in range(len(res[key])):
                # print(res[key][i],end=' ')
                if i != 0 and i != 6 and i != 7:
                    print('%s ' % res[key][i], end=' ')
                    po.write('%s ' % res[key][i])
            print()
            po.write('\n')
    po.flush()
    po.close()
    print("the minimal file  [[%s]], depth: %d " % (name, gatesum))


def selectTheMinimalGatesFromFiles(path, name):
    po = open(name, "w")
    files = os.listdir(path)
    res = dict()
    mapu = read_tabu_files('./results/example')
    it = mapu.keys()
    gatesum = 0
    print(
        '[Minimal mapping index] [Number of gates of the initial circuit]  [Depth of the generated circuit] \n[Number of SWAP inserted] [Runtime] ')
    for k in it:
        res['%s' % k] = mapu.get(k)
        for file in files:
            map = read_tabu_files('%s\%s' % (path, file))
            it1 = map.keys()
            for k1 in it1:
                if k1.__eq__(k):
                    if res['%s' % k][5] > map.get(k1)[5]:
                        res['%s' % k] = map.get(k1)
                    break
        if res['%s' %k][5] != 999999999:
            gatesum += res['%s' % k][5]
            key = '%s' % k
            print(key)
            po.write('%s\n' % k)
            for i in range(len(res[key])):
                if i != 0 and i != 6 and i != 7:
                    print('%s ' % res[key][i], end=' ')
                    po.write('%s ' % res[key][i])
            print()
            po.write('\n')
    po.flush()
    po.close()
    print("the minimal file  [[%s]] consists of %d gates " % (name, gatesum))


# mini ./results/qct/  ./results/test/tsa
def caculateTheAdjustTSA():
    print('_________________________comparison of <*_TSA_num>______________________')
    fcca = "./results/new/fidsltsa"
    fidslcca = read_tabu_files1(fcca)
    tcca = "./results/new/tsa"
    tsacca = read_tabu_files1(tcca)
    occa = "./results/new/gatsa"
    optmcca = read_tabu_files1(occa)
    sabrestr = "./results/new/sabretsa"
    sabremap = read_tabu_files1(sabrestr)
    names = list()
    it = tsacca.keys()
    for k in it:
        if fidslcca.get(k) == None:
            names.append(k)
        elif optmcca.get(k) == None:
            names.append(k)
        elif sabremap.get(k) == None:
            names.append(k)
    for i in range(len(names)):
        del tsacca[names[i]]
    tsagate = 0
    optmgate = 0
    fidslgate = 0
    ori = 0
    sabregate = 0
    it = tsacca.keys()
    for k in it:
        tsagate += tsacca.get(k)[4] * 3
        fidsltsa = fidslcca.get(k)
        fidslgate += fidsltsa[4] * 3
        optm = optmcca.get(k)
        ori += tsacca.get(k)[1]
        optmgate += optm[4] * 3
        sab = sabremap.get(k)
        sabregate += sab[4] * 3
    print("number of case:", len(tsacca), "ORI: ", ori, "SABRE: ", sabregate, "TSA_num: ", tsagate,
          "GA: ", optmgate, "FiDSL: ", fidslgate)
    print("GA: ", (optmgate - tsagate + 0.0) / optmgate)
    print("SABRE: ", (sabregate - tsagate + 0.0) / sabregate)
    print("FiDSL: ", (fidslgate - tsagate + 0.0) / fidslgate)


def caculateTheAdjustCCA():
    print('_________________________comparison of <*_TSA_cca>______________________')
    fcca = "./results/new/fidslcca"
    fidslcca = read_tabu_files(fcca)
    tcca = "./results/new/tsacca"
    tsacca = read_tabu_files(tcca)
    occa = "./results/new/gacca"
    optmcca = read_tabu_files(occa)
    sabrestr = "./results/new/sabrecca"
    sabremap = read_tabu_files(sabrestr)
    names = list()
    it = tsacca.keys()
    for k in it:
        if fidslcca.get(k) == None:
            names.append(k)
        elif optmcca.get(k) == None:
            names.append(k)
        elif sabremap.get(k) == None:
            names.append(k)
    for i in range(len(names)):
        del tsacca[names[i]]

    tsagate = 0
    optmgate = 0
    fidslgate = 0
    ori = 0
    sabregate = 0
    it = tsacca.keys()
    for k in it:
        tsagate += tsacca.get(k)[4] * 3
        fidsltsa = fidslcca.get(k)
        fidslgate += fidsltsa[4] * 3
        optm = optmcca.get(k)
        ori += tsacca.get(k)[1]
        optmgate += optm[4] * 3
        sab = sabremap.get(k)
        sabregate += sab[4] * 3

    print("number of case: ", len(tsacca), "ORI: ", ori, ", GA: ", optmgate, ", SABRE: ", sabregate,
          ", FiDSL: ", fidslgate, ", TSA_cca: ", tsagate)
    print("(GA-TSA_cca)/GA: ", (optmgate - tsagate + 0.0) / optmgate)
    print("(SABRE-TSA_cca)/SABRE: ", (sabregate - tsagate + 0.0) / sabregate)
    print("(FiDSL-TSA_cca)/FiDSL: ", (fidslgate - tsagate + 0.0) / fidslgate)


def caculateTheAdjustOptm():
    print('_________________________comparison of <*_GA>______________________')
    sabreoptm = "./results/data/optm/sabre_optm"
    sabremap = read_sabre_files(sabreoptm)
    optmStr = "./results/data/optm/total_A_ini_connect"
    optmmap = readOptm(optmStr)
    optmStr1 = "./results/data/optm/GA_num"
    optmmap1 = readOptm(optmStr1)
    tsamap = read_tabu_files1("./results/new/tsa")

    tsagate = 0
    optmgate = 0
    fidslgate = 0
    ori = 0
    count = 0
    sabregate = 0
    it = tsamap.keys()
    for k in it:
        optm = optmmap.get(k)
        optm1 = optmmap1.get(k)
        if optm[2][3] != 9999999 and optm[3][3] != 9999999 and optm1[1][3] != 9999999 and sabremap.get(k)[
            1] != 9999999:
            count += 1
            ori += tsamap.get(k)[1]
            tsagate += optm[3][3] * 3
            fidslgate += optm[2][3] * 3
            optmgate += optm1[1][3] * 3
            sabregate += sabremap.get(k)[2] * 3
    print("number of case: ", count, "ORI: ", ori, ", GA: ", optmgate, ", SABRE: ", sabregate, ", FiDSL: ", fidslgate,
          ", TSA_num: ", tsagate)
    print("(GA-TSA_num)/GA: ", (optmgate - tsagate + 0.0) / optmgate)
    print("(SABRE-TSA_num)/SABRE: ", (sabregate - tsagate + 0.0) / sabregate)
    print("(FiDSL-TSA_num)/FiDSL: ", (fidslgate - tsagate + 0.0) / fidslgate)


def caculateTheAdjustFiDSL():
    print('_________________________comparison of <*_FiDSL>______________________')
    fcca = "./results/data/fidsl/fidsl"
    fidslcca = read_topgraph_files(fcca)
    tcca = "./results/data/fidsl/tsa_fidsl"
    tsacca = read_topgraph_files(tcca)
    occa = "./results/data/fidsl/optm_fidsl"
    optmcca = read_topgraph_files(occa)
    sabre = "./results/data/fidsl/sabre_fidsl"
    sabremap = read_topgraph_files(sabre)
    names = list()
    it = tsacca.keys()
    for k in it:
        if fidslcca.get(k) == None or fidslcca.get(k)[1] == 9999999:
            names.append(k)
        elif optmcca.get(k) == None or optmcca.get(k)[1] == 9999999:
            names.append(k)
        elif sabremap.get(k) == None or sabremap.get(k)[1] == 9999999:
            names.append(k)
    for i in range(len(names)):
        del tsacca[names[i]]
    tsagate = 0
    optmgate = 0
    fidslgate = 0
    ori = 0
    sabregate = 0
    it = tsacca.keys()
    for k in it:
        tsagate += tsacca.get(k)[1] * 3
        fidsltsa = fidslcca.get(k)
        fidslgate += fidsltsa[1] * 3
        optm = optmcca.get(k)
        ori += tsacca.get(k)[1]
        optmgate += optm[1] * 3
        sab = sabremap.get(k)
        sabregate += sab[1] * 3
    print("number of case: ", len(tsacca), "ORI: ",
          ", GA: ", optmgate, ori, ", SABRE: ", sabregate, ", FiDSL: ", fidslgate, ", TSA_num: ", tsagate)
    print("(GA-TSA_num)/GA: ", (optmgate - tsagate + 0.0) / optmgate)
    print("(SABRE-TSA_num)/SABRE: ", (sabregate - tsagate + 0.0) / sabregate)
    print("(FiDSL-TSA_num)/FiDSL: ", (fidslgate - tsagate + 0.0) / fidslgate)


def caculateTheAdjustSABRE():
    print('_________________________comparison of <*_SABRE>______________________')
    fcca = "./results/data/sabre/fidsl_sabre"
    fidslcca = read_sabre_files(fcca)
    tcca = "./results/data/sabre/tsa_sabre"
    tsacca = read_sabre_files(tcca)
    occa = "./results/data/sabre/optm_sabre"
    optmcca = read_sabre_files(occa)
    sabre = "./results/data/sabre/sabre"
    sabremap = read_sabre_files(sabre)
    names = list()
    it = tsacca.keys()
    for k in it:
        if fidslcca.get(k) == None or fidslcca.get(k)[1] == 9999999:
            names.append(k)
        elif optmcca.get(k) == None or optmcca.get(k)[1] == 9999999:
            names.append(k)
        elif sabremap.get(k) == None or sabremap.get(k)[1] == 9999999:
            names.append(k)

    for i in range(len(names)):
        del tsacca[names[i]]
    tsagate = 0
    optmgate = 0
    fidslgate = 0
    ori = 0
    sabregate = 0
    it = tsacca.keys()
    for k in it:
        tsagate += tsacca.get(k)[1]
        fidsltsa = fidslcca.get(k)
        fidslgate += fidsltsa[1]
        optm = optmcca.get(k)
        ori += tsacca.get(k)[0]
        optmgate += optm[1]
        sab = sabremap.get(k)
        sabregate += sab[1]
    print("number of case: ", len(tsacca), "ORI: ", ori,
          ", GA: ", optmgate, ", SABRE: ", sabregate, ", FiDSL: ", fidslgate, ", TSA_num: ", tsagate)
    print("(GA-TSA_num)/GA: ", (optmgate - tsagate + 0.0) / optmgate)
    print("(SABRE-TSA_num)/SABRE: ", (sabregate - tsagate + 0.0) / sabregate)
    print("(FiDSL-TSA_num)/FiDSL: ", (fidslgate - tsagate + 0.0) / fidslgate)


def caculateFiDSL_():
    print('________________comparison of <FiDSL_*>__________________')
    topgraph = "./results/data/fidsl/fidsl"
    fidslmap = read_topgraph_files(topgraph)
    optmStr = "./results/data/optm/total_A_ini_connect"
    optmmap = readOptm(optmStr)
    # optmStr1 = "./results/data/optm/GA_num"
    # optm_result1 = readOptm(optmStr1)
    # optmStr = "./results/data/optm/sabre_optm"
    # optmmap = read_sabre_files(optmStr)

    sabrestr = "./results/data/sabre/fidsl_sabre"
    sabremap = read_sabre_files(sabrestr)
    count = 0
    tsamap = read_tabu_files1("./results/new/fidsltsa")
    ccamap = read_tabu_files1("./results/new/fidslcca")
    names = list()
    it = tsamap.keys()
    for k in it:
        if (optmmap.get(k) == None or optmmap.get(k)[2][3] == 9999999):
            names.append(k)
        if fidslmap.get(k) == None or fidslmap.get(k)[1] == 9999999:
            names.append(k)
        # if optmmap.get(k) == None or optmmap.get(k)[1]==9999999:
        #     names.append(k)
        if sabremap.get(k) == None or sabremap.get(k)[1] == 9999999:
            names.append(k)

    for i in range(len(names)):
        if names[i] in tsamap.keys():
            del tsamap[names[i]]

    ccagate = 0
    tsagate = 0
    optmgate = 0
    fidslgate = 0
    ori = 0
    sabregate = 0
    it = tsamap.keys()
    for k in it:
        tsagate += tsamap.get(k)[4] * 3
        fidslgate += fidslmap.get(k)[1] * 3
        ori += tsamap.get(k)[1]
        optmgate += optmmap.get(k)[2][3] * 3
        ccagate += ccamap.get(k)[4] * 3
        sabregate += sabremap.get(k)[1]
    print("number of case: ", len(tsamap),
          "GA: ", optmgate, "SABRE: ", sabregate, "FiDSL: ", fidslgate, "TSA_num: ", tsagate, ", TSA_cca: ", ccagate)
    print("(GA-TSA_num)/GA: ", (optmgate - tsagate + 0.0) / optmgate)
    print("(SABRE-TSA_num)/SABRE: ", (sabregate - tsagate + 0.0) / sabregate)
    print("(FiDSL-TSA_num)/FiDSL: ", (fidslgate - tsagate + 0.0) / fidslgate)
    print("(TSA_cca-TSA_num)/TSA_cca: ", (ccagate - tsagate + 0.0) / ccagate)


def caculateTSA_():
    print('________________comparison of <TSA_*>__________________')
    topgraph = "./results/data/fidsl/tsa_fidsl"
    fidslmap = read_topgraph_files(topgraph)
    optmStr = "./results/data/optm/total_A_ini_connect"
    optmmap = readOptm(optmStr)

    sabrestr = "./results/data/sabre/tsa_sabre"
    sabremap = read_sabre_files(sabrestr)
    tsamap = read_tabu_files1("./results/new/tsa")
    ccamap = read_tabu_files1("./results/new/tsacca")
    names = list()
    it = tsamap.keys()
    for k in it:
        if (optmmap.get(k) == None or optmmap.get(k)[3][3] - 9999999 == 0):
            names.append(k)
        if fidslmap.get(k) == None or fidslmap.get(k)[1] - 9999999 == 0:
            names.append(k)
        if sabremap.get(k) == None or sabremap.get(k)[1] - 9999999 == 0:
            names.append(k)
    for i in range(len(names)):
        if names[i] in tsamap.keys():
            del tsamap[names[i]]
    ccagate = 0
    tsagate = 0
    optmgate = 0
    fidslgate = 0
    ori = 0
    sabregate = 0
    it = tsamap.keys()
    for k in it:
        tsagate += tsamap.get(k)[4] * 3
        fidslgate += fidslmap.get(k)[1] * 3
        ori += tsamap.get(k)[1]
        optmgate += optmmap.get(k)[3][3] * 3
        ccagate += ccamap.get(k)[4] * 3
        sabregate += sabremap.get(k)[1]
    print("number of case: ", len(tsamap), "ori: ", ori, ", GA: ", optmgate, ", SABRE: ", sabregate,
          ", FiDSL: ", fidslgate, ", TSA_num: ", tsagate, ", TSA_cca: ", ccagate)
    print("(GA-TSA_num)/GA: ", (optmgate - tsagate + 0.0) / optmgate)
    print("(SABRE-TSA_num)/SABRE: ", (sabregate - tsagate + 0.0) / sabregate)
    print("(FiDSL-TSA_num)/FiDSL: ", (fidslgate - tsagate + 0.0) / fidslgate)
    print("(TSA_cca-TSA_num)/TSA_cca: ", (ccagate - tsagate + 0.0) / ccagate)


def caculateOptm_():
    print('________________comparison of <GA_*>__________________')
    topgraph = "./results/data/fidsl/optm_fidsl"
    fidslmap = read_topgraph_files(topgraph)
    optmStr = "./results/data/optm/total_A_ini_connect"
    optmmap = readOptm(optmStr)
    sabrestr = "./results/data/sabre/optm_sabre"
    sabremap = read_sabre_files(sabrestr)
    tsamap = read_tabu_files1("./results/new/gatsa")
    ccamap = read_tabu_files1("./results/new/gacca")
    names = list()
    it = tsamap.keys()
    for k in it:
        if (optmmap.get(k) == None or optmmap.get(k)[1][3] - 9999999 == 0):
            names.append(k)
        if fidslmap.get(k) == None or fidslmap.get(k)[1] - 9999999 == 0:
            names.append(k)
        if sabremap.get(k) == None or sabremap.get(k)[1] - 9999999 == 0:
            names.append(k)
    for i in range(len(names)):
        if names[i] in tsamap.keys():
            del tsamap[names[i]]
    ccagate = 0
    tsagate = 0
    optmgate = 0
    fidslgate = 0
    ori = 0
    sabregate = 0
    it = tsamap.keys()
    for k in it:
        tsagate += tsamap.get(k)[4] * 3
        fidslgate += fidslmap.get(k)[1] * 3
        ori += tsamap.get(k)[1]
        optmgate += optmmap.get(k)[1][3] * 3
        ccagate += ccamap.get(k)[4] * 3
        sabregate += sabremap.get(k)[1]

    print("number of case: ", len(tsamap), "ori: ", ori, ", GA: ", optmgate, ", SABRE: ", sabregate,
          ", FiDSL: ", fidslgate, ", TSA_num: ", tsagate, ", TSA_cca: ", ccagate)
    print("(GA-TSA_num)/GA: ", (optmgate - tsagate + 0.0) / optmgate)
    print("(SABRE-TSA_num)/SABRE: ", (sabregate - tsagate + 0.0) / sabregate)
    print("(FiDSL-TSA_num)/FiDSL: ", (fidslgate - tsagate + 0.0) / fidslgate)
    print("(TSA_cca-TSA_num)/TSA_cca: ", (ccagate - tsagate + 0.0) / ccagate)


def caculateSABRE_():
    print('________________comparison of <SABRE_*>__________________')
    topgraph = "./results/data/fidsl/sabre_fidsl"
    fidslmap = read_topgraph_files(topgraph)
    optmStr = "./results/data/optm/sabre_optm"
    optmmap = read_sabre_files(optmStr)
    sabrestr = "./results/data/sabre/sabre"
    sabremap = read_sabre_files(sabrestr)
    tsamap = read_tabu_files1("./results/new/sabretsa")
    ccamap = read_tabu_files1("./results/new/sabrecca")
    names = list()
    it = tsamap.keys()
    for k in it:
        if (optmmap.get(k) == None or optmmap.get(k)[2] - 9999999 == 0):
            names.append(k)
        if fidslmap.get(k) == None or fidslmap.get(k)[1] - 9999999 == 0:
            names.append(k)
        if sabremap.get(k) == None or sabremap.get(k)[1] - 9999999 == 0:
            names.append(k)
    for i in range(len(names)):
        if names[i] in tsamap.keys():
            del tsamap[names[i]]

    ccagate = 0
    tsagate = 0
    optmgate = 0
    fidslgate = 0
    ori = 0
    sabregate = 0
    it = tsamap.keys()
    for k in it:
        tsagate += tsamap.get(k)[4] * 3
        fidslgate += fidslmap.get(k)[1] * 3
        ori += tsamap.get(k)[1]
        optmgate += optmmap.get(k)[2] * 3
        ccagate += ccamap.get(k)[4] * 3
        sabregate += sabremap.get(k)[1]
    print("number of case: ", len(tsamap), "ori: ", ori,
          ", GA: ", optmgate, ", SABRE: ", sabregate, ", FiDSL: ", fidslgate, ", TSA_num: ", tsagate, ", TSA_cca: ",
          ccagate)
    print("(GA-TSA_num)/GA: ", (optmgate - tsagate + 0.0) / optmgate)
    print("(SABRE-TSA_num)/SABRE: ", (sabregate - tsagate + 0.0) / sabregate)
    print("(FiDSL-TSA_num)/FiDSL: ", (fidslgate - tsagate + 0.0) / fidslgate)
    print("(TSA_cca-TSA_num)/TSA_cca: ", (ccagate - tsagate + 0.0) / ccagate)


def compareSABRE_TSA(sabrepath, tsapath, type):
    sabremap = read_sabre_files(sabrepath)
    tsamap = read_tabu_files1(tsapath)

    greater_top_gql = 0
    greater_gql_top = 0
    eq_gql_top = 0
    gate_top = 0
    gate_gql = 0
    gate_gql_all = 0
    pub_res = 0
    pro_top_gql = 0
    pro_gql_top = 0
    sabretime = 0
    tsatime = 0
    it = tsamap.keys()
    for k in it:
        v1list = tsamap.get(k)
        gate_gql_all += v1list[1]
        if type == 'small':
            if v1list[1] > 100:
                continue
        elif type == 'medium':
            if v1list[1] <= 100 or v1list[1] > 1000:
                continue
        elif type == 'large':
            if v1list[1] <= 1000:
                continue
        if (sabremap.get(k) == None):
            continue
        # // 比较swap个数
        v1 = v1list[4] * 3
        v2 = sabremap.get(k)[1]
        pub_res += 1
        gate_gql += v1
        gate_top += v2
        tsatime += v1list[5]
        sabretime += sabremap.get(k)[2]
        if v1 < v2:
            greater_gql_top += 1
            pro_gql_top += v2 - v1

        elif (v2 < v1):
            # print(k)
            # print(v2 , "  ", v1)
            greater_top_gql += 1
            pro_top_gql += v1 - v2
        else:
            eq_gql_top += 1

    print("number of successful SABRE case：", len(sabremap), ", TSA case：", len(tsamap))
    print("both successful case:", pub_res)
    print("number of gates inserted: SABRE：", gate_top, ", TSA：", gate_gql)
    print("number of case:  SABRE < TSA： ", greater_top_gql, ", TSA < SABRE： ", greater_gql_top, ", equal： ",
          eq_gql_top)
    print("(SABRE-TSA)/SABRE：", (gate_top - gate_gql + 0.0) / gate_top * 100, "% ")
    print('TSA time: %s' % tsatime)


def compareFiDSL_TSA(fidslpath, tsapath, type):
    fidslmap = read_topgraph_files(fidslpath)
    tsamap = read_tabu_files1(tsapath)
    greater_top_gql = 0
    greater_gql_top = 0
    eq_gql_top = 0
    gate_top = 0
    gate_gql = 0
    gate_gql_all = 0
    pub_res = 0
    pro_top_gql = 0
    pro_gql_top = 0
    tsatime = 0
    it = tsamap.keys()
    for k in it:
        v1list = tsamap.get(k)
        if type == 'small':
            if v1list[1] > 100:
                continue
        elif type == 'medium':
            if v1list[1] <= 100 or v1list[1] > 1000:
                continue
        elif type == 'large':
            if v1list[1] <= 1000:
                continue
        if (fidslmap.get(k) == None):
            continue
        # // 比较swap个数
        v1 = v1list[4] * 3
        tsatime += v1list[5]
        v2 = fidslmap.get(k)[1] * 3
        pub_res += 1
        gate_gql += v1
        gate_top += v2
        if v1 < v2:
            greater_gql_top += 1
            pro_gql_top += v2 - v1

        elif (v2 < v1):
            # print(k)
            # print(v2 , "  ", v1)
            greater_top_gql += 1
            pro_top_gql += v1 - v2
        else:
            eq_gql_top += 1

    print("number of successful FiDSL case：", len(fidslmap), ", TSA case：", len(tsamap))
    print("both successful case:", pub_res)
    print("number of gates inserted: FiDSL：", gate_top, " TSA：", gate_gql)
    print("number of case:  FiDSL < TSA： ", greater_top_gql, ", TSA < FiDSL： ", greater_gql_top, ", equal： ",
          eq_gql_top)
    print("(FiDSL-TSA)/FiDSL：", (gate_gql - gate_top + 0.0) / gate_gql * 100, "% ")
    print('TSA time: %s' % tsatime)


def comparenumCCA_TSA(ccapath, tsapath, type='all'):
    ccamap = read_tabu_files1(ccapath)
    tsamap = read_tabu_files1(tsapath)
    greater_top_gql = 0
    greater_gql_top = 0
    eq_gql_top = 0
    gate_top = 0
    gate_gql = 0
    pub_res = 0
    pro_top_gql = 0
    pro_gql_top = 0
    tsatime = 0
    ccatime = 0
    it = tsamap.keys()
    for k in it:
        v1list = tsamap.get(k)
        if type == 'small':
            if v1list[1] > 100:
                continue
        elif type == 'medium':
            if v1list[1] <= 100 or v1list[1] > 1000:
                continue
        elif type == 'large':
            if v1list[1] <= 1000:
                continue
        if ccamap.get(k) == None:
            continue
        # // 比较swap个数
        v1 = v1list[4] * 3
        v2 = ccamap.get(k)[4] * 3
        pub_res += 1
        tsatime += v1list[5]
        ccatime += ccamap.get(k)[5]
        gate_gql += v1
        gate_top += v2
        if v1 < v2:
            greater_gql_top += 1
            pro_gql_top += v2 - v1
        elif (v2 < v1):
            greater_top_gql += 1
            pro_top_gql += v1 - v2
        else:
            eq_gql_top += 1

    print("number of successful TSA_cca case：", len(ccamap), ", TSA_num case：", len(tsamap))
    print("both successful case:", pub_res)
    print("number of gates inserted: TSA_cca：", gate_top, " TSA_num：", gate_gql)
    print("number of case: TSA_cca < TSA_num： ", greater_top_gql, ", TSA_num < TSA_cca： ", greater_gql_top, ", equal： ",
          eq_gql_top)
    print("(TSA_cca-TSA_num)/TSA_cca：", (gate_top - gate_gql + 0.0) / gate_top * 100, "% ")
    print('TSA time: %s,  CCA time: %s' % (tsatime, ccatime))


def comparenumDepth_TSA(depthpath, tsapath):
    depthmap = read_tabu_files1(depthpath)
    tsamap = read_tabu_files1(tsapath)
    greater_top_gql = 0
    greater_gql_top = 0
    eq_gql_top = 0
    gate_top = 0
    gate_gql = 0
    pub_res = 0
    pro_top_gql = 0
    pro_gql_top = 0
    it = tsamap.keys()
    for k in it:
        v1list = tsamap.get(k)
        if depthmap.get(k) == None:
            continue
        # // 比较swap个数
        v1 = v1list[4] * 3
        v2 = depthmap.get(k)[4] * 3
        pub_res += 1
        gate_gql += v1
        gate_top += v2
        if v1 < v2:
            greater_gql_top += 1
            pro_gql_top += v2 - v1
        elif (v2 < v1):
            greater_top_gql += 1
            pro_top_gql += v1 - v2
        else:
            eq_gql_top += 1

    print("number of successful TSA_depth case：", len(depthmap), ", TSA_num case：", len(tsamap))
    print("both successful case:", pub_res)
    print("number of gates inserted: TSA_depth：", gate_top, " TSA_num：", gate_gql)
    print("case:  TSA_depth < TSA_num： ", greater_top_gql, ", TSA_num < TSA_depth： ", greater_gql_top, ", equal： ",
          eq_gql_top)
    print("(TSA_depth-TSA_num)/TSA_depth：", (gate_top - gate_gql + 0.0) / gate_top * 100, "% ")


def comparenumCCA_Depth(ccapath, depthpath):
    ccamap = read_tabu_files1(ccapath)
    depthmap = read_tabu_files1(depthpath)
    greater_top_gql = 0
    greater_gql_top = 0
    eq_gql_top = 0
    gate_top = 0
    gate_gql = 0
    pub_res = 0
    pro_top_gql = 0
    pro_gql_top = 0
    it = depthmap.keys()
    for k in it:
        v1list = depthmap.get(k)
        if ccamap.get(k) == None:
            continue
        # // 比较swap个数
        v1 = v1list[4] * 3
        v2 = ccamap.get(k)[4] * 3
        pub_res += 1
        gate_gql += v1
        gate_top += v2
        if v1 < v2:
            greater_gql_top += 1
            pro_gql_top += v2 - v1
        elif (v2 < v1):
            greater_top_gql += 1
            pro_top_gql += v1 - v2
        else:
            eq_gql_top += 1

    print("number of successful TSA_cca case：", len(ccamap), " TSA_depth case：", len(depthmap))
    print("both successful case:", pub_res)
    print("number of gates inserted: TSA_cca：", gate_top, " TSA_depth：", gate_gql)
    print("case:  TSA_cca < TSA_depth： ", greater_top_gql, ", TSA_depth < TSA_cca： ", greater_gql_top, ", equal： ",
          eq_gql_top)
    print("(TSA_depth-TSA_cca)/TSA_depth：", (gate_gql - gate_top + 0.0) / gate_gql * 100, "% ")


def comparedepthCCA_TSA(ccapath, tsapath, type='all'):
    ccamap = read_tabu_files1(ccapath)
    tsamap = read_tabu_files1(tsapath)
    greater_top_gql = 0
    greater_gql_top = 0
    eq_gql_top = 0
    gate_top = 0
    gate_gql = 0
    pub_res = 0
    pro_top_gql = 0
    pro_gql_top = 0
    tsatime = 0
    ccatime = 0
    it = tsamap.keys()
    for k in it:
        v1list = tsamap.get(k)
        if type == 'small':
            if v1list[1] > 100:
                continue
        elif type == 'medium':
            if v1list[1] <= 100 or v1list[1] > 1000:
                continue
        elif type == 'large':
            if v1list[1] <= 1000:
                continue
        if ccamap.get(k) == None:
            continue
        # // 比较swap个数
        v1 = v1list[3]
        v2 = ccamap.get(k)[3]
        pub_res += 1
        tsatime += v1list[5]
        ccatime += ccamap.get(k)[5]
        gate_gql += v1
        gate_top += v2
        if v1 < v2:
            greater_gql_top += 1
            pro_gql_top += v2 - v1
        elif (v2 < v1):
            greater_top_gql += 1
            pro_top_gql += v1 - v2
        else:
            eq_gql_top += 1

    print("number of successful TSA_cca case：", len(ccamap), ", TSA_num case：", len(tsamap))
    print("both successful case:", pub_res)
    print("depth of gates inserted: TSA_cca：", gate_top, " TSA_num：", gate_gql)
    print("number of case: TSA_cca < TSA_num： ", greater_top_gql, ", TSA_num < TSA_cca： ", greater_gql_top, ", equal： ",
          eq_gql_top)
    print("(TSA_cca-TSA_num)/TSA_cca：", (gate_top - gate_gql + 0.0) / gate_top * 100, "% ")
    print('TSA time: %s,  CCA time: %s' % (tsatime, ccatime))


def comparedepthDepth_TSA(depthpath, tsapath):
    depthmap = read_tabu_files1(depthpath)
    tsamap = read_tabu_files1(tsapath)
    greater_top_gql = 0
    greater_gql_top = 0
    eq_gql_top = 0
    gate_top = 0
    gate_gql = 0
    pub_res = 0
    pro_top_gql = 0
    pro_gql_top = 0
    it = tsamap.keys()
    for k in it:
        v1list = tsamap.get(k)
        if depthmap.get(k) == None:
            continue
        # // 比较swap个数
        v1 = v1list[3]
        v2 = depthmap.get(k)[3]
        pub_res += 1
        gate_gql += v1
        gate_top += v2
        if v1 < v2:
            greater_gql_top += 1
            pro_gql_top += v2 - v1
        elif (v2 < v1):
            greater_top_gql += 1
            pro_top_gql += v1 - v2
        else:
            eq_gql_top += 1

    print("number of successful TSA_depth case：", len(depthmap), ", TSA_num case：", len(tsamap))
    print("both successful case:", pub_res)
    print("depth of gates inserted: TSA_depth：", gate_top, " TSA_num：", gate_gql)
    print("case:  TSA_depth < TSA_num： ", greater_top_gql, ", TSA_num < TSA_depth： ", greater_gql_top, ", equal： ",
          eq_gql_top)
    print("(TSA_depth-TSA_num)/TSA_depth：", (gate_top - gate_gql + 0.0) / gate_top * 100, "% ")


def comparedepthCCA_Depth(ccapath, depthpath):
    ccamap = read_tabu_files1(ccapath)
    depthmap = read_tabu_files1(depthpath)
    greater_top_gql = 0
    greater_gql_top = 0
    eq_gql_top = 0
    gate_top = 0
    gate_gql = 0
    pub_res = 0
    pro_top_gql = 0
    pro_gql_top = 0
    it = depthmap.keys()
    for k in it:
        v1list = depthmap.get(k)
        if ccamap.get(k) == None:
            continue
        # // 比较swap个数
        v1 = v1list[3]
        v2 = ccamap.get(k)[3]
        pub_res += 1
        gate_gql += v1
        gate_top += v2
        if v1 < v2:
            greater_gql_top += 1
            pro_gql_top += v2 - v1
        elif (v2 < v1):
            greater_top_gql += 1
            pro_top_gql += v1 - v2
        else:
            eq_gql_top += 1

    print("number of successful TSA_cca case：", len(ccamap), " TSA_depth case：", len(depthmap))
    print("both successful case:", pub_res)
    print("depth of gates inserted: TSA_cca：", gate_top, " TSA_depth：", gate_gql)
    print("case:  TSA_cca < TSA_depth： ", greater_top_gql, ", TSA_depth < TSA_cca： ", greater_gql_top, ", equal： ",
          eq_gql_top)
    print("(TSA_depth-TSA_cca)/TSA_depth：", (gate_gql - gate_top + 0.0) / gate_gql * 100, "% ")


def compareGA_TSA(gamap, tsamap):
    tsagate = 0
    optmgate = 0
    ori = 0
    count = 0
    tsagreat = 0
    optmgreat = 0
    eq = 0
    it = tsamap.keys()
    for k in it:
        optm = gamap.get(k)
        if optm != None and optm[1][3] != 9999999:
            count += 1
            ori += tsamap.get(k)[1]
            tsagate += tsamap.get(k)[4] * 3
            optmgate += optm[1][3] * 3
            if tsamap.get(k)[4] < optm[1][3]:
                tsagreat += 1
            elif tsamap.get(k)[4] > optm[1][3]:
                optmgreat += 1
            else:
                eq += 1

    print("number of successful FiDSL case：", len(gamap), ", TSA case：", len(tsamap))
    print("both successful case:", count)
    print("case:  GA < TSA： ", optmgreat + ", TSA < GA： ", tsagreat + ", equal： ", eq)
    print("ORI: ", ori, " number of gates inserted: TSA_num: ", tsagate,
          "GA: ", optmgate)
    print("(GA-TSA_num)/GA: ", (tsagate - optmgate + 0.0) / optmgate)


# evaldepth ./results/test/tsa_ccamindepth ./results/test/tsa_depthmindepth ./results/test/tsamindepth

if __name__ == '__main__':

    if sys.argv[1].__eq__('best'):
        if sys.argv[2] != '':
            selectTheBestResultFromFiles(sys.argv[2])
        else:
            print('please input the correct parameters')
    elif sys.argv[1].__eq__('minigate'):
        if sys.argv[2] != '' and sys.argv[3] != '':
            selectTheMinimalGatesFromFiles(sys.argv[2], sys.argv[3])
        else:
            print('please input the correct parameters')
    elif sys.argv[1].__eq__('minidepth'):
        if sys.argv[2] != '' and sys.argv[3] != '':
            selectTheMinimalDepthFromFiles(sys.argv[2], sys.argv[3])
        else:
            print('please input the correct parameters')
    elif sys.argv[1].__eq__('ini'):
        caculateTheAdjustOptm()
        caculateTheAdjustSABRE()
        caculateTheAdjustFiDSL()
        caculateTheAdjustTSA()
        caculateTheAdjustCCA()
    elif sys.argv[1].__eq__('adj'):
        caculateOptm_()
        caculateSABRE_()
        caculateFiDSL_()
        caculateTSA_()
    elif sys.argv[1].__eq__('pairwise'):
        # paiwise type sabre fidsl tsa cca
        #pairwise medium ./results/data/sabre/sabre ./results/data/fidsl/fidsl  ./results/data/tsa/tsa ./results/data/cca/tsa_cca  ./results/qct ./results/new/gatsa
        print("--------------------SABRE VS TSA_num--------------------")
        compareSABRE_TSA(sys.argv[3], sys.argv[5], sys.argv[2])
        print("--------------------FiDSL VS TSA_num--------------------")
        compareFiDSL_TSA(sys.argv[4], sys.argv[5], sys.argv[2])
        print("--------------------TSA_cca VS TSA_num--------------------")
        comparenumCCA_TSA(sys.argv[6], sys.argv[5], sys.argv[2])
    elif sys.argv[1].__eq__('evalnum'):
        # eval cca depth tsa
        print("--------------------TSA_cca VS TSA_num--------------------")
        comparenumCCA_TSA(sys.argv[2], sys.argv[4])
        print("--------------------TSA_depth VS TSA_num--------------------")
        comparenumDepth_TSA(sys.argv[3], sys.argv[4])
        print("--------------------TSA_cca VS TSA_depth--------------------")
        comparenumCCA_Depth(sys.argv[2], sys.argv[3])
    elif sys.argv[1].__eq__('evaldepth'):
        # eval cca depth tsa
        print("--------------------TSA_cca VS TSA_num--------------------")
        comparedepthCCA_TSA(sys.argv[2], sys.argv[4])
        print("--------------------TSA_depth VS TSA_num--------------------")
        comparedepthDepth_TSA(sys.argv[3], sys.argv[4])
        print("--------------------TSA_cca VS TSA_depth--------------------")
        comparedepthCCA_Depth(sys.argv[2], sys.argv[3])
    else:
        print('please input the correct parameters')