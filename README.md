Pest Resistance Analysis — pipeline overview

This repository contains code used to prepare data and fit spatio-temporal models for pest resistance (Colorado potato beetle) with genetics and environmental covariates.

Top-level workflow (recommended order):

1) compute PCo genetics
   - Script: `computePCoGenetics.R`
   - Purpose: compute principal coordinates (PCoA) from population/genotype covariance matrices and produce per-sample / per-population PCo axes that will be merged into the main dataset.
   - How to run: open `computePCoGenetics.R`, set working directory to where the covariance and metadata files live (or place the files in the repository `input_data/`), then run in R:
     - source('computePCoGenetics.R') or run the example block inside the file.

2) Merge environmental, resistance, and genetics data
   - RMarkdown: `mergeEnvironmentalResistanceGeneticsData.Rmd`
   - Purpose: takes climate/cropland/abundance points, merges temporal resistance records and (nearest) genetics samples to produce the final dataset used for modeling.
   - How to run: render the Rmd with `rmarkdown::render('mergeEnvironmentalResistanceGeneticsData.Rmd')`.
   - Outputs: a CSV like `PotatoClimateIntensityData_OK_resistance_better_genetics_*.csv` (see the script for exact filename).

3) Create Table 1 (descriptive table)
   - RMarkdown: `createTable1.Rmd`
   - Purpose: generate summary tables (Table 1) and descriptive statistics used in the manuscript.
   - How to run: render with `rmarkdown::render('createTable1.Rmd')`.

4) Variable selection
   - RMarkdown: `variableSelection.Rmd`
   - Purpose: exploratory variable filtering and scaling; used to prepare covariates for the INLA modeling step.
   - How to run: render with `rmarkdown::render('variableSelection.Rmd')`.

5) Grid search for model hyperparameters
   - Script / R: `gridSearchINLA.Rmd.R` (script-like Rmd)
   - Purpose: run a grid search over spatial/temporal prior settings for the INLAspacetime model family. Produces a `grid_search_results.csv` with WAIC/DIC for each combination.
   - How to run: open and run the script (or render if preferred). Note: this step can be computationally heavy — run on a compute node or workstation with enough memory.

      Quick run examples:

      - Non-interactive (recommended for batch jobs / compute nodes):

   ```bash
   # from the repository root (zsh)
   Rscript -e "source('gridSearchINLA.Rmd.R')"
   ```

      - Interactive (render the Rmd inside R/RStudio):

   ```r
   rmarkdown::render('gridSearchINLA.Rmd.R')
   ```

6) Fit pest resistance spatio-temporal model
   - RMarkdown: `pestResistanceModel.Rmd` and variants
   - Purpose: build and compare spatio-temporal INLA/inlabru models (non-separable vs separable structures), produce fitted values and spatial maps of predicted resistance.
   - How to run: render with `rmarkdown::render('pestResistanceModel.Rmd')`. Expect long run-times depending on mesh and priors.

Notes, dependencies and tips
- R version: use R >= 4.0.0.
- Important packages (install via install.packages or the package-specific installers):
  - INLA (install from https://www.r-inla.org/), inlabru, INLAspacetime
  - dplyr, ggplot2, readxl, raster, rgdal, sf, sp, maptools, broom, tidyr, gtsummary, vroom, plotly, viridis
- Rendering RMarkdown: use `rmarkdown::render()` or knit via RStudio. For long runs, consider running heavy model-fitting chunks with `eval=FALSE` in Rmd and executing interactively in the console.
- File locations: the repository expects several input files in `input_data/` (e.g. `final_data_for_modeling.csv`, `CPB_temp_avgcovariance.csv`, etc.). Adjust paths inside scripts if you keep inputs elsewhere.

Suggested lightweight workflow for a fresh run
1. Run `computePCoGenetics.R` to generate genetics PCo files.
2. Render `mergeEnvironmentalResistanceGeneticsData.Rmd` to produce the combined dataset.
3. Inspect and run `variableSelection.Rmd` and `createTable1.Rmd` for summaries.
4. Run `gridSearchINLA.Rmd.R` to find reasonable priors.
5. Render `pestResistanceModel.Rmd` to fit final models and generate figures.

Contact
If you need the scripts cleaned further (remove redundant commented code, restructure chunks, or parameterize paths), tell me which files to modify and I'll apply conservative, tested edits.
