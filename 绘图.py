import numpy as np
from tkinter import *
import tkinter.messagebox
from AI_implication import AI
import _thread


#导入 Tkinter 库  ，python的标准GUI


#五子棋尝试，五子棋默认是黑子优先，本程序没有编写出手顺序的选择功能，所以默认就是人类先手
#人类就是黑子
class Game(object):
    def __init__(self):
        self.ai = AI(15, 15)

        #生成棋盘
        # 棋盘状态数组  0---空格  2---白子电脑  1---黑子玩家
        self.chess = np.zeros((15, 15), dtype=int)
        #iscircle  表示本次落子是不是落的圆圈，即玩家
        #当isAI为True时候，轮到白色棋子落子  即电脑
        self.isAI = True

        ## 实例化Tk类（窗口对象）。Tk类是顶层的控件类，完成窗口的一系列初始化
        self.root = Tk()
        self.root.title('五子棋')
        #调用Tkinter 库 画布控件，生成一个白色背景的 长宽指定的画布
        self.canvas = Canvas(self.root, width=650, height=650, bg="white")
        #使用pack布局，从上到下，从左到右的摆放控件
        self.canvas.pack()
        #在画布上创建一个矩形，使用CA9762颜色填充
        #另外Tkinter中的坐标系也是从左上角开始的
        self.canvas.create_rectangle(25, 25, 625, 625, fill="#CA9762")
        for i in range(1, 16):
            self.canvas.create_line(25, 25 + 40 * (i - 1), 625, 25 + 40 * (i - 1))  # 横线
            self.canvas.create_line(25 + 40 * (i - 1), 25, 25 + 40 * (i - 1), 625)  # 竖线
        #<Button-1>表示鼠标左键单击   绑定到player 函数，表示玩家点击了棋盘某一点后触发函数
        self.canvas.bind("<Button-1>", self.player)
        #主窗口循环
        self.root.mainloop()

    #画圈，i j表示在15*15 棋盘的那个位置画，函数内部完成坐标转换
    def drawBlack(self, i, j):
        x = 25 + 40 * j
        y = 25 + 40 * i
        self.canvas.create_oval(x, y, x+40, y+40 ,fill="#000000 ")

    #画白子，i j表示在15*15 棋盘的那个位置画，函数内部完成坐标转换
    def drawWhite(self, i, j):
        x = 25 + 40 * j
        y = 25 + 40 * i
        self.canvas.create_oval(x, y, x + 40, y + 40, fill="#FFFFFF ")

    # 通过按钮事件来调用play，表示玩家下棋，玩家下完后需要电脑落子了
    # 所以play函数里面还会再调用电脑的下棋函数 self.computer()
    def player(self, event):

        y = event.y
        x = event.x
        if self.isAI and (25 <= x <= 625) and (25 <= y <= 625):
            #确定鼠标左键单击时的坐标对应棋盘几行 几列 ，本次棋盘是15列，i j范围是0 到14
            i = int((y - 25) / 40)
            j = int((x - 25) / 40)
            if not self.ai.is_ended:
                if not self.ai.isValid(i,j):
                    tkinter.messagebox.showerror(title='出错了！', message='请选择空余的格子下棋')
                else:
                    #人下棋
                    self.ai.put(i, j, 1)
                    self.drawBlack(i, j)

                    # 人赢了，结束游戏
                    if self.ai.isMaxWin():
                        self.ai.end()
                        tkinter.messagebox.showerror(title='结束', message='你赢了')

                    else:
                        # 没赢，但平手了
                        if self.ai.is_ended:
                            tkinter.messagebox.showerror(title='结束', message='平手')
                        else:
                            #未分胜负，AI下棋
                            res = self.ai.min(2)
                            #AI下棋
                            self.ai.put(res["row"], res["column"], 2)
                            self.drawWhite(res["row"],res["column"])

                            #AI赢了，结束游戏
                            if self.ai.isMinWin() :
                                self.ai.end();
                                tkinter.messagebox.showerror(title='结束', message='你输了')

                            #没赢，但平手了，否则未分胜负，等待人继续下棋
                            if self.ai.is_ended:
                                tkinter.messagebox.showerror(title='结束', message='平手')






if __name__ == '__main__':

    Game()
