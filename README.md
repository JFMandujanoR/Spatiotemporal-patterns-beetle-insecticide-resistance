Pest Resistance Analysis — pipeline overview

This repository contains the code and R Markdown files used to prepare data and fit spatio-temporal models for pest resistance (Colorado potato beetle) using genetics and environmental covariates.

Important note for users
- This project is organized around R Markdown files. We expect readers to open and run the R/RMarkdown files in an R environment (RStudio, VS Code with R extension, or similar). Open the `.Rmd` files and run chunks interactively or render them from R.

Top-level workflow (recommended order)

**IMPORTANT: Steps 1–2 must be run TWICE (once for each covariate set)** to produce outputs for both genetic datasets. After completing both runs, downstream scripts (steps 3–6) can be run with either covariate set by toggling the `covariate_set` variable.

1) Compute PCo genetics **[RUN TWICE]**
   - File: `PCoGenetics.Rmd`
   - Purpose: compute principal coordinates (PCoA) from population/genotype covariance matrices. This script uses two covariate sets:
     - **covar1**: CPB_temp_avgcovariance.csv → outputs `genetics_pco_covar1.csv` (better_genetics_Mar18)
     - **covar2**: pcangsd_cpb_temp_cands.cov → outputs `genetics_pco_covar2.csv` (better_genetics_Jun2)
   - How to use: 
     1. Open `PCoGenetics.Rmd` and set `covar = covar1` (line ~25), then render to produce `genetics_pco_covar1.csv`
     2. Change to `covar = covar2`, render again to produce `genetics_pco_covar2.csv`
     3. Both files are written to `output_data/01_genetics/`

2) Merge environmental, resistance, and genetics data **[RUN TWICE]**
   - R Markdown: `mergeEnvironmentalResistanceGeneticsData.Rmd`
   - Purpose: combine climate/cropland/abundance data with temporal resistance records and genetics. Produces two merged datasets:
     - **Run 1**: reads `genetics_pco_covar1.csv` → outputs `merged_data_covar1.csv`
     - **Run 2**: reads `genetics_pco_covar2.csv` → outputs `merged_data_covar2.csv`
   - How to use:
     1. Open the Rmd and set `genetics_file <- "genetics_pco_covar1.csv"`, render to produce `merged_data_covar1.csv`
     2. Change to `genetics_file <- "genetics_pco_covar2.csv"`, render again to produce `merged_data_covar2.csv`
     3. Both files are written to `output_data/02_merged_data/`


3) Create Table 1 (descriptive table)
   - R Markdown: `createTable1.Rmd`
   - Purpose: generate descriptive statistics and manuscript Table 1.
   - How to use: open and run the Rmd. This script reads from `input_data/` (legacy behavior for backward compatibility).

4) Variable selection **[SELECT COVARIATE SET]**
   - R Markdown: `variableSelection.Rmd`
   - Purpose: exploratory filtering, scaling, and selection of covariates used in modeling.
   - How to use: 
     - Set `covariate_set <- "covar1"` or `covariate_set <- "covar2"` to choose which genetics dataset to analyze
     - Reads from `output_data/02_merged_data/merged_data_covar*.csv`
     - Open and run the Rmd; inspect chunks interactively to choose variables.

5) Grid search for model hyperparameters
   - File / R Markdown: `gridSearch.Rmd`
   - Purpose: run a grid search over spatial/temporal prior settings for the INLAspacetime model family and produce a `grid_search_results.csv` with model selection metrics.
   - How to use: open and render the Rmd from R. Note this step can be computationally heavy — run on a workstation or compute node as appropriate.

6) Fit pest resistance spatio-temporal model **[SELECT COVARIATE SET]**
   - R Markdown: `pestResistanceModel.Rmd`
   - Purpose: build and compare spatio-temporal INLA/inlabru models (non-separable vs separable structures), produce fitted values and spatial maps.
   - How to use: 
     - Set `covariate_set <- "covar1"` or `covariate_set <- "covar2"` to choose which genetics dataset to use
     - Reads from `output_data/02_merged_data/merged_data_covar*.csv`
     - Open and run or render the Rmd. Expect long run-times depending on mesh and priors.


Input and Output Organization

**input_data/**
Contains all raw input files needed for the analysis pipeline:
- `better_genetics_*.csv` — PCo genetics data (sourced from genomic analysis)
- `CPB_temp_*.csv` — Covariance and metadata for genetic covariates
- `final_data_for_modeling.csv` — Base climate/abundance/cropland data
- `temporal_resistance_data.csv` — Beetle resistance records
- `PotatoClimateIntensityData_OK_resistance_better_genetics_imputed_*.csv` — Pre-merged datasets
- `Table_Genomic_Samplesv2.xlsx` — WGS sample metadata and reference tables
- `pcangsd_cpb_temp_cands.cov` — Alternative covariance matrix

**output_data/**
Automatically organized outputs from each workflow stage:
- `01_genetics/` — PCoA genetics outputs (e.g., `genetics_pco.csv`)
- `02_merged_data/` — Combined environmental+resistance+genetics dataset (e.g., `merged_data.csv`)
- `03_tables/` — Descriptive tables and Table 1 outputs
- `04_variable_selection/` — Covariate selection plots and scaled variable outputs
- `05_gridsearch/` — Grid search hyperparameter results (e.g., `grid_search_results.csv`)
- `06_models/` — Fitted INLA/inlabru models and predictions
- `07_predictions/` — Final prediction maps and spatial outputs

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
1. Compute PCo genetics (`PCoGenetics.R`)
2. Render `mergeEnvironmentalResistanceGeneticsData.Rmd` to produce the combined dataset
3. Inspect and run `variableSelection.Rmd` and `createTable1.Rmd` for summaries
4. Run `gridSearchINLA.Rmd.R` to find reasonable priors
5. Render `pestResistanceModel.Rmd` to fit final models and generate figures