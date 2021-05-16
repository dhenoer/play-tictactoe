import tkinter as tk

import cv2
import mediapipe as mp
import numpy
import time
import random
import PIL.Image, PIL.ImageTk, PIL.ImageDraw, PIL.ImageFont


class Game:
    '''class Game for tic-tac-toe
    This code is adapted from divyesh072019'''

    computer, human = 'x', 'o'
    board = [
            ['_','_','_'],
            ['_','_','_'],
            ['_','_','_']]

    def __init__(self):
        self.turn = random.choice([self.computer, self.human])
        self.run = False

    def start(self):
        # start / restart game
        self.board = [[ '_' for _ in range(3)] for _ in range(3) ]
        self.run = True
        self.lineWin = [[-1,-1], [-1,-1]]

        #swap player opponent
        self.swap_turn()

    def swap_turn(self):
        self.turn=self.computer if self.turn==self.human else self.human
        #print('You' if self.turn==self.human else 'Computer', 'turn..')

    def play(self,coord=None):

        if self.run:
            result = 'NONE'
            lastTurn = self.turn
            lastCoord = coord

            if coord == None:
                coord = self._findBestMove()

            print('game play on', coord)
            if self._isMovesLeft(coord):
                i,j = coord
                self.board[i][j] = self.turn
                reval = self._evaluate()
                lastCoord = coord

                if reval==10:
                    print('game end, ',self.turn,' wins!')
                    self.run = False
                    result = 'WIN'

                elif self._isMovesLeft():
                    self.swap_turn()
                    result = 'PLAY'

                else:
                    print('game tie!')
                    self.run = False
                    result = 'TIE'

                # print board
                for r in self.board:
                    print(r)

                #if self.turn==self.computer:
                #    self.play()
                return (result, lastCoord, lastTurn, )

            else:
                print('Move invalid')

        return (None, None, None, )


    def _findBestMove(self):
        '''_findBestMove() will return the best possible move for the player.
        Traverse all cells, evaluate minimax function for all empty cells.
        And return the cell with optimal value.
        '''

        bestVal = -1000
        bestMove = (-1, -1)

        random_i = list(range(3))
        random_j = list(range(3))
        random.shuffle(random_i)
        random.shuffle(random_j)

        for i in random_i :	
            for j in random_j :

                # Check if cell is empty
                if (self.board[i][j] == '_') :

                    # Make the move
                    self.board[i][j] = self.turn

                    # compute evaluation function for this
                    # move. depth=0, ismax=False
                    moveVal = self._minimax()

                    # Undo the move
                    self.board[i][j] = '_'

                    # If the value of the current move is
                    # more than the best value, then update
                    # best/
                    if (moveVal > bestVal) :			
                        bestMove = (i, j)
                        bestVal = moveVal

        print("The best move", self.turn,
            "is", bestMove, "with value", bestVal)
        #print()
        return bestMove

    def _minimax(self, depth=0, isMax=False, player=None) :
        '''_minimax() is the minimax function.
        It considers all the possible ways the game can go and returns
        the value of the board
        '''

        player = self.turn if player==None else player
        opponent = self.computer if player==self.human else self.human

        #print('depth=', depth, 'of player', player)

        score = self._evaluate()

        # If Maximizer has won the game return his/her
        # evaluated score
        if (score == 10) :
            return score

        # If Minimizer has won the game return his/her
        # evaluated score
        if (score == -10) :
            return score

        # If there are no more moves and no winner then
        # it is a tie
        if (self._isMovesLeft() == False) :
            return 0

        # If this maximizer's move
        if (isMax) :	
            best = -1000

            # Traverse all cells

            for i in range(3) :		
                for j in range(3) :

                    # Check if cell is empty
                    if (self.board[i][j]=='_') :

                        # Make the move
                        self.board[i][j] = player

                        # Call minimax recursively and choose
                        # the maximum value
                        best = max(best, self._minimax(depth + 1, not isMax, player))

                        # Undo the move
                        self.board[i][j] = '_'
            return best

        # If this minimizer's move
        else :
            best = 1000

            # Traverse all cells
            for i in range(3) :		
                for j in range(3) :

                    # Check if cell is empty
                    if (self.board[i][j] == '_') :

                        # Make the move
                        self.board[i][j] = opponent

                        # Call minimax recursively and choose
                        # the minimum value
                        best = min(best, self._minimax(depth + 1, not isMax, opponent))

                        # Undo the move
                        self.board[i][j] = '_'
            return best


    def _evaluate(self) :
        '''_evaluate() is the evaluation function as discussed
        in the previous article ( http://goo.gl/sJgv68 )
        Checking board for winner'''

        player = self.turn
        opponent = self.computer if player==self.human else self.human

        # Checking for Rows for X or O victory.
        for row in range(3):
            if (self.board[row][0] == self.board[row][1]
            and self.board[row][1] == self.board[row][2]) :	
                if (self.board[row][0] == player) :
                    self.lineWin = [[row, 0], [row,2]]
                    return 10
                elif (self.board[row][0] == opponent) :
                    self.lineWin = [[row, 0], [row,2]]
                    return -10

        # Checking for Columns for X or O victory.
        for col in range(3) :
            if (self.board[0][col] == self.board[1][col]
            and self.board[1][col] == self.board[2][col]) :
                if (self.board[0][col] == player) :
                    self.lineWin = [[0, col], [2,col]]
                    return 10
                elif (self.board[0][col] == opponent) :
                    self.lineWin = [[0, col], [2,col]]
                    return -10

        # Checking for Diagonals for X or O victory.
        if (self.board[0][0] == self.board[1][1]
        and self.board[1][1] == self.board[2][2]) :
            if (self.board[0][0] == player) :
                self.lineWin = [[0, 0], [2,2]]
                return 10
            elif (self.board[0][0] == opponent) :
                self.lineWin = [[0, 0], [2,2]]
                return -10

        if (self.board[0][2] == self.board[1][1]
        and self.board[1][1] == self.board[2][0]) :
            if (self.board[0][2] == player) :
                self.lineWin = [[0, 2], [2,0]]
                return 10
            elif (self.board[0][2] == opponent) :
                self.lineWin = [[0, 2], [2,0]]
                return -10

        # Else if none of them have won then return 0
        return 0

    def _isMovesLeft(self,coord=None):
        '''_isMovesLeft() there are no moves left to play
        or specified coordinate is valid?'''

        if coord==None:
            for i in range(3) :
                for j in range(3) :
                    if (self.board[i][j] == '_') :
                        return True
        else:
            i,j = coord
            if i in range(3):
                if j in range(3):
                    if self.board[i][j] == '_':
                        return True
        return False



