import cocotb
from cocotb.triggers import Timer
import random


#helper functions
def binary_to_hex(bin_str):
    #convert binary string to hexadecimal 
    hex_str = hex(int(str(bin_str),2))[2:]
    hex_str = hex_str.zfill(8)
    return hex_str.upper()
    
@cocotb.test()
async def sub_test(dut):
    await Timer(1, units='ns')
    dut.alu_control.value = 0b001  # Set ALU control to subtraction
    for _ in range(1000):
        opA = random.randint(0, 0xFFFFFFFF)
        opB = random.randint(0, 0xFFFFFFFF)
        dut.opA.value = opA
        dut.opB.value = opB
        expected = (opA - opB) & 0xFFFFFFFF  # Ensure 32-bit result
        await Timer(1, units='ns')  # Wait for the ALU to compute
        
        # additional assert tests
        assert str(dut.result.value) == bin(expected)[2:].zfill(32)
        assert binary_to_hex(dut.result.value) == hex(expected)[2:].zfill(8).upper()
        assert int(str(dut.result.value),2) == expected
        
        #quick test
        assert int(dut.result.value) == expected

@cocotb.test()
async def or_test(dut):
    await Timer(1, units='ns')
    dut.alu_control.value = 0b010  # Set ALU control to addition
    for _ in range(1000):
        opA = random.randint(0, 0xFFFFFFFF)
        opB = random.randint(0, 0xFFFFFFFF)
        dut.opA.value = opA
        dut.opB.value = opB
        expected = (opA | opB)  # Ensure 32-bit result
        await Timer(1, units='ns')  # Wait for the ALU to compute
        assert int(dut.result.value) == expected


@cocotb.test()
async def and_test(dut):
    await Timer(1, units='ns')
    dut.alu_control.value = 0b011  # Set ALU control to addition
    for _ in range(1000):
        opA = random.randint(0, 0xFFFFFFFF)
        opB = random.randint(0, 0xFFFFFFFF)
        dut.opA.value = opA
        dut.opB.value = opB
        expected = (opA & opB)  # Ensure 32-bit result
        await Timer(1, units='ns')  # Wait for the ALU to compute
        assert int(dut.result.value) == expected

@cocotb.test()
async def add_test(dut):
    await Timer(1, units='ns')
    dut.alu_control.value = 0b000  # Set ALU control to addition
    for _ in range(1000):
        opA = random.randint(0, 0xFFFFFFFF)
        opB = random.randint(0, 0xFFFFFFFF)
        dut.opA.value = opA
        dut.opB.value = opB
        expected = (opA + opB) & 0xFFFFFFFF  # Ensure 32-bit result
        await Timer(1, units='ns')  # Wait for the ALU to compute
        assert int(dut.result.value) == expected

@cocotb.test()
async def default_test(dut):
    await Timer(1, units='ns')
    dut.alu_control.value = 0b111  # Set ALU control to an undefined operation
    opA = random.randint(0, 0xFFFFFFFF)
    opB = random.randint(0, 0xFFFFFFFF)
    dut.opA.value = opA
    dut.opB.value = opB

    await Timer(1, units='ns')  # Wait for the ALU to compute
    assert int(dut.result.value) == 0  # Assuming the default result is 0 for undefined operations

@cocotb.test()
async def zero_test(dut):
    await Timer(1, units='ns')
    dut.alu_control.value = 0b000  # Set ALU control to addition
    dut.opA.value = 123
    dut.opB.value = -123
    await Timer(1, units='ns')  # Wait for the ALU to compute
    print(int(dut.result.value))
    assert int(dut.zero_flag.value) == 1  # Zero flag should be set
    assert int(dut.result.value) == 0  # Result should be zero