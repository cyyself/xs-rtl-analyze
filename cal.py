#!/usr/bin/env python3

import pathlib

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

def get_hier(src_dict):
    assert "SimTop" in src_dict
    res = dict() # module_name -> dict(instance_name -> module_name)
    to_process = ["SimTop"]
    while to_process:
        module_name = to_process.pop()
        if module_name in res:
            continue
        module_text = src_dict[module_name]
        child_modules = read_child_module(module_text, src_dict.keys())
        res[module_name] = child_modules
        for child_module in child_modules.values():
            if child_module not in res:
                to_process.append(child_module)
    return res

def output_in_tree(modules_dict, root_module="SimTop", indent="  ", max_depth=10):
    if max_depth == 0:
        return
    print(f"{indent}{root_module}")
    child_modules = modules_dict.get(root_module, {})
    for instance_name, module_name in child_modules.items():
        output_in_tree(modules_dict, module_name, indent + "  ", max_depth - 1)

def count_flat(cur_module, hier, src_map, res_dict):
    if cur_module in res_dict:
        return
    res_dict[cur_module] = src_map[cur_module].count("\n") + 1
    for child_module in hier.get(cur_module, {}).values():
        count_flat(child_module, hier, src_map, res_dict)
        res_dict[cur_module] += res_dict[child_module]

if __name__ == "__main__":
    yqh, nh, kmh, kmhv2 = dict(), dict(), dict(), dict()
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
    yqh_hier = get_hier(yqh)
    nh_hier = get_hier(nh)
    kmh_hier = get_hier(kmh)
    kmhv2_hier = get_hier(kmhv2)
    # output_in_tree(yqh_hier)
    # output_in_tree(nh_hier)
    # output_in_tree(kmh_hier)
    # output_in_tree(kmhv2_hier)
    yqh_count = dict()
    nh_count = dict()
    kmh_count = dict()
    kmhv2_count = dict()
    count_flat("SimTop", yqh_hier, yqh, yqh_count)
    count_flat("SimTop", nh_hier, nh, nh_count)
    count_flat("SimTop", kmh_hier, kmh, kmh_count)
    count_flat("SimTop", kmhv2_hier, kmhv2, kmhv2_count)
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
        }
    }
    # output in csv
    print("Part,Frontend,Backend,MemBlock,ICache,DCache,L2Top")
    for part in ["yqh", "nh", "kmh", "kmhv2"]:
        frontend = res[part]["Frontend"]
        backend = res[part]["Backend"]
        memblock = res[part]["MemBlock"]
        icache = res[part]["ICache"]
        dcache = res[part]["DCache"]
        l2top = res[part]["L2Top"]
        print(f"{part},{frontend},{backend},{memblock},{icache},{dcache},{l2top}")
