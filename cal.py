#!/usr/bin/env python3

import pathlib
import sys

def split_src(text):
    res = dict()
    # find module xxx( as the start of a module
    # find endmodule as the end of a module
    lines = text.splitlines()
    current_module = None
    module_lines = []
    for line in lines:
        line_strip = line.strip()
        if line_strip.startswith("module "):
            if current_module is not None:
                res[current_module] = "\n".join(module_lines)
                module_lines = []
            current_module = line_strip.split()[1].split("(")[0]
        if current_module is not None:
            module_lines.append(line)
        if line_strip == "endmodule":
            if current_module is not None:
                res[current_module] = "\n".join(module_lines)
                current_module = None
                module_lines = []
    return res

def read_child_module(module_text, module_names):
    res = dict() # instance_name -> module_name
    lines = module_text.splitlines()
    for line in lines:
        if line.startswith("  "):
            split_res = line.strip().split()
            if len(split_res) >= 3 and split_res[2] == '(':
                instance_name = split_res[1]
                module_name = split_res[0]
                if module_name not in module_names:
                    continue
                res[instance_name] = module_name
    return res

def read_module_scala_files(module_text):
    res = set()
    for line in module_text.splitlines():
        line_strip = line.strip()
        comment_pos = line_strip.rfind("// ")
        if comment_pos != -1 and ".scala:" in line_strip:
            source_pos = line_strip = line_strip[comment_pos + 3:].strip()
            line_pos = source_pos.find(":")
            res.add(source_pos[:line_pos].strip())
    return res

def get_hier(src_dict):
    assert "XSTop" in src_dict
    res = dict() # module_name -> dict(instance_name -> module_name)
    module_scala = dict()
    to_process = ["XSTop"]
    while to_process:
        module_name = to_process.pop()
        if module_name in res:
            continue
        module_text = src_dict[module_name]
        child_modules = read_child_module(module_text, src_dict.keys())
        module_scala[module_name] = read_module_scala_files(module_text)
        res[module_name] = child_modules
        for child_module in child_modules.values():
            if child_module not in res:
                to_process.append(child_module)
    return (res, module_scala)

def output_in_tree(modules_dict, root_module="XSTop", indent="  ", max_depth=10):
    if max_depth == 0:
        return
    print(f"{indent}{root_module}")
    child_modules = modules_dict.get(root_module, {})
    for instance_name, module_name in child_modules.items():
        output_in_tree(modules_dict, module_name, indent + "  ", max_depth - 1)

def count_flat(cur_module, hier, scala_files, src_map, res_dict, res_src_dict):
    if cur_module in res_dict:
        return
    res_dict[cur_module] = src_map[cur_module].count("\n") + 1
    res_src_dict[cur_module] = scala_files[cur_module].copy()
    for child_module in hier.get(cur_module, {}).values():
        count_flat(child_module, hier, scala_files, src_map, res_dict, res_src_dict)
        res_dict[cur_module] += res_dict[child_module]
        res_src_dict[cur_module].update(res_src_dict[child_module])

def cal_src_count(src_dict, src_count_dict, default_folder=None):
    line_cache = dict()
    for module_name, scala_files in src_dict.items():
        for scala_file in scala_files:
            if scala_file in line_cache:
                src_count_dict[module_name] = src_count_dict.get(module_name, 0) + line_cache[scala_file]
            else:
                read_success = False
                for prefix in ['/', default_folder]:
                    if prefix is None:
                        continue
                    try:
                        with open(f"{prefix}{scala_file}", "r") as f:
                            line_count = sum(1 for _ in f)
                            line_cache[scala_file] = line_count
                            src_count_dict[module_name] = src_count_dict.get(module_name, 0) + line_count
                            read_success = True
                            break
                    except FileNotFoundError:
                        continue
                if not read_success:
                    print(f"Warning: Scala source file {scala_file} not found.", file=sys.stderr)
                    line_cache[scala_file] = 0
                    src_count_dict[module_name] = 0

