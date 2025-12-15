uid: ISS-0101
status: BACKLOG
priority: medium
owner_role: FEATURE
estimate: TBD
dependencies: []
risk: medium
milestone: backlog

# Note when color palette wraps in colors_macro

When a color code palette is shorter than the requested legend color count, the generated legend repeats colors. The `colors_macro.html` template currently gives no user-facing indication of these duplicate entries. Add a small note or legend annotation when colors wrap, and consider adding textures/patterns to distinguish duplicates for accessibility. This likely involves extending the template macros to detect repeated colors and render an indicator, and possibly adding texture assets or CSS patterns.
