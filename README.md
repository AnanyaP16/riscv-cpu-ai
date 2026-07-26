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
The repository currently includes the following implemented components and their test coverage status:

- `Program Counter` (`cpu.sv`): implemented and advancing by 4 each cycle.
- `Instruction Memory` / `Data Memory` (`memory.sv`): implemented with parameterized word count and support for initializing from hex files (`test_imemory.hex`, `test_dmemory.hex`). Used by the CPU and exercisable from tests.
- `Register File` (`regfile.sv`): implemented; read/write interface present. Exercised by the CPU tests.
- `Sign Extender` (`signextender.sv`): implemented and used by the CPU immediate path.
- `ALU` (`alu.sv`): implemented. Unit tests exist under `testbench/alu/test_alu.py` covering addition, default operation, and zero-flag behavior.
- `Control Unit` (`control.sv`): skeleton/decoder implemented to produce `alu_control`, `imm_source`, `reg_write`, and `mem_write` signals. Tests are present under `testbench/control/`.
- `CPU Top-level` (`cpu.sv`): datapath skeleton implemented with PC, imem, databack path (load/store example), register file integration, ALU hookup, and sign-extension. A Cocotb test (`testbench/cpu/test_cpu.py`) includes a `cpu_insrt_test` that validates a simple `lw`/`sw` datapath scenario (loads `DEADBEEF` into a register then stores it).

Status summary: core datapath modules are present and unit-tested individually. The full CPU pipeline is in progress; basic load/store instruction flow is exercised by the existing CPU test, while some integration tests (for branches, full ISA support, and exception handling) are not yet implemented.

## Verification Status

Verification is organized under `testbench/` with a Makefile per target (for example, `testbench/cpu/Makefile`) configured for Verilator + Cocotb. Current state:

- Unit tests: `alu`, `regfile`, `memory`, `signextender`, and `control` have accompanying Cocotb tests (see their folders in `testbench/`).
- CPU tests: `testbench/cpu/test_cpu.py` includes `cpu_insrt_test` for a load/store flow. An initialization/reset test is present but commented out for now.


## Notes

This project is still under active development. The structure and implementation are expected to evolve as the CPU gains more functionality.

## Next Steps / Roadmap

- Complete and extend the `control` unit to cover additional RISC-V instruction types.
- Expand `testbench/cpu` tests to validate branching and ALU instructions.
- Implement and integrate an AI MAC unit once the scalar datapath is stable.
