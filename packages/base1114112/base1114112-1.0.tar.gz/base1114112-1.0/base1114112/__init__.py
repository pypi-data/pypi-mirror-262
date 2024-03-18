"""
who in the world would use this
"""

__author__ = "tema5002 <tema5002@gmail.com>"
__version__ = "1.0"
__license__ = "MIT"
__copyright__ = "2024, tema5002"
__short_description__ = "who in the world would use this"


def decode(num: str) -> int:
    if not isinstance(num, str):
        raise TypeError(f"Incorrect data type: {type(num)}")

    return sum(1114112 ** index * ord(i) for index, i in enumerate(num))


def encode(num: int) -> str:
    if not isinstance(num, int):
        raise TypeError(f"Incorrect data type: {type(num)}")

    def _encode(num_):
        return chr(num_ % 1114112) + _encode(num_ // 1114112) if num_ else ""

    return _encode(num)


print(encode(7047530565501760338737361894658820726940540227402822885687894635203120983481008233243662212034357802881306782862235760252165407918616036280427233029943797802060100190280982150662028214962892489489971962767068291095973135612183600))
