#!/bin/bash
set -x
./analyze.csh
./hadd_plot_files.csh
./histos.csh

