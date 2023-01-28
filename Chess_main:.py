from typing import Sequence
import pygame as p
import chess_engine
WIDTH=HEIGHT=532
DIMENSION=8
SQ_SIZE=HEIGHT//DIMENSION
MAX_FPS=15
IMAGES={}

def load_images():
    pieces=["bp","bR","bN","bB","bK","bQ","wp","wR","wN","wK","wQ","wB"]
    for piece in pieces:
        IMAGES[piece]=p.transform.scale(p.image.load("New/"+piece+".png") ,(SQ_SIZE,SQ_SIZE))
        
def main():
    p.init()
    screen=p.display.set_mode((WIDTH,HEIGHT))
    clock=p.time.Clock()
    screen.fill(p.Color("white"))
    gs=chess_engine.Gamestate()
    validMoves=gs.getValidMoves()
    moveMade=False#flag variable when move is made
    
     
    #print(gs.board)
    load_images()
    running=True
    
    sqSelected=()#no square is selected selected, keep track of last element selected by user
    playerClicks=[]#keep tracks of user clicks
    
    while running:
        for e in p.event.get():
            if (e.type==p.QUIT):
                running=False
            #mouse handlers    
            elif e.type==p.MOUSEBUTTONDOWN:
                location=p.mouse.get_pos()#(x,y) location of the object    
                col=location[0]//SQ_SIZE
                row=location[1]//SQ_SIZE
                if (sqSelected==(row,col)):#user clicked same square twice
                    sqSelected=()
                    playerClicks=[]#clearplayer clicks
                else:    
                 sqSelected=(row,col)    
                 playerClicks.append(sqSelected)
                if (len(playerClicks)==2):#after 2nd clicks
                     move=chess_engine.move(playerClicks[0],playerClicks[1],gs.board)                        
                     print(move.getchessnotation())#generate moves
                     
                     if move in validMoves:
                       gs.makeMove(move)#made mave
                       moveMade=True
                     sqSelected=()#reset user clicks
                     playerClicks=[]
            #key handlers
            elif e.type==p.KEYDOWN:
                if(e.key==p.K_z):#undo when z pressed
                    gs.undoMove()
                    moveMade=True         
                     
        if moveMade:
         validMoves = gs.getValidMoves()
         moveMade=False
                        
        drawgamestate(screen,gs)
        clock.tick(MAX_FPS)
        p.display.flip()        
                
def drawBoard(screen):
  colors=[p.Color("white"),p.Color("gray")]
  for r in range(DIMENSION):
      for c in range(DIMENSION):
          color=colors[((r+c)%2)]
          p.draw.rect(screen,color,p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))

def drawPieces(screen,board):
    for r in range(8):
          for c in range(8):
              piece=board[r][c]
              if  piece != "--" :
                  screen.blit(IMAGES[piece],p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))
            
def drawgamestate(screen,gs):
    drawBoard(screen)
    drawPieces(screen,gs.board)
                  
main() 




