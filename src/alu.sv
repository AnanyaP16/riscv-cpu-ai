//alu.sv
module alu (
    input logic [31:0] opA,
    input logic [31:0] opB,
    input logic [2:0] alu_control, // control signal to select the operation
    
    output logic [31:0] result,
    output logic zero_flag // flag to indicate if the result is zero
);

always_comb begin
    case (alu_control)
        //basic case, of alu is 0 then add the two inputs
        3'b000: result = opA + opB; // ADD
        3'b011: result = opA & opB; // ADD
        3'b010: result = opA | opB; // OR
        // 3'b001: Subtracts opB from opA using two's complement (opA + ~opB + 1)
        3'b001: result = opA +(~opB + 1'b1);
        default: result = 32'b0; // Default case, should not happen
    endcase
end
    assign zero_flag = (result == 32'b0); // Set zero flag if result is zero
endmodule