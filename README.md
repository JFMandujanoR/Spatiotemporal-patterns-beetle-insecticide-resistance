Pest Resistance Analysis — pipeline overview

This repository contains the code and R Markdown files used to prepare data and fit spatio-temporal models for pest resistance (Colorado potato beetle) using genetics and environmental covariates.

Important note for users
- This project is organized around R and R Markdown files. We expect readers to open and run the R/RMarkdown files in an R environment (RStudio, VS Code with R extension, or similar). You do not need to run terminal commands to use the repository — open the `.Rmd` or `.R` files and run chunks interactively or render them from R.

Top-level workflow (recommended order)

1) Compute PCo genetics
   - File: `computePCoGenetics.R`
   - Purpose: compute principal coordinates (PCoA) from population/genotype covariance matrices and produce per-sample / per-population PCo axes that will be merged into the main dataset.
   - How to use: open `computePCoGenetics.R` in R/RStudio and run the script or the example block. Place the covariance and metadata files in `input_data/` or adjust paths inside the script.

2) Merge environmental, resistance, and genetics data
   - R Markdown: `mergeEnvironmentalResistanceGeneticsData.Rmd`
   - Purpose: take climate/cropland/abundance data, merge temporal resistance records and (nearest) genetics samples to produce the final dataset used for modeling.
   - How to use: open and render the Rmd from R (for example, via the Knit button in RStudio or `rmarkdown::render()`). The Rmd writes a combined CSV such as `PotatoClimateIntensityData_OK_resistance_better_genetics_*.csv`.

3) Create Table 1 (descriptive table)
   - R Markdown: `createTable1.Rmd`
   - Purpose: generate descriptive statistics and manuscript Table 1.
   - How to use: open and run the Rmd.

4) Variable selection
   - R Markdown: `variableSelection.Rmd`
   - Purpose: exploratory filtering, scaling, and selection of covariates used in modeling.
   - How to use: open and run the Rmd; inspect chunks interactively to choose variables.

5) Grid search for model hyperparameters
   - File / R Markdown: `gridSearchINLA.Rmd.R` (script-like Rmd)
   - Purpose: run a grid search over spatial/temporal prior settings for the INLAspacetime model family and produce a `grid_search_results.csv` with model selection metrics.
   - How to use: open and run the script or render the Rmd from R. Note this step can be computationally heavy — run on a workstation or compute node as appropriate.

6) Fit pest resistance spatio-temporal model
   - R Markdown: `pestResistanceModel.Rmd` (and variants)
   - Purpose: build and compare spatio-temporal INLA/inlabru models (non-separable vs separable structures), produce fitted values and spatial maps.
   - How to use: open and run or render `pestResistanceModel.Rmd`. Expect long run-times depending on mesh and priors.

Notes about specific files and options
- In `PCoGenetics.Rmd` (and the compute PCo script), you can choose which covariates to include for downstream analysis — notably the workflow supports selecting either `covar1` or `covar2`. See the top of the file for guidance on which covariate set to use.
- In `geneticsImputation.Rmd`, two genetics data options are supported and named in code/comments as follows:
  - "regular genetics data": the original genetics dataset used previously (referred to in the code and comments as regular genetics data).
  - "adaptation genetics data": the newer genetics dataset used for adaptation analyses (referred to in the code and comments as adaptation genetics data).
  Select which dataset to use by setting the input file path or toggling the option inside `geneticsImputation.Rmd`.

Dependencies and tips
- R version: R >= 4.0.0 is recommended.
- Important packages: INLA (see https://www.r-inla.org/), inlabru, INLAspacetime, dplyr, ggplot2, readxl, raster, rgdal, sf, sp, maptools, broom, tidyr, gtsummary, vroom, plotly, viridis, and other packages used in each Rmd. Install packages from within R as needed.
- Rendering R Markdown: open the R Markdown file and use the Knit button in RStudio or `rmarkdown::render()` from an R session. We recommend running and inspecting code chunks interactively when possible.
- File locations: input files live under `input_data/` (for example: `final_data_for_modeling.csv`, `CPB_temp_avgcovariance.csv`, etc.). Adjust file paths in the Rmd/R scripts if you keep inputs elsewhere.

Suggested lightweight workflow (same order as above)
1. Compute PCo genetics (`computePCoGenetics.R`)
2. Render `mergeEnvironmentalResistanceGeneticsData.Rmd` to produce the combined dataset
3. Inspect and run `variableSelection.Rmd` and `createTable1.Rmd` for summaries
4. Run `gridSearchINLA.Rmd.R` to find reasonable priors
5. Render `pestResistanceModel.Rmd` to fit final models and generate figures

Contact
If you want the scripts cleaned further (remove redundant commented code, restructure chunks, or add parameterized YAML/options), tell me which files to modify and I will make conservative, tested edits.
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
