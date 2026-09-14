#=
🄯 Copyleft 2026 Ramrup Satpati | All Rights Reversed.
Released under the GNU General Public License v3.0 (GPLv3).

Notebooks Directory Overview - notebooks/
=#

module NotebooksDirectoryOverview

"""
    list_milestone_notebooks()

Lists all 5 milestone notebooks documenting the full ML pipeline progression.
"""
function list_milestone_notebooks()
    println("📓 Machine_Learning_Practice_Project/notebooks Overview:")
    println("  • 01_Exploratory_Data_Analysis.ipynb                  : EDA & Target Log1p Distribution")
    println("  • 02_Spec_Parsing_And_Baselines.ipynb                 : Regex HP/Tonnage parsing & RF Baseline")
    println("  • 03_Feature_Engineering_And_Encoding.ipynb           : Depreciation Ratios & Frequency Encoding")
    println("  • 04_Multi_Model_Gradient_Boosting.ipynb              : XGBoost, LightGBM, CatBoost Tuning")
    println("  • 05_Production_Ensemble_And_Jensens_Multiplier.ipynb : 5-Seed Ensemble & Jensen Multiplier (0.18663 RMSLE)")
    println("  • MLP_Production_Pipeline.ipynb                       : Complete end-to-end execution notebook")
end

end # module

if abspath(PROGRAM_FILE) == @__FILE__
    NotebooksDirectoryOverview.list_milestone_notebooks()
end
