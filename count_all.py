#!/usr/bin/env python3

# count source lines from ../all except ./**/.*

import pathlib

def count_lines(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return len(f.readlines())

def main():
    src_dir = pathlib.Path('../all')
    # git checkout 93e4c986cb705ce6b741ef4b98eb50923c25d369 && git checkout -b count-all && git submodule update --init .
    total_lines = 0
    for scala_file in src_dir.rglob('*.*'):
        if '/.' in str(scala_file) or '/rocket-chip/' in str(scala_file):
            continue
        if ['.jpg', '.bin', '.db', '.img', '.pdf', '.png', '.pack', '.rev', '.svg'].count(scala_file.suffix) > 0:
            continue
        if scala_file.is_file():
            cur_lines = count_lines(scala_file)
            print(f'{scala_file},{cur_lines}')
            total_lines += cur_lines
    print(f'all,{total_lines}')

if __name__ == '__main__':
    main()
