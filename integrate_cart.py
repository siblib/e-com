import os
import re
import sys

TEMPLATES_DIR = "/home/eju/Desktop/SITE MIRROR/SHOP/SHOP 3/ecommerce/templates"

def insert_load_tag(content):
    if "{% load cart_tags %}" in content:
        return content
        
    # Check for extends tag first
    extends_match = re.search(r'({%\s*extends\s+[^%]+\s*%})', content)
    if extends_match:
        pos = extends_match.end()
        return content[:pos] + "\n{% load cart_tags %}" + content[pos:]
        
    # Check for load static tag
    load_static_match = re.search(r'({%\s*load\s+static\s*%})', content)
    if load_static_match:
        pos = load_static_match.end()
        return content[:pos] + " {% load cart_tags %}" + content[pos:]
        
    # Otherwise prepend
    return "{% load cart_tags %}\n" + content

def run_integration(dry_run=True):
    html_files = []
    for root, dirs, files in os.walk(TEMPLATES_DIR):
        if "venv" in root or "cart" in root:
            continue
        for file in files:
            if file.endswith(".html"):
                html_files.append(os.path.join(root, file))
                
    modified_count = 0
    print(f"--- Running Cart Integration (Dry Run = {dry_run}) ---")
    
    for path in sorted(html_files):
        rel_path = os.path.relpath(path, TEMPLATES_DIR)
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            
        modified = False
        new_content = content
        
        # 1. Replace Cart Button
        btn_comment_start = "<!-- Cart Button Icon -->"
        btn_comment_end = "<!-- End Cart Button Icon -->"
        
        if btn_comment_start in new_content and btn_comment_end in new_content:
            def repl_btn(match):
                text = match.group(0)
                if 'data-hs-overlay="#hs-pro-shco"' in text:
                    return "{% cart_button %}"
                return text
                
            pattern = re.compile(re.escape(btn_comment_start) + r'.*?' + re.escape(btn_comment_end), re.DOTALL)
            new_content, count = pattern.subn(repl_btn, new_content)
            # Check if the text actually changed (repl_btn could return the original text)
            if new_content != content:
                modified = True
                print(f"[{rel_path}] Replaced Cart Button Icon comment block.")
                
        # 2. Replace Cart Drawer/Offcanvas
        panel_comment_start = "<!-- Cart Offcanvas -->"
        panel_comment_end = "<!-- End Cart Offcanvas -->"
        
        # We need to store state of content before panel replace to check if it changed
        content_before_panel = new_content
        if panel_comment_start in new_content and panel_comment_end in new_content:
            def repl_panel(match):
                text = match.group(0)
                if 'id="hs-pro-shco"' in text:
                    return "{% cart_panel %}"
                return text
                
            pattern = re.compile(re.escape(panel_comment_start) + r'.*?' + re.escape(panel_comment_end), re.DOTALL)
            new_content, count = pattern.subn(repl_panel, new_content)
            if new_content != content_before_panel:
                modified = True
                print(f"[{rel_path}] Replaced Cart Offcanvas comment block.")
                
        if modified:
            new_content = insert_load_tag(new_content)
            modified_count += 1
            if not dry_run:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"[{rel_path}] SAVED changes.")
                
    print(f"\nTotal files modified: {modified_count}")

if __name__ == "__main__":
    dry_run = True
    if len(sys.argv) > 1 and sys.argv[1] == "--apply":
        dry_run = False
    run_integration(dry_run)
