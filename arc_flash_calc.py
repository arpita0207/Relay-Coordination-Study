import pandas as pd
import numpy as np

# Re-run since code execution environment was reset
# Generate synthetic dataset for demonstration
df_input = pd.read_excel("data_arcflash.xlsx")
# Conservative assumptions
assumed_fault_current_kA = 20  # typical LV conservative value
assumed_arc_duration_s = 0.2   # conservative breaker clearing time

# IEEE 1584-2002 empirical constants for VCB configuration
k1, k2, k3, k4 = 0.00402, 0.983, 0.708, 0.004

# Perform arc flash calculations
results = []
for _, row in df_input.iterrows():
    V = row["Nominal Voltage (V)"]
    G = row["Gap (mm)"]
    D = row["Working Distance (mm)"]

    logIarc = (k1 * V + k2) + k3 * np.log10(assumed_fault_current_kA) - k4 * G
    Iarc = 10 ** logIarc

    IE_J_cm2 = (4.184e-4) * (Iarc * 1000) * assumed_arc_duration_s * (5271 / D ** 2)
    IE_cal_cm2 = IE_J_cm2 / 4.184

    AFB_mm = D * np.sqrt(IE_cal_cm2 / 1.2)
    AFB_in = AFB_mm / 25.4

    results.append({
        "Nominal Voltage (V)": V,
        "Gap (mm)": round(G, 1),
        "Working Distance (mm)": round(D, 1),
        "Arcing Current (kA)": round(Iarc, 2),
        "Incident Energy (cal/cm²)": round(IE_cal_cm2, 2),
        "Arc Flash Boundary (mm)": round(AFB_mm, 2),
        "Arc Flash Boundary (inches)": round(AFB_in, 2)
    })

# Create output DataFrame and save
df_output = pd.DataFrame(results)
output_path = "/mnt/data/Arc_Flash_VCB_Estimator.xlsx"
df_output.to_excel(output_path, index=False)

output_path
