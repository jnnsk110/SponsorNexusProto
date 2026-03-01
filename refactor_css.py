import os
import re

base_dir = r'g:\マイドライブ\10_Biz_Cockpit\20_Projects\13_AI_Consultant\20_Clients\Client_SatoTakuya\Prototype'
css_dir = os.path.join(base_dir, 'css')
os.makedirs(css_dir, exist_ok=True)
style_path = os.path.join(base_dir, 'style.css')

with open(style_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Define the split markers exactly as they appear in the file
markers = [
    "/* =========================================\n   Base Variables & Themes",
    "/* =========================================\n   Global Reset & Typhography",
    "/* =========================================\n   Sidebar Area",
    "/* =========================================\n   User Switcher",
    "/* =========================================\n   Main Content",
    "/* =========================================\n   KPI Cards",
    "/* =========================================\n   Lists & Tables",
    "/* =========================================\n   Sponsor Cloud Specific Styles",
    "/* =========================================\n   Detail View",
    "/* =========================================\n   Sponsor List Redesign",
    "/* =========================================\n   Project List Redesign",
    "/* =========================================\n   Modal Popup Styles"
]

# Find indices of markers
indices = {}
for m in markers:
    idx = text.find(m)
    if idx != -1:
        indices[m] = idx

# Sort markers by appearance
sorted_markers = sorted(indices.items(), key=lambda x: x[1])

# Extract blocks
blocks = []
for i in range(len(sorted_markers)):
    start_idx = sorted_markers[i][1]
    if i < len(sorted_markers) - 1:
        end_idx = sorted_markers[i+1][1]
        blocks.append(text[start_idx:end_idx])
    else:
        blocks.append(text[start_idx:])

# Group them into the new CSS files
# base.css: Base Variables & Themes, Global Reset & Typhography
base_css = text[:sorted_markers[0][1]] + blocks[0] + blocks[1]
# layout.css: Sidebar Area, User Switcher, Main Content
layout_css = blocks[2] + blocks[3] + blocks[4]
# components.css: KPI Cards, Lists & Tables, Modal Popup Styles
components_css = blocks[5] + blocks[6] + blocks[11]
# specific_ui.css (combining the rest for now so nothing breaks): Sponsor Nexus styles, Detail View, Sponsor/Project Lists
specific_ui_css = blocks[7] + blocks[8] + blocks[9] + blocks[10]

# Write the CSS files
with open(os.path.join(css_dir, 'base.css'), 'w', encoding='utf-8') as f: f.write(base_css)
with open(os.path.join(css_dir, 'layout.css'), 'w', encoding='utf-8') as f: f.write(layout_css)
with open(os.path.join(css_dir, 'components.css'), 'w', encoding='utf-8') as f: f.write(components_css)
with open(os.path.join(css_dir, 'specific_ui.css'), 'w', encoding='utf-8') as f: f.write(specific_ui_css)

print("Split CSS files created successfully in /css/ directory.")

# Update HTML files to link to the new CSS files
link_tags_html_root = """    <link href="css/base.css" rel="stylesheet">
    <link href="css/layout.css" rel="stylesheet">
    <link href="css/components.css" rel="stylesheet">
    <link href="css/specific_ui.css" rel="stylesheet">"""

link_tags_html_sub = """    <link href="../css/base.css" rel="stylesheet">
    <link href="../css/layout.css" rel="stylesheet">
    <link href="../css/components.css" rel="stylesheet">
    <link href="../css/specific_ui.css" rel="stylesheet">"""

for root, dirs, files in os.walk(base_dir):
    for str_file in files:
        if str_file.endswith('.html'):
            filepath = os.path.join(root, str_file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Figure out depth
            is_root = root == base_dir
            replacement = link_tags_html_root if is_root else link_tags_html_sub
            
            # Replace various occurrences
            content = content.replace('    <link href="style.css" rel="stylesheet">', replacement)
            content = content.replace('    <link href="../style.css" rel="stylesheet">', replacement)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"Updated {str_file}")

# Rename style.css to style.css.bak to disable the monolith
os.rename(style_path, style_path + '.bak')
print("style.css backed up.")
