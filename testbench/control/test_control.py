import cocotb
from cocotb.triggers import Timer
import random
from cocotb.types import LogicArray


async def set_unknown(dut):
    # Set all input to unknown before each test
    await Timer(1, units="ns")
    dut.op.value = LogicArray("XXXXXXX")
    #
    # Uncomment the following throughout the course when needed
    #
    # dut.func3.value = BinaryValue("XXX")
    # dut.func7.value = BinaryValue("XXXXXXX")
    # dut.alu_zero.value = BinaryValue("X")
    # dut.alu_last_bit.value = BinaryValue("X")
    await Timer(1, units="ns")

@cocotb.test()
async def lw_control_test(dut):
    await set_unknown(dut)
    # TEST CONTROL SIGNALS FOR LW
    await Timer(1, units="ns")
    dut.op.value = 0b0000011 #lw
    await Timer(1, units="ns")
    #logic block control signals
    assert dut.alu_control.value == "000"
    assert dut.imm_source.value == "00"
    assert dut.mem_write.value == "0"
    assert dut.reg_write.value == "1"
    
    #datapass mux signals 
    assert dut.alu_src.value == "1"
    assert dut.wb_src.value == "1"
    assert dut.pc_src.value == "0"

@cocotb.test()
async def sw_control_test(dut):
    await set_unknown(dut)
    # TEST CONTROL SIGNALS FOR SW
    await Timer(10, units="ns")
    dut.op.value = 0b0100011 #sw
    await Timer(1, units="ns")

    assert dut.alu_control.value == "000"
    assert dut.imm_source.value == "01"
    assert dut.mem_write.value == "1"
    assert dut.reg_write.value == "0"

    #datapass mux signals
    assert dut.alu_src.value == "1"
    assert dut.pc_src.value == "0"

@cocotb.test()
async def r_add_control_test(dut):
    await set_unknown(dut)
    # TEST CONTROL SIGNALS FOR R-type Add
    await Timer(10, units="ns")
    dut.op.value = 0b0110011 #R ADD
    await Timer(1, units="ns")
    
    assert dut.alu_control.value == "000"
    #assert dut.imm_source.value == "01"
    assert dut.mem_write.value == "0"
    assert dut.reg_write.value == "1"

    #datapass mux signals
    assert dut.alu_src.value == "0"
    assert dut.wb_src.value == "0"
    assert dut.pc_src.value == "0"


@cocotb.test()
async def r_and_control_test(dut):
    await set_unknown(dut)
    # TEST CONTROL SIGNALS FOR R-type And
    await Timer(10, units="ns")
    dut.op.value = 0b0110011 #R-type
    dut.func3.value = 0b111
    await Timer(1, units="ns")
    
    assert dut.alu_control.value == "011" #and
    #assert dut.imm_source.value == "01"
    assert dut.mem_write.value == "0"
    assert dut.reg_write.value == "1"
    
    #datapass mux signals
    assert dut.alu_src.value == "0"
    assert dut.wb_src.value == "0"
    assert dut.pc_src.value == "0"

@cocotb.test()
async def beg_control_test(dut):
    await set_unknown(dut)
    # TEST CONTROL SIGNALS FOR R-type And
    await Timer(10, units="ns")
    dut.op.value = 0b1100011 #B-type
    dut.alu_zero.value = 0b0
    #do we need this? i dont think so for the current test and setup
    #dut.func3.value = 0b000 #beq
    await Timer(1, units="ns")
    
    assert dut.alu_control.value == "001" #or
    assert dut.imm_source.value == "10"
    assert dut.mem_write.value == "0"
    assert dut.reg_write.value == "0"
    assert dut.branch.value == "1"
    assert dut.pc_src.value == "0"

    #datapass mux signals
    assert dut.alu_src.value == "0"
    #assert dut.wb_src.value == "0"

    #test if branching condition is met
    await Timer(3, units="ns")
    dut.alu_zero.value = 0b1
    await Timer(1, units="ns")
    assert dut.pc_src.value == "1"

