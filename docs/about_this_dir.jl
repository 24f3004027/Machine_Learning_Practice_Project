#=
🄯 Copyleft 2026 Ramrup Satpati | All Rights Reversed.
Released under the GNU General Public License v3.0 (GPLv3).

Docs Directory Overview - docs/
=#

module DocsDirectoryOverview

"""
    explain_docs_landing_page()

Explains the GitHub Pages web landing page structure.
"""
function explain_docs_landing_page()
    println("🌐 Machine_Learning_Practice_Project/docs Overview:")
    println("  • index.html : Responsive glassmorphic showcase web page")
    println("  • style.css  : Emerald/cyan dark theme styles & responsive design layout")
    println("Live GitHub Pages URL: https://24f3004027.github.io/Machine_Learning_Practice_Project/")
end

end # module

if abspath(PROGRAM_FILE) == @__FILE__
    DocsDirectoryOverview.explain_docs_landing_page()
end
