""" rendering wrappers """

import numpy as np

from .utils import series_xy

from .model import Wrapper

from .extalib import talib_function_check, TalibWrapper

wrapper_registry = dict()


def register(name: str):
    """register a wrapper class for given indicator names"""

    def decorator(func):
        wrapper_registry[name] = func
        return func

    return decorator


def indicator_name(indicator):
    """indicator name (uppercase)"""

    if hasattr(indicator, "__name__"):
        name = indicator.__name__
    else:
        name = indicator.__class__.__name__

    return name.upper()


def get_wrapper(indicator):
    """create rendering wrapper for naive indicator"""

    if hasattr(indicator, "plot_result"):
        return None

    if talib_function_check(indicator):
        return TalibWrapper(indicator)

    name = indicator_name(indicator)

    if name in wrapper_registry:
        wrapper = wrapper_registry.get(name)
        return wrapper(indicator)


class LinePlot(Wrapper):
    """LinePlot Wrapper"""

    def plot_result(self, data, chart, ax=None):
        if ax is None:
            ax = chart.get_axes("below")

        label = repr(self)
        xv, yv = series_xy(data)

        ax.plot(xv, yv, label=label)


@register("BOP")
@register("CMF")
@register("CCI")
class AreaPlot(Wrapper):
    """AreaPlot Wrapper"""

    def plot_result(self, data, chart, ax=None):
        if ax is None:
            ax = chart.get_axes("below")

        label = repr(self)

        xv, yv = series_xy(data)

        ax.fill_between(xv, yv, alpha=0.4, label=label)


@register("RSI")
class RSI(Wrapper):
    """RSI Wrapper"""

    default_pane = "above"
    COLOR = "black"

    def check_result(self, data):
        return data.ndim == 1

    def plot_result(self, data, chart, ax=None):
        if ax is None:
            ax = chart.get_axes("above")

        label = repr(self)
        xv, yv = series_xy(data)

        color = chart.get_setting("rsi", "color", self.COLOR)

        ax.plot(xv, yv, label=label, color=color)

        with np.errstate(invalid="ignore"):
            ax.fill_between(xv, yv, 70, where=(yv >= 70), interpolate=True, alpha=0.5)
            ax.fill_between(xv, yv, 30, where=(yv <= 30), interpolate=True, alpha=0.5)

        ax.set_yticks([30, 70])
        ax.set_yticks([10, 30, 50, 70, 90], minor=True)
        ax.grid(axis="y", which="major", linestyle="-", linewidth=2)
        ax.grid(axis="y", which="minor", linestyle=":", linewidth=2)

        yformatter = ax.yaxis.get_major_formatter()
        ax.yaxis.set_minor_formatter(yformatter)


@register("SAR")
@register("PSAR")
class PSAR(Wrapper):
    """PSAR WRapper"""

    def check_result(self, data):
        return data.ndim == 1

    def plot_result(self, data, chart, ax=None):
        if ax is None:
            ax = chart.get_axes("samex")

        xv, yv = series_xy(data)

        ax.scatter(xv, yv, alpha=0.5, marker=".")


@register("ADX")
class ADX(Wrapper):
    """ADX Wrapper"""

    def check_result(self, data):
        return data.ndim == 2 and data.shape[1] == 3

    def plot_result(self, data, chart, ax=None):
        if ax is None:
            ax = chart.get_axes("below")

        label = repr(self)

        adx = data.iloc[:, 0]
        pdi = data.iloc[:, 1]
        mdi = data.iloc[:, 2]

        xv, yv = series_xy(adx)
        ax.plot(xv, yv, color="k", label=label)

        xv, yv = series_xy(pdi)
        ax.plot(xv, yv, color="g")

        xv, yv = series_xy(mdi)
        ax.plot(xv, yv, color="r")

        ax.set_yticks([20])
        ax.set_yticks([20, 40], minor=True)
        ax.grid(axis="y", which="major", linestyle="-", linewidth=2)
        ax.grid(axis="y", which="minor", linestyle=":", linewidth=2)

        yformatter = ax.yaxis.get_major_formatter()
        ax.yaxis.set_minor_formatter(yformatter)


@register("MACD")
@register("PPO")
class MACD(Wrapper):
    """MACD Wrapper"""

    def check_result(self, data):
        return data.ndim == 2 and data.shape[1] == 3

    def plot_result(self, data, chart, ax=None):
        if ax is None:
            ax = chart.get_axes("below")

        label = repr(self)

        macd = data.iloc[:, 0]
        signal = data.iloc[:, 1]
        dist = data.iloc[:, 2] * 2.0

        xv, yv = series_xy(macd)
        ax.plot(xv, yv, color="k", label=label)

        xv, yv = series_xy(signal)
        ax.plot(xv, yv)

        xv, yv = series_xy(dist)
        ax.bar(xv, yv, alpha=0.5, width=0.8)


@register("BBANDS")
@register("KELTNER")
class BBANDS(Wrapper):
    """BBANDS Wrapper"""

    same_scale = True
    COLOR = "orange"

    def check_result(self, data):
        return data.ndim == 2 and data.shape[1] == 3

    def plot_result(self, data, chart, ax=None):
        if ax is None:
            ax = chart.get_axes("samex")

        label = repr(self)

        upper = data.iloc[:, 0]
        middle = data.iloc[:, 1]
        lower = data.iloc[:, 2]

        color = self.COLOR

        xs, ms = series_xy(middle)
        ax.plot(xs, ms, color=color, linestyle="dashed", label=label)

        xs, hs = series_xy(upper)
        ax.plot(xs, hs, color=color, linestyle="dotted")

        xs, ls = series_xy(lower)
        ax.plot(xs, ls, color=color, linestyle="dotted")

        ax.fill_between(xs, ls, hs, color=color, interpolate=True, alpha=0.2)
