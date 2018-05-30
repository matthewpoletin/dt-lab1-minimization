#!/usr/bin/env python3
# -*- coding: utf-8 -*

import sys
import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def two_axis(func):
    """
    2D representation
    :param func:
    :return:
    """
    n = 256
    x = np.linspace(-4, 4, n)
    y = np.linspace(-4, 4, n)
    X, Y = np.meshgrid(x, y)
    plt.contourf(X, Y, func([X, Y]), 8, alpha=.75, cmap='jet')
    C = plt.contour(X, Y, func([X, Y]), 8, colors='black', linewidth=.5)
    plt.show()


def W(S, T):
    """
    Расчёт ширины проводника
    :param S: Площадь сечения
    :param T: Высота дорожки
    :return: Ширина проводника (милы)
    """
    return S / (T * 1.378)


def S(I, dt, k, b, c):
    """
    Расчёт площади проводника
    :param I: Максимальный ток (А)
    :param dt: Изменение температуры (°С)
    :param k: Константа из стандарта
    :param b: Константа из стандарта
    :param c: Константа из стандарта
    :return: Площадь сечения дорожки (мил^2)
    """
    return (I / (k * (dt ** b))) ** (1 / c)


def f(x, t=0):
    """
    Целевая функция
    :param x:
    :param t: Тип проводника (0-внешний, 1-внутренний)
    :return:
    """
    if t is 0:
        k = 0.024
    else:
        k = 0.048
    b = 0.44
    c = 0.725
    I = x[0]
    dt = x[1]
    T = x[2]
    return W(S(I, dt, k, b, c), T)


def minim(func, I0, dt0, T0, method):
    """
    Минимизация заданной функции
    :param method: Метод минимизации
    :param func: Целевая функция
    :param I0: Начальный ток (А)
    :param dt0: Начальное изменение температуры (°С)
    :param T0: Начальная толщина проводящего слоя (мил)
    :return: Результат минимизации
    """
    # Начальное предположение
    x0 = np.array([I0, dt0, T0])
    # Границы значений переменных (более нуля)
    bounds = ((15, 50), (0, 20), (0, 20))
    # Выполняем минимизацию
    res = minimize(func, x0, method=method, bounds=bounds)
    return res.x


# Используемыем методы
methods = [
    'SLSQP',
    'L-BFGS-B',
]


def main(argv):
    for method in methods:
        print('\nОптимизирую используя метод {}'.format(method))
        # Опитимузируем функцию при начальных значениях
        x = minim(f, 11, 0.75, 1, method)
        # Выподим результат
        print('Сила тока: {} А'.format(x[0]))
        print('Изменение температуры: {} °С'.format(x[1]))
        print('Толщина медного слоя: {} мил'.format(x[2]))
        print('Ширина внешнего проводника: {} мил'.format(f(x, 0)))
        print('Ширина внутреннего проводника: {} мил'.format(f(x, 1)))
        # Отобразить на картинке
        # two_axis()


if __name__ == '__main__':
    main(sys.argv)
