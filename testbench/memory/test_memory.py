#test_memory.py

import cocotb
from cocotb.triggers import Timer, RisingEdge
from cocotb.clock import Clock

@cocotb.test()
async def memory_data_test(dut):
    #start a 10ns clock, dut is design under test
    cocotb.start_soon(Clock(dut.clk, 1, unit="ns").start())
    await RisingEdge(dut.clk)

    #test reset
    dut.rst_n.value = 0 #reset, active low
    dut.write_enable.value = 0
    dut.addr.value = 0
    dut.write_data.value = 0

    await RisingEdge(dut.clk)
    dut.rst_n.value = 1 #deassert reset
    await RisingEdge(dut.clk)

    #all is 0 after rest
    for addr in range(dut.WORDS.value):
        dut.addr.value = addr
        await Timer(1, unit="ns")
        assert dut.read_data.value == "00000000000000000000000000000000"

    #test write and read back data 
    #data in (memory addr, data value) tuple formate
    #memory address increments by 4, every 4 bytes for the 32 bit hexadeicaml value
    test_data = [
        (0, 0xDEADBEEF),
        (4, 0xCAFEBABE),
        (8, 0x12345678), 
        (12, 0xA5A5A5A5)
    ]

    for addr, data in test_data:
        dut.addr.value = addr 
        dut.write_data.value = data
        dut.write_enable.value = 1 #enable write
        await RisingEdge(dut.clk)

        dut.write_enable.value = 0 #disable write
        await RisingEdge(dut.clk)

        #verify write by reading back 
        dut.addr.value = addr
        await RisingEdge(dut.clk)
        assert dut.read_data.value == data

    #Test: write to multiple addresses and read back
    for i in range(40,4):
        dut.addr.value = i
        dut.write_data.value = i + 100
        dut.write_enable.value = 1
        await RisingEdge(dut.clk)

    #disable write and read back data
    dut.write_enable.value = 0
    #for i less than 40, read back the data and verify, increment i by 4 every loop
    for i in range(40,4):
        dut.addr.value = i
        await RisingEdge(dut.clk)
        expected_value = i + 100
        assert dut.read_data.value == expected_value


