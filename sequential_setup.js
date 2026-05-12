(function(){
"use strict";

/* ============================================================
   WORKFLOW DATA – edit this array to change the pipeline
   status: "completed" | "active" | "pending"
   ============================================================ */
const WORKFLOW = [
  {
    id:"home", title:"Home Page", status:"completed",
    icon:"🏠",
    explanation:"The storefront landing page is the first thing visitors see. It must be built first because every other page links back to it and it establishes the global layout, header, footer, and nav — shared by all subsequent pages.",
    prev:null, next:"Auth Pages",
    variants:[
      {name:"Home", url:"http://0.0.0.0:8382/", path:"path('', home.index, name='home')"}
    ],
    checklist:["Global layout & nav","Hero section","Featured products","Footer"]
  },
  {
    id:"auth", title:"Auth Pages", status:"completed",
    icon:"🔐",
    explanation:"Authentication pages come second because user accounts underpin the entire personalized experience — favorites, orders, checkout. Building them early lets you test logged-in vs guest flows for every subsequent page.",
    prev:"Home Page", next:"Product Browsing (Shop Grid)",
    variants:[
      {name:"Login", url:"http://0.0.0.0:8382/login/", path:"path('login/', auth.login_page, name='login')"},
      {name:"Sign Up", url:"http://0.0.0.0:8382/signup/", path:"path('signup/', auth.create_account, name='signup')"},
      {name:"Forgot Password", url:"http://0.0.0.0:8382/forgot-password/", path:"path('forgot-password/', auth.forgot_password, name='forgot_password')"}
    ],
    checklist:["Login form + validation","Sign up form","Forgot password flow","Session/cookie handling"]
  },
  {
    id:"shop", title:"Product Browsing (Shop Grid)", status:"active",
    icon:"🛍️",
    explanation:"The shop grid is the primary product discovery surface. It must exist before product detail pages because users navigate FROM the grid TO individual products. All grid variants share the core product-card component and filtering/sorting logic.",
    prev:"Auth Pages", next:"Categories",
    variants:[
      {name:"Default Grid", url:"http://0.0.0.0:8382/shop/", path:"path('shop/', products.grid, name='shop_grid')"},
      {name:"Hero Grid", url:"http://0.0.0.0:8382/shop/hero/", path:"path('shop/hero/', products.grid_hero, name='shop_grid_hero')"},
      {name:"With Categories", url:"http://0.0.0.0:8382/shop/categories/", path:"path('shop/categories/', products.grid_with_categories, name='shop_grid_categories')"},
      {name:"Mini Categories", url:"http://0.0.0.0:8382/shop/mini-categories/", path:"path('shop/mini-categories/', products.grid_mini_categories, name='shop_grid_mini')"},
      {name:"Sidebar", url:"http://0.0.0.0:8382/shop/sidebar/", path:"path('shop/sidebar/', products.grid_sidebar, name='shop_grid_sidebar')"}
    ],
    checklist:["Product card component","Grid layout","Filtering & sorting","Pagination","Search integration"]
  },
  {
    id:"categories", title:"Categories", status:"pending",
    icon:"📂",
    explanation:"Category pages organize products into browsable groups. They depend on the shop grid's product-card component and link directly into filtered grid views. Building them after the grid means reusing the same card and filter components.",
    prev:"Product Browsing (Shop Grid)", next:"Brands",
    variants:[
      {name:"Categories", url:"http://0.0.0.0:8382/categories/", path:"path('categories/', products.categories, name='categories')"},
      {name:"Categories Sidebar", url:"http://0.0.0.0:8382/categories/sidebar/", path:"path('categories/sidebar/', products.categories_sidebar, name='categories_sidebar')"}
    ],
    checklist:["Category listing","Category images/icons","Link to filtered shop grid"]
  },
  {
    id:"brands", title:"Brands", status:"pending",
    icon:"🏷️",
    explanation:"Brand pages are similar to categories but filter by manufacturer. They reuse the same grid and product-card components. Building after categories ensures the filtering pattern is already established.",
    prev:"Categories", next:"Product Detail",
    variants:[
      {name:"Brand Products", url:"http://0.0.0.0:8382/brands/example-brand/", path:"path('brands/<slug:brand_slug>/', products.products_by_brand, name='products_by_brand')"}
    ],
    checklist:["Brand listing page","Brand-filtered product grid","Brand logo/banner"]
  },
  {
    id:"product_detail", title:"Product Detail", status:"active",
    icon:"📦",
    explanation:"The product detail page is the heart of conversion — where users decide to buy. It depends on the grid (for 'related products' and breadcrumbs) and must be built before cart/checkout because 'Add to Cart' lives here. All detail variants share the same product data model.",
    prev:"Brands", next:"Product Reviews",
    variants:[
      {name:"Default Detail", url:"http://0.0.0.0:8382/product/iphone17/", path:"path('product/<slug:slug>/', products.product_detail, name='product_detail')"},
      {name:"Sticky Sidebar", url:"http://0.0.0.0:8382/product/1/sticky/", path:"path('product/<int:product_id>/sticky/', products.product_sticky_sidebar, name='product_sticky_sidebar')"},
      {name:"Gallery Slider", url:"http://0.0.0.0:8382/product/1/slider/", path:"path('product/<int:product_id>/slider/', products.product_gallery_slider, name='product_gallery_slider')"}
    ],
    checklist:["Image gallery","Product info & pricing","Variant selector (size/color)","Add to Cart button","Related/complementary products","Breadcrumbs"]
  },
  {
    id:"reviews", title:"Product Reviews", status:"pending",
    icon:"⭐",
    explanation:"Reviews attach to individual products, so they require the product detail page to exist first. They influence purchase decisions and must be in place before checkout to drive conversions.",
    prev:"Product Detail", next:"Compare",
    variants:[
      {name:"Write Review", url:"http://0.0.0.0:8382/product/1/review/", path:"path('product/<int:product_id>/review/', products.write_review, name='write_review')"}
    ],
    checklist:["Review form (stars, text, images)","Review display on product page","Verified purchase badge","Helpful vote"]
  },
  {
    id:"compare", title:"Compare Products", status:"pending",
    icon:"⚖️",
    explanation:"Comparison requires product data and attributes to already be structured from the detail page work. It helps users decide between similar products before adding to cart.",
    prev:"Product Reviews", next:"Cart",
    variants:[
      {name:"Compare", url:"http://0.0.0.0:8382/compare/", path:"path('compare/', products.compare, name='compare')"}
    ],
    checklist:["Side-by-side table","Add/remove from compare","Spec highlighting"]
  },
  {
    id:"cart", title:"Shopping Cart", status:"pending",
    icon:"🛒",
    explanation:"The cart collects items from product detail pages — it can't function until 'Add to Cart' works. It's the direct prerequisite for checkout. Both cart states (with items and empty) should be built together.",
    prev:"Compare Products", next:"Checkout Flow",
    variants:[
      {name:"Cart", url:"http://0.0.0.0:8382/cart/", path:"path('cart/', cart.index, name='cart')"},
      {name:"Empty Cart", url:"http://0.0.0.0:8382/cart/empty/", path:"path('cart/empty/', cart.empty_cart, name='empty_cart')"}
    ],
    checklist:["Cart item list","Quantity update","Remove item","Price summary","Proceed to checkout CTA","Empty state"]
  },
  {
    id:"checkout", title:"Checkout Flow", status:"pending",
    icon:"💳",
    explanation:"Checkout is the multi-step purchase funnel. It depends on cart data and auth (guest vs member). The sub-pages must be built in order: options → info entry → review → payment → confirmation. This is the revenue-critical path.",
    prev:"Shopping Cart", next:"Order Tracking",
    variants:[
      {name:"Checkout Options", url:"http://0.0.0.0:8382/checkout/start/", path:"path('checkout/start/', checkout.checkout_options, name='checkout_options')"},
      {name:"Guest Checkout", url:"http://0.0.0.0:8382/checkout/guest/", path:"path('checkout/guest/', checkout.checkout_guest, name='checkout_guest')"},
      {name:"Member Checkout", url:"http://0.0.0.0:8382/checkout/member/", path:"path('checkout/member/', checkout.checkout_member, name='checkout_member')"},
      {name:"Review & Pay", url:"http://0.0.0.0:8382/checkout/review/", path:"path('checkout/review/', checkout.review_and_pay, name='review_and_pay')"},
      {name:"Payment", url:"http://0.0.0.0:8382/checkout/payment/", path:"path('checkout/payment/', checkout.payment, name='payment')"},
      {name:"Order Confirmation", url:"http://0.0.0.0:8382/checkout/confirmation/", path:"path('checkout/confirmation/', checkout.order_confirmation, name='order_confirmation')"}
    ],
    checklist:["Guest vs member routing","Shipping address form","Billing form","Payment integration","Order summary","Confirmation page"]
  },
  {
    id:"order_tracking", title:"Order Tracking", status:"pending",
    icon:"📍",
    explanation:"Order tracking comes after checkout because it displays data created by the purchase flow. It serves both logged-in users and guests who need to look up orders by email/number.",
    prev:"Checkout Flow", next:"Account Dashboard",
    variants:[
      {name:"Order Status", url:"http://0.0.0.0:8382/order-status/", path:"path('order-status/', checkout.order_status, name='order_status')"},
      {name:"Order Checkup", url:"http://0.0.0.0:8382/order-checkup/", path:"path('order-checkup/', checkout.order_checkup, name='order_checkup')"}
    ],
    checklist:["Status timeline","Guest lookup form","Order detail view"]
  },
  {
    id:"account", title:"Account Dashboard", status:"pending",
    icon:"👤",
    explanation:"The account area aggregates data from orders, favorites, and addresses — all generated by earlier flows. It's best built after the core shopping flow is functional so there's real data to display. All sub-pages share the account sidebar layout.",
    prev:"Order Tracking", next:"Support & Help",
    variants:[
      {name:"Dashboard", url:"http://0.0.0.0:8382/account/", path:"path('account/', account.dashboard, name='account')"},
      {name:"Personal Info", url:"http://0.0.0.0:8382/account/profile/", path:"path('account/profile/', account.personal_info, name='personal_info')"},
      {name:"Addresses", url:"http://0.0.0.0:8382/account/addresses/", path:"path('account/addresses/', account.addresses, name='addresses')"},
      {name:"Favorites", url:"http://0.0.0.0:8382/account/favorites/", path:"path('account/favorites/', account.favorites, name='favorites')"},
      {name:"My Orders", url:"http://0.0.0.0:8382/account/orders/", path:"path('account/orders/', account.my_orders, name='my_orders')"},
      {name:"Order Details", url:"http://0.0.0.0:8382/account/orders/details/", path:"path('account/orders/details/', account.order_details, name='order_details')"},
      {name:"Payment Methods", url:"http://0.0.0.0:8382/account/payment/", path:"path('account/payment/', account.payment_methods, name='payment_methods')"},
      {name:"Returns", url:"http://0.0.0.0:8382/account/returns/", path:"path('account/returns/', account.account_returns, name='account_returns')"}
    ],
    checklist:["Account sidebar nav","Dashboard overview","Profile edit form","Address CRUD","Favorites list","Order history","Payment methods","Returns management"]
  },
  {
    id:"support", title:"Support & Help", status:"pending",
    icon:"🆘",
    explanation:"Support pages are the last priority because they're informational and don't block the core shopping flow. They provide help content, store locations, and policies that complement the functional e-commerce experience.",
    prev:"Account Dashboard", next:null,
    variants:[
      {name:"Help Center", url:"http://0.0.0.0:8382/help/", path:"path('help/', support.help_center, name='help')"},
      {name:"Help Topic", url:"http://0.0.0.0:8382/help/shipping/", path:"path('help/<slug:topic_id>/', support.help_topic, name='help_topic')"},
      {name:"Our Stores", url:"http://0.0.0.0:8382/stores/", path:"path('stores/', support.our_stores, name='stores')"},
      {name:"Returns Policy", url:"http://0.0.0.0:8382/returns/", path:"path('returns/', support.returns, name='returns')"},
      {name:"Gift Cards", url:"http://0.0.0.0:8382/gift-cards/", path:"path('gift-cards/', support.gift_cards, name='gift_cards')"},
      {name:"Newsletter", url:"http://0.0.0.0:8382/newsletter/", path:"path('newsletter/', support.newsletter, name='newsletter')"}
    ],
    checklist:["Help center layout","FAQ / topic pages","Store locator","Returns policy page","Gift cards page","Newsletter signup"]
  }
];

const STORAGE_KEY = "ecom_workflow_state";

/* ---- State ---- */
let state = loadState();
let editMode = false;

function defaultState(){
  const s = {};
  WORKFLOW.forEach(w=>{
    s[w.id] = { status: w.status, checklist: w.checklist.map(()=>false), open: w.status==="active" };
  });
  return s;
}
function loadState(){
  try{ const raw=localStorage.getItem(STORAGE_KEY); if(raw) return JSON.parse(raw); } catch(e){}
  return defaultState();
}
function saveState(){ localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); }
function ensureState(id, step){
  if(!state[id]) state[id] = { status:step.status, checklist:step.checklist.map(()=>false), open:false };
  while(state[id].checklist.length < step.checklist.length) state[id].checklist.push(false);
}

/* ---- Render ---- */
function render(){
  const pipe = document.getElementById("pipeline");
  pipe.innerHTML = "";
  WORKFLOW.forEach((step,i)=>{
    ensureState(step.id, step);
    const st = state[step.id];
    // connector arrow
    if(i > 0){
      const conn = document.createElement("div");
      conn.className = "connector";
      conn.innerHTML = `<svg width="24" height="32" viewBox="0 0 24 32"><path d="M12 0v24M6 20l6 8 6-8" fill="none" stroke="var(--accent)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>`;
      pipe.appendChild(conn);
    }
    // card
    const card = document.createElement("div");
    card.className = `step-card status-${st.status}${st.open?" open":""}`;
    card.dataset.id = step.id;
    card.dataset.status = st.status;
    card.innerHTML = buildCard(step, st, i);
    pipe.appendChild(card);
  });
  bindEvents();
  updateProgress();
}

function buildCard(step, st, idx){
  const statusLabel = st.status.charAt(0).toUpperCase()+st.status.slice(1);
  const checkedCount = st.checklist.filter(Boolean).length;
  const totalCheck = step.checklist.length;
  const variantCount = step.variants.length;

  let html = `
  <div class="card-header" data-id="${step.id}">
    ${editMode?'<span class="drag-handle" style="display:flex">⠿</span>':''}
    <div class="step-number">${idx+1}</div>
    <div class="card-title">
      <h3>${step.icon} ${step.title}</h3>
      <div class="card-meta">
        <span>📄 ${variantCount} variant${variantCount>1?'s':''}</span>
        <span>☑️ ${checkedCount}/${totalCheck}</span>
      </div>
    </div>
    <span class="status-badge">${statusLabel}</span>
    <span class="chevron">▼</span>
  </div>
  <div class="card-body"><div class="card-content">`;

  // Explanation
  html += `<div class="explanation">${step.explanation}`;
  html += `<div class="dep-arrows">`;
  if(step.prev) html += `<span class="dep-arrow">← ${step.prev}</span>`;
  if(step.next) html += `<span class="dep-arrow">${step.next} →</span>`;
  html += `</div></div>`;

  // Variants
  html += `<div class="variants-section"><div class="variants-header">🔀 Page Variants</div><div class="variant-list">`;
  step.variants.forEach(v=>{
    html += `<div class="variant-item">
      <div style="flex:1">
        <div class="v-name">${v.name}</div>
        <a href="${v.url}" target="_blank" class="v-url">${v.url}</a><br>
        <span class="v-path">${v.path}</span>
      </div>
    </div>`;
  });
  html += `</div></div>`;

  // Checklist
  html += `<div class="checklist"><div class="checklist-title">✅ Development Checklist</div>`;
  step.checklist.forEach((item,ci)=>{
    const checked = st.checklist[ci];
    html += `<label class="check-item${checked?' done':''}">
      <input type="checkbox" data-step="${step.id}" data-ci="${ci}" ${checked?'checked':''}>
      <span>${item}</span>
    </label>`;
  });
  html += `</div>`;

  // Status controls (edit mode)
  html += `<div class="status-controls">
    <button class="btn btn-sm btn-outline" data-set-status="completed" data-step="${step.id}">✅ Completed</button>
    <button class="btn btn-sm btn-outline" data-set-status="active" data-step="${step.id}">🔵 Active</button>
    <button class="btn btn-sm btn-outline" data-set-status="pending" data-step="${step.id}">⏳ Pending</button>
  </div>`;

  html += `</div></div>`;
  return html;
}

/* ---- Events ---- */
function bindEvents(){
  // Toggle open/close
  document.querySelectorAll(".card-header").forEach(h=>{
    h.addEventListener("click", ()=>{
      const id = h.dataset.id;
      state[id].open = !state[id].open;
      saveState(); render();
    });
  });
  // Checklist
  document.querySelectorAll('.check-item input[type="checkbox"]').forEach(cb=>{
    cb.addEventListener("change", e=>{
      e.stopPropagation();
      const sid = cb.dataset.step, ci = parseInt(cb.dataset.ci);
      state[sid].checklist[ci] = cb.checked;
      saveState(); render();
    });
  });
  // Status buttons
  document.querySelectorAll("[data-set-status]").forEach(btn=>{
    btn.addEventListener("click", e=>{
      e.stopPropagation();
      const sid = btn.dataset.step;
      state[sid].status = btn.dataset.setStatus;
      saveState(); render();
    });
  });
}

function updateProgress(){
  const total = WORKFLOW.length;
  const done = WORKFLOW.filter(w=> state[w.id] && state[w.id].status==="completed").length;
  document.getElementById("progressBadge").textContent = `${done} / ${total} completed`;
  const pct = Math.round((done/total)*100);
  document.getElementById("progressPct").textContent = pct+"%";
  const circle = document.getElementById("progressCircle");
  const r = 18, c = 2*Math.PI*r;
  circle.style.strokeDasharray = c;
  circle.style.strokeDashoffset = c - (c * done / total);
}

/* ---- Top-bar controls ---- */
document.getElementById("btnCollapseAll").addEventListener("click",()=>{
  WORKFLOW.forEach(w=>{ if(state[w.id]) state[w.id].open=false; });
  saveState(); render();
});
document.getElementById("btnExpandAll").addEventListener("click",()=>{
  WORKFLOW.forEach(w=>{ if(state[w.id]) state[w.id].open=true; });
  saveState(); render();
});
document.getElementById("btnEditMode").addEventListener("click",()=>{
  editMode = !editMode;
  document.body.classList.toggle("edit-mode", editMode);
  document.getElementById("btnEditMode").textContent = editMode ? "✅ Done Editing" : "✏️ Edit Mode";
  render();
});

/* ---- Filters ---- */
document.querySelectorAll(".filter-btn").forEach(btn=>{
  btn.addEventListener("click",()=>{
    document.querySelectorAll(".filter-btn").forEach(b=>b.classList.remove("active"));
    btn.classList.add("active");
    const f = btn.dataset.filter;
    document.querySelectorAll(".step-card").forEach(card=>{
      if(f==="all") card.classList.remove("filtered-out");
      else card.classList.toggle("filtered-out", card.dataset.status !== f);
    });
    // also hide connectors next to hidden cards
    document.querySelectorAll(".connector").forEach(c=>{
      const next = c.nextElementSibling;
      c.style.display = (next && next.classList.contains("filtered-out")) ? "none" : "";
    });
  });
});

/* ---- Init ---- */
render();
})();
