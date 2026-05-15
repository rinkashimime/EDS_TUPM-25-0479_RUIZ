# HVA-04: Duct Leakage Flow Rate Analysis
**Researcher:** Marck Ruiz  
**Topic ID:** HVA-04 (Pillar 9)

## Project Overview
This pipeline analyzes AHU (Air Handling Unit) telemetry to identify mechanical duct leakage. 
By correlating Fan Power and Return Static Pressure, we identify non-linear energy spikes that 
signify air loss within the ventilation system.

## How to Run
1. Install dependencies: `pip install -r requirements.txt`
2. Ensure `HVAC_NE_EC_19-21.csv` is in the root directory.
3. Run the pipeline: `python main.py`

## Outputs
- `data/`: Contains the filtered "High-Load" dataset.
- `outputs/`: Contains the Pressure-Power scatter plots and leakage animations.