class VideoCapture:
    ''' Class VideoCapture
True
    vid: instance for VideoCapture
    '''

    def __init__(self, video_source=0):
        ''' init Video Capture '''

        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            #raise ValueError("Unable to open video source", video_source)
            for i in range(5):
                self.vid = cv2.VideoCapture(i)
                if self.vid.isOpened():
                    break
            else:
                raise ValueError("Unable to open video source", video_source)

        # Command Line Parser
        # args=CommandLineParser().args

        # 2. Video Dimension
        STD_DIMENSIONS =  {
            '480p': (640, 480),
            '720p': (1280, 720),
            '1080p': (1920, 1080),
            '4k': (3840, 2160),
        }
        #res=STD_DIMENSIONS[args.res[0]]
        res=STD_DIMENSIONS['480p']

        #set video sourec width and height
        self.vid.set(3,res[0])
        self.vid.set(4,res[1])

        # Get video source width and height
        self.width,self.height=res


    # To get frames
    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            frame = cv2.flip(frame, 1)
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
            else:
                return (ret, None)
        else:
            return (ret, None)

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
            cv2.destroyAllWindows()


class App:
    ''' Application Class

    # vid: instance of VideoCapture
    # video_source: video port number. try 0, 1, 2 and so on

    # face: instance of Face

    # game: instance of Game


    # window: instance of root window
    # timer = 0
    # canvas: instance of canvas widget
    # btn_start: widget of button to start game
    # btn_quit: widget of button to end the application
    # delay = 10
    '''

    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)

        self.video_source = video_source
        self.hands = mp.solutions.hands.Hands()

        self.board = PIL.Image.open('grid9-alpha.png')
        self.xplay = PIL.Image.open('x-alpha.png')
        self.oplay = PIL.Image.open('o-alpha.png')
        self.font = PIL.ImageFont.truetype('ZillaSlabHighlight-Bold.ttf', 30)

        self.fingertip = {'coord':(-1,-1), 'count':0}
        self.message = 'Click [START] to play Tic-Tac-Toe'

        # open video source (by default this will try to open the computer webcam)
        self.vid = VideoCapture(self.video_source)

        self.game = Game()
        #self.game.start()

        frame1 = tk.Frame(window)

        # control start of game
        self.btn_start = tk.Button(frame1, text='START', command=self.game_start)
        self.btn_start.pack(side=tk.LEFT)

        # control play
        #self.btn_play = tk.Button(frame1, text='PLAY', command=self.game_play)
        #self.btn_play.pack(side=tk.LEFT)

        # quit button
        self.btn_quit = tk.Button(frame1, text='QUIT', command=quit)
        self.btn_quit.pack(side=tk.LEFT)

        frame1.pack()

        # Create a canvas that can fit the above video source size
        self.canvas = tk.Canvas(window, width = self.vid.width, height = self.vid.height)
        self.canvas.pack()#side=tk.LEFT)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 10

        self.update()
        self.window.mainloop()

    def game_role(self, tip=None):
        if self.game.turn == self.game.computer:
            self.game_play()
        elif self.game.turn == self.game.human and tip:
            #print('tip', tip)
            if self.fingertip['coord'] == tip:
                delta = time.perf_counter() - self.fingertip['count']
                #print('increment in', tip, 'delta', delta)
                if  delta > 1.5:
                    #print('play on', tip)
                    self.game_play(tip)
            else:
                #print('init in ', tip)
                self.fingertip['coord'] = tip
                self.fingertip['count'] = time.perf_counter()

    def game_start(self):
        self.game.start()
        self.board = PIL.Image.open('grid9-alpha.png')
        if self.game.turn == self.game.human:
            self.message = 'Your turn by pointing index finger'
        else:
            self.message = ''
        #self.game.level = 'smile'

    def game_play(self, tip=None):
        status, lastCoord, lastTurn = self.game.play(tip)
        if status in ['PLAY', 'WIN', 'TIE']:
            button = self.oplay if lastTurn==self.game.human else self.xplay
            i,j = lastCoord
            self.board.paste(button, (10+j*68,10+i*68), button)
            if lastTurn==self.game.computer:
                self.message = 'Your turn by pointing index finger'
            else:
                self.message = ''

        if status=='TIE':
            self.message = 'Game ties!'

        if status=='WIN':
            print('Win')
            player = 'You' if lastTurn==self.game.human else 'Computer'
            self.message = '{} win!'.format(player)
            lineWin = []
            colorWin = (255,0,0) if lastTurn==self.game.computer else (0,0,255)
            for c in self.game.lineWin:
                lineWin.append((50+c[1]*68, 50+c[0]*68))
            draw = PIL.ImageDraw.Draw(self.board)
            draw.line(tuple(lineWin), width=15, fill=colorWin, joint='curve')


    # update frame display
    def update(self):

        ret, frame = self.vid.get_frame()

        results = self.hands.process(frame)
        #print(results.multi_hand_landmarks)

        topleft_board = (frame.shape[1]-300, 50)

        h, w, c = frame.shape
        tip = None
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                # tips and middle
                for id in [8, 4,20]:
                    lm = handLms.landmark[8]
                    # print(id)
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    cv2.circle(frame, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

                    if id==8:
                        tip0 = int(((cy-topleft_board[0])/self.board.height) // 0.334)
                        tip1 = int(((cx-topleft_board[1])/self.board.width) // 0.334)
                        tip = [tip0+4, tip1-4]

                break

        self.game_role(tip)

        pil_image = PIL.Image.fromarray(frame)
        pil_image.paste(self.board, topleft_board, self.board)

        draw = PIL.ImageDraw.Draw(pil_image)
        if time.time() % 3 < 2:
            draw.text((20,5), self.message,
                (255,0,0) if self.game.turn==self.game.computer else (0,0,255),
                font=self.font)

        self.photo = PIL.ImageTk.PhotoImage(image = pil_image)
        self.canvas.create_image(0, 0, image = self.photo, anchor = tk.NW)

        self.window.after(self.delay,self.update)


if __name__ == '__main__':
    # Create a window and pass it to the Application object
    App(tk.Tk(),'Game Tic-Tac-Toe')