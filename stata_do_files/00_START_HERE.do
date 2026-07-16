*==============================================================*
*  STRUCTURAL BREAKS IN PANEL DATA  -  BEGINNER DO-FILES        *
*  Author of the commands: Dr Merwan Roudane                    *
*==============================================================*
*
*  WHAT THIS FOLDER IS
*  -------------------
*  One easy do-file per command. Each file:
*     1. loads a REAL dataset,
*     2. sets it as a panel (xtset),
*     3. runs the command with SIMPLE options,
*     4. tells you what to look at in the output.
*
*  You can open and run any single file on its own.
*
*  THE DATA (real, not simulated)
*  ------------------------------
*  We use "grunfeld" - the classic Grunfeld (1958) investment data
*  that ships with Stata (10 firms, 20 years, balanced panel).
*     invest  = firm investment      (our y)
*     mvalue  = market value         (an x)
*     kstock  = capital stock        (an x)
*     company = the firm id          (panel id)
*     year    = the year             (time)
*  Load it any time with:   webuse grunfeld, clear
*
*  It is short (T = 20), which is perfect for LEARNING THE SYNTAX.
*  For real research use a longer panel (T of 30 or more).
*
*  BEFORE YOU START
*  ----------------
*  These are Dr Roudane's commands. Make sure they are installed.
*  If a command is "unrecognized", install its package first
*  (ssc install <name>, or net install from the package folder).
*
*  HOW TO RUN A FILE
*  -----------------
*  Open a file in Stata's Do-file Editor and click "Do" (Ctrl+D),
*  or type in the Command window, e.g.:   do 01_xtpkpss.do
*
*  ORDER OF THE FILES
*  ------------------
*  01-02  Unit-root / stationarity tests (is the series I(1)?)
*  03-09  Cointegration tests (is there a long-run relation?)
*  10-16  Break estimators (where do the coefficients shift?)
*  17     Break detection (find the break dates)
*  99     Runs everything in order
*
*  Tip: run 01 first to check the data loads and everything works.
*==============================================================*

* quick check that the real data loads:
webuse grunfeld, clear
xtset company year
xtdescribe          // shows the panel is balanced: 10 firms x 20 years
summarize invest mvalue kstock
list company year invest in 1/5

display "Setup OK - now open 01_xtpkpss.do and start."
