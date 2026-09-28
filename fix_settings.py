import re

def main():
    with open('web/index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # The buggy block is:
    # document.getElementById('results').innerHTML = `<div class="card" style="padding:20px; background:#FFF3E0; color:#E65100; margin-bottom:20px;"><i class='bx bx-info-circle'></i> Settings API is not connected. The below configurations are read-only and not configurable from UI.</div>` + document.getElementById('results').innerHTML;
    # document.getElementById('results').innerHTML = `
    
    old_block = r"""document.getElementById('results').innerHTML = `<div class="card" style="padding:20px; background:#FFF3E0; color:#E65100; margin-bottom:20px;"><i class='bx bx-info-circle'></i> Settings API is not connected. The below configurations are read-only and not configurable from UI.</div>` + document.getElementById('results').innerHTML;
                document.getElementById('results').innerHTML = `"""
                
    new_block = r"""document.getElementById('results').innerHTML = `<div class="card" style="padding:20px; background:#FFF3E0; color:#E65100; margin-bottom:20px;"><i class='bx bx-info-circle'></i> Settings API is not connected. The below configurations are read-only and not configurable from UI.</div>` + `"""
    
    html = html.replace(old_block, new_block)
    
    with open('web/index.html', 'w', encoding='utf-8') as f:
        f.write(html)
        
if __name__ == '__main__':
    main()
