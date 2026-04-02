from django.urls import path
from .views import home, auth, account, products, checkout, cart, support

urlpatterns = [
    # --- Home ---
    path('', home.index, name='home'),

    # --- Auth ---
    path('login/', auth.login_page, name='login'),
    path('signup/', auth.create_account, name='signup'),
    path('forgot-password/', auth.forgot_password, name='forgot_password'),

    # --- Account ---
    path('account/', account.dashboard, name='account'),
    path('account/profile/', account.personal_info, name='personal_info'),
    path('account/addresses/', account.addresses, name='addresses'),
    path('account/favorites/', account.favorites, name='favorites'),
    path('account/orders/', account.my_orders, name='my_orders'),
    path('account/orders/details/', account.order_details, name='order_details'),

    path('account/payment/', account.payment_methods, name='payment_methods'),
    path('account/returns/', account.account_returns, name='account_returns'),

    # --- Products (Browsing) ---
    path('shop/', products.grid, name='shop_grid'),



    # --- Product Detail Pages ---
    path('product/<int:product_id>/', products.product_detail, name='product_detail'),
    
    # NEW: Sticky Sidebar and Gallery Slider Variations
    path('product/<int:product_id>/sticky/', products.product_sticky_sidebar, name='product_sticky_sidebar'),
    path('product/<int:product_id>/slider/', products.product_gallery_slider, name='product_gallery_slider'),

    # ... (categories and compare urls) ...
    # NEW: Grid Variations
    path('shop/hero/', products.grid_hero, name='shop_grid_hero'),
    path('shop/categories/', products.grid_with_categories, name='shop_grid_categories'),
    path('shop/mini-categories/', products.grid_mini_categories, name='shop_grid_mini'),
    path('shop/sidebar/', products.grid_sidebar, name='shop_grid_sidebar'),
    
    # Categories
    path('categories/', products.categories, name='categories'),
    # NEW: Categories Sidebar
    path('categories/sidebar/', products.categories_sidebar, name='categories_sidebar'),
    
    path('compare/', products.compare, name='compare'),
    
    # NEW: Write Review
    path('product/<int:product_id>/review/', products.write_review, name='write_review'),

    # --- Cart & Checkout ---
    path('cart/', cart.index, name='cart'),
    
    # --- ADD THIS NEW LINE ---
    path('cart/empty/', cart.empty_cart, name='empty_cart'),     
    
    # ... (checkout paths below) ...    
      # --- Checkout Variations ---
    # 1. The Options Page (Entry point for not-logged-in users)
    path('checkout/start/', checkout.checkout_options, name='checkout_options'),

    # 2. Guest Checkout
    path('checkout/guest/', checkout.checkout_guest, name='checkout_guest'),

    # 3. Member/Logged-In Checkout
    path('checkout/member/', checkout.checkout_member, name='checkout_member'),

    path('checkout/review/', checkout.review_and_pay, name='review_and_pay'), # NEW
    path('checkout/payment/', checkout.payment, name='payment'),
    path('checkout/confirmation/', checkout.order_confirmation, name='order_confirmation'),
    # NEW: Order Status (Guest Checkup)
    # Order Status (Displays the results)
    path('order-status/', checkout.order_status, name='order_status'),

    # Order Checkup (The search form)
    path('order-checkup/', checkout.order_checkup, name='order_checkup'),

    # --- Support ---
    path('help/', support.help_center, name='help'),
    # NEW: Help Topic
    path('help/<slug:topic_id>/', support.help_topic, name='help_topic'),
    path('stores/', support.our_stores, name='stores'),
    # NEW: Support Pages
    path('returns/', support.returns, name='returns'),
    path('gift-cards/', support.gift_cards, name='gift_cards'),
    path('newsletter/', support.newsletter, name='newsletter'),
]
