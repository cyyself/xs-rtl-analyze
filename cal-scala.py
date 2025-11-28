#!/usr/bin/env python3

import pathlib

def count_scala_line_path(path):
    dir = pathlib.Path(path)
    scala_lines = 0
    for file in dir.rglob("*.scala"):
        with open(file, "r") as f:
            scala_lines += len(f.readlines())
    assert scala_lines > 0, f"No scala lines found in path: {path}"
    return scala_lines

if __name__ == "__main__":
    res = dict()
    res = {
        'yqh': {
            'Frontend': count_scala_line_path('../yanqihu/src/main/scala/xiangshan/frontend'),
            'Backend': count_scala_line_path('../yanqihu/src/main/scala/xiangshan/backend'),
            'MemBlock': count_scala_line_path('../yanqihu/src/main/scala/xiangshan/mem'),
            'L1Cache': count_scala_line_path('../yanqihu/src/main/scala/xiangshan/cache'),
            'L2Cache': count_scala_line_path('../yanqihu/block-inclusivecache-sifive/design/craft/inclusivecache/src'),
            'Others': count_scala_line_path('../yanqihu/src/main/scala') + \
                      count_scala_line_path('../yanqihu/utility/src/main') - \
                      count_scala_line_path('../yanqihu/src/main/scala/xiangshan/frontend') - \
                      count_scala_line_path('../yanqihu/src/main/scala/xiangshan/backend') - \
                      count_scala_line_path('../yanqihu/src/main/scala/xiangshan/mem') - \
                      count_scala_line_path('../yanqihu/src/main/scala/xiangshan/cache')
        },
        'nh': {
            'Frontend': count_scala_line_path('../nanhu/src/main/scala/xiangshan/frontend'),
            'Backend': count_scala_line_path('../nanhu/src/main/scala/xiangshan/backend') + \
                       count_scala_line_path('../nanhu/fudian/src/main/scala/fudian'),
            'MemBlock': count_scala_line_path('../nanhu/src/main/scala/xiangshan/mem'),
            'L1Cache': count_scala_line_path('../nanhu/src/main/scala/xiangshan/cache'),
            'L2Cache': count_scala_line_path('../nanhu/huancun/src/main/scala/huancun'),
            'Others': count_scala_line_path('../nanhu/src/main/scala') + \
                      count_scala_line_path('../nanhu/utility/src/main') - \
                      count_scala_line_path('../nanhu/src/main/scala/xiangshan/frontend') - \
                      count_scala_line_path('../nanhu/src/main/scala/xiangshan/backend') - \
                      count_scala_line_path('../nanhu/src/main/scala/xiangshan/mem') - \
                      count_scala_line_path('../nanhu/src/main/scala/xiangshan/cache')
        },
        'kmh': {
            'Frontend': count_scala_line_path('../kunminghu/src/main/scala/xiangshan/frontend'),
            'Backend': count_scala_line_path('../kunminghu/src/main/scala/xiangshan/backend') + \
                       count_scala_line_path('../kunminghu/fudian/src/main/scala/fudian'),
            'MemBlock': count_scala_line_path('../kunminghu/src/main/scala/xiangshan/mem'),
            'L1Cache': count_scala_line_path('../kunminghu/src/main/scala/xiangshan/cache'),
            'L2Cache': count_scala_line_path('../kunminghu/coupledL2/src/main/scala'),
            'Others': count_scala_line_path('../kunminghu/src/main/scala') + \
                      count_scala_line_path('../kunminghu/utility/src/main') - \
                      count_scala_line_path('../kunminghu/src/main/scala/xiangshan/frontend') - \
                      count_scala_line_path('../kunminghu/src/main/scala/xiangshan/backend') - \
                      count_scala_line_path('../kunminghu/src/main/scala/xiangshan/mem') - \
                      count_scala_line_path('../kunminghu/src/main/scala/xiangshan/cache')
        },
        'kmhv2': {
            'Frontend': count_scala_line_path('../kunminghu-v2/src/main/scala/xiangshan/frontend'),
            'Backend': count_scala_line_path('../kunminghu-v2/src/main/scala/xiangshan/backend') + \
                       count_scala_line_path('../kunminghu-v2/fudian/src/main/scala/fudian') + \
                       count_scala_line_path('../kunminghu-v2/yunsuan/src/main/scala/yunsuan'),
            'MemBlock': count_scala_line_path('../kunminghu-v2/src/main/scala/xiangshan/mem'),
            'L1Cache': count_scala_line_path('../kunminghu-v2/src/main/scala/xiangshan/cache'),
            'L2Cache': count_scala_line_path('../kunminghu-v2/coupledL2/src/main/scala'),
            'Others': count_scala_line_path('../kunminghu-v2/src/main/scala') + \
                      count_scala_line_path('../kunminghu-v2/utility/src/main') - \
                      count_scala_line_path('../kunminghu-v2/src/main/scala/xiangshan/frontend') - \
                      count_scala_line_path('../kunminghu-v2/src/main/scala/xiangshan/backend') - \
                      count_scala_line_path('../kunminghu-v2/src/main/scala/xiangshan/mem') - \
                      count_scala_line_path('../kunminghu-v2/src/main/scala/xiangshan/cache')
        },
        'kmhv3': {
            'Frontend': count_scala_line_path('../kunminghu-v3/src/main/scala/xiangshan/frontend'),
            'Backend': count_scala_line_path('../kunminghu-v3/src/main/scala/xiangshan/backend') + \
                       count_scala_line_path('../kunminghu-v3/fudian/src/main/scala/fudian') + \
                       count_scala_line_path('../kunminghu-v3/yunsuan/src/main/scala/yunsuan'),
            'MemBlock': count_scala_line_path('../kunminghu-v3/src/main/scala/xiangshan/mem'),
            'L1Cache': count_scala_line_path('../kunminghu-v3/src/main/scala/xiangshan/cache'),
            'L2Cache': count_scala_line_path('../kunminghu-v3/coupledL2/src/main/scala'),
            'Others': count_scala_line_path('../kunminghu-v3/src/main/scala') + \
                      count_scala_line_path('../kunminghu-v3/ChiselAIA/src/main/scala') + \
                      count_scala_line_path('../kunminghu-v3/utility/src/main') - \
                      count_scala_line_path('../kunminghu-v3/src/main/scala/xiangshan/frontend') - \
                      count_scala_line_path('../kunminghu-v3/src/main/scala/xiangshan/backend') - \
                      count_scala_line_path('../kunminghu-v3/src/main/scala/xiangshan/mem') - \
                      count_scala_line_path('../kunminghu-v3/src/main/scala/xiangshan/cache')
        }
    }
    # Output in CSV
    categories = ['Frontend', 'Backend', 'MemBlock', 'L1Cache', 'L2Cache', 'Others']
    print("Architecture," + ",".join(categories))
    for arch, counts in res.items():
        line = [arch] + [str(counts[cat]) for cat in categories]
        print(",".join(line))
