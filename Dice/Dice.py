#
# Dice.py 2022/9/14
#
import pyxel

WINDOW_WIDTH, WINDOW_HEIGHT = 138, 144
BUTTON_NUM = 4
BUTTON_X = [2, 36, 70, 104]
BUTTON_Y = WINDOW_HEIGHT-19
L_PAREN, R_PAREN, EQU, ADD, SUB, MUL, DIV, POW = 10, 11, 12, 13, 14, 15, 16, 17
CALC_MAX_VAL = 12*12*2  # 288
ABC_KEY = (pyxel.KEY_Z, pyxel.KEY_X, pyxel.KEY_C, pyxel.KEY_V)
NUM_KEY = (pyxel.KEY_1, pyxel.KEY_2, pyxel.KEY_3, pyxel.KEY_4)
ARW_KEY = (pyxel.KEY_LEFT, pyxel.KEY_UP, pyxel.KEY_RIGHT, pyxel.KEY_DOWN)
DPAD = (pyxel.GAMEPAD1_BUTTON_DPAD_LEFT, pyxel.GAMEPAD1_BUTTON_DPAD_UP, pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT, pyxel.GAMEPAD1_BUTTON_DPAD_DOWN)
ABXY = (pyxel.GAMEPAD1_BUTTON_Y, pyxel.GAMEPAD1_BUTTON_X, pyxel.GAMEPAD1_BUTTON_A, pyxel.GAMEPAD1_BUTTON_B)
MOUSE_OFF, MOUSE_PUSH, MOUSE_RELEASE = 1, 2, 3
SCORE_LIST = ((500,10,7), (900,8,15), (1200,5,14), (-1,2,9))  # time, score, color 
HOP = (0,0,-1,-2,-3,-4,-5,-6,-7,-7,-8,-8,-9,-9,-9,-8,-8,-7,-7,-6,-5,-4,-3,-2,-1,0,-1,-2,-2,-3,-3,-3,-2,-2,-1,0)
ST_TITLE  = 110
ST_TARGET = 210
ST_3DICE  = 310
ST_CHOICE = 410
ST_ANSWER = 510
ST_RESULT = 610

