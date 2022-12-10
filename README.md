# RiscV

A RiscV disassembler for all flavors of RiscV.

## Supported extensions

This plugin can disassemble `RiscV32`, `RiscV64` and `RiscV128`. 
Additionally all floating point extensions (`F`, `D`, `Q`) can be selected.  
All XLEN versions include most ratified non floating point extensions:
* `Zifencei` (Fence instructions)
* `I` (Base integer instructions)
* `M` (Multiplication/Division instructions)
* `A` (Atomic instructions)
* `Zicsr` (Control and Status Register instructions)
* `C` (Compressed instructions)

Since the `E` extension is a strict subset of the base `I` extension it is excluded.

Additionally all privileged instructions are supported.

## Todo

* [] RiscV32
* [] RiscV64
* [] RiscV128

* [] F Extension
* [] D Extension
* [] Q Extension

* [] Zifenci Extension
* [] I Extension
* [] M Extension
* [] A Extension
* [] Zicsr Extension
* [] C Extension

* [] Supervisor mode