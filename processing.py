import sys, os

from base.Level import Level
from base.Translate import Translate
from qct_tools.utils.FileUtils import FileUtils

start_index = 0
end_index = 0
N = 999999


def translate(path, ss, linecount):
    if os.path.isdir(path) or path.endswith('.zip'):
        return
    file = open(path, 'r')
    tower = []
    for k in range(N):
        tower.append(Level(k))
    trans = Translate()
    total_level = trans.translate(tower, file, linecount)
    outpath = 'processed_data/%s.qasm' % (ss)
    print('output to ', outpath)
    outfile = open(outpath, 'w+')
    for j in range(1, total_level + 1):
        p = tower[j].head.next
        while p != None:
            p.printCode(writer=outfile)
            p = p.next
    outfile.close()
    file.close()
    return


def process(start,end):
    path = 'data/'
    files = os.listdir(path)
    for k in range(start,end):
        ss = files[k].split('.')[0]
        current_path = 'data/%s' % (files[k])
        if os.path.isdir(current_path) or current_path.endswith('.zip'):
            continue
        gates = FileUtils.precessReadQasm(current_path, ss)
        print('processing the %d-th file:%s, consisting of %d gates.' % (k, ss, gates))
        if gates < 10000:
            translate(current_path, ss, gates + 50)
    pass


def processingle(path):
    p = path.split('/')
    ss = p[len(p) - 1].split('.')[0]
    current_path = path
    if os.path.isdir(current_path) or current_path.endswith('.zip'):
        print('The path [%s] is invalid!' % path)
        sys.exit(-1)
    gates = FileUtils.precessReadQasm(current_path, ss)
    print('processing file:%s, consisting of %d gates.' % (ss, gates))
    if gates < 10000:
        translate(current_path, ss, gates + 50)

    pass

if __name__ == '__main__':
    if len(sys.argv) == 3:
        start_index = int(sys.argv[1])
        end_index = int(sys.argv[2])
        process(start_index, end_index)
