*==============================================================*
*  99 - RUN ALL                                                 *
*  Runs every example do-file in order.                         *
*==============================================================*
*
*  Each file loads its own data and runs on its own, so this
*  simply calls them one after another.
*
*  If it stops on one command, that command's package is probably
*  not installed - just skip that file and run the rest by hand.
*
*  Make sure Stata's working directory is THIS folder first:
*     cd "C:\Users\HP\Documents\xtpmg\lecture\stata_do_files"
*==============================================================*

do 01_xtpkpss.do
do 02_xtpqroot.do
do 03_xtlmbreak.do
do 04_xtpcointegwe.do
do 05_xtpcointegboot.do
do 06_xtbreakcoint.do
do 07_xtccecoint.do
do 08_xtcadfcoint.do
do 09_xtnonlincoint.do
do 10_xtbreakmodel.do
do 11_xtcbc.do
do 12_xtkpybreak.do
do 13_xtbfkbreak.do
do 14_xtquantilebreak.do
do 15_xtdynestimb.do
do 16_xtpvarcoint.do
do 17_xtgets.do

display "All example do-files finished."
