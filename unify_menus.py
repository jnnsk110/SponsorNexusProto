import os
import re

base_dir = r"g:\マイドライブ\10_Biz_Cockpit\20_Projects\13_AI_Consultant\20_Clients\Client_SatoTakuya\Prototype"
roles = ['admin', 'sponsor', 'owner']

for role in roles:
    role_dir = os.path.join(base_dir, role)
    index_path = os.path.join(role_dir, 'index.html')
    
    with open(index_path, 'r', encoding='utf-8') as f:
        index_content = f.read()
    
    # Extract the nav-menu from index.html
    # We look for `<div id="menu-..." class="nav-menu">` up to its closing `</div>`
    # Warning, there is a `</div>` for the nested elements. Let's use a regex that matches until the next section.
    # We know the nav-menu ends right before `<!-- User Switcher -->` or `<div class="legal-links"`
    
    nav_match = re.search(r'(<div id="menu-[a-z]+" class="nav-menu">[\s\S]*?)</div>\s*<div class="legal-links"', index_content)
    if not nav_match:
        # try without legal-links just in case
        nav_match = re.search(r'(<div id="menu-[a-z]+" class="nav-menu">[\s\S]*?)</div>\s*(?:<!-- User Switcher -->|<div class="user-bottom">)', index_content)
    
    if not nav_match:
        print(f"Could not find nav menu in {role}/index.html")
        continue
        
    # The actual extracted HTML includes the opening `<div id="menu-X" class="nav-menu">` 
    # and we captured up to but not including the closing `</div>` of the nav-menu because of how the regex is structured?
    # Actually `</div>\s*<div class="legal...` captures the `</div>` that closes the nav-menu.
    # Let's cleanly extract it by finding `<div id="menu` and the `</div>` before `legal-links` or `user-bottom`.
    
    start_str = f'<div id="menu-{role}" class="nav-menu">'
    start_idx = index_content.find(start_str)
    if start_idx == -1:
        # Try without id if it doesn't match
        start_str = '<div class="nav-menu">'
        start_idx = index_content.find(start_str)
    
    end_idx = index_content.find('<div class="legal-links"', start_idx)
    if end_idx == -1:
        end_idx = index_content.find('<div class="user-bottom"', start_idx)
    # The `</div>` before end_idx belongs to nav-menu.
    # Let's just take index_content[start_idx:end_idx].strip() which might have a trailing `</div>`.
    
    # Better yet, regex to grab the whole block safely:
    match = re.search(r'(<div[^>]*class="nav-menu"[^>]*>[\s\S]*?)(?=\s*<div class="legal-links"|\s*<!-- User Switcher -->|\s*<div class="user-bottom")', index_content)
    
    if not match:
        print(f"Error extracting from {role}")
        continue
        
    canonical_nav = match.group(1).rstrip()
    
    # Ensure it ends with </div>
    if not canonical_nav.endswith('</div>'):
        canonical_nav += '\n        </div>'

    # Now apply to all files in the directory
    for file in os.listdir(role_dir):
        if file.endswith('.html') and file != 'index.html':
            filepath = os.path.join(role_dir, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Find the nav block to replace
            target_match = re.search(r'(<div[^>]*class="nav-menu"[^>]*>[\s\S]*?)(?=\s*<div class="legal-links"|\s*<!-- User Switcher -->|\s*<div class="user-bottom")', content)
            if not target_match:
                print(f"Skipping {filepath}, couldn't find target nav-menu")
                continue
                
            # We want to replace it with canonical_nav, BUT we must adjust the `active` class.
            
            # Step 1: Remove `active` class from everywhere in canonical_nav
            nav_clean = canonical_nav.replace(' class="nav-link active"', ' class="nav-link"')
            
            # Step 2: Add `active` class to the correct link based on the current file
            # e.g., if we are in settings.html, we look for href="settings.html"
            # It might be `href="settings.html"`
            replace_str = f'href="{file}" class="nav-link"'
            active_str = f'href="{file}" class="nav-link active"'
            
            if replace_str in nav_clean:
                nav_clean = nav_clean.replace(replace_str, active_str)
            else:
                # Fallback, maybe just href="settings.html"
                print(f"Warning: Could not set active state for {file} in {filepath}")
            
            # Replace in file
            new_content = content[:target_match.start()] + nav_clean + content[target_match.end():]
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {filepath}")
