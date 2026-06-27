# tiny-cpu — explained in plain language

This is a tiny computer chip you built and simulated. This document explains
what it is and how to read it, assuming you're new to all of this.

---

## The big idea

A CPU can only do a small, fixed list of actions — about 12 in this one:
add, subtract, load a number, store to memory, jump, stop, and a few more.
That list is its entire vocabulary. It can't do anything outside it.

A "program" is just a list of these actions, written one per line, that the
CPU runs from top to bottom.

---

## What an opcode is

The CPU can't read words like "add." It only deals in numbers. So every action
is given a number:

| number (hex) | action            | plain meaning              |
|--------------|-------------------|----------------------------|
| 1            | ADD               | add two numbers            |
| 2            | SUB               | subtract                   |
| 7            | SW                | store a value into memory  |
| 8            | LI                | load a number              |
| 9            | ADDI              | add a small fixed number   |
| a            | BEQZ              | jump, but only if zero     |
| b            | JMP               | jump to a line             |
| f            | HLT               | stop                       |

That number — the one that says WHICH action — is called the **opcode**
(short for "operation code"). Think of it like a number on a takeout menu:
"#8" doesn't mean anything special, someone just decided #8 = fried rice.
Here, someone (us) decided 8 = load a number.

The opcode is always the **first character** of an instruction.

---

## How to read program.hex

`program.hex` is your actual program. Open it and you'll see 8 lines:

```
8200      line 0
8405      line 1
a404      line 2
1250      line 3
94bf      line 4
b002      line 5
7008      line 6
f000      line 7
```

Each line is one instruction, made of 4 characters. The FIRST character is the
opcode (the action). The other 3 are details (which register, what number).

Cover the last 3 characters with your finger and read only the first:

```
8200  ->  8  ->  load a number
8405  ->  8  ->  load a number
a404  ->  a  ->  jump if zero
1250  ->  1  ->  add
94bf  ->  9  ->  add a small number
b002  ->  b  ->  jump
7008  ->  7  ->  store to memory
f000  ->  f  ->  stop
```

So the program, in plain English, is:
1. load a starting number
2. load a counter
3. if the counter is zero, jump to the end
4. add the counter to a running total
5. subtract 1 from the counter
6. jump back to step 3
7. store the total into memory
8. stop

That's a loop that adds 5 + 4 + 3 + 2 + 1 = 15.

---

## How to read the waveform (Surfer)

When you simulate, Surfer shows signals changing over time. The useful rows:

- **pc**  = which line the CPU is on right now (the "program counter").
           It goes 0,1,2,3,4,5, then jumps back to 2 and repeats — that's the loop.
- **inst** = the full instruction on that line (e.g. 8200). Same as program.hex.
- **op**  = JUST the first character of inst (e.g. 8). This is the opcode.
           Read it ONE character at a time: "a, 1, 9, b" is four opcodes, not "a1, 9b".
- **R1**  = a register holding the running total. Climbs 0 -> 5 -> 9 -> 12 -> 14 -> 15.
- **R2**  = the counter. Counts down 5 -> 4 -> 3 -> 2 -> 1 -> 0.
- **halted** = goes high at the very end, when the CPU hits "stop".

The key thing to see: `op` is just the first character of `inst`, and `inst` is
just your `program.hex`. They're the same data shown three ways.

---

## How to run it

```
iverilog -g2012 -o cpu.out cpu.v cpu_tb.v
vvp cpu.out
```

You should see R1 = 15 and dmem[0] = 15 at the end. Then open `cpu.vcd` in
Surfer to watch it run.