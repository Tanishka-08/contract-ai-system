
import os

file_path = "app.py"

with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Define ranges to indent (1-based line numbers from view_file, converted to 0-based indices)
# Ranges are inclusive of start, exclusive of end (but careful with line numbers)
# Line 185 (index 184) to 281 (index 281) -> Indent +4
# Line 287 to 343 -> Indent +4
# Line 349 to 375 -> Indent +4
# Line 382 to 424 -> Indent +4
# Line 430 to 446 -> Indent +4
# Line 452 to 463 -> Indent +4

# Note: lines list is 0-indexed. Line 185 is index 184.
ranges = [
    (185, 281),
    (287, 343),
    (349, 375),
    (382, 424),
    (430, 446),
    (452, 463)
]

new_lines = []
for i, line in enumerate(lines):
    line_num = i + 1
    should_indent = False
    for start, end in ranges:
        if start <= line_num <= end:
            should_indent = True
            break
    
    if should_indent and line.strip(): # Only indent if not empty (though empty lines don't matter much)
        new_lines.append("    " + line)
    else:
        new_lines.append(line)

with open(file_path, "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("Indentation fixed.")