def cal_count(yqh_count, nh_count, kmh_count, kmhv2_count, kmhv3_count, output_file):
    res = {
        "yqh": {
            "Frontend": yqh_count["Frontend"] - yqh_count["ICache"],
            "Backend": yqh_count["XSCore"] - yqh_count["Frontend"] - yqh_count["MemBlock"],
            "MemBlock": yqh_count["MemBlock"],
            "ICache": yqh_count["ICache"],
            "DCache": yqh_count["DCache"],
            "L2Top": yqh_count["InclusiveCache"]
        },
        "nh": {
            "Frontend": nh_count["Frontend"] - nh_count["ICache"],
            "Backend": nh_count["XSCore"] - nh_count["Frontend"] - nh_count["MemBlock"],
            "MemBlock": nh_count["MemBlock"],
            "ICache": nh_count["ICache"],
            "DCache": nh_count["DCache"],
            "L2Top": nh_count["HuanCun"]
        },
        "kmh": {
            "Frontend": kmh_count["Frontend"] - kmh_count["ICache"],
            "Backend": kmh_count["Backend"],
            "MemBlock": kmh_count["MemBlock"] - kmh_count["DCacheWrapper"],
            "ICache": kmh_count["ICache"],
            "DCache": kmh_count["DCacheWrapper"],
            "L2Top": kmh_count["L2Top"]
        },
        "kmhv2": {
            "Frontend": kmhv2_count["Frontend"] - kmhv2_count["ICache"],
            "Backend": kmhv2_count["Backend"],
            "MemBlock": kmhv2_count["MemBlock"] - kmhv2_count["DCacheWrapper"],
            "ICache": kmhv2_count["ICache"],
            "DCache": kmhv2_count["DCacheWrapper"],
            "L2Top": kmhv2_count["L2Top"]
        },
        "kmhv3": {
            "Frontend": kmhv3_count["Frontend"] - kmhv3_count["ICache"],
            "Backend": kmhv3_count["Backend"],
            "MemBlock": kmhv3_count["MemBlock"] - kmhv3_count["DCacheWrapper"],
            "ICache": kmhv3_count["ICache"],
            "DCache": kmhv3_count["DCacheWrapper"],
            "L2Top": kmhv3_count["L2Top"]
        },
    }
    # output in csv
    buf = ""
    buf += "Part,Frontend,Backend,MemBlock,ICache,DCache,L2Top\n"
    for part in ["yqh", "nh", "kmh", "kmhv2", "kmhv3"]:
        frontend = res[part]["Frontend"]
        backend = res[part]["Backend"]
        memblock = res[part]["MemBlock"]
        icache = res[part]["ICache"]
        dcache = res[part]["DCache"]
        l2top = res[part]["L2Top"]
        buf += f"{part},{frontend},{backend},{memblock},{icache},{dcache},{l2top}\n"
    with open(output_file, "w") as f:
        f.write(buf)

if __name__ == "__main__":
    yqh, nh, kmh, kmhv2, kmhv3 = dict(), dict(), dict(), dict(), dict()
    for path in pathlib.Path("verilog/yanqihu").rglob("*.sv"):
        file = path.name
        with open(path, "r") as f:
            yqh_part = split_src(f.read())
            yqh.update(yqh_part)
    for path in pathlib.Path("verilog/nanhu").rglob("*.sv"):
        file = path.name
        with open(path, "r") as f:
            nh_part = split_src(f.read())
            nh.update(nh_part)
    for path in pathlib.Path("verilog/kunminghu").rglob("*.sv"):
        file = path.name
        with open(path, "r") as f:
            kmh_part = split_src(f.read())
            kmh.update(kmh_part)
    for path in pathlib.Path("verilog/kunminghu_v2").rglob("*.sv"):
        file = path.name
        with open(path, "r") as f:
            kmhv2_part = split_src(f.read())
            kmhv2.update(kmhv2_part)
    for path in pathlib.Path("verilog/kunminghu_v3").rglob("*.sv"):
        file = path.name
        with open(path, "r") as f:
            kmhv3_part = split_src(f.read())
            kmhv3.update(kmhv3_part)
    yqh_hier, yqh_scala = get_hier(yqh)
    nh_hier, nh_scala = get_hier(nh)
    kmh_hier, kmh_scala = get_hier(kmh)
    kmhv2_hier, kmhv2_scala = get_hier(kmhv2)
    kmhv3_hier, kmhv3_scala = get_hier(kmhv3)
    # output_in_tree(yqh_hier)
    # output_in_tree(nh_hier)
    # output_in_tree(kmh_hier)
    # output_in_tree(kmhv2_hier)
    # output_in_tree(kmhv3_hier)
    yqh_count, nh_count, kmh_count, kmhv2_count, kmhv3_count = dict(), dict(), dict(), dict(), dict()
    yqh_src, nh_src, kmh_src, kmhv2_src, kmhv3_src = dict(), dict(), dict(), dict(), dict()
    count_flat("XSTop", yqh_hier, yqh_scala, yqh, yqh_count, yqh_src)
    count_flat("XSTop", nh_hier, nh_scala, nh, nh_count, nh_src)
    count_flat("XSTop", kmh_hier, kmh_scala, kmh, kmh_count, kmh_src)
    count_flat("XSTop", kmhv2_hier, kmhv2_scala, kmhv2, kmhv2_count, kmhv2_src)
    count_flat("XSTop", kmhv3_hier, kmhv3_scala, kmhv3, kmhv3_count, kmhv3_src)
    yqh_scala_count, nh_scala_count, kmh_scala_count, kmhv2_scala_count, kmhv3_scala_count = dict(), dict(), dict(), dict(), dict()
    cal_src_count(yqh_src, yqh_scala_count, "/mnt/data/xs/xs-env/yanqihu/")
    cal_src_count(nh_src, nh_scala_count, "/mnt/data/xs/xs-env/nanhu/")
    cal_src_count(kmh_src, kmh_scala_count, "/mnt/data/xs/xs-env/kunminghu/")
    cal_src_count(kmhv2_src, kmhv2_scala_count, "/mnt/data/xs/xs-env/kunminghu-v2/")
    cal_src_count(kmhv3_src, kmhv3_scala_count, "/mnt/data/xs/xs-env/XiangShan/")
    cal_count(yqh_count, nh_count, kmh_count, kmhv2_count, kmhv3_count, "verilog.csv")
    cal_count(yqh_scala_count, nh_scala_count, kmh_scala_count, kmhv2_scala_count, kmhv3_scala_count, "scala.csv")
