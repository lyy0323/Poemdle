import random
from typing import Union


# config
key_word = '青'


class Wordle:
    def __init__(self, pool_id=None, from_dict: Union[None, dict] = None):
        self.key_word = key_word
        if not from_dict:
            self.current = None
            self.historic = []
            self.need_solve = True
            pool = open(f'./pool_{key_word}.csv', encoding='GBK').read().splitlines()
            pool_length = len(pool)
            if pool_id and 1 <= int(pool_id) <= pool_length:
                goal = pool[int(pool_id) - 1]
            else:
                goal = pool[random.randint(0, pool_length - 1)]
            self.goal = goal.split(',')[0]
            self.length = len(self.goal)
            self.explain = f"{goal.split(',')[0]} ——{goal.split(',')[1]}《{goal.split(',')[2]}》"
            self.goal_dict = {}
            for char in self.goal:
                if char not in self.goal_dict.keys():
                    self.goal_dict[char] = 1
                else:
                    self.goal_dict[char] -= 1
        else:
            for ky in from_dict.keys():
                exec(f'self.{ky} = from_dict["{ky}"]')

    def get_init(self) -> tuple:
        """
        获取正确答案的首尾字。
        """
        return self.goal[0], self.goal[-1]

    def set_current(self, current_guess) -> object:
        """
        设置当前作答内容。
        """
        if len(current_guess) == self.length:
            self.current = current_guess
        return self

    def match(self) -> list[int]:
        """
        检测和匹配作答与正确答案。
        """
        match_result = [0] * self.length
        match_dict = self.goal_dict.copy()
        for i in range(self.length):
            if self.current[i] == self.goal[i]:
                match_result[i] = 1
        for i in range(self.length):
            if match_result[i]:
                match_dict[self.goal[i]] -= 1
        for i in range(self.length):
            if not match_result[i]:
                if match_dict.get(self.current[i]):
                    match_result[i] = -1
        del match_dict
        if sum(match_result) == self.length:
            self.need_solve = False
        return match_result

    def to_json(self) -> dict:
        """
        将Wordle对象导出为字典。
        """
        jsonlized_self = {
            'current': self.current,
            'historic': self.historic,
            'need_solve': self.need_solve,
            'goal': self.goal,
            'length': self.length,
            'explain': self.explain,
            'goal_dict': self.goal_dict
        }
        return jsonlized_self

    @classmethod
    def from_dict(cls, from_dict: dict) -> object:
        """
        通过读取字典来构建一个Wordle对象。
        """
        return cls(from_dict=from_dict)


if __name__ == '__main__':
    w = Wordle(3)
    print(w.get_init())
    w.set_current('海月明不月断生')
    print(w.match())
    w.set_current('海月明月月断生')
    print(w.match())
    w.set_current('海上明月共潮生')
    print(w.match())
