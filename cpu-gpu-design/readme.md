# tiny-cpu — a minimal 16-bit CPU in Verilog

Single-cycle, 8 registers (R0 always 0), 256-word instruction & data memory.
Verified with Icarus Verilog 12.0.

## Run it
```
iverilog -g2012 -o cpu.out cpu.v cpu_tb.v
vvp cpu.out
```
Expected output ends with `dmem[0] = 15`. Open `cpu.vcd` in GTKWave to see waveforms.

## Instruction set (16-bit words)
| op  | name | format            | effect                                   |
|-----|------|-------------------|------------------------------------------|
| 0x0 | NOP  | —                 | nothing                                  |
| 0x1 | ADD  | rd, rs, rt        | rd = rs + rt                             |
| 0x2 | SUB  | rd, rs, rt        | rd = rs - rt                             |
| 0x3 | AND  | rd, rs, rt        | rd = rs & rt                             |
| 0x4 | OR   | rd, rs, rt        | rd = rs \| rt                            |
| 0x5 | XOR  | rd, rs, rt        | rd = rs ^ rt                             |
| 0x6 | LW   | rd, [rs]          | rd = dmem[rs]                            |
| 0x7 | SW   | [rs], rt          | dmem[rs] = rt                            |
| 0x8 | LI   | rd, imm9          | rd = sign_extend(imm9)                   |
| 0x9 | ADDI | rd, rs, imm6      | rd = rs + sign_extend(imm6)              |
| 0xA | BEQZ | rd, off9          | if rd==0: pc += off (relative to itself) |
| 0xB | JMP  | addr12            | pc = addr                                |
| 0xF | HLT  | —                 | stop                                     |

### Encoding
- R-type: `[op:4][rd:3][rs:3][rt:3][000]`
- LI    : `[1000][rd:3][imm9:9]`
- ADDI  : `[1001][rd:3][rs:3][imm6:6]`
- BEQZ  : `[1010][rd:3][off9:9]`
- JMP   : `[1011][addr12:12]`

## Sample program (program.hex): sum 5+4+3+2+1
```
8200  LI   R1, 0      ; sum = 0
8405  LI   R2, 5      ; i = 5
A404  BEQZ R2, +4     ; if i==0 jump to SW (pc 2 -> 6)
1250  ADD  R1, R1, R2 ; sum += i
94BF  ADDI R2, R2, -1 ; i -= 1
B002  JMP  2          ; loop
7008  SW   [R0], R1   ; dmem[0] = sum
F000  HLT
```
