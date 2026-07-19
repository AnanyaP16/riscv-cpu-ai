#test_cpu.py

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge 

#helper functions
def binary_to_hex(bin_str):
    #convert binary string to hexadecimal 
    hex_str = hex(int(str(bin_str),2))[2:]
    hex_str = hex_str.zfill(8)
    return hex_str.upper()

def hex_to_bin(hex_str):
    #convert hex str to bin
    bin_str = bin(int(str(hex_str), 16))[2:]
    bin_str = bin_str.zfill(32)
    return bin_str.upper()

async def cpu_reset(dut):
    #init and rest 
    dut.rst_n.value=0
    await RisingEdge(dut.clk) #wait for clock edge after reset 
    dut.rst_n.value = 1 #de-assert reset
    await RisingEdge(dut.clk) #wait for a clock edge after reset 

#@cocotb.test()
#async def cpu_init_test(dut):
#    """Reset the CPU and check for a good imem read"""
#    cocotb.start_soon(Clock(dut.clk, 1, units="ns").start())
#    await RisingEdge(dut.clk)

#    await cpu_reset(dut)
#    assert binary_to_hex(dut.pc.value) == "00000000"

    # Load the expected instruction memory as binary 
    # Loaded in sim direction thrugh verilog code 
    # load is only for expected 
#    imem = []
#    with open("test_imemory.hex", "r") as file: 
#        for line in file:
            #ignore comments 
#            line_content = line.split("//")[0].strip()
#            if line_content:
#                imem.append(hex_to_bin(line_content))
    
    # We limit this inital test to the first couple of instruction 
    # will later implement branches 
#    for counter in range(5):
#        expected_instruction = imem[counter]
#        assert dut.instruction.value == expected_instruction 
#        await RisingEdge(dut.clk)

@cocotb.test()
async def cpu_insrt_test(dut):
    """Runs a lw datapath test"""
    cocotb.start_soon(Clock(dut.clk, 1, units= "ns").start())
    await RisingEdge(dut.clk)

    await cpu_reset(dut)
    print("\n\nTESTING LW\n\n")

    # The first instruction for the test in imem.hex load the data from
    # dmem @ adress 0x00000008 that happens to be 0xDEADBEEF into register x18

    # Wait a clock cycle for the instruction to execute
    await RisingEdge(dut.clk)

    print(binary_to_hex(dut.regfile.registers[18].value))

    #Check the value of reg x18 
    assert binary_to_hex(dut.regfile.registers[18].value) == "DEADBEEF"

    print("\n\nTESTING SW\n\n")
    test_address = int(0xC / 4) #mem is byte adressed but is made out of words in the eyes of the software
    # The second instruction for the test in imem.hex stores the data from
    # x18 (that happens to be 0xDEADBEEF from the previous LW test) @ adress 0x0000000C

    #check inital value
    print(binary_to_hex(dut.data_memory.mem[test_address].value))
    assert binary_to_hex(dut.data_memory.mem[test_address].value) == "F2F2F2F2"

    #wait clock cucle for the instruction to execute 
    await RisingEdge(dut.clk)
    
    # check valu at test_address
    print(binary_to_hex(dut.data_memory.mem[test_address].value))
    assert binary_to_hex(dut.data_memory.mem[test_address].value) == "DEADBEEF"
