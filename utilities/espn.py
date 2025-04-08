from classes.espn.base import Position, Stat
from time import strftime, localtime
from typing import Union


def get_position(position: Union[str, int] = None):
    """
    Retrieve the shorthand representation for a given position identifier.

    This function attempts to convert the provided position value into an integer and then
    uses it to look up the corresponding member in the ``Position`` enumeration. If the input
    is None, cannot be converted to an integer, or corresponds to the default position
    (``Position.DEFAULT``), the function returns None.

    :param position: The position identifier as an integer or a string representation of an integer.
                     Defaults to None.
    :type position: int or str, optional
    :return: The shorthand representation of the position or None if the position is invalid or default.
    :rtype: str or None
    """
    if position is None:
        return None
    if not isinstance(position, int):
        try:
            position = int(position)
        except Exception:
            return None
    return Position(position)


def get_stat(stat: Union[str, int] = None):
    """
    Retrieve the shorthand representation for a given statistical identifier.

    This function attempts to convert the provided stat value into an integer and then
    uses it to look up the corresponding member in the ``Stat`` enumeration. If the input
    is None, cannot be converted to an integer, or corresponds to the default statistic
    (``Stat.DEFAULT``), the function returns None.

    :param stat: The statistical identifier as an integer or a string representation of an integer.
                 Defaults to None.
    :type stat: int or str, optional
    :return: The shorthand representation of the statistic or None if the statistic is invalid or default.
    :rtype: str or None
    """
    if stat is None:
        return None
    if not isinstance(stat, int):
        try:
            stat = int(stat)
        except Exception:
            return None
    return Stat(stat)


def convert_epoch_to_date(epoch: Union[str, int] = None):
    """
    Converts an ESPN Epoch to a valid datetime
    """

    if epoch is None:
        return None

    if not isinstance(epoch, str):
        try:
            epoch = str(epoch)
        except Exception:
            return None
    epoch = epoch[:10]
    epoch = int(epoch)
    return strftime('%Y-%m-%d %H:%M:%S', localtime(epoch))
