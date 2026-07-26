// control.sv -- control unit starting with load word 

module control(
    input logic[2:0] func3,
    input logic[6:0] func7,
    input logic[6:0] op, 
    input logic alu_zero,


    output logic reg_write,
    output logic [2:0]alu_control,
    output logic [1:0]imm_source,
    output logic mem_write,

    output logic alu_src,
    output logic wb_src, //result_src (write back?)
    output logic pc_src
);

/*
Main Decoder
*/
logic [1:0] alu_op;
logic branch;
always_comb begin
    case (op)
        //LW
        7'b0000011: begin
            reg_write = 1'b1;
            imm_source = 2'b00;
            alu_src = 1'b1;
            mem_write = 1'b0;
            wb_src = 1'b1;
            alu_op = 2'b00;
            branch = 1'b0;
        end
        //SW
        7'b0100011: begin 
            reg_write = 1'b0;
            imm_source= 2'b01;
            alu_src = 1'b1;
            mem_write = 1'b1;
            alu_op = 2'b00;
            branch = 1'b0;
        end
        //R-TYPE
        7'b0110011: begin 
            reg_write = 1'b1;
            alu_src = 1'b0;
            mem_write = 1'b0;
            wb_src = 1'b0;
            alu_op = 2'b10;
            branch = 1'b0;
        end
        //BEQ
        7'b1100011: begin 
            reg_write = 1'b0;
            imm_source= 2'b10;
            alu_src = 1'b0;
            mem_write = 1'b0;
            alu_op = 2'b01;
            branch = 1'b1;
        end
        //Everything else
        default: begin
            reg_write = 1'b0;
            imm_source = 2'b00;
            mem_write = 1'b0;
            alu_op = 2'b00;
            alu_src = 1'b0;
            branch = 1'b0;
            wb_src = 1'b0;
        end
    endcase
end

/*
ALU Decoder
*/
always_comb begin
    case (alu_op)
        //LW, SW
        2'b00 : alu_control = 3'b000;
        2'b01 : alu_control = 3'b001;
        2'b10 : begin
            case(func3)
                // ADD -- will later add sub, with a different func7 value
                3'b000 : alu_control = 3'b000;
                //AND
                3'b111 : alu_control = 3'b011;
                //OR
                3'b110 : alu_control = 3'b010;
                default: alu_control = 3'b111;
            endcase
        end
        default: alu_control = 3'b111;
    endcase
end

assign pc_src = (alu_zero & (op == 7'b1100011));

endmodule