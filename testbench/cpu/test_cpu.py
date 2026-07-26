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

    # Add Test 
    # lw x19 0x10(x0) (this memory spot contains 0x00000AAA)
    # add x20 x18 x19

    #expected result of reg 18 +reg 19 and store in reg 20
    expected_result = (0xDEADBEEF +0x00000AAA) & 0xFFFFFFFF
    await RisingEdge(dut.clk)
    assert binary_to_hex(dut.regfile.registers[19].value) == "00000AAA" # ensure the right value was loaded from reg 19 
    await RisingEdge(dut.clk)# add x20 x18 x19
    assert binary_to_hex(dut.regfile.registers[20].value) == hex(expected_result)[2:].upper()

    # AND TEST
    # and x21 x18 x20 (result shall be 0xDEAD8889)
    # Use last expected result, as this instr uses last op result register
    expected_result = expected_result & 0xDEADBEEF
    await RisingEdge(dut.clk) # and x21 x18 x20
    assert binary_to_hex(dut.regfile.registers[21].value) == "DEAD8889"

    # OR TEST
    # (Value pre-computed in python)
    # lw x5 0x14(x0) | x5  <= 125F552D
    # lw x6 0x18(x0) | x6  <= 7F4FD46A
    # or x7 x5 x6    | x7  <= 7F5FD56F
    print("\n\nTESTING OR\n\n")
    expected_result = (0x125F552D | 0x7F4FD46A) & 0xFFFFFFFF
    await RisingEdge(dut.clk) # lw x5 0x14(x0) | x5  <= 125F552D
    assert binary_to_hex(dut.regfile.registers[5].value) == "125F552D"
    await RisingEdge(dut.clk) # lw x6 0x18(x0) | x6  <= 7F4FD46A
    assert binary_to_hex(dut.regfile.registers[6].value) == "7F4FD46A"
    await RisingEdge(dut.clk) # or x7 x5 x6    | x7  <= 7F5FD56F
    assert binary_to_hex(dut.regfile.registers[7].value) == "7F5FD56F"
    assert binary_to_hex(dut.regfile.registers[7].value) == hex(expected_result)[2:].upper()


    ##################
    # BEQ TEST
    # 00730663  //BEQ TEST START :    beq x6 x7 0xC       | #1 SHOULD NOT BRANCH
    # 00802B03  //                    lw x22 0x8(x0)      | x22 <= DEADBEEF
    # 01690863  //                    beq x18 x22 0x10    | #2 SHOULD BRANCH (+ offset)
    # 00000013  //                    nop                 | NEVER EXECUTED
    # 00000013  //                    nop                 | NEVER EXECUTED
    # 00000663  //                    beq x0 x0 0xC       | #4 SHOULD BRANCH (avoid loop)
    # 00002B03  //                    lw x22 0x0(x0)      | x22 <= AEAEAEAE
    # FF6B0CE3  //                    beq x22 x22 -0x8    | #3 SHOULD BRANCH (-offset)
    # 00000013  //                    nop                 | FINAL NOP
    ##################
    print("\n\nTESTING BEQ\n\n")

    assert binary_to_hex(dut.instruction.value) == "00730663"

    await RisingEdge(dut.clk) # beq x6 x7 0xC NOT TAKEN
    # Check if the current instruction is the one we expected
    assert binary_to_hex(dut.instruction.value) == "00802B03"

    await RisingEdge(dut.clk) # lw x22 0x8(x0)
    assert binary_to_hex(dut.regfile.registers[22].value) == "DEADBEEF"

    await RisingEdge(dut.clk) # beq x18 x22 0x10 TAKEN
    # Check if the current instruction is the one we expected
    assert binary_to_hex(dut.instruction.value) == "00002B03"

    await RisingEdge(dut.clk) # lw x22 0x0(x0)
    assert binary_to_hex(dut.regfile.registers[22].value) == "AEAEAEAE"

    await RisingEdge(dut.clk) # beq x22 x22 -0x8 TAKEN
    # Check if the current instruction is the one we expected
    assert binary_to_hex(dut.instruction.value) == "00000663"

    await RisingEdge(dut.clk) # beq x0 x0 0xC TAKEN
    # Check if the current instruction is the one we expected
    assert binary_to_hex(dut.instruction.value) == "00000013"