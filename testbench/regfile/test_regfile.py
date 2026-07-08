#test_regfile.py

import cocotb
from cocotb.triggers import Timer, RisingEdge
from cocotb.clock import Clock
import random

@cocotb.test()
async def random_write_read_test(dut):
    #start a 10ns clock 
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())
    await RisingEdge(dut.clk)

    #init and reset
    dut.rst_n.value = 0 #reset, active low
    dut.write_enable.value = 0
    dut.addr1.value = 0
    dut.addr2.value = 0
    dut.addr3.value = 0
    dut.write_data.value = 0

    await RisingEdge(dut.clk)
    dut.rst_n.value = 1 #deassert reset
    await RisingEdge(dut.clk)

    #fill a heorical state of the regs, all 0's for starters
    theoretical_regs = [0 for _ in range(32)]

    #loop to write and read random values (1000 tests)
    for _ in range(1000):
        #generate random reg address (1 to 31, skip 0)
        addr1 = random.randint(1, 31)
        addr2 = random.randint(1, 31)
        addr3 = random.randint(1, 31)
        write_value = random.randint(0, 0xFFFFFFFF)

        #perform reads
        await Timer(1, unit="ns")
        dut.addr1.value = addr1
        dut.addr2.value = addr2
        await Timer(1, unit="ns")
        assert dut.read_data1.value == theoretical_regs[addr1]
        assert dut.read_data2.value == theoretical_regs[addr2]

        # perform a random write 
        dut.addr3.value = addr3
        dut.write_enable.value = 1
        dut.write_data.value = write_value
        await RisingEdge(dut.clk)
        dut.write_enable.value = 0 #disable write
        theoretical_regs[addr3] = write_value #update theoretical state
        await Timer(1, unit="ns")

    #try to write at write enable =0 and check that its still 0 
    await Timer(1, unit="ns")
    dut.addr3.value = 0
    dut.write_enable.value = 1
    dut.write_data.value = 0xAEAEAEAE
    await RisingEdge(dut.clk)
    dut.write_enable.value = 0 #disable write
    theoretical_regs[0] = 0 #reg 0 is always 0
    
    await Timer(1, units="ns") # wait a ns to test async read
    dut.addr1.value = 0
    await Timer(1, units="ns")
    print(dut.read_data1.value)
    assert int(dut.read_data1.value) == 0

    print("Random write/read test completed successfully.")