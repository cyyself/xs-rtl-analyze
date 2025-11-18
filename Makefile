YQH_FIR = ../yanqihu/build/rtl/SimTop.fir
NH_FIR = ../nanhu/build/rtl/SimTop.fir
KMH_FIR = ../kunminghu/build/SimTop.fir
KMHV2_FIR = ../XiangShan/build/rtl/SimTop.fir

FIRTOOL = ~/.cache/llvm-firtool/1.62.1/bin/firtool
FIRTOOL_OPTS = --split-verilog -O=release --disable-annotation-classless --disable-annotation-unknown

result.csv: cal.py verilog/yanqihu/SimTop.sv verilog/nanhu/SimTop.sv verilog/kunminghu/SimTop.sv verilog/kunminghu_v2/SimTop.sv
	./cal.py > result.csv

verilog/yanqihu/SimTop.sv: $(YQH_FIR)
	mkdir -p verilog/yanqihu
	$(FIRTOOL) $(YQH_FIR) -o verilog/yanqihu $(FIRTOOL_OPTS)

verilog/nanhu/SimTop.sv: $(NH_FIR)
	mkdir -p verilog/nanhu
	$(FIRTOOL) $(NH_FIR) -o verilog/nanhu $(FIRTOOL_OPTS)

verilog/kunminghu/SimTop.sv: $(KMH_FIR)
	mkdir -p verilog/kunminghu
	$(FIRTOOL) $(KMH_FIR) -o verilog/kunminghu $(FIRTOOL_OPTS)

verilog/kunminghu_v2/SimTop.sv: $(KMHV2_FIR)
	mkdir -p verilog/kunminghu_v2
	$(FIRTOOL) $(KMHV2_FIR) -o verilog/kunminghu_v2 $(FIRTOOL_OPTS)
