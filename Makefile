YQH_FIR = ../yanqihu/build/rtl/XSTop.fir # git checkout 52bb30fe05350d4756db2626949510dd86a9f0bd && make verilog 
NH_FIR = ../nanhu/build/rtl/XSTop.fir # git checkout ffee184f3d83a9adb2730090d7754bb48b2f33eb && make verilog
KMH_FIR = ../kunminghu/build/XSTop.fir # git checkout 533652847a406411557b4b8cd1b7c3e7f3712ca6 && make verilog MFC=1
KMHV2_FIR = ../kunminghu-v2/build/rtl/XSTop.fir # git checkout 316d62e5952bb47fd7224b5fcf4591813a05e08a && make verilog

FIRTOOL = ~/.cache/llvm-firtool/1.62.1/bin/firtool
FIRTOOL_OPTS = --split-verilog -O=release --disable-annotation-classless --disable-annotation-unknown

result.csv: cal.py verilog/yanqihu/XSTop.sv verilog/nanhu/XSTop.sv verilog/kunminghu/XSTop.sv verilog/kunminghu_v2/XSTop.sv
	./cal.py > result.csv

verilog/yanqihu/XSTop.sv: $(YQH_FIR)
	mkdir -p verilog/yanqihu
	$(FIRTOOL) $(YQH_FIR) -o verilog/yanqihu $(FIRTOOL_OPTS)

verilog/nanhu/XSTop.sv: $(NH_FIR)
	mkdir -p verilog/nanhu
	$(FIRTOOL) $(NH_FIR) -o verilog/nanhu $(FIRTOOL_OPTS)

verilog/kunminghu/XSTop.sv: $(KMH_FIR)
	mkdir -p verilog/kunminghu
	$(FIRTOOL) $(KMH_FIR) -o verilog/kunminghu $(FIRTOOL_OPTS)

verilog/kunminghu_v2/XSTop.sv: $(KMHV2_FIR)
	mkdir -p verilog/kunminghu_v2
	$(FIRTOOL) $(KMHV2_FIR) -o verilog/kunminghu_v2 $(FIRTOOL_OPTS)
