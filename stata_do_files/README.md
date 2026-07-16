# Beginner do-files — Structural breaks in panel data

Simple, one-command-at-a-time Stata do-files for the `xt*` structural-break
panel commands by **Dr Merwan Roudane**. Each file loads **real data**, sets the
panel, and runs the command with **easy options** and plain-language comments.

## Real data used
- **`webuse grunfeld`** — Grunfeld (1958) firm investment data (10 firms × 20 years,
  balanced). Variables: `invest` (y), `mvalue`, `kstock` (x), `company`, `year`.
- **`webuse grunfeld2`** — a longer real Grunfeld panel (used by file 16).

Both ship with Stata; nothing to download. The panel is short (T = 20) — ideal for
**learning the syntax**. For real research use a longer panel (T ≥ 30).

## Files (each = one command's role)

| File | Command | Role |
|---|---|---|
| 00 | — | Start here: setup + data check |
| 01 | `xtpkpss` | Panel stationarity test with breaks |
| 02 | `xtpqroot` | Quantile unit-root + Fourier-break test |
| 03 | `xtlmbreak` | LM cointegration test, multiple breaks |
| 04 | `xtpcointegwe` | Cointegration with breaks + factors |
| 05 | `xtpcointegboot` | Bootstrap cointegration test |
| 06 | `xtbreakcoint` | Cointegration + breaks + CSD (BC 2015) |
| 07 | `xtccecoint` | CCE cointegration test (BC 2017) |
| 08 | `xtcadfcoint` | Cointegration with instabilities (BC 2025) |
| 09 | `xtnonlincoint` | Nonlinear / Fourier cointegration |
| 10 | `xtbreakmodel` | Estimate breaks (4 methods) |
| 11 | `xtcbc` | Coefficient-by-coefficient breaks |
| 12 | `xtkpybreak` | CCE + I(1) factors + breaks |
| 13 | `xtbfkbreak` | CCE common break, endogenous x |
| 14 | `xtquantilebreak` | Breaks across quantiles |
| 15 | `xtdynestimb` | Dynamic panel robust to breaks |
| 16 | `xtpvarcoint` | Panel VAR with cointegration + breaks |
| 17 | `xtgets` | Automatic break detection |
| 18 | `xtfmg` | 2nd-gen heterogeneous estimators: FE, MG, CCEMG, SURMG, F-SURMG, **F-CCEMG** (+ `map`, `breaks`) |
| 19 | `xtpfardl` | **Fourier-augmented panel ARDL / CS-ARDL** (long-run + short-run) — needs `xtdcce2` |
| 20 | `xtpcaus` | **Panel causality**: Fourier Toda–Yamamoto (PFTY) & Panel Quantile Causality (PQC) |
| 99 | — | Run everything in order |

## Two text files to keep open

| File | What it gives you |
|---|---|
| **`COMMANDS_reference.txt`** | **All 20 commands**: what each *does*, its **H₀** (the tests disagree!), its key options, its do-file, and its source paper. Ends with a quick-lookup table ("which command do I use?") and the workflow. |
| **`INSTALL_commands.txt`** | Every `ssc install` line — run once before you start. |

## How to run
1. In Stata set the working folder:
   `cd "C:\Users\HP\Documents\xtpmg\lecture\stata_do_files"`
2. Run **`00_START_HERE.do`** to check the data loads.
3. Open any file and click **Do** (Ctrl+D), or `do 01_xtpkpss.do`.

## Notes for beginners
- Commands are written the **plain** way — no `quietly`, no `capture`, so you always
  see the full output.
- Read the top comment of each file: it says what the command does and **what to look
  at** in the output (which statistic, which p-value, the break dates).
- If a command is “unrecognized”, install its package first, then re-run the file.
