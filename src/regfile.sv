//regfile.sv

module regfile (
    //basic logic (clock and reset)
    input logic clk,
    input logic rst_n,

    //write logic
    input logic write_enable,
    input logic [4:0] addr3,
    input logic [31:0] write_data,

    //read logic
    input logic [4:0] addr1,
    input logic [4:0] addr2,

    output logic [31:0] read_data1,
    output logic [31:0] read_data2
);

reg [31:0] registers [0:31]; // register array of 32 bit registers (addressed with 5 bits)

always @(posedge clk) begin
    // reset logic when rst_n is low
    if(rst_n == 1'b0) begin
        for (int i = 0; i < 32; i++) begin
            registers[i] <= 32'b0; // reset all registers to zero
        end
    end 
    // Write, except on 0, reserved for a zero constant according to RISC-V specs
    else if (write_enable && addr3 != 0) begin
        registers[addr3] <= write_data; // write data to the specified register
    end
end

//read logic, asynchronous reads, no clock edge needed
always_comb begin : read_logic
    read_data1 = registers[addr1]; // read data from the first specified register
    read_data2 = registers[addr2]; // read data from the second specified register
end

endmodule