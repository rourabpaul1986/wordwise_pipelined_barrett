library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;
use work.variant_pkg.all;
entity SRM_fault is
    Port (
        clk   : in  STD_LOGIC;
        rst   : in  STD_LOGIC;
        c0    : in  STD_LOGIC;
        c1    : in  STD_LOGIC;
        c2    : in  STD_LOGIC;
        c3    : in  STD_LOGIC;
        done_rcom : in  STD_LOGIC;
        fault : out STD_LOGIC
    );
end SRM_fault;
--Statistical Reduction Monitoring for Fault Detection
architecture Behavioral of SRM_fault is
    signal fault_reg : STD_LOGIC;
    signal c0_count : UNSIGNED(31 downto 0) := (others => '0');
    signal c1_count : UNSIGNED(31 downto 0) := (others => '0');
    signal c2_count : UNSIGNED(31 downto 0) := (others => '0');
    signal c3_count : UNSIGNED(31 downto 0) := (others => '0');
    signal c0_fault : STD_LOGIC;
    signal c1_fault : STD_LOGIC;
    signal c2_fault : STD_LOGIC;
    signal c3_fault : STD_LOGIC;
    signal total_run :  integer;
    
    
--attribute keep : string;
--attribute keep of c0_count : signal is "true";
--attribute keep of c1_count : signal is "true";
--attribute keep of c2_count : signal is "true";
--attribute keep of c3_count : signal is "true";

begin

    process(clk, rst)
    begin
        if rst = '1' then
            fault_reg <= '0';
            c0_count <= (others => '0');
            c1_count <= (others => '0');
            c2_count <= (others => '0');
            c3_count <= (others => '0');
            total_run <= total_run_init;
        elsif rising_edge(clk) then
            -- Expected statistical relation:
            if c0 = '1' then
                c0_count <= c0_count + 1;
            end if;

            if c1 = '1' then
                c1_count <= c1_count + 1;
            end if;

            if c2 = '1' then
                c2_count <= c2_count + 1;
            end if;

            if c3 = '1' then
                c3_count <= c3_count + 1;
            end if;
            
            if done_rcom='1' then
              total_run<=total_run+1;
              
              if(c0_count(c0_count'length-1 downto total_run-reference)>c0_count_max) or (c0_count(c0_count'length-1 downto total_run-reference)<c0_count_min) then
                 c0_fault<='1';
              else
                c0_fault<='0';
              end if;
              
               if(c1_count(c1_count'length-1 downto total_run-reference)>c1_count_max) or (c1_count(c1_count'length-1 downto total_run-reference)<c1_count_min) then
                 c1_fault<='1';
              else
                c1_fault<='0';
                
                
             if(c2_count(c2_count'length-1 downto total_run-reference)>c2_count_max) or (c2_count(c2_count'length-1 downto total_run-reference)<c2_count_min) then
                 c2_fault<='1';
              else
                c2_fault<='0';
              end if;
              
            end if;
            
           end if; 
        end if;
        
    end process;

--c0_fault<='1' when (c0_count(c0_count'length-1 downto total_run-reference)>c0_count_max) or (c0_count(c0_count'length-1 downto total_run-reference)<c0_count_min) else '0';
--c1_fault<='1' when (c1_count(c1_count'length-1 downto total_run-reference)>c1_count_max) or (c1_count(c0_count'length-1 downto total_run-reference)<c1_count_min) else '0';
--c2_fault<='1' when (c2_count(c2_count'length-1 downto total_run-reference)>c2_count_max) or (c2_count(c0_count'length-1 downto total_run-reference)<c2_count_min) else '0';



    fault <= c0_fault or c2_fault or c2_fault;

end Behavioral;
