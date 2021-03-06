"""team39"""
import copy
import random
import time

# possible combinations for winning:
win_rows = [
    # diagonals
    ((0, 0), (1, 1), (2, 2), (3, 3)),
    ((3, 0), (2, 1), (1, 2), (0, 3)),
    # rows
    ((0, 0), (0, 1), (0, 2), (0, 3)),
    ((1, 0), (1, 1), (1, 2), (1, 3)),
    ((2, 0), (2, 1), (2, 2), (2, 3)),
    ((3, 0), (3, 1), (3, 2), (3, 3)),
    # columns
    ((0, 0), (1, 0), (2, 0), (3, 0)),
    ((0, 1), (1, 1), (2, 1), (3, 1)),
    ((0, 2), (1, 2), (2, 2), (3, 2)),
    ((0, 3), (1, 3), (2, 3), (3, 3))
]

block_map = [
    [0, 0, 0, 1, 0, 2, 0, 3, 1, 0, 1, 1, 1, 2, 1, 3, 2, 0, 2, 1, 2, 2, 2, 3, 3, 0, 3, 1, 3, 2, 3, 3],
    [0, 4, 0, 5, 0, 6, 0, 7, 1, 4, 1, 5, 1, 6, 1, 7, 2, 4, 2, 5, 2, 6, 2, 7, 3, 4, 3, 5, 3, 6, 3, 7],
    [0, 8, 0, 9, 0, 10, 0, 11, 1, 8, 1, 9, 1, 10, 1, 11, 2, 8, 2, 9, 2, 10, 2, 11, 3, 8, 3, 9, 3, 10, 3, 11],
    [0, 12, 0, 13, 0, 14, 0, 15, 1, 12, 1, 13, 1, 14, 1, 15, 2, 12, 2, 13, 2, 14, 2, 15, 3, 12, 3, 13, 3, 14, 3, 15],

    [4, 0, 4, 1, 4, 2, 4, 3, 5, 0, 5, 1, 5, 2, 5, 3, 6, 0, 6, 1, 6, 2, 6, 3, 7, 0, 7, 1, 7, 2, 7, 3],
    [4, 4, 4, 5, 4, 6, 4, 7, 5, 4, 5, 5, 5, 6, 5, 7, 6, 4, 6, 5, 6, 6, 6, 7, 7, 4, 7, 5, 7, 6, 7, 7],
    [4, 8, 4, 9, 4, 10, 4, 11, 5, 8, 5, 9, 5, 10, 5, 11, 6, 8, 6, 9, 6, 10, 6, 11, 7, 8, 7, 9, 7, 10, 7, 11],
    [4, 12, 4, 13, 4, 14, 4, 15, 5, 12, 5, 13, 5, 14, 5, 15, 6, 12, 6, 13, 6, 14, 6, 15, 7, 12, 7, 13, 7, 14, 7, 15],

    [8, 0, 8, 1, 8, 2, 8, 3, 9, 0, 9, 1, 9, 2, 9, 3, 10, 0, 10, 1, 10, 2, 10, 3, 11, 0, 11, 1, 11, 2, 11, 3],
    [8, 4, 8, 5, 8, 6, 8, 7, 9, 4, 9, 5, 9, 6, 9, 7, 10, 4, 10, 5, 10, 6, 10, 7, 11, 4, 11, 5, 11, 6, 11, 7],
    [8, 8, 8, 9, 8, 10, 8, 11, 9, 8, 9, 9, 9, 10, 9, 11, 10, 8, 10, 9, 10, 10, 10, 11, 11, 8, 11, 9, 11, 10, 11, 11],
    [8, 12, 8, 13, 8, 14, 8, 15, 9, 12, 9, 13, 9, 14, 9, 15, 10, 12, 10, 13, 10, 14, 10, 15, 11, 12, 11, 13, 11, 14, 11, 15],

    [12, 0, 12, 1, 12, 2, 12, 3, 13, 0, 13, 1, 13, 2, 13, 3, 14, 0, 14, 1, 14, 2, 14, 3, 15, 0, 15, 1, 15, 2, 15, 3],
    [12, 4, 12, 5, 12, 6, 12, 7, 13, 4, 13, 5, 13, 6, 13, 7, 14, 4, 14, 5, 14, 6, 14, 7, 15, 4, 15, 5, 15, 6, 15, 7],
    [12, 8, 12, 9, 12, 10, 12, 11, 13, 8, 13, 9, 13, 10, 13, 11, 14, 8, 14, 9, 14, 10, 14, 11, 15, 8, 15, 9, 15, 10, 15, 11],
    [12, 12, 12, 13, 12, 14, 12, 15, 13, 12, 13, 13, 13, 14, 13, 15, 14, 12, 14, 13, 14, 14, 14, 15, 15, 12, 15, 13, 15, 14, 15, 15]
]

