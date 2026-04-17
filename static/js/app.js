const updateText = (selector, newText) => {
    const elements = document.querySelectorAll(selector);
    elements.forEach((element) => {
        element.textContent = isNaN(newText) ? newText : Math.floor(newText);
    });
};
const updateAttr = (selector, attr, val) => {
    const elements = document.querySelectorAll(selector);
    elements.forEach((element) => {
        element.setAttribute(attr, val);
    });
};
const handleEl = (selector, cb) => {
    const elements = document.querySelectorAll(selector);
    elements.forEach((element) => {
        cb(element);
    });
};

document.addEventListener("DOMContentLoaded", function () {
    const account = window.accountVariables;
    const defaults = window.defaultVariables;

    if (account) {
        updateText("[data-account-name]", account.name);
        updateText("[data-account-email]", account.email);

        handleEl("[data-p-team-upgrade-checkout-link]", (el) => {
            if (account.hasTeamLicense) {
                el.parentElement.parentElement.remove();
            } else {
                el.parentElement.setAttribute(
                    "href",
                    account.teamUpgradeCheckoutLink
                );
            }
        });
    }
    handleEl("[data-download]", (el) => {
        el.addEventListener("click", (e) => {
            e.preventDefault();
            const name = el.dataset.download;
            window.location.href = defaults.baseUrl + "/files/download/" + name;
        });
    });

    handleEl("[data-sign-out]", (el) => {
        el.addEventListener(
            "click",
            () => (window.location = defaults.baseUrl + "/logout")
        );
    });

    // === PRELINE RE-INITIALIZATION FOR DYNAMIC TABS/CAROUSELS ===
    if (window.HSCore && typeof HSCore.components === 'object') {
        // Re-initialize tabs
        document.querySelectorAll('[data-hs-tab]').forEach(el => {
            if (!el._hsTabInitialized) {
                try {
                    HSCore.components.HSTab.init(el);
                    el._hsTabInitialized = true;
                } catch (e) {
                    console.warn('HSTab init failed:', e);
                }
            }
        });
        
        // Re-initialize carousels
        document.querySelectorAll('[data-hs-carousel]').forEach(el => {
            if (!el._hsCarouselInitialized) {
                try {
                    HSCore.components.HSCarousel.init(el);
                    el._hsCarouselInitialized = true;
                } catch (e) {
                    console.warn('HSCarousel init failed:', e);
                }
            }
        });
    }
    // === END PRELINE RE-INITIALIZATION ===

});
