# coding: UTF-8
"""
Created on 2020/9/20

@author: Mark Hsu
"""
import random


class Game:
    ans = ""
    pool = []

    def __init__(self):
        for i in range(10):
            self.pool.append(i)
        for i in range(4):
            self.ans += str(self.pool.pop(random.randint(0, len(self.pool) - 1)))

    @staticmethod
    def is_illegal(_guess):
        if len(_guess) != 4:
            return True
        for x in _guess:
            if _guess.find(x) != _guess.rfind(x):
                return True
        return False

    def guess(self, _guess):
        if self.is_illegal(_guess):
            return "It's a illegal guess. Please enter four unique digits, e.g., 0123."
        if _guess == self.ans:
            return "BINGO"
        a = 0
        b = 0
        for x, ans_i in zip(_guess, self.ans):
            if x == ans_i:
                a += 1
            elif x in self.ans:
                b += 1
        return str(a) + "A" + str(b) + "B"


if __name__ == '__main__':
    g = Game()
    print("The answer is:", g.ans)
    s = ""
    while s != 'BINGO':
        rs = input("Guess a number: ")
        s = g.guess(rs)
        print(s)
