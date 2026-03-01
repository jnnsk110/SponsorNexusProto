import os
import re

base_dir = r"g:\マイドライブ\10_Biz_Cockpit\20_Projects\13_AI_Consultant\20_Clients\Client_SatoTakuya\Prototype"

root_partner_link = """                <a href="partner/index.html" class="role-option">
                    <div style="width:24px; text-align:center;"><i class="fa-solid fa-magnifying-glass-chart"></i></div>インパクトパートナーモード
                </a>"""
sub_partner_link = """                <a href="../partner/index.html" class="role-option">
                    <div style="width:24px; text-align:center;"><i class="fa-solid fa-magnifying-glass-chart"></i></div>インパクトパートナーモード
                </a>"""

for root, dirs, files in os.walk(base_dir):
    for str_file in files:
        if str_file.endswith('.html'):
            filepath = os.path.join(root, str_file)
            
            # Skip the newly created partner directory
            if 'partner' in filepath: 
                continue

            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if 'インパクトパートナーモード' not in content and '<div class="role-menu"' in content:
                is_root = root == base_dir
                insert_str = root_partner_link if is_root else sub_partner_link
                
                # Regex to find the <a> tag that contains "ログアウト"
                # Looks like: <a href="../index.html" class="role-option" ... ><div ...></div>ログアウト...</a>
                # Let's match the start of that <a> tag reliably by finding the first <a> that has "ログアウト" 
                # inside it, and insert before it.
                
                # A safer approach:
                # Find the logout string index
                # Search backwards for the `<a ` opening tag before the logout string.
                
                logout_idx = content.find('ログアウト')
                if logout_idx != -1:
                    a_tag_start = content.rfind('<a ', 0, logout_idx)
                    
                    if a_tag_start != -1:
                        # Insert before the logout <a> tag
                        new_content = content[:a_tag_start] + insert_str + '\n' + content[a_tag_start:]
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f'Updated {filepath}')
                    else:
                        print(f'Could not find <a tag for logout in {filepath}')
                else:
                    print(f'Logout link not found in {filepath}')
