import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer
import random 
import numpy as np 

@cocotb.test
async def random_write_read_test(dut):
    #TEST POS IMM =123 W/ SOURCE = 0 
    imm = 0b000001111011 # 123 - 13 bits
    imm <<= 13 # leave room for random junk
    source = 0b00
    #25 bits sent to sign extend contains data before that will be ignored (rd, f3, ..)
    #masked to leave room for imm "test payload"

    random_junk = 0b000000000000_1010101010101 
    raw_data = random_junk | imm

    await Timer(1, units="ns")
    dut.raw_src.value = raw_data
    dut.imm_source.value = source
    await Timer(1, units="ns") #let it propagate ...
    assert dut.immediate.value == "00000000000000000000000001111011" #32 bits, what it should be 
    assert int(dut.immediate.value) == 123

    #test negative imm = -42 with source = 0 
    imm = 0b111111010110 #-42
    imm <<=13 # leave "room" for random junk 
    source = 0b00
     # masked to leave room for imm "test payload"
    random_junk = 0b000000000000_1010101010101 
    raw_data = random_junk | imm
    await Timer(1, units="ns")
    dut.raw_src.value = raw_data
    dut.imm_source.value = source
    await Timer(1, units="ns") # let it propagate ...
    assert dut.immediate.value == "11111111111111111111111111010110"
    # Python interprets int as uint. we sub 1<<32 as int to get corresponding negative value
    assert int(dut.immediate.value) - (1 << 32)  == -42