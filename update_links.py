import os

base_dir = r"g:\マイドライブ\10_Biz_Cockpit\20_Projects\13_AI_Consultant\20_Clients\Client_SatoTakuya\Prototype"

link_html = '\n            <a href="../concept.html" class="nav-link" style="margin-top: 1.5rem; color: #B794F4;">\n                <i class="fa-solid fa-book-open"></i> コンセプト・意義\n            </a>\n        '
root_link_html = '\n            <a href="concept.html" class="nav-link" style="margin-top: 1.5rem; color: #B794F4;">\n                <i class="fa-solid fa-book-open"></i> コンセプト・意義\n            </a>\n        '

for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith('.html') and file not in ('concept.html', 'index.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            is_root = root == base_dir
            insert_link = root_link_html if is_root else link_html
            
            search_str = '</a>\n        </div>\n\n        <div class="user-bottom">'
            
            if search_str in content and 'コンセプト・意義' not in content:
                new_content = content.replace(search_str, '</a>' + insert_link + '</div>\n\n        <div class="user-bottom">')
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Updated {filepath}")