class App:
    def restart(self):
        self.st_button = [MOUSE_OFF]*BUTTON_NUM
        self.button_str = [[],[],[],[]]
        self.button_val = [0]*BUTTON_NUM
        self.target1, self.target2 = pyxel.rndi(1, 12), pyxel.rndi(1, 12)
        self.dice1, self.dice2, self.dice3 = pyxel.rndi(1, 6), pyxel.rndi(1, 6), pyxel.rndi(1, 6)
        self.str_ans1, self.str_ans2 = [], []
        self.status, self.step = ST_TITLE, 0
        self.score, self.miss = 0, 0
        self.five_operators = True
        pyxel.stop()

    def calc2v(self, val1, val2):
        ans = []
        ans.append([val1+val2, [val1,ADD,val2], True])  # add
        ans.append([val1*val2, [val1,MUL,val2], False])  # mul
        if val1 >= val2:
            ans.append([val1-val2, [val1,SUB,val2], True])  # sub
            if val2 != 0 and val1%val2 == 0:
                ans.append([val1//val2, [val1,DIV,val2], False])  # div
        else:
            ans.append([val2-val1, [val2,SUB,val1], True])  # sub
            if val1 != 0 and val2%val1 == 0:
                ans.append([val2//val1, [val2,DIV,val1], False])  # div
        if self.five_operators:
            ans.append([val1**val2, [val1,POW,val2], False])  # pow
            ans.append([val2**val1, [val2,POW,val1], False])  # pow
        return ans

    def calc3v(self, val1, val2, formula, precedence):
        ans = []
        if val1+val2 < CALC_MAX_VAL:
            ans.append([val1+val2, formula+[ADD,val2,EQU]+self.num2str(val1+val2)])  # add
        if 0< val1*val2 < CALC_MAX_VAL:
            if precedence:
                ans.append([val1*val2, [L_PAREN]+formula+[R_PAREN,MUL,val2,EQU]+self.num2str(val1*val2)])  # mul
            else:
                ans.append([val1*val2, formula+[MUL,val2,EQU]+self.num2str(val1*val2)])  # mul
        if val1 >= val2:
            if 0 < val1-val2 < CALC_MAX_VAL:
                ans.append([val1-val2, formula+[SUB,val2,EQU]+self.num2str(val1-val2)])  # sub
            if val2 != 0 and val1%val2 == 0 and 0 < val1//val2 < CALC_MAX_VAL:
                if precedence:
                    ans.append([val1//val2, [L_PAREN]+formula+[R_PAREN,DIV,val2,EQU]+self.num2str(val1//val2)])  # div
                else:
                    ans.append([val1//val2, formula+[DIV,val2,EQU]+self.num2str(val1//val2)])  # div
        else:
            if val2-val1 < CALC_MAX_VAL:
                ans.append([val2-val1, [val2,SUB,L_PAREN]+formula+[R_PAREN,EQU]+self.num2str(val2-val1)])  # sub
            if val1 != 0 and val2%val1 == 0 and val2//val1 < CALC_MAX_VAL:
                if precedence:
                    ans.append([val2//val1, [val2,DIV,L_PAREN]+formula+[R_PAREN,EQU]+self.num2str(val2//val1)])  # div
                else:
                    ans.append([val2//val1, [val2,DIV]+formula+[EQU]+self.num2str(val2//val1)])  # div
        if self.five_operators:
            if val1<4 or (val1<6 and val2<5) or (val1<10 and val2<4) or (val1<32 and val2<3) or (val1<1000 and val2<2) or val2==0:  # <1000
                if 0< val1**val2 < CALC_MAX_VAL:
                    ans.append([val1**val2, [L_PAREN]+formula+[R_PAREN,POW,val2,EQU]+self.num2str(val1**val2)])  # pow
            if val2<2 or (val2<3 and val1<10) or (val2<4 and val1<7) or (val2<6 and val1<5) or val1<4:  # <1000
                if val2**val1 < CALC_MAX_VAL:
                    ans.append([val2**val1, [val2,POW,L_PAREN]+formula+[R_PAREN,EQU]+self.num2str(val2**val1)])  # pow
        return ans

    def calc(self):  # return : list [value, formula]
        all_ans = []
        ans = self.calc2v(self.dice1, self.dice2)
        for each in ans:
            all_ans.extend(self.calc3v(each[0], self.dice3, each[1], each[2]))
        ans = self.calc2v(self.dice1, self.dice3)
        for each in ans:
            all_ans.extend(self.calc3v(each[0], self.dice2, each[1], each[2]))
        ans = self.calc2v(self.dice2, self.dice3)
        for each in ans:
            all_ans.extend(self.calc3v(each[0], self.dice1, each[1], each[2]))
        return all_ans

    def find_correct(self, all_ans, target_val):
        diff_prev = 1000
        for i, each in enumerate(all_ans):
            diff = each[0]-target_val if each[0]>target_val else target_val-each[0]
            if diff < diff_prev:
                correct_idx = []
                near_big_idx = []
                near_small_idx = []
                correct_val = set()
                diff_prev = diff
            if diff == diff_prev:
                if each[0] == target_val:
                    correct_idx.append(i)
                    correct_val.add(each[0])
                elif each[0] > target_val:
                    near_big_idx.append(i)
                    correct_val.add(each[0])
                else:
                    near_small_idx.append(i)
                    correct_val.add(each[0])
        return correct_idx, near_big_idx, near_small_idx, correct_val

    def make_incorrect(self, all_ans, target_val, correct_val):
        more_val = set()
        less_val = set()
        for i, each in enumerate(all_ans):
            if each[0] < target_val:
                less_val.add(each[0])
            elif each[0] > target_val:
                more_val.add(each[0])
        # print(f'target_val, correct_val : {target_val}, {correct_val}')
        # print(f'all_ans : {sorted(less_val)}, {sorted(more_val)}')
        sort_less = sorted(less_val)
        sort_more = sorted(more_val)
        # print(f'sort_less[-2:], sort_more[:2] : {sort_less[-2:]}, {sort_more[:2]}')
        incorrect_val = {target_val} | set(sort_less[-2:]) | set(sort_more[:2]) 
        p1, p2, m1 = pyxel.rndi(1,3), pyxel.rndi(2,4), pyxel.rndi(1,4)
        incorrect_val |= {target_val+p1} | {target_val+p2}
        if target_val > m1:
            incorrect_val |= {target_val-m1}
        p1, p2, m1 = pyxel.rndi(1,3), pyxel.rndi(2,4), pyxel.rndi(1,4)
        m1 = pyxel.rndi(1,4)
        correct_val_one = list(correct_val)[0]
        incorrect_val |= {correct_val_one+p1} | {correct_val_one+p2}
        if correct_val_one > m1:
            incorrect_val |= {correct_val_one-m1}
        incorrect_val -= correct_val
        # print(f'incorrect_val : {sorted(incorrect_val)}')
        if len(incorrect_val)+len(correct_val) > 4:
            incorrect_val.remove(max(incorrect_val))
        if len(incorrect_val)+len(correct_val) > 4:
            incorrect_val.remove(min(incorrect_val))
        if len(incorrect_val)+len(correct_val) > 4:
            incorrect_val.remove(max(incorrect_val))
        # print(f'incorrect_val : {sorted(incorrect_val)}')
        return incorrect_val

    def push_any(self):
        if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
            return True
        for i in range(BUTTON_NUM):
            if pyxel.btnr(ABC_KEY[i]) or pyxel.btnr(NUM_KEY[i]) or pyxel.btnr(ARW_KEY[i]) or pyxel.btnr(DPAD[i]) or pyxel.btnr(ABXY[i]):
                return True
        return False

    def __init__(self):
        pyxel.init(WINDOW_WIDTH, WINDOW_HEIGHT, title='Dice')
        pyxel.load('assets/Dice.pyxres')
        pyxel.mouse(True)
        self.high_4op, self.high_5op = 10, 10
        self.restart()
        pyxel.run(self.update, self.draw)

    def update(self):
        if self.status == ST_TITLE:
            self.five_operators = not (pyxel.btn(pyxel.KEY_SHIFT) or pyxel.btn(pyxel.MOUSE_BUTTON_RIGHT))
            if self.push_any():
                self.status, self.step = ST_TARGET, 0
        if self.status == ST_TARGET:
            self.step += 1
            if self.step%3 == 0:
                self.target1, self.target2 = pyxel.rndi(1, 12), pyxel.rndi(1, 12)
                # self.target1, self.target2 = 1, 1
            if self.step > 40:
                self.status, self.step = ST_3DICE, 0
        elif self.status == ST_3DICE:
            self.step += 1
            if self.step%3 == 0:
                self.dice1, self.dice2, self.dice3 = pyxel.rndi(1, 6), pyxel.rndi(1, 6), pyxel.rndi(1, 6)
                # self.dice1, self.dice2, self.dice3 = 6, 6, 6
            if self.step > 40:
                all_ans = self.calc()
                cor_idx, big_idx, small_idx, cor_val = self.find_correct(all_ans, self.target1*self.target2)
                incor_idx = self.make_incorrect(all_ans, self.target1*self.target2, cor_val)
                self.button_val = list(cor_val)
                incor_list = list(incor_idx)
                for _ in range(20):
                    p = pyxel.rndi(0, len(incor_list)-1)
                    q = pyxel.rndi(0, len(incor_list)-1)
                    incor_list[p], incor_list[q] = incor_list[q], incor_list[p]
                self.button_val.extend(incor_list[:BUTTON_NUM-len(self.button_val)])
                self.button_val.sort()
                self.button_val.extend([-1]*(BUTTON_NUM-len(self.button_val)))
                self.correct_btn_idx = []
                for i, v in enumerate(self.button_val):
                    self.button_str[i] = self.num2str(v)
                    if v in cor_val:
                        self.correct_btn_idx.append(i)
                self.str_ans1 = []
                self.str_ans2 = []
                if cor_idx:
                    self.str_ans1 = all_ans[cor_idx[pyxel.rndi(0, len(cor_idx)-1)]][1]
                else:
                    if big_idx:
                        self.str_ans1 = all_ans[big_idx[pyxel.rndi(0, len(big_idx)-1)]][1]
                    if small_idx:
                        self.str_ans2 = all_ans[small_idx[pyxel.rndi(0, len(small_idx)-1)]][1]
                self.start_frame = pyxel.frame_count
                self.score_no = 0
                self.status, self.step = ST_CHOICE, 0
        elif self.status == ST_CHOICE:
            f = pyxel.frame_count-self.start_frame
            for i, sl in enumerate(SCORE_LIST):
                if f < sl[0]:
                    self.score_no = i
                    break
            else:
                self.score_no = len(SCORE_LIST)-1
            self.push_button = -1
            for i in range(BUTTON_NUM):
                if BUTTON_X[i]<=pyxel.mouse_x<BUTTON_X[i]+32 and BUTTON_Y<=pyxel.mouse_y<BUTTON_Y+17:
                    if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) or (pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and self.st_button[i]==MOUSE_PUSH):
                        self.st_button[i] = MOUSE_PUSH
                    elif pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT) and self.st_button[i]==MOUSE_PUSH:
                        self.st_button[i] = MOUSE_RELEASE
                        self.push_button = i
                    else:
                        self.st_button[i] = MOUSE_OFF
                else:
                    self.st_button[i] = MOUSE_OFF
                if pyxel.btn(ABC_KEY[i]) or pyxel.btn(NUM_KEY[i]) or pyxel.btn(ARW_KEY[i]) or pyxel.btn(DPAD[i]) or pyxel.btn(ABXY[i]):
                    self.st_button[i] = MOUSE_PUSH
                elif pyxel.btnr(ABC_KEY[i]) or pyxel.btnr(NUM_KEY[i]) or pyxel.btnr(ARW_KEY[i]) or pyxel.btnr(DPAD[i]) or pyxel.btnr(ABXY[i]):
                    self.st_button[i] = MOUSE_RELEASE
                    self.push_button = i
            if 0 <= self.push_button < BUTTON_NUM:
                if self.push_button in self.correct_btn_idx:
                    pyxel.play(0, 0)
                else:
                    pyxel.play(0, 1)
                self.status, self.step = ST_ANSWER, 0
        elif self.status == ST_ANSWER:
            self.step += 1
            if self.step == len(HOP):
                if self.push_button in self.correct_btn_idx:
                    self.score += SCORE_LIST[self.score_no][1]
                    if self.score > 999:
                        self.score = 999
                else:
                    self.miss += 1
                    if self.miss >= 2:
                        if (self.five_operators and self.score > self.high_5op) or (not self.five_operators and self.score > self.high_4op):
                            pyxel.play(0, 3)
                        else:
                            pyxel.play(0, 2)
                self.status, self.step = ST_RESULT, 0
        elif self.status == ST_RESULT:
            if self.push_any():
                if self.miss >= 2:
                    if self.five_operators:
                        if self.score > self.high_5op:
                            self.high_5op = self.score
                    else:
                        if self.score > self.high_4op:
                            self.high_4op = self.score
                    self.restart()
                    self.status, self.step = ST_TITLE, 0
                else:
                    self.status, self.step = ST_TARGET, 0

    def draw_text(self, x, y, f):
        for i, c in enumerate(f):
            pyxel.blt(x+i*9, y, 0, c*8, 96, 8, 10, 0)

    def draw_button(self, ans):
        for i, s in enumerate(self.button_str):
            p = 1 if self.st_button[i]==MOUSE_PUSH else 0
            pyxel.rectb(BUTTON_X[i]+1, BUTTON_Y+1, 31, 16, 1)
            pyxel.rectb(BUTTON_X[i]+p, BUTTON_Y+p, 31, 16, SCORE_LIST[self.score_no][2])
            pyxel.rect( BUTTON_X[i]+1+p, BUTTON_Y+1+p, 29, 14, 5 if ans and i in self.correct_btn_idx else p)
            self.draw_text(BUTTON_X[i]+3+15-len(s)*5+p, BUTTON_Y+3+p, s)

    def num2str(self, n):
        if n < 0 or 1000 <= n:
            return []
        n1 = n//100
        n2 = n//10%10
        n3 = n%10
        if n >= 100:
            return [n1, n2, n3]
        elif n >= 10:
            return [n2, n3]
        else:
            return [n3]

    def draw(self):
        pyxel.cls(3)
        pyxel.rect(0, 0, WINDOW_WIDTH, 7, 0)
        if self.five_operators:
            pyxel.text(4, 1, f'HIGH-SCORE:{self.high_5op:3}', 13 if self.status==ST_RESULT and self.miss>=2 and self.score>self.high_5op else 7)
        else:
            pyxel.text(4, 1, f'4-OP. HIGH:{self.high_4op:3}', 13 if self.status==ST_RESULT and self.miss>=2 and self.score>self.high_4op else 7)
        pyxel.text(68, 1, f'SCORE:{self.score:3}', 10 if self.status in (ST_ANSWER, ST_RESULT) and \
                (self.push_button in self.correct_btn_idx or self.miss>=2) else 7)
        pyxel.text(112, 1, f'MISS:{self.miss}', 10 if self.status in (ST_ANSWER, ST_RESULT) and not self.push_button in self.correct_btn_idx else 7)
        
        pyxel.blt(32, 9, 0, ((self.target1-1)%8)*32, ((self.target1-1)//8)*32, 32, 32, 2)
        pyxel.blt(73, 9, 0, ((self.target2-1)%8)*32, ((self.target2-1)//8)*32, 32, 32, 2)
        self.draw_text(65, 21, [MUL])
        pyxel.rectb(53, 43, 31, 16, 7)
        pyxel.rect( 54, 44, 29, 14, 0)
        s = self.num2str(self.target1*self.target2)
        self.draw_text(56+15-len(s)*5, 46, s)
        
        if self.status in (ST_TITLE, ST_3DICE, ST_CHOICE, ST_ANSWER, ST_RESULT):
            pyxel.blt(21, 61, 0, (self.dice1-1)*32, 64, 32, 32, 2)
            pyxel.blt(53, 61, 0, (self.dice2-1)*32, 64, 32, 32, 2)
            pyxel.blt(85, 61, 0, (self.dice3-1)*32, 64, 32, 32, 2)
        
        if self.status == ST_TITLE:
            pyxel.text(4, 100, 'Using the 6-sided dice, combine', 7)
            pyxel.text(4, 107, 'addition, subtraction, multi-', 7)
            if self.five_operators:
                pyxel.text(4, 114, 'plication, division, and power', 7)
            else:
                pyxel.text(4, 114, 'plication, and division', 7)
                pyxel.text(4, 136, ' - 4 Arithmetic Operations.', 7)
            pyxel.text(4, 121, 'to make the number closest to the', 7)
            pyxel.text(4, 128, 'multiplied by the 12-sided dice.', 7)
        
        if self.status in (ST_CHOICE, ST_ANSWER, ST_RESULT):
            self.draw_button(True if self.status in (ST_ANSWER, ST_RESULT) else False)
        
        if self.status in (ST_ANSWER, ST_RESULT):
            pyxel.rectb(13, 95, 111, 28, 7)
            pyxel.rect( 14, 96, 109, 26, 0)
            if self.str_ans1 and self.str_ans2:
                self.draw_text(19+55-len(self.str_ans1)*5, 98, self.str_ans1)
                self.draw_text(19+55-len(self.str_ans2)*5, 110, self.str_ans2)
            elif self.str_ans1:
                self.draw_text(19+55-len(self.str_ans1)*5, 104, self.str_ans1)
            else:
                self.draw_text(19+55-len(self.str_ans2)*5, 104, self.str_ans2)
            if self.push_button in self.correct_btn_idx:
                pyxel.circb(BUTTON_X[self.push_button]+16, BUTTON_Y+8, 9, 8)
                pyxel.circb(BUTTON_X[self.push_button]+15, BUTTON_Y+8, 9, 8)
            else:
                pyxel.line(BUTTON_X[self.push_button]+7, BUTTON_Y-1, BUTTON_X[self.push_button]+25, BUTTON_Y+17, 8)
                pyxel.line(BUTTON_X[self.push_button]+6, BUTTON_Y-1, BUTTON_X[self.push_button]+24, BUTTON_Y+17, 8)
                pyxel.line(BUTTON_X[self.push_button]+25, BUTTON_Y-1, BUTTON_X[self.push_button]+7, BUTTON_Y+17, 8)
                pyxel.line(BUTTON_X[self.push_button]+24, BUTTON_Y-1, BUTTON_X[self.push_button]+6, BUTTON_Y+17, 8)
            s = f'+{SCORE_LIST[self.score_no][1]}' if self.push_button in self.correct_btn_idx else 'miss' 
            for i in (-1,0,1):
                for j in (-1,0,1):
                    pyxel.text(BUTTON_X[self.push_button]+1+i, BUTTON_Y-6+HOP[self.step]+j, s, 1)
            pyxel.text(BUTTON_X[self.push_button]+1, BUTTON_Y-6+HOP[self.step], s, 10)
        
        if self.status == ST_RESULT and self.miss >= 2:
            if (self.five_operators and self.score > self.high_5op) or (not self.five_operators and self.score > self.high_4op):
                s = 'HIGH SCORE'
                for i in (-1,0,1):
                    for j in (-1,0,1):
                        pyxel.text(49+i, 79+j, s, 1)
                pyxel.text(49, 79, s, 10)
            s = 'GAME OVER'
            for i in (-1,0,1):
                for j in (-1,0,1):
                    pyxel.text(51+i, 88+j, s, 1)
            pyxel.text(51, 88, s, 8)

App()