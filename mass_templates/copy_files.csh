#!/bin/tcsh
if ( "$1" =~ *"/") then
    set input="$1"
else
    set input="$1/"
endif

if ( "$2" =~ *"/") then
    set output="$2"
else
    set output="$2/"
endif


mkdir -p "$output""/tt"
mkdir -p "$output""/tW"
cp -rf "$input""/plots2017/mc_TT.root" "$output/tt/mc_TT.root"
cp -rf "$input""/plots2017/mc_ST_s.root" "$output/mc_ST_s.root"
cp -rf "$input""/plots2017/mc_ST_t_antitop.root" "$output/mc_ST_t_antitop.root"
cp -rf "$input""/plots2017/mc_ST_t_top.root" "$output/mc_ST_t_top.root"
cp -rf "$input""/plots2017/plots/plotter.root" "$output/plotter.root"
cp -rf "$input""/plots2017/mc_ST_tW_antitop.root" "$output/tW/mc_ST_tW_antitop.root"
cp -rf "$input""/plots2017/mc_ST_tW_top.root" "$output/tW/mc_ST_tW_top.root"

# TT
cp -rf "$input/plots_mt1665/mc_TT_mt1665.root" "$output/tt/mc_TT_mt1665.root"
cp -rf "$input/plots_mt1695/mc_TT_mt1695.root" "$output/tt/mc_TT_mt1695.root" 
cp -rf "$input/plots_mt1715/mc_TT_mt1715.root" "$output/tt/mc_TT_mt1715.root"
cp -rf "$input/plots_mt1735/mc_TT_mt1735.root" "$output/tt/mc_TT_mt1735.root"
cp -rf "$input/plots_mt1755/mc_TT_mt1755.root" "$output/tt/mc_TT_mt1755.root"
cp -rf "$input/plots_mt1785/mc_TT_mt1785.root" "$output/tt/mc_TT_mt1785.root"

# tW
cp -rf "$input/plots_mt1695/mc_ST_tW_antitop_mt1695.root" "$output/tW/mc_ST_tW_antitop_mt1695.root" 
cp -rf "$input/plots_mt1695/mc_ST_tW_top_mt1695.root" "$output/tW/mc_ST_tW_top_mt1695.root" 
cp -rf "$input/plots_mt1755/mc_ST_tW_antitop_mt1755.root" "$output/tW/mc_ST_tW_antitop_mt1755.root" 
cp -rf "$input/plots_mt1755/mc_ST_tW_top_mt1755.root" "$output/tW/mc_ST_tW_top_mt1755.root" 
