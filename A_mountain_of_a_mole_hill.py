# link: https://www.codingame.com/ide/puzzle/a-mountain-of-a-mole-hill

import sys
import queue
from enum import Enum


# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.



class State(Enum):
    Unsure = 1  # no sure yet
    Garden = 2  # sure, it is garden
    Other = 3   # sure, it is other space

class Test:
    ground = []
    graphs = []

    def __init__(self):
        for i in range(16):
            line = input()
            self.ground.append(line)
    
    def _isInBoundary(self, x, y):
        if x < 0 or x > 15 or y < 0 or y > 15:
            return False
        else:
            return True

    def _isFence(self, x, y):
        if self.ground[x][y] in ["+", "-", "|"]:
            return True
        else:
            return False
    
    def _existCommonFence(self, index_graph_1, index_graph_2):
        fences1 = self.graphs[index_graph_1][2]
        fences2 = self.graphs[index_graph_2][2]
        for fence1 in fences1:
            for fence2 in fences2:
                if fence1 == fence2:
                    return True
        return False
    
    def printGraphs(self):
        for graph in self.graphs:
            print("State..." + str(graph[0]), file=sys.stderr, flush=True)
            print("Moles..." + str(graph[1]), file=sys.stderr, flush=True)
            #print("Fences..." + str(graph[2]), file=sys.stderr, flush=True)
            #print("Area..." + str(graph[3]), file=sys.stderr, flush=True)
            pass

    def printGround(self):
        for i in range(16):
            print("Ground..." + str(self.ground[i]), file=sys.stderr, flush=True)
    
    def floodFill(self, x, y):
        state = State.Unsure
        moles = 0
        fences = []
        area = []

        q = queue.Queue()
        q.put([x, y])
        if [x, y] not in area:
            area.append([x, y])
        if self.ground[x][y] == "o":
            moles = moles + 1
        
        while (not q.empty()):
            [xx, yy] = q.get()
            neighbors = [[xx-1,yy-1],[xx-1,yy],[xx-1,yy+1],[xx,yy-1],[xx,yy+1],[xx+1,yy-1],[xx+1,yy],[xx+1,yy+1]]
            for [xx, yy] in neighbors:
                # put neighbors into a queue
                if self._isInBoundary(xx, yy) and [xx, yy] not in area:
                    if not self._isFence(xx, yy):
                        q.put([xx, yy])
                        if [xx, yy] not in area:
                            area.append([xx, yy])
                        if self.ground[xx][yy] == "o":
                            moles = moles + 1
                    else:
                        # record the fence of this area
                        if [xx, yy] not in fences:
                            fences.append([xx, yy])
                # addtional work, mark state as other space
                if not self._isInBoundary(xx, yy) or self.ground[xx][yy] == ".":
                    state = State.Other
        return state, moles, fences, area

    def floodFillAll(self):
        floodedAreas = []
        for i in range(16):
            for j in range(16):
                if self.ground[i][j] == " " or self.ground[i][j] == "o":
                    if [i,j] not in floodedAreas:
                        state, moles, fences, area = self.floodFill(i,j)
                        self.graphs.append([state, moles, fences, area])
                        floodedAreas += area
                        print("floodFill..." + str([i,j]), file=sys.stderr, flush=True)

    def checkGraphs(self):
        q_unsure = queue.Queue()
        index_unsure = 0
        list_of_index_garden = []
        list_of_index_other_space = []

        if all(graph[0] == State.Unsure for graph in self.graphs):
            # if none graph has a asured state, no solution
            return False

        for graph in self.graphs:
            state = graph[0]
            if state == State.Unsure:
                q_unsure.put(index_unsure)
                index_unsure += 1
            elif state == State.Garden:
                list_of_index_garden.append(index_unsure)
                index_unsure += 1
            elif state == State.Other:
                list_of_index_other_space.append(index_unsure)
                index_unsure += 1

        print("Checking..." + str(list(q_unsure.queue)), file=sys.stderr, flush=True)
        qsize = q_unsure.qsize()
        loop_counter = qsize
        while(not q_unsure.empty()):
            index_unsure = q_unsure.get()
            print("Checking..." + str(index_unsure), file=sys.stderr, flush=True)
            if any(self._existCommonFence(index_unsure, index_garden) for index_garden in list_of_index_garden):
                self.graphs[index_unsure][0] = State.Other
                list_of_index_other_space.append(index_unsure)
                print("Modified..." + str(index_unsure) + " State.Other", file=sys.stderr, flush=True)
            elif any(self._existCommonFence(index_unsure, index_other) for index_other in list_of_index_other_space):
                self.graphs[index_unsure][0] = State.Garden
                list_of_index_garden.append(index_unsure)
                print("Modified..." + str(index_unsure) + " State.Garden", file=sys.stderr, flush=True)
            else:
                q_unsure.put(index_unsure)
            
            # avoid infinit loop
            # if after one round pf check, queue size remains the same,
            # there is no need to run another round, no solution
            loop_counter = loop_counter - 1
            if loop_counter == 0:
                new_qsize = q_unsure.qsize()
                if  qsize == new_qsize:
                    # no solution
                    return False
                else:
                    qsize = new_qsize
                    loop_counter = new_qsize
        return True

    def countMolesInGarden(self):
        sum_moles_in_garden = 0
        for graph in iter(self.graphs):
            if graph[0] == State.Garden:
                sum_moles_in_garden += graph[1]
        return sum_moles_in_garden


def doMain():
    t = Test()
    t.printGround()
    t.floodFillAll()
    t.printGraphs()
    res = t.checkGraphs()
    t.printGraphs()
    if res:
        print(t.countMolesInGarden())

if __name__ == '__main__':
    doMain()

# Write an answer using print
# To debug: print("Debug messages...", file=sys.stderr, flush=True)

# print("answer")
