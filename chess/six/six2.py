#我想先做一个六冲棋的移植，在进一步作出国际象棋
from types import GetSetDescriptorType
from typing import Sequence

STONE =3#白色棋子
LEAF  =7#黑色棋子
WHITE =0#白方用0表示
BLACK =1#黑方用1表示
NOPIECE =0#无棋子用0
#棋盘数组(with 开局位置)
board = [
  0,0,0,0,0,0,0,0,
  0,0,0,0,0,0,0,0,
  0,0,7,7,7,7,0,0,
  0,0,7,0,0,7,0,0,
  0,0,3,0,0,3,0,0,
  0,0,3,3,3,3,0,0,
  0,0,0,0,0,0,0,0,
  0,0,0,0,0,0,0,0,
]
inBoard = [
  0,0,0,0,0,0,0,0,
  0,0,0,0,0,0,0,0,
  0,0,1,1,1,1,0,0,
  0,0,1,1,1,1,0,0,
  0,0,1,1,1,1,0,0,
  0,0,1,1,1,1,0,0,
  0,0,0,0,0,0,0,0,
  0,0,0,0,0,0,0,0,
]
#通过location 和 xy坐标互换的函数
def getXFromLocation(location):
  return (location & 7)-2
def getYFromLocation(location):
  return (location>>3)-2
def getLocationFromXY(x,y):
  return (x+2)+(y+2<<3)

#当前执祺人
currentPlayer = 0 #初始执祺人white
def changePlayer():
  global currentPlayer
  currentPlayer = 1 - currentPlayer
  return

#在棋盘上放置一枚(黑/白)棋子
def addPiece(location):
  piece = currentPlayer*4+3 #黑7 白三
  if(inBoard[location]):
    board[location] = piece
  return 
#在棋盘上删除一枚棋子（不用区分黑白）
def delPiece(location):
  if(inBoard[location]):
    board[location] =NOPIECE
  return 
#用一个二字节数字表示走法
#低位表示起点，高位表示终点
def generateMoveFrom(move):
  return move & 255
def generateMoveTo(move):
  return move >> 8
def composeMove(locationFrom,locationTo):
  return locationFrom + locationTo*256
MAX_GEN_MOVES = 32
theMoves=[]
for i in  range(32):
  theMoves.append(-1)#初始化六十四格的数组
movesTable = [-8,8,-1,1]
#生成所有可行走法 ————遍历所有己方棋子以及走法
# 而且 这个小游戏的走法相当简单

def generateAllMoves(movesList):#传入一个moves列表 并将所有的着法传入list中
  genCount =0
  myPiece = currentPlayer * 4+3
  for fro in range(64):
    pieceFrom =board[fro]
    if(pieceFrom!=myPiece):#不是己方棋子
      continue
    for i in range(4):
      to = fro +movesTable[i]
      if(inBoard[to]):
        pieceTo = board[to]
        if(pieceTo == NOPIECE):
          movesList[genCount]=composeMove(fro,to) 
          genCount = genCount +1
  return genCount
eatTable =[]#用于保存吃子位置的数组
for i in range(2):
  eatTable.append(-1)#初始化一次性最多吃两颗
#能走一步棋的函数
    ##吃子检查序列
eatSequence = [[[7,3,3,0],[0,7,3,3]],[[3,7,7,0],[0,3,7,7]]]
#检查吃子 上下下上 左右 右左
def checkEat(to,eatList):
  eatCount = 0
  pieceSequence =[0,0,0,0]#检查吃子时使用
  for i in range(4):
    check =to 
    step = movesTable[i]
    while(inBoard[check]):
      check =check -step#3 && 4通过反向移动焦点然后再正向移动填充seq组的方式测序
    for j in range(4):
      check = check +step
      if(inBoard[check]):
        pieceSequence[j] = board[check]
    while(inBoard[check]):
      check = check-step#5再次网反方向移动    
    for k in range(2):#6.检查序列
      eat = 1 
      for j in range(4):
        if(pieceSequence[j]!=eatSequence[currentPlayer][k][j]):
          eat = 0
      if(eat ==1):
        eatList[eatCount] = check + step*(k+1)
        delPiece(check + step*(k+1))
        eatCount= eatCount +1
  return eatCount#返回吃子数目
##能根据走法走一步棋的函数 需要传入一个走法move

def makeOneMove(move,eatList):
  isLegalMove = 1
  movesList = theMoves[:]#新增一个临时容器相当于 int movesList[32]={-1}
  genCount = generateAllMoves(movesList)
  for i in range(genCount):
    if(movesList[i] == move):
      isLegalMove = 0
      break
  if(isLegalMove == 1):
    return -1####不合法返回-1 以-1为传入的move不和法的返回码,在交互识别时注意反应
  fro = generateMoveFrom(move)
  to = generateMoveTo(move)
  #走一步棋
  delPiece(fro)
  addPiece(to)
  #吃子检查
  eatCount = checkEat(to,eatList)#吃掉被吃的子并且计数
  changePlayer()
  return eatCount#makeMove 返回吃子数>=0
# --局面评估
  #胜负局面评估
