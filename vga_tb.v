`timescale 1ns/1ps
// Renders one full frame of the vga module into frame.ppm (an image file).
module vga_tb;
    reg clk = 0, rst = 1;
    wire [9:0] hpos, vpos;
    wire hsync, vsync, visible;
    wire [3:0] red, green, blue;
    integer f, x, y;
    reg [11:0] fb [0:640*480-1];   // framebuffer we fill during the scan

    vga uut(.clk(clk), .rst(rst), .hpos(hpos), .vpos(vpos),
            .hsync(hsync), .vsync(vsync), .visible(visible),
            .red(red), .green(green), .blue(blue));

    always #20 clk = ~clk;          // 40 ns period ~= 25 MHz

    // capture every visible pixel into the framebuffer by its (row,col)
    always @(negedge clk)
        if (!rst && visible) fb[vpos*640 + hpos] = {red, green, blue};

    initial begin
        repeat (3) @(negedge clk);
        rst = 0;
        // run for a bit more than one full frame (525*800 pixel-clocks)
        repeat (525*800 + 2000) @(negedge clk);
        // dump framebuffer as a PPM image (maxval 15 since colors are 4-bit)
        f = $fopen("frame.ppm", "w");
        $fwrite(f, "P3\n640 480\n15\n");
        for (y=0; y<480; y=y+1)
            for (x=0; x<640; x=x+1)
                $fwrite(f, "%0d %0d %0d\n",
                    fb[y*640+x][11:8], fb[y*640+x][7:4], fb[y*640+x][3:0]);
        $fclose(f);
        $display("Wrote frame.ppm (640x480)");
        $finish;
    end
endmodule
