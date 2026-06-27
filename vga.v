// vga.v - VGA 640x480 @ 60Hz video module
// Draws a red box in the middle of a blue screen.
module vga (
    input  wire        clk,       // pixel clock (~25 MHz on the real board)
    input  wire        rst,
    output reg  [9:0]  hpos,      // current column, 0..799
    output reg  [9:0]  vpos,      // current row,    0..524
    output wire        hsync,
    output wire        vsync,
    output wire        visible,
    output wire [3:0]  red,
    output wire [3:0]  green,
    output wire [3:0]  blue
);
    localparam H_VISIBLE=640, H_FRONT=16, H_SYNC=96, H_BACK=48;  // 800 total
    localparam V_VISIBLE=480, V_FRONT=10, V_SYNC=2,  V_BACK=33;  // 525 total
    localparam H_TOTAL = H_VISIBLE+H_FRONT+H_SYNC+H_BACK;
    localparam V_TOTAL = V_VISIBLE+V_FRONT+V_SYNC+V_BACK;

    // raster scan: left->right, then top->bottom
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

    assign hsync = ~((hpos >= H_VISIBLE+H_FRONT) && (hpos < H_VISIBLE+H_FRONT+H_SYNC));
    assign vsync = ~((vpos >= V_VISIBLE+V_FRONT) && (vpos < V_VISIBLE+V_FRONT+V_SYNC));
    assign visible = (hpos < H_VISIBLE) && (vpos < V_VISIBLE);

    // ---- the painter: choose a color for pixel (hpos, vpos) ----
    // The box spans columns 220..419 and rows 165..314 (a 200x150 box,
    // centered on the 640x480 screen). Inside the box = red. Outside = blue.
    reg [11:0] rgb;
    always @(*) begin
        if (!visible)
            rgb = 12'h000;                              // off-screen -> black
        else if (hpos>=220 && hpos<420 && vpos>=165 && vpos<315)
            rgb = 12'hF00;                              // red box in the middle
        else
            rgb = 12'h00F;                              // blue background
    end
    assign {red, green, blue} = rgb;
endmodule
