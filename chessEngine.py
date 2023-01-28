from pygame.display import get_allow_screensaver

class Gamestate():
    def __init__(self):

        self.board=[
        ["bR","bN","bB","bQ","bK","bB","bN","bR"],
        ["bp","bp","bp","bp","bp","bp","bp","bp"],
        ["--","--","--","--","--","--","--","--"],
        ["--","--","--","--","--","--","--","--"],
        ["--","--","--","--","--","--","--","--"],
        ["--","--","--","--","--","--","--","--"],  
        ["wp","wp","wp","wp","wp","wp","wp","wp"],
        ["wR","wN","wB","wQ","wK","wB","wN","wR"]]
        
        self.moveFunctions={'p':self.getPawnMoves,'R':self.getRookMoves,'N':self.getKnightMoves,'B':self.getBishopMoves,'Q':self.getQueenMoves,'K':self.getKingMoves}
        
        self.whiteTomove=True
        self.moveLog=[]
       
    #Takes a move as a parameter and executes it    
    def makeMove(self,move):
            self.board[move.startRow][move.startCol]="--"
            self.board[move.endRow][move.endCol]=move.pieceMoved
            self.moveLog.append(move)#log the move so we can undo it later
            self.whiteTomove=not self.whiteTomove#swap player
    
    #undo the ast move made
    def undoMove(self):
        if (len(self.moveLog)!=0):#make sure that there is move to make
            move=self.moveLog.pop()
            self.board[move.startRow][move.startCol]=move.pieceMoved
            self.board[move.endRow][move.endCol]=move.pieceCaptured
            self.whiteTomove=not self.whiteTomove#switch turns back
            
    #all move withconsidering checks
    def getValidMoves(self):
        return self.getallPossibleMoves()
    
    def getallPossibleMoves(self):#generate moves
        moves=[]
        for r in range(len(self.board)):
            for c in range(len(self.board)):
                turn=self.board[r][c][0]#player turn
                if (turn=='w' and self.whiteTomove) or (turn=='b' and not self.whiteTomove):
                    piece=self.board[r][c][1]   
                    self.moveFunctions[piece](r,c,moves)
                    #self.moveFunctions[piece](r,c,moves)
                    
        return moves                   
    #get all the pawn moves for the pawn located at row,col and add those moves to list
    
    def getPawnMoves(self,r,c,moves):
        if self.whiteTomove:#white pawn move
            if self.board[r-1][c]=="--":#square pawn advance
                moves.append(move((r,c),(r-1,c),self.board))
                if(r==6 and self.board[r-2][c]=="--"):#2 square pawn advance
                    moves.append(move((r,c),(r-2,c),self.board))
        
            if c-1 >= 0:#capture to left
                if self.board[r-1][c-1][0]=='b':
                     moves.append(move((r,c),(r-1,c-1),self.board))
            
            if c+1 <= 7:#captures to right
                if self.board[r-1][c+1][0]=="b":
                  moves.append(move((r,c),(r-1,c+1),self.board))
        else:          
           if self.board[r+1][c]=="--":
                moves.append(move((r,c),(r+1,c),self.board))
                if(r==1 and self.board[r+2][c]=="--"):#2 square pawn advance
                    moves.append(move((r,c),(r+2,c),self.board))
            #captures
           if c-1 >= 0:
                if self.board[r+1][c-1][0]=='w':
                     moves.append(move((r,c),(r+1,c-1),self.board))
            
           if c+1 <= 7:#captures to right
                if self.board[r+1][c+1][0]=="w":
                  moves.append(move((r,c),(r+1,c+1),self.board))    
                        
                   
    def getRookMoves(self,r,c,moves):
        direction=((-1,0),(0,-1),(1,0),(0,1))
        enemyColor="b" if self.whiteTomove else "w"
        for d in direction:
            for i in range(1,8):
                endRow=r+d[0] * i
                endCol=c+d[1] * i
                if 0 <= endRow <8 and 0 <= endCol<0:#on board
                   endPiece=self.board[endRow][endCol]
                   if endPiece=="--":#empty space valid
                       moves.append(move((r-c),(endRow,endCol),self.board))
                   elif endPiece[0] == enemyColor:#enemy piece valid
                      move.append(move((r,c),(endRow,endCol),self.board))
                      break
                else:
                  break
              
                    
                   
                       
                        
    
    def getKnightMoves(self,r,c,moves):
       knightMoves=((-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1))
       allyColor="w" if self.whiteTomove else "b"
       for m in knightMoves:
            endRow=r + m[0]
            endCol=c + m[1]
            if 0 <= endRow<8 and 0 <= endCol<8:
                endPiece=self.board[endRow][endCol]
                if endPiece[0]!=allyColor:
                    moves.append(move((r,c),(endRow,endCol),self.board))

                    
           

    def getBishopMoves(self,r,c,moves):
        directions=((-1,-1),(-1,1,),(1,-1),(1,1))
        enemyColor="b" if self.whiteTomove else "w"
        for d in directions:
            for i in range(1,8):
                endRow=r+d[0] *i
                endCol=c+d[1] *i
                if 0<=endRow<8 and 0<=endCol<8:
                    endPiece=self.board[endRow][endCol]
                    if endPiece=="--":
                        moves.append(move((r,c),(endRow,endCol),self.board))
                    elif endPiece==enemyColor:
                         moves.append(move((r,c),(endRow,endCol),self.board))   
                         break
                    else:
                         break 
                else:
                    break

                     
    def getQueenMoves(self,r,c,moves):
        self.getRookMoves(r,c,moves)
        self.getBishopMoves(r,c,moves)

          
    def getKingMoves(self,r,c,moves):
        kingMoves=((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))
        allyColor="w" if self.whiteTomove else "b"
        
        for i in range(8):
            endRow=r+kingMoves[i][0]
            endCol=c+kingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol <8:
                endPiece=self.board[endRow][endCol]
                if endPiece[0]!=allyColor:#not an allay piece (empty or enemy piece)
                    moves.append(move((r,c),(endRow,endCol),self.board))

       
          
class move():
 
 rankTorows= {"1":7,"2":6,"3":5,"4":4,"5":3,"6":2,"7":1,"8":0}
 rowsTorank={v: k for k,v in rankTorows.items()}# dictionary traversal 
 filesTocol={"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7}
 colTofiles={v:k for k , v in filesTocol.items()}
 
    
 def __init__(self,startSq,endSq,board):
    self.startRow=startSq[0]
    self.startCol=startSq[1]
    self.endRow=endSq[0]
    self.endCol=endSq[1]
    
    self.pieceMoved=board[self.startRow][self.startCol]
    self.pieceCaptured=board[self.endRow][self.endCol]
    self.moveID=self.startRow*1000+self.startCol*100 +self.endRow*10+self.endCol#unique to board state
    print(self.moveID)
    #overiding the equals method
 def __eq__(self,other):
        if isinstance(other,move):
            return self.moveID==other.moveID
        return False
 def getchessnotation(self):
     return self.getRankFile(self.startRow,self.startCol)+self.getRankFile(self.endRow,self.endCol)
     
 def getRankFile(self,r,c):
     return self.colTofiles[c]+self.rowsTorank[r]        
    
          

