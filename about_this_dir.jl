#=
🄯 Copyleft 2026 Ramrup Satpati | All Rights Reversed.
Released under the GNU General Public License v3.0 (GPLv3).

Root Directory Overview - Heavy Equipment Price Prediction Project
=#

module RootDirectoryOverview

"""
    summarize_project()

Prints an executive overview of the IIT Madras MLP S-Grade (90.00% / 10.0 GPA) project.
"""
function summarize_project()
    println("="^70)
    println("🚜 Heavy Equipment Price Prediction Pipeline (IIT Madras MLP Project)")
    println("Author: Ramrup Satpati | Grade: S (10.0 GPA / 90.00%)")
    println("License: GNU GPLv3 Copyleft 2026 | All Rights Reversed")
    println("="^70)
    println("Directory Components:")
    println("  • src/          : Modular Python production pipeline")
    println("  • notebooks/    : 5 Milestone progression Jupyter Notebooks")
    println("  • input_data/   : Raw dataset CSVs (train, test, metadata)")
    println("  • docs/         : GitHub Pages glassmorphism web landing page")
    println("="^70)
end

end # module

if abspath(PROGRAM_FILE) == @__FILE__
    RootDirectoryOverview.summarize_project()
end
