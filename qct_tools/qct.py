import sys

import time
from queue import Queue

import numpy as np

from base.MySolution import MySolution
from base.NeighborResult import NeighborResult
from base.WriteResult import WriteResult
from qct_tools.TabuSearch import TabuSearch
from qct_tools.utils.FileUtils import FileUtils


class QCT:
    @classmethod
    def improveSearch(self, layers, forw, delta, file_name, graph, dist, tem_locations: list, tem_qubits: list, x,
                      type:int,direc,out_file) -> WriteResult:
        iniWriter = WriteResult()
        locations = tem_locations.copy()
        qubits = tem_qubits.copy()
        in_start = time.time()
        swaps = []
        tabuResultPath = 'results/circuits/%s/improve/%s_%s_%d.qasm' % (direc,
                                                                        out_file,
                                                                        file_name, x)
        resultwriter = open(tabuResultPath, 'w+')
        resultwriter.write('OPENQASM 2.0;\n'
                           'include \"qelib1.inc\";\n'
                           'qreg q[16];\n'
                           'creg c[16];\n')
        ts = TabuSearch(list(), maxIterations=500)
        for d in range(len(layers)):
            all_gates = []
            currentLayers = []
            for s in range(len(layers[d])):
                if layers[d][s].control != -1:
                    currentLayers.append(layers[d][s])
                else:
                    all_gates.append(layers[d][s])
            nextlayers_1 = []
            lookNum = 1
            while lookNum < forw:
                s = 0
                while d + lookNum < len(layers) - 1 and s < len(layers[d + lookNum]):
                    if layers[d + lookNum][s].control != -1:
                        nextlayers_1.append(layers[d + lookNum][s])
                    s += 1
                lookNum += 1
            if len(currentLayers) <= 0:
                self.writeCircuits(all_gates=all_gates, fw=resultwriter)
                continue
            initialSolution = MySolution(graph, dist, locations.copy(), qubits.copy(), currentLayers, nextlayers_1)
            for all_g in all_gates:
                initialSolution.circuits.append(all_g)
            neighborResult = self.buildInstance(graph= graph,currentLayers=currentLayers, dist= dist, qubits=qubits, locations=locations, nextLayers_1=nextlayers_1, parent=initialSolution,type=type,delta=delta)
            solutions = neighborResult.solutions
            if len(solutions) > 0:
                tem_swap = 9999999
                returnValue = initialSolution
                for i in range(len(solutions)):
                    initialSolution = solutions[i]
                    tempValue = ts.run(initialSolution, type, delta)
                    if tempValue == None:
                        self.writeCircuits(initialSolution.circuits, resultwriter)
                        print('no candidate set')
                        return
                    if tem_swap > len(tempValue.swaps):
                        returnValue = tempValue
                        tem_swap = len(tempValue.swaps)
                locations = returnValue.locations
                qubits = returnValue.qubits
                for i in range(len(returnValue.swaps)):
                    swaps.append(returnValue.swaps[i])
                self.writeCircuits(all_gates=returnValue.circuits, fw=resultwriter)
            else:
                self.writeCircuits(all_gates=all_gates, fw = resultwriter)
                self.writeCircuits(all_gates=neighborResult.curr_solved_gates,fw= resultwriter)
                continue
        resultwriter.close()
        in_end = time.time()
        iniWriter.min_index = x
        iniWriter.min_swaps = len(swaps)
        iniWriter.time = in_end - in_start
        return iniWriter

        pass
    @classmethod
    def originalSearch(self, layers, forw, delta, file_name, graph, dist, tem_locations: list, tem_qubits: list, x,
                       type:int,direc,out_file) -> WriteResult:
        iniWriter = WriteResult()
        locations = tem_locations.copy()
        qubits = tem_qubits.copy()
        start = time.time()
        in_start = time.time()
        solutions = []
        swaps = []
        # print('-------start---------')
        tabuResultPath = 'results/circuits/%s/original/%s_%s_%d.qasm' % (direc,
                                                                         out_file,
                                                                         file_name,x)
        resultwriter = open(tabuResultPath, 'w+')
        resultwriter.write('OPENQASM 2.0;\n'
                           'include \"qelib1.inc\";\n'
                           'qreg q[16];\n'
                           'creg c[16];\n')
        ts = TabuSearch(list(), maxIterations=100)
        for d in range(len(layers)):
            # print(d,'=================================================')
            all_gates = []
            currentLayers = []
            for s in range(len(layers[d])):
                if layers[d][s].control != -1:
                    currentLayers.append(layers[d][s])
                else:
                    all_gates.append(layers[d][s])

            nextlayers_1 = []
            lookNum = 1
            while lookNum <= forw:
                s = 0
                while d + lookNum < len(layers) - 1 and s < len(layers[d + lookNum]):
                    if layers[d + lookNum][s].control != -1:
                        nextlayers_1.append(layers[d + lookNum][s])
                    s += 1
                lookNum += 1
            if len(currentLayers) <= 0:
                self.writeCircuits(all_gates=all_gates, fw=resultwriter)
                continue
            initialSolution = MySolution(graph, dist, locations.copy(), qubits.copy(), currentLayers, nextlayers_1)
            for all_g in all_gates:
                initialSolution.circuits.append(all_g)
            neighborResult = self.buildInstance(graph= graph,currentLayers=currentLayers, dist= dist, qubits=qubits, locations=locations, nextLayers_1=nextlayers_1, parent=initialSolution,type=type,delta=delta)
            solutions = neighborResult.solutions
            if len(solutions) > 0:
                initialSolution = solutions[0]
            else:
                self.writeCircuits(all_gates=all_gates, fw= resultwriter)
                self.writeCircuits(all_gates=neighborResult.curr_solved_gates,fw= resultwriter)

                continue
            returnValue = ts.run(initialSolution, type, delta)
            if returnValue == None:
                self.writeCircuits(all_gates=initialSolution.circuits, fw=resultwriter)
                print('no candidates')
            locations = returnValue.locations
            qubits = returnValue.qubits
            # if len(returnValue.swaps)>50:
            #     print(d,'swaps:')
            #     for swa in returnValue.swaps:
            #         print(swa.source, swa.target, end=', ')
            #     print()
            #
            for swa in returnValue.swaps:
                swaps.append(swa)
            self.writeCircuits(all_gates=returnValue.circuits, fw=resultwriter)
        resultwriter.close()
        in_end = time.time()
        iniWriter.min_index = x
        iniWriter.min_swaps = len(swaps)
        iniWriter.time = in_end - in_start

        return iniWriter
    @classmethod
    def writeCircuits(self, all_gates: list, fw):
        for i in all_gates:
            if i.control + 1 == 0:
                if i.type == 'rz':
                    content = '%s(%f) q[%d];\n'%(i.type,i.angle,i.target)
                    fw.write(content)
                else:
                    content = '%s q[%d];\n'%(i.type,i.target)
                    fw.write(content)
                continue
            content = '%s q[%d],q[%d];\n'%(i.type,i.control,i.target)
            fw.write(content)
        fw.flush()
    @classmethod
    def buildInstance(self,graph, currentLayers, dist, qubits, locations, nextLayers_1, parent, type,
                      delta) -> NeighborResult:
        neighborResult = MySolution.computeNeighbor(graph=graph, parent=parent, dist=dist,qubits= qubits, locations=locations, currentLayers1=currentLayers, nextLayers_1=nextLayers_1,
                                                    type=type, delta=delta)
        solutions = neighborResult.solutions
        neighborResult.solutions = sorted(solutions, key=lambda s :(s.score,s.subscore))
        return neighborResult
