import math
import random


def randomDNA(length):
    DNA = []
    for i in range(length):
        DNA.append(random.random()*2-1)
    return DNA


def NN(input, weight):
    i = input
    w = weight
    a = sigmoid(i[0]*w[0] + i[1]*w[1]+i[2]*w[2])
    b = sigmoid(i[0]*w[3] + i[1]*w[4]+i[2]*w[5])

    return sigmoid(a*w[6]+b*w[7])


def sigmoid(x):
    return (math.exp(x) - math.exp(-x))/(math.exp(x) + math.exp(-x))  # -1~1

    # return 1 / (1 + math.exp(-x))#0~1
# s = ['a', 'b']
# print(s)
# s.pop()
# print(s)
# print(math.exp(700))
