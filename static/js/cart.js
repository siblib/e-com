const CartManager = {
    async fetchCart() {
        try {
            const response = await fetch('/api/cart/');
            if (!response.ok) throw new Error('Failed to fetch cart');
            const cartData = await response.json();
            this.updateCartUI(cartData);
            return cartData;
        } catch (error) {
            console.error('Error fetching cart:', error);
        }
    },

    async addToCart(productId, selectedValues, quantity) {
        try {
            const response = await fetch('/api/cart/add/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    product_id: productId,
                    selected_values: selectedValues,
                    quantity: quantity
                })
            });
            if (!response.ok) throw new Error('Failed to add to cart');
            const data = await response.json();
            if (data.success) {
                this.updateCartUI(data.cart);
                this.openCartOffcanvas();
            } else {
                console.error(data.error);
            }
        } catch (error) {
            console.error('Error adding to cart:', error);
        }
    },

    async updateQuantity(itemId, quantity) {
        try {
            const response = await fetch('/api/cart/update/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    item_id: itemId,
                    quantity: quantity
                })
            });
            if (!response.ok) throw new Error('Failed to update cart');
            const data = await response.json();
            if (data.success) {
                this.updateCartUI(data.cart);
            } else {
                console.error(data.error);
            }
        } catch (error) {
            console.error('Error updating quantity:', error);
        }
    },

    async removeItem(itemId) {
        try {
            const response = await fetch('/api/cart/remove/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    item_id: itemId
                })
            });
            if (!response.ok) throw new Error('Failed to remove item');
            const data = await response.json();
            if (data.success) {
                this.updateCartUI(data.cart);
            } else {
                console.error(data.error);
            }
        } catch (error) {
            console.error('Error removing item:', error);
        }
    },

    updateCartUI(cart) {
        // Update header badge
        const badgeElement = document.getElementById('cart-badge-count');
        if (badgeElement) {
            badgeElement.textContent = cart.item_count;
            if (cart.item_count > 0) {
                badgeElement.classList.remove('hidden');
            } else {
                badgeElement.classList.add('hidden');
            }
        }

        // Update offcanvas header
        const offcanvasLabel = document.getElementById('hs-pro-shco-label');
        if (offcanvasLabel) {
            offcanvasLabel.textContent = `Cart (${cart.item_count} items)`;
        }

        // Update offcanvas subtotal
        const offcanvasSubtotal = document.getElementById('cart-subtotal-value');
        if (offcanvasSubtotal) {
            offcanvasSubtotal.textContent = `$${cart.total.toFixed(2)}`;
        }

        // Update "View cart (N)" link
        const viewCartLink = document.getElementById('cart-view-link');
        if (viewCartLink) {
            viewCartLink.textContent = `View cart (${cart.item_count})`;
        }

        // Update items container
        const itemsContainer = document.getElementById('cart-items-container');
        if (itemsContainer) {
            itemsContainer.innerHTML = ''; // Clear current items

            if (cart.items.length === 0) {
                itemsContainer.innerHTML = `
                    <div class="text-center py-10">
                        <p class="text-gray-500 dark:text-neutral-500">Your cart is empty.</p>
                    </div>
                `;
            } else {
                cart.items.forEach(item => {
                    const itemHTML = this.createCartItemHTML(item);
                    itemsContainer.insertAdjacentHTML('beforeend', itemHTML);
                });
            }
        }
    },

    createCartItemHTML(item) {
        // Build variant info lines matching original format: "Color: White", "Size: M"
        let variantListItems = '';
        if (item.variant && item.variant.name) {
            const parts = item.variant.name.split(' / ');
            parts.forEach(part => {
                variantListItems += `
                    <li class="xs2f2 jy5gh dark:text-neutral-500">
                        ${part}
                    </li>
                `;
            });
        }

        // Fallback image
        const imageUrl = item.image_url || '/static/images/photo-1699595749116-33a4a869503c(2)';

        return `
            <!-- Item -->
            <div id="cart-item-${item.id}" class="hs-removing:opacity-0 ufjzp flex p5sau">
                <div class="relative">
                    <img class="e731n fl6qw i5kts x1s1r f4yn1 pb094 dark:bg-neutral-700" src="${imageUrl}" alt="${item.product_name}">

                    <div class="absolute fuv09 kji94 wzd7f tgq8c wn488">
                        <button type="button" class="yhc35 flex jkwm1 items-center n6i5x kghwt xs2f2 aqyoh rsdjd azddh c9jt8 mmvvq disabled:opacity-50 disabled:pointer-events-none focus:outline-hidden rr3j6">
                            <svg class="e731n mo9p3" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                <path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"></path>
                            </svg>
                            <span class="et50x">Add to favorites</span>
                        </button>
                    </div>
                </div>

                <div class="hlt95 flex flex-col">
                    <h4 class="w4xo0 c9jt8 dark:text-neutral-200">
                        ${item.product_name}
                    </h4>

                    <ul class="y18m4 space-y-1">
                        ${variantListItems}
                    </ul>

                    <p class="y18m4 xs2f2 jy5gh dark:text-neutral-500">
                        <span>Qty:</span>
                        <button type="button" class="cart-qty-btn cart-qty-minus inline-flex items-center justify-center cursor-pointer" data-item-id="${item.id}" data-action="decrease" aria-label="Decrease">
                            <svg class="size-3" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"></path></svg>
                        </button>
                        <span class="cart-qty-display" data-item-id="${item.id}">${item.quantity}</span>
                        <button type="button" class="cart-qty-btn cart-qty-plus inline-flex items-center justify-center cursor-pointer" data-item-id="${item.id}" data-action="increase" aria-label="Increase">
                            <svg class="size-3" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"></path><path d="M12 5v14"></path></svg>
                        </button>
                    </p>

                    <span class="y18m4 w4xo0 c9jt8 dark:text-neutral-200">
                        $${item.subtotal.toFixed(2)}
                    </span>

                    <div class="">
                        <button type="button" class="cart-remove-btn inline-flex items-center b1nd2 z4zqw c9jt8 l5oyh povjg iiod0 focus:outline-hidden s6w37 dark:text-neutral-200 dark:hover:text-indigo-400 dark:focus:text-indigo-400" data-item-id="${item.id}">
                            Remove
                        </button>
                    </div>
                </div>
            </div>
            <!-- End Item -->
        `;
    },

    openCartOffcanvas() {
        if (typeof window.HSOverlay !== 'undefined') {
            window.HSOverlay.open('#hs-pro-shco');
        } else {
            console.warn('HSOverlay is not available.');
        }
    },

    init() {
        // Fetch cart on load
        this.fetchCart();

        // Product detail page quantity inc/dec buttons
        document.addEventListener('click', (e) => {
            const decBtn = e.target.closest('.cart-detail-dec');
            if (decBtn) {
                const input = document.getElementById('product-quantity');
                if (input && parseInt(input.value) > 1) {
                    input.value = parseInt(input.value) - 1;
                }
                return;
            }

            const incBtn = e.target.closest('.cart-detail-inc');
            if (incBtn) {
                const input = document.getElementById('product-quantity');
                if (input) {
                    input.value = parseInt(input.value) + 1;
                }
                return;
            }
        });

        // Add to cart button
        const addToCartBtn = document.getElementById('add-to-cart-btn');
        if (addToCartBtn) {
            addToCartBtn.addEventListener('click', () => {
                const productId = addToCartBtn.getAttribute('data-product-id');
                const quantityInput = document.getElementById('product-quantity');
                const quantity = quantityInput ? parseInt(quantityInput.value) : 1;
                
                // Get selected variant values
                const selectedValues = [];
                const variantRadios = document.querySelectorAll('.variant-input:checked');
                variantRadios.forEach(radio => {
                    selectedValues.push(radio.value);
                });
                
                this.addToCart(productId, selectedValues, quantity);
            });
        }

        // Event delegation for cart actions in offcanvas
        document.addEventListener('click', (e) => {
            const removeBtn = e.target.closest('.cart-remove-btn');
            if (removeBtn) {
                const itemId = removeBtn.getAttribute('data-item-id');
                this.removeItem(itemId);
                return;
            }

            const qtyBtn = e.target.closest('.cart-qty-btn');
            if (qtyBtn) {
                const itemId = qtyBtn.getAttribute('data-item-id');
                const action = qtyBtn.getAttribute('data-action');
                const display = document.querySelector(`.cart-qty-display[data-item-id="${itemId}"]`);
                let newQty = parseInt(display.textContent);
                
                if (action === 'increase') {
                    newQty++;
                } else if (action === 'decrease') {
                    newQty--;
                }
                
                if (newQty > 0) {
                    display.textContent = newQty;
                    this.updateQuantity(itemId, newQty);
                } else if (newQty === 0 && action === 'decrease') {
                    this.removeItem(itemId);
                }
            }
        });
    }
};

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', () => {
    CartManager.init();
});
