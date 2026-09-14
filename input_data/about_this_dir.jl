#=
🄯 Copyleft 2026 Ramrup Satpati | All Rights Reversed.
Released under the GNU General Public License v3.0 (GPLv3).

Input Data Directory Overview - input_data/
=#

module InputDataDirectoryOverview

"""
    explain_dataset_files()

Details the raw competition dataset CSV files stored in input_data/.
"""
function explain_dataset_files()
    println("📊 Machine_Learning_Practice_Project/input_data Overview:")
    println("  • train.csv             : Heavy equipment training records with ground truth SalePrice")
    println("  • test.csv              : Unseen test machinery records for evaluation")
    println("  • sample_submission.csv : Kaggle submission format template")
    println("  • metadata.csv          : Feature definitions and column schemas")
    println("Note: Self-contained dataset files for direct local & Kaggle CLI testing.")
end

end # module

if abspath(PROGRAM_FILE) == @__FILE__
    InputDataDirectoryOverview.explain_dataset_files()
end
