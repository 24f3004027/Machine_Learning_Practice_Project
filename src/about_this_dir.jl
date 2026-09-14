#=
🄯 Copyleft 2026 Ramrup Satpati | All Rights Reversed.
Released under the GNU General Public License v3.0 (GPLv3).

Source Directory Overview - src/
=#

module SourceDirectoryOverview

"""
    explain_src_modules()

Describes the modular Python source files contained within src/.
"""
function explain_src_modules()
    println("📦 Machine_Learning_Practice_Project/src Overview:")
    println("  • __init__.py            : Package export initialization")
    println("  • feature_engineering.py : Temporal features, regex physical spec parsers (HP, Tonnage, Yardage)")
    println("  • preprocessing.py       : Out-of-fold frequency encoding & NaN median imputation")
    println("  • models.py              : Deep XGBoost (45%), LightGBM (35%), CatBoost (20%) hyperparams")
    println("  • evaluate.py            : RMSLE metric, 5-seed log-space blending & Jensen's multiplier (1.001300)")
end

end # module

if abspath(PROGRAM_FILE) == @__FILE__
    SourceDirectoryOverview.explain_src_modules()
end
