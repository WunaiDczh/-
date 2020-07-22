import numpy as np
import random


Chessboard_NONE = 0
Chessboard_MAX = 1
Chessboard_MIN = 2
Chessboard_FIVE_TYPE = 1
Chessboard_SFOUR_TYPE = 2
Chessboard_FOUR_TYPE = 3
Chessboard_STHREE_TYPE = 4
Chessboard_THREE_TYPE = 5
Chessboard_STWO_TYPE = 6
Chessboard_TWO_TYPE = 7

#下面是评估时候对于每一种赢法的权重
Chessboard_MAX_VALUE = 100000
Chessboard_MIN_VALUE = -100000
Chessboard_FIVE_W = 100000
Chessboard_FOUR_W = 5000
Chessboard_THREE_W = 1000
Chessboard_TWO_W = 200
Chessboard_ONE_W = 10
Infinity=99999999

class AI(object):
    def __init__(self,rowNum,colNum):
        self.data =  np.zeros((rowNum, colNum), dtype=int)
        self.row = rowNum
        self.column = colNum
        # 赢法数组
        #self.wins = np.zeros((rowNum, colNum,-1), dtype=bool)
        self.wins = [[[] for i in range(colNum)] for j in range(rowNum)]
        # 赢法数
        self.count = 0

        # 横向赢法
        for  i in range(self.row):
            for j in range(self.column-5+1):
                for k in range(5):
                    #self.wins[i][j+k][self.count]=1
                    self.wins[i][j + k].append(self.count)
                self.count+=1
        ##纵向赢法
        for  i in range(self.column):
            for j in range(self.row-5+1):
                for k in range(5):
                    self.wins[j+k][i].append(self.count)
                self.count+=1

        ## 左上到右下的倾斜赢法
        for  i in range(self.row-5+1):
            for j in range(self.column-5+1):
                for k in range(5):
                    self.wins[i+k][j+k].append(self.count)
                self.count+=1

        ##右上到左下的斜线赢法
        for  i in range(self.row-5+1):
            for j in range(self.column-1,3,-1):
                for k in range(5):
                    self.wins[i+k][j-k].append(self.count)
                self.count+=1

        #初始化max和min每一种赢法的下子情况

        # 记录max每一种赢法的已经达成棋子数
        self.maxWin = [{"max":0,"min":0} for i in range(self.count) ]
        # 记录min每一种赢法的已经达成棋子数
        self.minWin = [{"max":0,"min":0} for i in range(self.count) ]


        #下棋记录堆栈
        self.stack = []
        #游戏是否结束
        self.is_ended = False
    def put(self,row,column,type):
        if self.data[row][column] == Chessboard_NONE:
            self.data[row][column] = type
        ##放进记录堆栈
        self.stack.append({"row":row,"column":column,"type":type})

        # 下棋之后对每一种赢法的下棋情况进行更新
        for i in self.wins[row][column]:
            if type == Chessboard_MAX:
                self.maxWin[i]["max"] +=1
                self.minWin[i]["max"] +=1
            else:
                self.minWin[i]["min"] +=1
                self.maxWin[i]["min"]+=1

        # 如果下子满了则结束游戏
        if (self.stack.__len__() == self.row * self.column) :
            self.is_ended = True;
    def rollback(self,n):
        # 记录后退的n步棋子
        for i in range(n):
            step=self.stack.pop()
            row=step["row"]
            column=step["column"]
            type=step["type"]
            # 置空格点
            self.data[row][column] = Chessboard_NONE
            # 更新每一种赢法的下子情况
            for j in self.wins[row][column]:
                if type == Chessboard_MAX:
                    self.maxWin[j]["max"] -=1
                    self.minWin[j]["max"] -=1
                else:
                    self.minWin[j]["min"] -=1
                    self.maxWin[j]["min"] -=1
        self.is_ended = False

    # 该位置是否合法
    def isValid(self,row, column):
        return row >= 0 and row < self.row and column >= 0 and\
               column < self.column and self.data[row][column] == Chessboard_NONE


    def getNearPoints(self,row,column):
        points=[]
        for  i in range(-2,3):
            # 右倾
            r = row + i
            c = column + i
            if self.isValid(r, c):
                points.append({"row": r,"column": c})
            # 左倾
            r = row - i
            c = column + i
            if self.isValid(r, c):
                points.append({"row": r, "column": c})
            # 行
            r = row
            c = column + i
            if self.isValid(r, c):
                points.append({"row": r, "column": c})
            # 列
            r = row+i
            c = column
            if self.isValid(r, c):
                points.append({"row": r, "column": c})
        return points
    def availableSteps(self):
        availableSteps = []
        row = self.row
        column = self.column
        stackLen = self.stack.__len__()

        centerRow = int((row - 1) / 2)
        centerColumn = int((column - 1) / 2)

        #这里就是如果棋盘为空或者（棋盘就一个棋子并且棋盘中心位置为空） 先
        # 向棋盘的中心位置放置棋子
        if (stackLen==0 or (stackLen == 1 and self.data[centerRow][centerColumn] == Chessboard_NONE)):
            availableSteps.append({"row":centerRow,"column":centerColumn})
            return availableSteps
        else:
            # 如果棋盘就一个棋子并且刚好把棋盘中心位置占据了，
            # 那么就在棋盘中心位置附近随机放置一个棋子
            if stackLen == 1:
                nextRow= centerRow + -1 if random() < 0.5 else 1
                nextColumn = centerColumn + -1 if random() < 0.5 else 1
                availableSteps.append({"row": nextRow, "column": nextColumn})
                return availableSteps
            else:
                # 如果棋盘有多个棋子的时候了，那就需要好好查找附近的空置的位子了
                sign = np.zeros((15,15,1),dtype=int)
                for lastPoint in self.stack:
                    nearPoints = self.getNearPoints(lastPoint["row"],lastPoint["column"])
                    for point in nearPoints:
                        row = point["row"]
                        column = point["column"]
                        # 如果这个点之前没添加到availableSteps里面，这次添加到里面
                        # hash对应的也就是为false
                        if sign[row][column]==0:
                            availableSteps.append({"row": row, "column": column})
                            sign[row][column] = 1
                return availableSteps
    def evaluate(self):
        maxW = 0
        minW = 0
        maxGroup = {   "5": 0,
                       "4": 0,
                       "3": 0,
                       "2": 0,
                       "1": 0
                   }
        minGroup = { "5": 0,
            "4": 0,
            "3": 0,
            "2": 0,
            "1": 0
        }
        for  i in range(self.count):
            # 有5个max棋子，min棋子为0
            # 所以已经确定 MAX胜利了，直接返回最大的权重
            if self.maxWin[i]["max"] == 5 and  not self.maxWin[i]["min"]:
                return Chessboard_MAX_VALUE
            # 有5个min棋子，max棋子为0
            #所以已经确定MIN棋子胜利了，直接返回权重
            if self.minWin[i]["min"] == 5 and not self.minWin[i]["max"]:
                return Chessboard_MIN_VALUE

            if self.maxWin[i]["max"] == 4 and not self.maxWin[i]["min"] :
                maxGroup["4"]+=1

            if self.minWin[i]["min"] == 4 and not self.minWin[i]["max"]:
                minGroup["4"]+=1

            if self.maxWin[i]["max"] == 3 and not self.maxWin[i]["min"]:
                maxGroup["3"]+=1

            if self.minWin[i]["min"] == 3 and not self.minWin[i]["max"] :
                minGroup["3"]+=1

            if self.maxWin[i]["max"] == 2 and not self.maxWin[i]["min"] :
                maxGroup["2"]+=1

            if self.minWin[i]["min"] == 2 and not self.minWin[i]["max"] :
                minGroup["2"]+=1

            if self.maxWin[i]["max"] == 1 and not self.maxWin[i]["min"] :
                maxGroup["1"]+=1

            if self.minWin[i]["min"] == 1 and not self.minWin[i]["max"] :
                minGroup["1"]+=1
        maxW = maxGroup["4"] * Chessboard_FOUR_W + maxGroup["3"] * Chessboard_THREE_W + maxGroup["2"] * Chessboard_TWO_W + \
               maxGroup["1"] * Chessboard_ONE_W;
        minW = minGroup["4"] * Chessboard_FOUR_W + minGroup["3"] * Chessboard_THREE_W + minGroup["2"] * Chessboard_TWO_W + \
               minGroup["1"] * Chessboard_ONE_W
        return maxW - minW
    def isMaxWin(self):
        w = self.evaluate()
        return  True if w == Chessboard_MAX_VALUE else False
    def isMinWin(self):
        w = self.evaluate()
        return  True if w == Chessboard_MIN_VALUE  else False

    def end(self):
        self.is_ended=True

    def max(self,depth,beta=Infinity):
        # 记录优势值，应该下棋的位置
        row=-Infinity
        column=-Infinity
        alpha = -Infinity
        if depth == 0:
            alpha = self.evaluate()
            return {"w": alpha}
        else:
            #//获取每一步可以走的方案
            steps = self.availableSteps()
            if (steps.__len__()>0) :
                #对于每一种走法
                for step in steps:
                    #下棋
                    self.put(step["row"], step["column"], Chessboard_MAX)
                    #如果已经赢了，则直接下棋，不再考虑对方下棋
                    if self.isMaxWin():
                        alpha = Chessboard_MAX_VALUE
                        row = step.row
                        column = step.column
                        # 退回上一步下棋
                        self.rollback()
                        break
                    else:
                        #考虑对方depth - 1步下棋之后的优势值，如果对方没棋可下了，
                        # 则返回当前棋盘估值
                        res = self.min(depth - 1,alpha)
                        if(res==None):
                            res["w"]= self.evaluate()

                        #退回上一步下棋
                        self.rollback(1)
                        if res["w"] > alpha:
                            # 选择最大优势的走法
                            alpha = res["w"]
                            row = step["row"]
                            column = step["column"]

                        # 如果人可以获得更好的走法，则AI必然不会选择这一步走法，所以不用再考虑人的其他走法
                        if alpha >= beta:
                        #console.log('MAX节点' + l + '个棋局，剪掉了' + (l - 1 - i) + '个MIN棋局');
                            break
                return  {"w": alpha,"row": row,"column":column}

    def min(self,depth,alpha=-Infinity):
        # 记录优势值，应该下棋的位置

        row=Infinity
        column=Infinity
        beta = Infinity
        if depth == 0:
            beta = self.evaluate()
            return {"w": beta}
        else:
            #获取每一步可以走的方案
            steps = self.availableSteps()
            if (steps.__len__()>0) :
                #对于每一种走法
                for step in steps:
                    #下棋
                    self.put(step["row"], step["column"], Chessboard_MIN)
                    #如果已经赢了，则直接下棋，不再考虑对方下棋
                    if self.isMinWin():
                        beta = Chessboard_MIN_VALUE
                        row = step["row"]
                        column = step["column"]
                        # 退回上一步下棋
                        self.rollback(1)
                        break
                    else:
                        #考虑对方depth - 1步下棋之后的优势值，如果对方没棋可下了，
                        # 则返回当前棋盘估值
                        res = self.max( depth - 1,beta)
                        if(res==None):
                            res["w"]= self.evaluate()

                        #退回上一步下棋
                        self.rollback(1)
                        if res["w"] < beta:
                            # 选择最大优势的走法
                            beta = res["w"]
                            row = step["row"]
                            column = step["column"]

                        # 如果人可以获得更好的走法，则AI必然不会选择这一步走法，所以不用再考虑人的其他走法
                        if beta <= alpha:
                        #console.log('MAX节点' + l + '个棋局，剪掉了' + (l - 1 - i) + '个MIN棋局');
                            break

                return {"w": beta, "row": row, "column": column}
