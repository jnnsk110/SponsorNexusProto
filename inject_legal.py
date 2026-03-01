import os
import re

base_dir = r"g:\マイドライブ\10_Biz_Cockpit\20_Projects\13_AI_Consultant\20_Clients\Client_SatoTakuya\Prototype"

footer_links_root = """
        <div class="legal-links" style="padding: 1rem 1.5rem; font-size: 0.75rem; text-align: center; margin-top: auto; padding-bottom: 0; border-top: 1px solid rgba(255,255,255,0.1);">
            <a href="tokushoho.html" style="color: rgba(255,255,255,0.6); text-decoration: none; display: block; margin-bottom: 0.5rem;">特定商取引法に基づく表記</a>
            <a href="privacy.html" style="color: rgba(255,255,255,0.6); text-decoration: none; display: block; margin-bottom: 0.5rem;">プライバシーポリシー</a>
            <a href="terms.html" style="color: rgba(255,255,255,0.6); text-decoration: none; display: block;">利用規約・免責事項</a>
        </div>
"""

footer_links_sub = """
        <div class="legal-links" style="padding: 1rem 1.5rem; font-size: 0.75rem; text-align: center; margin-top: auto; padding-bottom: 0; border-top: 1px solid rgba(255,255,255,0.1);">
            <a href="../tokushoho.html" style="color: rgba(255,255,255,0.6); text-decoration: none; display: block; margin-bottom: 0.5rem;">特定商取引法に基づく表記</a>
            <a href="../privacy.html" style="color: rgba(255,255,255,0.6); text-decoration: none; display: block; margin-bottom: 0.5rem;">プライバシーポリシー</a>
            <a href="../terms.html" style="color: rgba(255,255,255,0.6); text-decoration: none; display: block;">利用規約・免責事項</a>
        </div>
"""

exclude_exact = [
    os.path.join(base_dir, 'concept.html'),
    os.path.join(base_dir, 'tokushoho.html'),
    os.path.join(base_dir, 'privacy.html'),
    os.path.join(base_dir, 'terms.html'),
    os.path.join(base_dir, 'index.html'), 
    os.path.join(base_dir, 'admin.html'),
    os.path.join(base_dir, 'sponsor.html'),
    os.path.join(base_dir, 'owner.html')
]

for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            if filepath in exclude_exact:
                continue
                
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # --- 1. CLEANUP PHASE ---
            idx = content.find('<div class="legal-links"')
            while idx != -1:
                content = re.sub(r'\s*<div class="legal-links"[\s\S]*?</div>(\s*</div>)?', '\n', content, count=1)
                idx = content.find('<div class="legal-links"')
                
            # --- 2. INJECTION PHASE ---
            # Inject right before <div class="user-bottom">
            if '<div class="user-bottom">' in content:
                is_root = root == base_dir
                insert_html = footer_links_root if is_root else footer_links_sub
                
                # Replace the marker
                # Ensure we only replace the FIRST occurrence to be safe, though there should only be one per page
                content = content.replace('<div class="user-bottom">', insert_html.strip('\n') + '\n\n        <div class="user-bottom">', 1)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Fixed and Injected into {filepath}")
            else:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Cleaned (no inject) for {filepath}")