def isCurrentPlayerDie():
  movesList = theMoves[:]
  if(generateAllMoves(movesList)):
    return 0
  return 1
  #当前场面评估
  #设定一颗棋子的子力为3，实际情况中子与位置也相关
def evaluatePosition():
  whiteValue = 0
  blackValue =0
  for i in range(64):
    if(board[i] == STONE):
      whiteValue = whiteValue+3
    if(board[i]==LEAF):
      blackValue=blackValue+3
  value = whiteValue - blackValue
  return value
  #子力计算为单纯的子数相加
SEARCH_DEPTH = 2
INFINITY_VALUE = 100
#撤销一步棋的函数
def undoOneMove(move,eatCount,eatList):
  fro=generateMoveFrom(move)
  to =generateMoveTo(move)
  for i in range(eatCount):#吃掉一个子 从eatTable（0）开始回溯 不然会出bug
    addPiece(eatList[i])#根据传入的吃子列表，恢复对方的棋子
  changePlayer()
  delPiece(to)
  addPiece(fro)
  return 
#极小值极大值搜索函数

def MinMaxSearch(depth):
  global bestMove
  movesList = theMoves[:]
  eatList = eatTable[:]#新建的列表 以防止python的缺点
  if(depth == 0):
    return evaluatePosition()
  #初始化最佳 若当前player为黑色1 则初始化最糟糕的情况为正无穷
  #若当前player 为 白色0 则初始化最糟糕的情况为负无穷
  if(currentPlayer):
    bestValue = INFINITY_VALUE
  else:
    bestValue = -INFINITY_VALUE
  genCount = generateAllMoves(movesList)
  for i in range(genCount):
    print("move:",generateMoveFrom(movesList[i]),generateMoveTo(movesList[i]))
    eatCount = makeOneMove(movesList[i],eatList)
    if(eatCount ==-1):
      print("产生了非法落点")
    if(eatCount>=0):
      value = MinMaxSearch(depth-1)
      undoOneMove(movesList[i],eatCount,eatList)
      if(currentPlayer):
        if(value<bestValue):#对于黑方而言越小越好
          bestValue = value
          if(depth == SEARCH_DEPTH):
            bestMove = movesList[i]
      else:
        if(value>bestValue):
          bestValue = value 
          if(depth == SEARCH_DEPTH):
            bestMove = movesList[i]
  if(currentPlayer):
    if(bestValue == INFINITY_VALUE):#没有找到任何解法，GG
      return INFINITY_VALUE - (SEARCH_DEPTH - depth)#能拖一会是一会
  else:
    if(bestValue == -INFINITY_VALUE):
      return (SEARCH_DEPTH - depth)-INFINITY_VALUE
  return bestValue
#让电脑走
def computerThink():
  theDepth = 0
  eatList = eatTable[:]
  MinMaxSearch(SEARCH_DEPTH)
  eatCount = makeOneMove(bestMove,eatList)
  return eatCount -1
###################################################
engine = BLACK
def flipLocation(location):
  location =63-location
  return location
def showBoard():
  print("                    y ********")
  for i in range(4):
    print("                   ",i,end =' ')
    for j in range(4):
      location = getLocationFromXY(j,i)
      if(engine == WHITE):
        location = flipLocation(location)
      piece = board[location]
      if(piece==STONE):
        print("●",end=' ')
      elif(piece == LEAF):
        print("○",end=' ')
      elif(piece == NOPIECE):
        print("╋",end=' ')
      else:
        print(" ",end =' ')
    print(" ")
  print("                      ********")
  print("                      0 1 2 3 x")
  print(board)
  return


showBoard()
while True:
  print("Q退出,D下棋")
  command= input()
  if(command == "Q" or command =="q"):
    print("quit")
    break
  if(command =="D"or command=="d"):
    #默认电脑为黑方
    print("默认您为白方,先手")
    currentPlayer =WHITE
  while True:
    if(isCurrentPlayerDie() and currentPlayer!=engine):
      print("you lose")
      break
    if(isCurrentPlayerDie() and currentPlayer==engine):
      print("you win")
      break
    showBoard()
    print("player's turn,input x1y1x2y2,eg 1213")
    command = int(input())
    froX = int(command/1000)
    froY = int(command/100)%10
    toX =int(command/10)%10
    toY = command%10
    fro = getLocationFromXY(froX,froY)
    to = getLocationFromXY(toX,toY)
    move =composeMove(fro,to)
    eatList = eatTable[:]
    while(makeOneMove(move,eatList)==-1):
      print("非法输入")
      command = int(input())
      froX = int(command/1000)
      froY = int(command/100)%10
      toX =int(command/10)%10
      toY = command%10
      fro = getLocationFromXY(froX,froY)
      to = getLocationFromXY(toX,toY)
      move =composeMove(fro,to)
       #makeonemove时已经切换player
    showBoard()
    if(isCurrentPlayerDie()):
      continue
    print("AI's turn")
    computerThink() 
    print(bestMove)
    move = bestMove
    fro = generateMoveFrom(move)
    to = generateMoveTo(move)
    froX = getXFromLocation(fro)
    froY = getYFromLocation(fro)
    toX = getXFromLocation(to)
    toY = getYFromLocation(to)
    print(froX,froY,toX,toY,sep='')
    