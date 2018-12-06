#-*- coding: utf-8 -*-
#MIT License

#Copyright (c) 2018 Sangbum Kim, Jongseo Lee

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

import signal
import sys
from collections import deque as queue

numvar = 0
numstack = 0
numqueue = 0

VAR = dict()
STACK = dict()
QUE = dict()

var = []
stack = []
que = []

def declareVar(varName):
    assert varName not in VAR
    assert varName[0] in ["꾸", "뀨", "까", "꺄", "뿌", "쀼"]
    s = {"꾸" : "우", "뀨" : "우", "까" : "아", "꺄" : "아", "뿌" : "우", "쀼" : "우"}
    for i in range(1, len(varName)):
        assert varName[i] == s[varName[0]]
    var.append(0)
    VAR[varName] = len(var)-1

def declareStack(stackName):
    assert stackName not in STACK
    assert stackName[0] == "끼"
    for i in range(1, len(stackName)):
        assert stackName[i] == "이"
    stack.append([])
    STACK[stackName] = len(stack)-1

def declareQueue(queName):
    assert queName not in QUE
    assert queName[0] == "삐"
    for i in range(1, len(queName)):
        assert queName[i] == "이"
    que.append(queue())
    QUE[queName] = len(que)-1