class Player39():
    """AI Bot"""

    def __init__(self):
        "Constructor"
        self.board = []
        self.valid_moves = []
        self.blocks_state = ['-' for i in xrange(16)]

        self.flag = " "
        self.levelincr = 0
        self.moves = 0
        self.depthlimit = 2
        self.good_terminal = False
        self.start = 0

        self.utilwts = [6000, 0, 0, 0, 0, 1500, -1500, 1500, -1500, 710000, -750000, 710000, -750000, 920000, -900000, -10000, 4000, 100000, -100000, 100000, -100000, 130000, -130000]

    def blocks_allowed(self, old_move, blocks_state):

        r = int(old_move[0] % 4)
        c = int(old_move[1] % 4)
        blocknum = r*4 + c;

        if old_move[0] == (-1, -1):
            return [x for x in xrange(16)]
        else:
            r = int(old_move[0] % 4)
            c = int(old_move[1] % 4)
            possblock = r * 4 + c

            if blocks_state[possblock] != '-':
                possblocks = []
                for i in xrange(16):
                    if blocks_state[i] == '-':
                        possblocks.append(i)
                return possblocks

            else:
                return [possblock]

    def cells_allowed(self, tempboard, blocks_allowed, blockstatus):

        p_cells = []
        for block in blocks_allowed:
                v = (int(block / 4)) * 4
                h = (block % 4) * 4
                for i in range(v, v + 4):
                    for j in range(h, h + 4):

                        if tempboard[i][j] == '-':
                            p_cells.append((i, j))

        return p_cells

    def move(self, board, old_move, currflag):

        self.start = time.time()

        self.board = copy.deepcopy(board.board_status)
        tempblockstatus = copy.deepcopy(board.block_status)

        for i in xrange(4):
            for j in xrange(4):
                self.blocks_state[4*i + j] = tempblockstatus[i][j]

        self.flag = currflag
        self.moves += 1

        # prevmove = self.cells_allowed(self.blocks_state, self.blocks_allowed(old_move, self.blocks_state), self.blocks_state)

        prevmove = board.find_valid_move_cells(old_move)
        prevmove = random.choice(prevmove)

        self.levelincr = 0

        while time.time() - self.start <= 14.5:
            bestmove = self.alphabeta(self.board, self.blocks_state, old_move, self.flag, self.levelincr)
            self.levelincr += 1
            if bestmove == "fail":
                # print "TIME:", time.time() - self.start
                # print "PREVMOVE:", prevmove
                if board.check_valid_move(old_move, prevmove):
                    return prevmove
                else:
                    temp = board.find_valid_move_cells(old_move)
                    # print "fail"
                    return random.choice(temp)
            else:
                # print 2 + self.levelincr
                prevmove = bestmove

        # print "TIME:", time.time() - self.start
        # print "PREVMOVE:", prevmove
        if board.check_valid_move(old_move, prevmove):
            return prevmove
        else:
            temp = board.find_valid_move_cells(old_move)
            # print "fail"
            return random.choice(temp)

    def feature_extractor(self, board, blocks_state, flag, old_move):

        cornerblockswon = sideblockswon = centerblockswon = cornerslost = sideslost = centerblockslost = 0
        totalwon = totallost = 0
        freemove = 0

        if self.is_good_terminal(blocks_state) is True:
            return float('inf')

        """Number of corners, sides and center blocks"""
        if flag == 'o':
            counterflag = 'x'
        elif flag == 'x':
            counterflag = 'o'

        for i in xrange(16):
            if i == 0 or i == 3 or i == 12 or i == 15:
                if blocks_state[i] == flag:
                    cornerblockswon += 1
                elif blocks_state[i] == counterflag:
                    cornerslost += 1

            if i == 1 or i == 2 or i == 4 or i == 8 or i == 13 or i == 14 or i == 7 or i == 11:
                if blocks_state[i] == flag:
                    sideblockswon += 1
                elif blocks_state[i] == counterflag:
                    sideslost += 1

            if i == 5 or i == 6 or i == 9 or i == 10:
                if blocks_state[i] == flag:
                    centerblockswon += 1
                elif blocks_state[i] == counterflag:
                    centerblockslost += 1

        totalwon = cornerblockswon + sideblockswon + centerblockswon
        totallost = cornerslost + sideslost + centerblockslost

        """Victory distance"""
        rowwon = []
        rowlost = []
        columnwon = []
        columnlost = []
        diagleftwon = []
        diagleftlost = []
        diagrightwon = []
        diagrightlost = []
        count = countlost = 0
        for i in [0, 1, 2, 3]:
            if blocks_state[i] == flag:
                count += 1
            if blocks_state[i] == counterflag:
                countlost += 1
        rowwon.append(count)
        rowlost.append(countlost)
        count = 0
        countlost = 0
        for i in [4, 5, 6, 7]:
            if blocks_state[i] == flag:
                count += 1
            if blocks_state[i] == counterflag:
                countlost += 1
        rowwon.append(count)
        rowlost.append(countlost)
        count = 0
        countlost = 0
        for i in [8, 9, 10, 11]:
            if blocks_state[i] == flag:
                count += 1
            if blocks_state[i] == counterflag:
                countlost += 1
        rowwon.append(count)
        rowlost.append(countlost)
        count = 0
        countlost = 0
        for i in [12, 13, 14, 15]:
            if blocks_state[i] == flag:
                count += 1
            if blocks_state[i] == counterflag:
                countlost += 1
        rowwon.append(count)
        rowlost.append(countlost)
        count = 0
        countlost = 0
        for i in [0, 4, 8, 12]:
            if blocks_state[i] == flag:
                count += 1
            if blocks_state[i] == counterflag:
                countlost += 1
        columnwon.append(count)
        columnlost.append(countlost)
        count = 0
        countlost = 0
        for i in [1, 5, 9, 13]:
            if blocks_state[i] == flag:
                count += 1
            if blocks_state[i] == counterflag:
                countlost += 1
        columnwon.append(count)
        columnlost.append(countlost)
        count = 0
        countlost = 0
        for i in [2, 6, 10, 14]:
            if blocks_state[i] == flag:
                count += 1
            if blocks_state[i] == counterflag:
                countlost += 1
        columnwon.append(count)
        columnlost.append(countlost)
        count = 0
        countlost = 0
        for i in [3, 7, 11, 15]:
            if blocks_state[i] == flag:
                count += 1
            if blocks_state[i] == counterflag:
                countlost += 1
        columnwon.append(count)
        columnlost.append(countlost)
        count = 0
        countlost = 0
        for i in [0, 5, 10, 15]:
            if blocks_state[i] == flag:
                count += 1
            if blocks_state[i] == counterflag:
                countlost += 1
        diagleftwon.append(count)
        diagleftlost.append(countlost)
        count = 0
        countlost = 0
        for i in [3, 6, 9, 12]:
            if blocks_state[i] == flag:
                count += 1
            if blocks_state[i] == counterflag:
                countlost += 1
        diagrightwon.append(count)
        diagrightlost.append(countlost)
        count = 0
        countlost = 0

        """"Dont make move which lets opponent chose any move"""
        r = int(old_move[0] / 4)
        c = int(old_move[1] / 4)
        if blocks_state[r * 4 + c] == flag or blocks_state[r * 4 + c] == counterflag or blocks_state[r * 4 + c] == 'd':
            freemove = 1

        freedom = 0
        for i in xrange(4):
            if rowlost[i] == 0:
                freedom += 1

        for i in xrange(4):
            if columnlost[i] == 0:
                freedom += 1

        if diagleftlost[0] == 0:
            freedom += 1

        if diagrightlost[0] == 0:
            freedom += 1

        """Cell statistics"""

        blocknow = r * 4 + c

        rowcorner = r * 4
        columncorner = c * 4

        cellrowwin = []
        cellrowlost = []
        cellcolumnwin = []
        cellcolumnlost = []
        celldiagleftwon = []
        celldiagleftlost = []
        celldiagrightwon = []
        celldiagrightlost = []
        count = countlost = 0

        for i in xrange(4):
            for j in xrange(4):
                if board[rowcorner + i][columncorner + j] == flag:
                    count += 1
                if board[rowcorner + i][columncorner + j] == counterflag:
                    countlost += 1
            cellrowwin.append(count)
            cellrowlost.append(countlost)
            count = 0
            countlost = 0

        for i in xrange(4):
            for j in xrange(4):
                if board[rowcorner + j][columncorner + i] == flag:
                    count += 1
                if board[rowcorner + j][columncorner + i] == counterflag:
                    countlost += 1
            cellcolumnwin.append(count)
            cellcolumnlost.append(countlost)
            count = 0
            countlost = 0

        for i in xrange(4):
            if board[rowcorner + i][columncorner + i] == flag:
                count += 1
            if board[rowcorner + i][columncorner + i] == counterflag:
                countlost += 1
        celldiagleftwon.append(count)
        celldiagleftlost.append(countlost)
        count = 0
        countlost = 0

        for i in xrange(4):
            if board[rowcorner + 3 - i][columncorner + i] == flag:
                count += 1
            if board[rowcorner + 3 - i][columncorner + i] == counterflag:
                countlost += 1
        celldiagrightwon.append(count)
        celldiagrightlost.append(countlost)
        count = 0
        countlost = 0

        totalcellrowwin = []
        totalcellrowlost = []
        totalcellcolumnwin = []
        totalcellcolumnlost = []
        totalcelldiagleftwon = []
        totalcelldiagleftlost = []
        totalcelldiagrightwon = []
        totalcelldiagrightlost = []
        totalcount = totalcountlost = 0

        for i in xrange(16):
            r = int(i / 4);
            c = int(i % 4);
            rowcorner = r * 4
            columncorner = c * 4

            for i in xrange(4):
                for j in xrange(4):
                    if board[rowcorner + i][columncorner + j] == flag:
                        totalcount += 1
                    if board[rowcorner + i][columncorner + j] == counterflag:
                        totalcountlost += 1
                totalcellrowwin.append(totalcount)
                totalcellrowlost.append(totalcountlost)
                totalcount = 0
                totalcountlost = 0

            for i in xrange(4):
                for j in xrange(4):
                    if board[rowcorner + j][columncorner + i] == flag:
                        totalcount += 1
                    if board[rowcorner + j][columncorner + i] == counterflag:
                        totalcountlost += 1
                totalcellcolumnwin.append(totalcount)
                totalcellcolumnlost.append(totalcountlost)
                totalcount = 0
                totalcountlost = 0

            for i in xrange(4):
                if board[rowcorner + i][columncorner + i] == flag:
                    totalcount += 1
                if board[rowcorner + i][columncorner + i] == counterflag:
                    totalcountlost += 1
            totalcelldiagleftwon.append(totalcount)
            totalcelldiagleftlost.append(totalcountlost)
            totalcount = 0
            totalcountlost = 0

            for i in xrange(4):
                if board[rowcorner + 3 - i][columncorner + i] == flag:
                    totalcount += 1
                if board[rowcorner + 3 - i][columncorner + i] == counterflag:
                    totalcountlost += 1
            totalcelldiagrightwon.append(totalcount)
            totalcelldiagrightlost.append(totalcountlost)
            totalcount = 0
            totalcountlost = 0

        x1 = (totalwon - totallost) / 9.0 #10.2 ->redundan
        x2 = totalwon / 9.0#5.4 -> redundant
        x3 = totallost / 9.0#-4.8 -> redundant

        x4 = sideblockswon / 8.0#0.4 -> 2
        x5 = sideslost / 8.0 #-0.03 -> -2
        x6 = centerblockswon / 4.0 # 3
        x7 = centerblockslost / 4.0#-4 -> -3
        x8 = cornerblockswon / 4.0#2.2 -> 3
        x9 = cornerslost / 4.0#-1 -> -3

        x10 = (rowwon[0] * rowwon[0] * rowwon[0] + rowwon[1] * rowwon[1] * rowwon[1] + rowwon[2] * rowwon[2] * rowwon[2] + rowwon[3] * rowwon[3] * rowwon[3]) / 81.0 #4.2 -> 4
        x11 = (rowlost[0] * rowlost[0] * rowlost[0]+ rowlost[1] * rowlost[1] * rowlost[1] + rowlost[2] * rowlost[2] * rowlost[2] + rowlost[3] * rowlost[3] * rowlost[3]) / 81.0
        x12 = (columnwon[0] * columnwon[0] * columnwon[0] + columnwon[1] * columnwon[1] * columnwon[1] + columnwon[2] * columnwon[2] * columnwon[2] + columnwon[3] * columnwon[3] * columnwon[3]) / 81.0
        x13 = (columnlost[0] * columnlost[0] * columnlost[0] + columnlost[1] * columnlost[1] * columnlost[1] + columnlost[2] * columnlost[2] * columnlost[2] + columnlost[3] * columnlost[3] * columnlost[3]) / 81.0
        x14 = (diagleftwon[0] * diagleftwon[0] * diagleftwon[0] + diagrightwon[0] * diagrightwon[0] * diagrightwon[0]) / 50 #4
        x15 = (diagleftlost[0] * diagleftlost[0] * diagleftlost[0]+ diagrightlost[0] * diagrightlost[0] * diagrightlost[0]) / 50 #-4

        x16 = freemove #-15
        x17 = (freedom) / 10.0 #0.1 -> 1

        x18 = (sum([x * x for x in cellrowwin])+ sum([x * x for x in totalcellrowwin])) / (27.0 * 16.0) #4.2 -> 4
        x19 = (sum([x * x for x in cellrowlost])+ sum([x * x for x in totalcellrowlost])) / (27.0 * 16.0)
        x20 = (sum([x * x for x in cellcolumnwin])+ sum([x * x for x in totalcellcolumnwin])) / (27.0 * 16.0)
        x21 = (sum([x * x for x in cellcolumnlost])+ sum([x * x for x in totalcellcolumnlost])) / (27.0 * 16.0)
        x22 = ( sum([x * x for x in celldiagleftwon])+ sum([x * x for x in totalcelldiagleftwon]) + sum([x * x for x in celldiagrightwon])+ sum([x * x for x in totalcelldiagrightwon])  ) / (17.0 * 16.0)
        x23 = ( sum([x * x for x in celldiagleftlost])+ sum([x * x for x in totalcelldiagleftlost]) + sum([x * x for x in celldiagrightlost])+ sum([x * x for x in totalcelldiagrightlost])) / (17.0 * 16.0)

        return [x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11,
                x12, x13, x14, x15, x16,
                x17, x18, x19, x20, x21, x22,
                x23]

    def temp(self, board, blocks_state, flag, old_move):
        varlist = self.feature_extractor(board, blocks_state, flag, old_move)
        eval = 0

        for i in xrange(len(self.utilwts)):
            eval += self.utilwts[i] * varlist[i]

        return eval


    def is_good_terminal(self, blocks):
        """Check if a good terminal state is reached."""
        flag = self.flag
        if blocks[0] == blocks[1] == blocks[2] == blocks[3] == flag:
            self.good_terminal = True
            return True
        if blocks[4] == blocks[5] == blocks[6] == blocks[7] == flag:
            self.good_terminal = True
            return True
        if blocks[8] == blocks[9] == blocks[10] == blocks[11] == flag:
            self.good_terminal = True
            return True
        if blocks[12] == blocks[13] == blocks[14] == blocks[15] == flag:
            self.good_terminal = True
            return True

        if blocks[0] == blocks[4] == blocks[8] == blocks[12] == flag:
            self.good_terminal = True
            return True
        if blocks[1] == blocks[5] == blocks[9] == blocks[13] == flag:
            self.good_terminal = True
            return True
        if blocks[2] == blocks[6] == blocks[10] == blocks[14] == flag:
            self.good_terminal = True
            return True
        if blocks[3] == blocks[7] == blocks[11] == blocks[15] == flag:
            self.good_terminal = True
            return True

        if blocks[0] == blocks[5] == blocks[10] == blocks[15] == flag:
            self.good_terminal = True
            return True
        if blocks[3] == blocks[6] == blocks[9] == blocks[12] == flag:
            self.good_terminal = True
            return True

    def is_bad_terminal(self, blocks):
        """Check if a bad terminal state is reached."""
        flag = 'x' if self.flag == 'o' else 'o'

        if blocks[0] == blocks[1] == blocks[2] == blocks[3] == flag:
            return True
        if blocks[4] == blocks[5] == blocks[6] == blocks[7] == flag:
            return True
        if blocks[8] == blocks[9] == blocks[10] == blocks[11] == flag:
            return True
        if blocks[12] == blocks[13] == blocks[14] == blocks[15] == flag:
            return True

        if blocks[0] == blocks[4] == blocks[8] == blocks[12] == flag:
            return True
        if blocks[1] == blocks[5] == blocks[9] == blocks[13] == flag:
            return True
        if blocks[2] == blocks[6] == blocks[10] == blocks[14] == flag:
            return True
        if blocks[3] == blocks[7] == blocks[11] == blocks[15] == flag:
            return True

        if blocks[0] == blocks[5] == blocks[10] == blocks[15] == flag:
            return True
        if blocks[3] == blocks[6] == blocks[9] == blocks[12] == flag:
            return True


    def evolvedblockstate(self, board, old_move, oldblockstate, currflag):

        block_stat = oldblockstate[:]

        if old_move == (-1, -1):
            return block_stat

        blockx = int(old_move[0] / 4)
        blocky = int(old_move[1] / 4)
        block_num = blockx * 4 + blocky
        currblock = block_map[blockx * 4 + blocky]

        #rows
        if board[currblock[0]][currblock[1]] == board[currblock[2]][currblock[3]] == board[currblock[4]][currblock[5]] == board[currblock[6]][currblock[7]] == currflag:
            block_stat[block_num] = currflag
            return block_stat

        if board[currblock[8]][currblock[9]] == board[currblock[10]][currblock[11]] == board[currblock[12]][currblock[13]] == board[currblock[14]][currblock[15]] == currflag:
            block_stat[block_num] = currflag
            return block_stat

        if board[currblock[16]][currblock[17]] == board[currblock[18]][currblock[19]] == board[currblock[20]][currblock[21]] == board[currblock[22]][currblock[23]] == currflag:
            block_stat[block_num] = currflag
            return block_stat

        if board[currblock[24]][currblock[25]] == board[currblock[26]][currblock[27]] == board[currblock[28]][currblock[29]] == board[currblock[30]][currblock[31]] == currflag:
            block_stat[block_num] = currflag
            return block_stat

        #columns
        if board[currblock[0]][currblock[1]] == board[currblock[8]][currblock[9]] == board[currblock[16]][currblock[17]] == board[currblock[24]][currblock[25]] == currflag:
            block_stat[block_num] = currflag
            return block_stat

        if board[currblock[2]][currblock[3]] == board[currblock[10]][currblock[11]] == board[currblock[18]][currblock[19]] == board[currblock[26]][currblock[27]] == currflag:
            block_stat[block_num] = currflag
            return block_stat

        if board[currblock[4]][currblock[5]] == board[currblock[12]][currblock[13]] == board[currblock[20]][currblock[21]] == board[currblock[28]][currblock[29]] == currflag:
            block_stat[block_num] = currflag
            return block_stat

        if board[currblock[6]][currblock[7]] == board[currblock[14]][currblock[15]] == board[currblock[22]][currblock[23]] == board[currblock[30]][currblock[31]] == currflag:
            block_stat[block_num] = currflag
            return block_stat

        #diagonals
        if board[currblock[0]][currblock[1]] == board[currblock[10]][currblock[11]] == board[currblock[20]][currblock[21]] == board[currblock[30]][currblock[31]] == currflag:
            block_stat[block_num] = currflag
            return block_stat

        if board[currblock[6]][currblock[7]] == board[currblock[12]][currblock[13]] == board[currblock[18]][currblock[19]] == board[currblock[24]][currblock[25]] == currflag:
            block_stat[block_num] = currflag
            return block_stat

        for i in range(blockx, blockx + 4):
            for j in range(blocky, blocky + 4):
                if board[i][j] == '-':
                    return block_stat

        block_stat[block_num] = 'D'
        return block_stat

    def alphabeta(self, board, blocks_state, old_move, flag, levelincr):

        if time.time() - self.start >= 14.5:
            return "fail"

        if old_move == (-1, -1):
            return (4, 4)

        playable_cells = self.cells_allowed(board, self.blocks_allowed(old_move, blocks_state), blocks_state)

        if not playable_cells:
            return self.temp(board, blocks_state, flag, old_move)

        alpha = best_score = score = float('-inf')
        beta = float('inf')
        best_move = []

        for move in playable_cells:

            tempblockstate = blocks_state[:]
            board[move[0]][move[1]] = flag
            tempblockstate = self.evolvedblockstate(board, move, blocks_state, flag)

            score = self.alpha_min(board, tempblockstate, move, flag, 0, alpha, beta, levelincr)

            if score == "fail":
                return "fail"

            if time.time() - self.start >= 14.5:
                return "fail"

            board[move[0]][move[1]] = '-'

            if score == best_score:
                best_move.append(move)
            if score > best_score:
                best_score = score
                best_move = [move]

            alpha = max(alpha, best_score)
            if alpha >= beta:
                break

        return best_move[random.randrange(len(best_move))]

    def alpha_max(self, board, blocks_state, old_move, flag, depth, alpha, beta, levelincr):
        if time.time() - self.start >= 14.5:
            return "fail"

        if self.is_bad_terminal(blocks_state) is True:
            return float('-inf')

        if depth > self.depthlimit + levelincr:
            return self.temp(board, blocks_state, flag, old_move)

        playable_cells = self.cells_allowed(board, self.blocks_allowed(old_move, blocks_state), blocks_state)

        if not playable_cells:
            return self.temp(board, blocks_state, flag, old_move)

        best_score = float('-inf')

        nummoves = 0

        for move in playable_cells:
            tempblockst = blocks_state[:]
            board[move[0]][move[1]] = flag
            tempblockst = self.evolvedblockstate(board, move,tempblockst, flag)

            score = self.alpha_min(board, tempblockst, move, flag, depth + 1, alpha, beta, levelincr)

            if score == "fail":
                return "fail"

            if time.time() - self.start >= 14.5:
                return "fail"

            board[move[0]][move[1]] = '-'

            if score > best_score:
                best_score = score

            alpha = max(alpha, best_score)
            if alpha >= beta:
                break

            nummoves += 1

        return best_score

    def alpha_min(self, board, blocks_state, old_move, flag, depth, alpha, beta, levelincr):
        if time.time() - self.start >= 14.5:
            return "fail"

        if self.is_good_terminal(blocks_state) is True:
            return float('inf')

        t_flag = 'o' if flag == 'x' else 'x'

        if depth > self.depthlimit + levelincr:
            return self.temp(board, blocks_state, flag, old_move)

        playable_cells = self.cells_allowed(board, self.blocks_allowed(old_move, blocks_state), blocks_state)

        if not playable_cells:
            return self.temp(board, blocks_state, flag, old_move)

        best_score = float('inf')
        nummoves = 0

        for move in playable_cells:
            temp_blocks_st = blocks_state[:]
            board[move[0]][move[1]] = t_flag
            temp_blocks_st = self.evolvedblockstate(board, move, temp_blocks_st, t_flag)

            score = self.alpha_max(board, temp_blocks_st, move, flag,depth + 1, alpha, beta, levelincr)

            if score == "fail":
                return "fail"

            if time.time() - self.start >= 14.5:
                return "fail"

            board[move[0]][move[1]] = '-'
            if score < best_score:
                best_score = score

            beta = min(beta, best_score)
            if alpha >= beta:
                break

            nummoves += 1

        return best_score
