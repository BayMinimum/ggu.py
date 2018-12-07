#!/usr/bin/python3
import sys
from collections import deque
from enum import Enum


# set DEBUG = True for debug mode
# debug mode shows current line during execution
# and final value of all variables after execution
DEBUG = False


INT_VAR_U = '꾸뀨뿌쀼뚜'
INT_VAR_A = '까꺄'
INT_VAR = INT_VAR_A + INT_VAR_U
EXT_U = '우'
EXT_A = '아'

STACK = '끼'
QUEUE = '삐'
COLLECTION_VAR = STACK + QUEUE
EXT_E = '이'

PRINT = '!'
INPUT = '?'
ZERO = '.'
COND = '\'"'

VARS = INT_VAR + COLLECTION_VAR
ALLOWED_CHARS = '꾸뀨까꺄끼뿌쀼삐뚜우아이!?\'".'

# store code
lines = []

# variables used by program
var = {'꾸': 0, '뀨': 0, '뿌': 0, '쀼': 0, '뚜': 0, '까': 0, '꺄': 0, '?': -1,
       '끼': [], '삐': deque()}


class Action(Enum):
    PRINT_INT = 1
    PRINT_UNICODE = 2
    SET_ZERO = 3


class Ggu문법오류(Exception):
    pass


class Ggu런타임오류(Exception):
    pass


def next_allowed(c):
    if c in INT_VAR_A or c in EXT_A:
        return VARS + EXT_A + PRINT + INPUT + ZERO
    if c in INT_VAR_U or c in EXT_U:
        return VARS + EXT_U + PRINT + INPUT + ZERO
    if c in COLLECTION_VAR or c in EXT_E:
        return VARS + EXT_E + PRINT + INPUT + ZERO
    if c in ZERO or c in INPUT:
        return PRINT
    if c in PRINT:
        return VARS + PRINT + INPUT + ZERO


def checkggu(line):
    if len(line) == 0:
        return
    for c in line:
        if c not in ALLOWED_CHARS:
            raise Ggu문법오류('{}는 허용되지 않는 문자입니다.'.format(c))
    if line[0] in COND:
        if line[-1] != line[0] or len(line) == 1:
            large_small = '큰' if line[0] == '"' else '작은'
            raise Ggu문법오류('{} 따옴표로 시작한 줄은 {} 따옴표로 끝나야 합니다.'
                            .format(large_small, large_small))
        line = line[1:len(line)-1]
    print_conti = 0
    for i in range(len(line)-1):
        next = next_allowed(line[i])
        if line[i] in PRINT:
            print_conti += 1
            if print_conti >= 3:
                raise Ggu문법오류('!는 연속해서 3개 이상 사용할 수 없습니다.')
        else:
            print_conti = 0
        if line[i+1] in COND or line[i] in COND:
            raise Ggu문법오류('문장 중간에는 {} 따옴표가 올 수 없습니다.'
                            .format('큰' if line[0] == '"' else '작은'))
        if next == None:
            raise Ggu문법오류('{} 뒤에는 다른 글자가 올 수 없습니다.'.format(line[i]))
        if line[i+1] not in next:
            raise Ggu문법오류('{} 뒤에는 {}가 올 수 없습니다.'.format(line[i], line[i+1]))

    
def main():
    if len(sys.argv) == 1:
        print('입력 파일이 없습니다.')
        return
    L = open(sys.argv[1], 'r').readlines()
    for i in range(len(L)):
        new_line = ''.join(L[i].split())
        try:
            checkggu(new_line)
            lines.append(new_line)
        except Ggu문법오류 as e:
            print('{}번째 줄: {}'.format(i, e))
            if DEBUG:
                print('===문법 오류로 종료됨===')
            return
    if len(L) == 0:
        print('입력 파일이 비어 있습니다.')
        return
    while 0 <= var['뚜'] < len(lines):
        line_num = var['뚜']
        line = lines[line_num]
        if not line:
            var['뚜'] += 1
            continue
        if DEBUG:
            print('[{:d}] {}'.format(var['뚜'], line))
        if line[0] in COND:
            try:
                run(line[1:len(line)-1], rightmost=True)
            except Ggu런타임오류 as e:
                print('{}번째 줄: {}'.format(line_num, e))
                break
            var['뚜'] = line_num
            if line[0] == '"':
                var['뚜'] += 1 if get(line[1]) == 0 else 2
            else:
                var['뚜'] += 1 if get(line[1]) <= 0 else 2
        else:
            try:
                run(line, rightmost=True)
            except Ggu런타임오류 as e:
                print('{}번째 줄: {}'.format(line_num, e))
                break
            if line_num == var['뚜']:
                var['뚜'] += 1
    if DEBUG:
        print('===프로그램 종료됨===')
        print(var)


def print_int(var_name):
    print('{:d}'.format(get(var_name)))


def print_unicode(var_name):
    print('{:s}'.format(chr(get(var_name))), end='')


def add(var_name, delta):
    try:
        var[var_name] += delta
    except TypeError:
        var[var_name] += [delta]


def reset(var_name, value):
    if var_name in INT_VAR:
        var[var_name] = value
    elif var_name in COLLECTION_VAR:
        var[var_name] += [value]


def get(var_name, pop=True):
    if var_name in INT_VAR:
        return var[var_name]
    if var_name in STACK:
        try:
            if pop:
                return var[var_name].pop()
            else:
                return var[var_name][-1]
        except IndexError:
            raise Ggu런타임오류('비어있는 스택 {}에서 인출을 시도했습니다.'.format(var_name))
    if var_name in QUEUE:
        try:
            if pop:
                return var[var_name].popleft()
            else:
                return var[var_name][0]
        except IndexError:
            raise Ggu런타임오류('비어있는 큐 {}에서 인출을 시도했습니다.'.format(var_name))


def run(line, action=[], rightmost=False, base_value=0):
    if not line:
        return
    n = len(line)
    if line[-1] == '!':
        if line[-2] == '!':
            return run(line[:n-2], action=action+[Action.PRINT_UNICODE],
                       rightmost=rightmost, base_value=base_value)
        return run(line[:n-1], action=action+[Action.PRINT_INT],
                   rightmost=rightmost, base_value=base_value)
    
    if line[-1] in INPUT:
        try:
            var[line[-1]] = int(input())
        except ValueError:
            raise Ggu런타임오류('입력은 정수만 가능합니다.')
        return run(line[:n-1], base_value=var[line[-1]], action=action)
    if line[-1] in ZERO:
        return run(line[:n-1], action=action+[Action.SET_ZERO])

    i = n - 1
    while line[i] not in VARS:
        i -= 1
    value_change = reset if Action.SET_ZERO in action else add
    if rightmost:
        if line[i] in INT_VAR or i != n - 1:
            value_change(line[i], n - 1 - i)
    else:
        value_change(line[i], base_value + i + 1 - n)
    
    if Action.PRINT_UNICODE in action:
        print_unicode(line[i])
    elif Action.PRINT_INT in action:
        print_int(line[i])
    
    if i > 0:
        return run(line[:i], base_value=get(line[i]))


if __name__ == '__main__':
    main()
