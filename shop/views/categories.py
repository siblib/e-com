from django.shortcuts import render

# CHANGE THIS: logic was likely "def categories(request):"
# TO THIS: Rename it to "index" so it matches your new structure
def index(request): 
    return render(request, 'categories/index.html')

def detail(request, category_id):
    # You might have called this "category_detail" before. 
    # It is cleaner to just call it "detail" inside this file.
    return render(request, 'categories/detail.html', {'category_id': category_id})
