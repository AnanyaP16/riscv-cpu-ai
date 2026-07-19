//memory.sv

module memory #(
    parameter WORDS = 64,
    parameter mem_init = ""
) (
    input logic clk, 
    input logic [31:0] addr,
    input logic write_enable,
    input logic [31:0] write_data,
    //reset logic reset,
    input logic rst_n,

    output logic [31:0] read_data
);
/*
Memory is byte addressed,
so each individual byte of data(8bits) has its own unique physical address
but have no support for mis-aligned write or reads
-- what does this mean
*/
 // may need later 
//localparam ADDR_BITS = $clog2(WORDS);   // <-- add this

reg [31:0] mem [0:WORDS-1]; // memory array of 32 bit words

//added for verification 
initial begin 
    $readmemh(mem_init, mem); // load mem for sim
end

//at rising clock edge this block is executed
always @(posedge clk) begin
    // reset logic when rst_n is low
    if(rst_n == 1'b0) begin
        for (int i = 0; i < WORDS; i++) begin
            mem[i] <= 32'b0; // reset all memory locations to zero
        end
    end else if (write_enable) begin
        //ensure the address is aligned to a word boundary (4 bytes)
        //if not ignore the write 
        if(addr[1:0] == 2'b00) begin
            //address 31:2 is the word index
            mem[addr[31:2]] <= write_data;
            //mem[addr[ADDR_BITS+1:2]] <= write_data;   // <-- changed from addr[31:2]
        end
    end
end

//read logic 
always_comb begin
    //address 31:2 is the word index
    read_data = mem[addr[31:2]]; // read data from memory at the given address
    //mem[addr[ADDR_BITS+1:2]] <= write_data;   // <-- changed from addr[31:2]
end

endmodule