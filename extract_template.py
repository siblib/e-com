import re

with open('templates/products/product_detail.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find main content start and end
main_start_match = re.search(r'<!-- ========== MAIN CONTENT ========== -->', content)
footer_start_match = re.search(r'<!-- ========== FOOTER ========== -->', content)

if main_start_match and footer_start_match:
    main_start_idx = main_start_match.start()
    footer_start_idx = footer_start_match.start()
    
    header_part = content[:main_start_idx]
    main_part = content[main_start_idx:footer_start_idx]
    footer_part = content[footer_start_idx:]
    
    with open('header_part.html', 'w', encoding='utf-8') as f:
        f.write(header_part)
    with open('main_part.html', 'w', encoding='utf-8') as f:
        f.write(main_part)
    with open('footer_part.html', 'w', encoding='utf-8') as f:
        f.write(footer_part)
    
    print(f"Extraction successful: Header {len(header_part)}, Main {len(main_part)}, Footer {len(footer_part)}")
else:
    print("Could not find delimiters")
