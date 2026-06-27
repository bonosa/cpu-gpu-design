// cpu.v - minimal single-cycle 16-bit CPU
// 8 registers (R0 hardwired to 0), 256-word instruction & data memory.
module cpu (
    input  wire        clk,
    input  wire        rst,
    output reg         halted
);
    reg [15:0] imem [0:255];   // instruction memory
    reg [15:0] dmem [0:255];   // data memory
    reg [15:0] regs [0:7];     // register file
    reg [7:0]  pc;
    wire [15:0] R1 = regs[1];   // for waveform viewing
    wire [15:0] R2 = regs[2];

    // ---- instruction decode (combinational) ----
    wire [15:0] inst  = imem[pc];
    wire [3:0]  op    = inst[15:12];
    wire [2:0]  rd    = inst[11:9];
    wire [2:0]  rs    = inst[8:6];
    wire [2:0]  rt    = inst[5:3];
    wire [8:0]  imm9  = inst[8:0];
    wire [5:0]  imm6  = inst[5:0];
    wire [11:0] imm12 = inst[11:0];

    wire signed [15:0] sext9 = {{7{imm9[8]}}, imm9};
    wire signed [15:0] sext6 = {{10{imm6[5]}}, imm6};

    // register reads (R0 always reads 0)
    wire [15:0] vs = (rs==0) ? 16'd0 : regs[rs];
    wire [15:0] vt = (rt==0) ? 16'd0 : regs[rt];
    wire [15:0] vd = (rd==0) ? 16'd0 : regs[rd];

    integer i;
    always @(posedge clk or posedge rst) begin
        if (rst) begin
            pc <= 0; halted <= 0;
            for (i=0;i<8;i=i+1) regs[i] <= 0;
        end else if (!halted) begin
            case (op)
                4'h0: pc <= pc+1;                                        // NOP
                4'h1: begin if(rd!=0) regs[rd] <= vs + vt; pc<=pc+1; end // ADD  rd,rs,rt
                4'h2: begin if(rd!=0) regs[rd] <= vs - vt; pc<=pc+1; end // SUB
                4'h3: begin if(rd!=0) regs[rd] <= vs & vt; pc<=pc+1; end // AND
                4'h4: begin if(rd!=0) regs[rd] <= vs | vt; pc<=pc+1; end // OR
                4'h5: begin if(rd!=0) regs[rd] <= vs ^ vt; pc<=pc+1; end // XOR
                4'h6: begin if(rd!=0) regs[rd] <= dmem[vs[7:0]]; pc<=pc+1; end // LW  rd,[rs]
                4'h7: begin dmem[vs[7:0]] <= vt; pc<=pc+1; end           // SW  [rs],rt
                4'h8: begin if(rd!=0) regs[rd] <= sext9; pc<=pc+1; end   // LI  rd,imm9
                4'h9: begin if(rd!=0) regs[rd] <= vs + sext6; pc<=pc+1; end // ADDI rd,rs,imm6
                4'hA: begin if(vd==0) pc <= pc + sext9[7:0]; else pc<=pc+1; end // BEQZ rd,off (rel to this instr)
                4'hB: pc <= imm12[7:0];                                  // JMP addr
                4'hF: halted <= 1;                                       // HLT
                default: pc <= pc+1;
            endcase
        end
    end
endmodule
