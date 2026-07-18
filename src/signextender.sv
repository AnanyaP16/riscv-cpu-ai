//signextender.sv
module signextender (
    // IN
    input logic [24:0] raw_src, //24 is the max number of bits sent to the sign extender, 25 is the max number of bits sent to the sign extender + 1 bit for the sign bit
    input logic [1:0] imm_source,

    // OUT (immediate)
    output logic [31:0] immediate
);

//i-type:
logic [11:0] gathered_imm;


always_comb begin
    case (imm_source)
        1'b00: gathered_imm = raw_src[24:13]; // I-type
        default: gathered_imm = 12'b0; // Default case, should not happen
    endcase
end

//put bit 12 of the gather imm for the first 20 bits of the immediate, and then concatenate the gathered imm to the last 12 bits of the immediate
assign immediate = {{20{gathered_imm[11]}}, gathered_imm}; // sign extend the immediate value to 32 bits

endmodule
