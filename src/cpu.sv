// cpu.sv -- starting with load word 

module cpu (
    input logic clk,
    input logic rst_n
);

/**
* Program Counter
*/

reg [31:0] pc;
logic [31:0] pc_next;

always_comb begin : pcSelect
    pc_next = pc + 4;
end

always @(posedge clk) begin
    if(rst_n == 0) begin
        pc <= 32'b0;
    end else begin 
        pc <= pc_next;
    end
end

/**
* Instruction Memory
*/

// acts as rom
wire [31:0] instruction;

memory #(
    //passes a parameter to the module telling it to preload its contents from this hexa decimal file with compiled machine code (instructions that the processory will run)
    .WORDS(256),
    .mem_init("./test_imemory.hex") 
) instruction_memory (
    //memory inputs 
    .clk(clk),
    .addr(pc),
    .write_enable(1'b0),
    .write_data(32'b0),
    .rst_n(1'b1),

    //memory outputs
    .read_data(instruction)
);

/**
*Control
*/
//intercepts instructions data, generate control signals accordingly in the control unit

//control input
logic [6:0] op;
assign op = instruction [6:0];
logic [2:0] func3;
assign func3 = instruction[14:12];
logic [6:0] func7;
assign func7= 7'b0;
wire alu_zero;

//control output
wire [2:0] alu_control;
wire [1:0] imm_source;
wire reg_write;
wire mem_write;

control control_unit(
    //control inputs 
    .func3(func3),
    .func7(func7),
    .op(op),
    .alu_zero(alu_zero),

    //control outputs
    .reg_write(reg_write),
    //will be determined within the control.sv file depending on instruction
    .alu_control(alu_control),
    .imm_source(imm_source),
    .mem_write(mem_write)
);

/**
*RegFile
*/

logic [4:0] rs1;
assign rs1 = instruction[19:15]; //rs1
logic [4:0] rs2;
assign rs2 = instruction [24:20]; //rs2

logic [4:0] dest_reg; //dest _reg
assign dest_reg = instruction[11:7];

wire [31:0] read_reg1;
wire [31:0] read_reg2;

logic [31:0] write_back_data;
always_comb begin : wbSelect
//write back to cpu (write data) what was read from data memory
    write_back_data = mem_read;
end

regfile regfile(
    .clk(clk),
    .rst_n(rst_n),

    .write_enable(reg_write),
    .addr3(dest_reg),
    .write_data(write_back_data),

    .addr1(rs1),
    .addr2(rs2),

    .read_data1(read_reg1),
    .read_data2(read_reg2)
);

/**
*Sign Extender
*/

logic [24:0] raw_imm;
assign raw_imm = instruction[31:7];

wire [31:0] immediate;

signextender signext (
    .raw_src(raw_imm),
    .imm_source(imm_source),

    .immediate(immediate)
);

/**
*ALU 
*/

wire [31:0] alu_result;
logic [31:0] alu_srcB;

always_comb begin : srcBSelect
    alu_srcB = immediate;
end
alu alu_instc(
    .opA(read_reg1),
    .opB(alu_srcB),
    .alu_control(alu_control),
    .result(alu_result),
    .zero_flag (alu_zero)
);

/**
*Data Memory
*/

logic [31:0] mem_read;

memory #(
    //passes a parameter to the module telling it to preload its contents from this hexa decimal file with compiled machine code (instructions that the processory will run)
    .WORDS(256),
    .mem_init("./test_dmemory.hex") 
) data_memory (
    //memory inputs 
    .clk(clk),
    .addr(alu_result),
    .write_enable(mem_write),
    .write_data(read_reg2),
    .rst_n(1'b1),

    //memory outputs
    .read_data(mem_read)
);

endmodule