from django.shortcuts import render

def help_center(request):
    return render(request, 'support/help.html')

def returns(request): # Covers Returns, Refunds, Exchanges
    return render(request, 'support/returns.html')

def our_stores(request):
    return render(request, 'support/stores.html')

def gift_cards(request):
    return render(request, 'support/gift_cards.html')

def help_topic(request, topic_id):
    # Matches "Help: About Topic"
    return render(request, 'support/help_topic.html', {'topic_id': topic_id})

def newsletter(request):
    # Matches "Email Newsletter"
    return render(request, 'support/newsletter.html')

