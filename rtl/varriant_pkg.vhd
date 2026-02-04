library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_ARITH.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;
use ieee.math_real.all;

package variant_pkg is

constant l  : integer := 12;
constant q  : integer := 3329;


constant logq : positive := positive(ceil(log2(real(q))));
constant w : positive := 6;
end variant_pkg;