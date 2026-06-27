`timescale 1ns/1ps
module cpu_tb;
    reg clk = 0, rst = 1;
    wire halted;
    integer i;
    cpu uut (.clk(clk), .rst(rst), .halted(halted));
    always #5 clk = ~clk;               // 100 MHz

    initial begin
        $dumpfile("cpu.vcd"); $dumpvars(0, cpu_tb);
        $readmemh("program.hex", uut.imem);
        #12 rst = 0;                     // release reset
        wait (halted == 1); #10;
        $display("== CPU halted ==");
        for (i=0;i<8;i=i+1)
            $display("R%0d = %0d (0x%04h)", i, uut.regs[i], uut.regs[i]);
        $display("dmem[0] = %0d (0x%04h)", uut.dmem[0], uut.dmem[0]);
        $finish;
    end
    initial begin #10000 $display("TIMEOUT (no HLT)"); $finish; end
endmodule
