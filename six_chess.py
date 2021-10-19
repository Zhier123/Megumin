from chess.six.sixforMegumin import *
from receive import rev_msg
from send_message.send_message import send_message
#这一部分负责交互 核心部分负责计算
import json
self_qq = json.load(open("./config.json", encoding='utf-8'))["self_qq"]
def getCommand(userId,groupId):
  while True:
    try:
      rev = rev_msg()
      if "[CQ:at,qq={}]".format(self_qq) in rev["raw_message"]:
        if rev == None:
          continue
        else:
          if(rev["post_type"]=="message"):
            if(rev["sender"]["user_id"]==userId):
              print(rev['raw_message'])
              return rev['raw_message'].split(" ")[1]#将@惠惠的指令进行处理
            elif(rev["sender"]["user_id"]!=userId and rev["group_id"]==groupId):
              send_message("不要指指点点",groupId,"group")
              continue
            else:
              continue
    except:
     continue
def qqShowBoard():
  qqboard="y ********\n"
  for i in range(4):
    qqboard = qqboard+str(i)+" "
    for j in range(4):
      location = getLocationFromXY(j,i)
      if(engine == WHITE):
        location = flipLocation(location)
      piece = board[location]
      if(piece==STONE):
        qqboard =qqboard+"● "
      elif(piece==LEAF):
        qqboard =qqboard+"○ "
      elif(piece==NOPIECE):
        qqboard= qqboard+"╋ "
      else:
        qqboard= qqboard+"  "
    qqboard=qqboard+"\n"
  qqboard=qqboard+"  ********\n"
  qqboard=qqboard+"  0 1 2 3 x\n"
  return qqboard
def GameStart(userId,groupId):
  print("game start with",userId,groupId,sep="_")
  msg=str(userId)+"正在测试中"
  send_message(msg,groupId,"group")
  while True:
    msg="输入q退出 输入d继续"
    send_message(msg,groupId,"group")
    #器具程序的确认阶段
    #进行一次监听
    command = getCommand(userId,groupId)
    print(command)
    while(True):
      if(command == "q" or command =="Q"):
        send_message("quit game",groupId,"group")
        print("确认退出")
        return 
      elif(command == "d" or command == "D"):
        print("确认开始")
        send_message("您是白方",groupId,"group")
        break
      else:
        print("无效指令")
        send_message("无效指令,重新输入",groupId,"")
        command = getCommand(userId,groupId)
    surrend = 0
    global move
    while True:
      if(surrend):
        print("surrend")
        break
      if(isCurrentPlayerDie() and currentPlayer!=engine):
        print("Playerlose")
        send_message("逊",groupId,"group")
        break
      if(isCurrentPlayerDie() and currentPlayer!=engine):
        print("playerwin")
        send_message("勇",groupId,"group")
        break
      send_message(qqShowBoard(),groupId,"group")
      send_message("player's turn,input x1y1x2y2,eg 1312",groupId,"group")
      command = getCommand(userId,groupId)
      if(command == "surrend"):
        surrend =1
        continue
      try:
        command = int(command)
      except:
        send_message("这样下是不对的 Q^Q ",groupId,"group")
        command = 4444
      froX =int(command/1000)
      froY =int(command/100)%10
      toX = int(command/10)%10
      toY =command%10
      fro = getLocationFromXY(froX,froY)
      to = getLocationFromXY(toX,toY)
      move = composeMove(fro,to)
      eatList = eatTable[:]
      while(makeOneMove(move,eatList)==-1):
        print("非法着棋")
        command = getCommand(userId,groupId)
        try:
          command = int(command)
        except:
          send_message("这样下是不对的 Q^Q ",groupId,"group")
          command = 4444
        froX =int(command/1000)
        froY =int(command/100)%10
        toX = int(command/10)%10
        toY =command%10
        fro = getLocationFromXY(froX,froY)
        to = getLocationFromXY(toX,toY)
        move = composeMove(fro,to)
      print(qqShowBoard())
      send_message("你的行动",groupId,"group")
      send_message(qqShowBoard(),groupId,"group")
      if(isCurrentPlayerDie()):
        continue
      print("AI's turn")
      send_message("我的回合！",groupId,"group")
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
      send_message("惠惠行动",groupId,"group")
      