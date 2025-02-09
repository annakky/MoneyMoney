from typing import List
from pandas import DataFrame

from strategy.Strategy import Strategy, Position

class MyStrategy:
    _strategies: List[Strategy]
    _positions: List[Position]
    _threshold: int

    def __init__(self, strategies: List[Strategy], threshold: int, stop_loss: float = 0.9, position_size: float = 1.0):
        self._strategies = strategies
        self._positions = [Position.NONE] * len(strategies)
        self._threshold = threshold

        self.stop_loss = stop_loss
        self.position_size = position_size

    def draw_indicators(self, chart):
        for strategy in self._strategies:
            strategy.draw_indicator(chart)

    def clear_indicators(self, chart):
        for strategy in self._strategies:
            strategy.clear_indicator(chart)

    def append_data(self, data: DataFrame):
        for s in self._strategies:
            s.append_data(data)

    def position(self):
        for i in range(0, len(self._strategies)):
            self._positions[i] = self._strategies[i].position()

        total = sum(position.value for position in self._positions)

        if abs(total) >= self._threshold:
            if total > 0:
                return Position.BUY
            elif total < 0:
                return Position.SELL

        return Position.NONE

    def set_stop_loss(self, value):
        if value > 1:
            print("STOP LOSS는 1보다 클 수 없습니다. 기본값 0.9로 입력됩니다.")
            self.stop_loss = 0.9
        elif value < 0:
            print("STOP LOSS는 0보다 작을 수 없습니다. 기본값 0.9로 입력됩니다.")
            self.stop_loss = 0.9
        else:
            self.stop_loss = value
