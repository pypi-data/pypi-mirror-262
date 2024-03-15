from .ema import Strategy as ema
from .rsi import Strategy as rsi
from .macd import Strategy as macd
from .sma import Strategy as sma
from .dummy import Strategy as dummy
from .selector import ModelSelector

strategies_list = ['ema', 'rsi', 'macd', 'sma', 'dummy']

intervals_list = [
        '1h',
        # '2h'
        # '4h',
        # '6h',
        # '8h',
    ]