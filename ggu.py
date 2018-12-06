#!/usr/bin/python3
import sys
from collections import deque


INT_VAR_U = '꾸뀨뿌쀼뚜'
INT_VAR_A = '까꺄'
EXT_U = '우'
EXT_A = '아'
STACK = '끼'
QUEUE = '삐'
EXT_E = '이'
PRINT = '!'
INPUT = '?'
ZERO = '.'
COND = '\'"'
VARS = INT_VAR_A + INT_VAR_U + STACK + QUEUE
ALLOWED_CHARS = '꾸뀨까꺄끼뿌쀼삐뚜우아!?\'".'

lines = []
var = {'꾸': 0, '뀨': 0, '뿌': 0, '쀼': 0, '뚜': 0, '까': 0, '꺄': 0, '?': -1}
stack = []
queue = deque()


class Ggu문법오류(Exception):
    pass


class Ggu런타임오류(Exception):
    pass


def next_allowed(c):
    if c in INT_VAR_A or c in EXT_A:
        return VARS + EXT_A + PRINT + INPUT + ZERO
    if c in INT_VAR_U or c in EXT_U:
        return VARS + EXT_U + PRINT + INPUT + ZERO
    if c in STACK or c in QUEUE or EXT_E:
        return VARS + EXT_E + PRINT + INPUT + ZERO
    if c in ZERO or c in INPUT:
        return None
    if c in PRINT:
        return VARS + PRINT + INPUT + ZERO


def checkggu(line):
    if len(line) == 0:
        return
    for c in line:
        if c not in ALLOWED_CHARS:
            raise Ggu문법오류('{}는 허용되지 않는 문자입니다.')
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
            raise Ggu문법오류('{} 뒤에는 다른 글자가 올 수 없습니다.')
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
            print('{}번째 줄: {}'.format(i+1, e))
            return
    if len(L) == 0:
        print('입력 파일이 비어 있습니다.')
        return
    while 0 <= var['뚜'] < len(lines):
        line_num = var['뚜']
        line = lines[line_num]
        if line[0] in COND:
            run(line[1:len(line)-1])
            is_zero = var[line[1]] == 0
            var['뚜'] = line_num
            if line[0] == '"':
                var['뚜'] += 1 if is_zero else 2
            else:
                var['뚜'] += 2 if is_zero else 1
        else:
            run(line)
            if line_num == var['뚜']:
                var['뚜'] += 1


def run(line):
    pass


if __name__ == '__main__':
    main()
