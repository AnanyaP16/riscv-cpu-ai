#Makefile
SIM ?= verilator
TOPLEVEL_LANG ?= verilog

#enables waveform dumpting generating .vcd or .fst trace files to visually inspect clock cylces wires and registers in a wave viewer like GTKWave
EXTRA_ARGS += --trace --trace-structs
WAVES = 1

VERILOG_SOURCES += $(PWD)/../../src/memory.sv
# use VHDL_SOURCES for VHDL files

# COCOTB_TOPLEVEL is the name of the toplevel module in your Verilog or VHDL file
COCOTB_TOPLEVEL = memory

# COCOTB_TEST_MODULES is the basename of the Python test file(s)
COCOTB_TEST_MODULES = test_memory

#suppress bit extraction warnings from verilator when using structs and arrays
EXTRA_ARGS += --trace --trace-structs -Wno-WIDTHTRUNC

# include cocotb's make rules to take care of the simulator setup
include $(shell cocotb-config --makefiles)/Makefile.sim