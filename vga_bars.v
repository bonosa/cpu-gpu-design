// vga.v - VGA 640x480 @ 60Hz timing generator + test pattern
// This is the "GPU": it sweeps across the screen pixel by pixel and
// decides a color for each one. Same module you'd flash to the Tang Nano.
module vga (
    input  wire        clk,       // pixel clock (~25 MHz on the real board)
    input  wire        rst,
    output reg  [9:0]  hpos,      // current column, 0..799
    output reg  [9:0]  vpos,      // current row,    0..524
    output wire        hsync,     // horizontal sync pulse to the monitor
    output wire        vsync,     // vertical sync pulse to the monitor
    output wire        visible,   // high only inside the 640x480 picture area
    output wire [3:0]  red,
    output wire [3:0]  green,
    output wire [3:0]  blue
);
    // ---- standard 640x480 @ 60Hz timing numbers ----
    localparam H_VISIBLE=640, H_FRONT=16, H_SYNC=96, H_BACK=48;  // -> 800 total
    localparam V_VISIBLE=480, V_FRONT=10, V_SYNC=2,  V_BACK=33;  // -> 525 total
    localparam H_TOTAL = H_VISIBLE+H_FRONT+H_SYNC+H_BACK;        // 800
    localparam V_TOTAL = V_VISIBLE+V_FRONT+V_SYNC+V_BACK;        // 525

    // ---- raster scan: walk left->right, then top->bottom ----
    always @(posedge clk or posedge rst) begin
        if (rst) begin
            hpos <= 0; vpos <= 0;
        end else if (hpos == H_TOTAL-1) begin
            hpos <= 0;
            vpos <= (vpos == V_TOTAL-1) ? 0 : vpos + 1;
        end else begin
            hpos <= hpos + 1;
        end
    end

    // ---- sync pulses (active low in this video mode) ----
    assign hsync = ~((hpos >= H_VISIBLE+H_FRONT) && (hpos < H_VISIBLE+H_FRONT+H_SYNC));
    assign vsync = ~((vpos >= V_VISIBLE+V_FRONT) && (vpos < V_VISIBLE+V_FRONT+V_SYNC));

    // ---- visible picture area? ----
    assign visible = (hpos < H_VISIBLE) && (vpos < V_VISIBLE);

    // ---- the "painter": choose a color for pixel (hpos, vpos) ----
    wire [2:0] bar = hpos / 80;     // which of the 8 vertical bars (0..7)
    reg [11:0] rgb;                 // packed {R[4], G[4], B[4]}, 0=off 15=full
    always @(*) begin
        if (!visible)
            rgb = 12'h000;                                   // blanking -> black
        else if (hpos<3 || hpos>=637 || vpos<3 || vpos>=477)
            rgb = 12'hFFF;                                   // white screen border
        else case (bar)
            3'd0: rgb = 12'hFFF; // white
            3'd1: rgb = 12'hFF0; // yellow
            3'd2: rgb = 12'h0FF; // cyan
            3'd3: rgb = 12'h0F0; // green
            3'd4: rgb = 12'hF0F; // magenta
            3'd5: rgb = 12'hF00; // red
            3'd6: rgb = 12'h00F; // blue
            default: rgb = 12'h000; // black
        endcase
    end
    assign {red, green, blue} = rgb;
endmodule
