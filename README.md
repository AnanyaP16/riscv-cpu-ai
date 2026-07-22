# RISC-V CPU + AI MAC Extension

This repository contains a small RISC-V CPU design written in SystemVerilog, along with Cocotb-based verification tests and a Verilator integration setup. The project is currently in an early-stage development cycle focused on building a minimal datapath and validating core modules.

## Project Goal

The long-term goal is to develop a simple RISC-V CPU core that supports basic instructions and can later be extended with an AI-oriented MAC unit. At the moment, the focus is on establishing the core pipeline, instruction/data memory behavior, register file access, and basic ALU/control logic.

## Current Repository Structure

- src/ - SystemVerilog source files for the CPU core
  - alu.sv - ALU implementation
  - control.sv - control unit for decoding and control signal generation
  - cpu.sv - top-level CPU datapath skeleton
  - memory.sv - instruction/data memory module
  - regfile.sv - register file implementation
  - signextender.sv - sign extension logic
- testbench/ - Cocotb tests for each module
  - alu/ - ALU tests
  - control/ - control unit tests
  - cpu/ - CPU datapath tests
  - memory/ - memory tests
  - regfile/ - register file tests
  - signextender/ - sign extender tests
- verilator/ - local Verilator source and build support
- docs/ - documentation and project notes
- waveforms/ - waveform output directory

## Current Progress

The repository currently includes:

- a basic CPU datapath with program counter logic
- instruction memory and data memory modules
- a register file and sign-extension unit
- ALU and control-unit modules
- initial Cocotb-based tests for the CPU and core components

The CPU implementation is progressing from a simple skeleton toward a functional datapath for basic load/store-style instruction execution.

## Verification Status

Tests are being developed under the testbench/ directory using Cocotb. The current work focuses on validating the individual modules first and then integrating them into the full CPU datapath.

## Notes

This project is still under active development. The structure and implementation are expected to evolve as the CPU gains more functionality.
