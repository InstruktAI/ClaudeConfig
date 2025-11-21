# Astro Integrations Reference

## Form Services

### Web3Forms (Recommended)
Free tier: 250 submissions/month

```astro
<form action="https://api.web3forms.com/submit" method="POST">
  <input type="hidden" name="access_key" value="YOUR_KEY">
  <input type="hidden" name="redirect" value="https://yoursite.com/thanks">
  <input type="hidden" name="subject" value="New Contact Form Submission">
  <input type="hidden" name="from_name" value="Your Site">
  
  <!-- Optional: Custom email template -->
  <input type="hidden" name="template" value="box">
  
  <!-- Honeypot spam protection -->
  <input type="checkbox" name="botcheck" class="hidden" style="display: none;">
</form>
```

### Formspree
```astro
<form action="https://formspree.io/f/YOUR_FORM_ID" method="POST">
  <input type="email" name="email" required>
  <textarea name="message" required></textarea>
  <button type="submit">Send</button>
</form>
```

## Booking & Calendar

### Cal.com Embed
```astro
---
// CalendarEmbed.astro
export interface Props {
  calLink: string; // e.g., "john-doe/30min"
  theme?: "light" | "dark" | "auto";
}

const { calLink, theme = "auto" } = Astro.props;
---

<div id="cal-embed"></div>

<script define:vars={{ calLink, theme }}>
  (function (C, A, L) {
    let p = function (a, ar) { a.q.push(ar); };
    let d = C.document;
    C.Cal = C.Cal || function () {
      let cal = C.Cal;
      let ar = arguments;
      if (!cal.loaded) {
        cal.ns = {};
        cal.q = cal.q || [];
        d.head.appendChild(d.createElement("script")).src = A;
        cal.loaded = true;
      }
      if (ar[0] === L) {
        const api = function () { p(api, arguments); };
        const namespace = ar[1];
        api.q = api.q || [];
        typeof namespace === "string" ? (cal.ns[namespace] = api) && p(api, ar) : p(cal, ar);
        return;
      }
      p(cal, ar);
    };
  })(window, "https://app.cal.com/embed/embed.js", "init");
  
  Cal("init", { origin: "https://cal.com" });
  Cal("inline", {
    elementOrSelector: "#cal-embed",
    calLink: calLink,
    layout: "month_view",
    config: { theme: theme }
  });
</script>

<style>
  #cal-embed {
    width: 100%;
    height: 100%;
    overflow: hidden;
  }
</style>
```

### Calendly
```html
<!-- Inline Widget -->
<div class="calendly-inline-widget" 
     data-url="https://calendly.com/YOUR_USER/30min"
     style="min-width:320px;height:630px;">
</div>
<script type="text/javascript" 
        src="https://assets.calendly.com/assets/external/widget.js" 
        async>
</script>
```

## Analytics

### Plausible Analytics
```html
<!-- In Layout.astro <head> -->
<script defer 
        data-domain="yoursite.com" 
        src="https://plausible.io/js/script.js">
</script>
```

### Google Analytics 4
```astro
---
// GoogleAnalytics.astro
const GA_MEASUREMENT_ID = import.meta.env.PUBLIC_GA_MEASUREMENT_ID;
---

{GA_MEASUREMENT_ID && (
  <>
    <script async src={`https://www.googletagmanager.com/gtag/js?id=${GA_MEASUREMENT_ID}`}></script>
    <script define:vars={{ GA_MEASUREMENT_ID }}>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', GA_MEASUREMENT_ID);
    </script>
  </>
)}
```

## Payment Integration

### Stripe Checkout
```typescript
// src/pages/api/create-checkout.ts
import type { APIRoute } from 'astro';
import Stripe from 'stripe';

const stripe = new Stripe(import.meta.env.STRIPE_SECRET_KEY);

export const POST: APIRoute = async ({ request }) => {
  const { priceId, successUrl, cancelUrl } = await request.json();
  
  const session = await stripe.checkout.sessions.create({
    line_items: [{ price: priceId, quantity: 1 }],
    mode: 'payment',
    success_url: successUrl,
    cancel_url: cancelUrl,
  });
  
  return new Response(JSON.stringify({ url: session.url }), {
    status: 200,
    headers: { 'Content-Type': 'application/json' },
  });
};
```

### PayPal Buttons
```html
<div id="paypal-button-container"></div>
<script src="https://www.paypal.com/sdk/js?client-id=YOUR_CLIENT_ID&currency=EUR"></script>
<script>
  paypal.Buttons({
    createOrder: (data, actions) => {
      return actions.order.create({
        purchase_units: [{
          amount: { value: '25.00' }
        }]
      });
    },
    onApprove: (data, actions) => {
      return actions.order.capture().then(function(details) {
        // Handle successful payment
        window.location.href = '/thank-you';
      });
    }
  }).render('#paypal-button-container');
</script>
```

## Email Services

### SendGrid
```typescript
// src/pages/api/send-email.ts
import type { APIRoute } from 'astro';
import sgMail from '@sendgrid/mail';

sgMail.setApiKey(import.meta.env.SENDGRID_API_KEY);

export const POST: APIRoute = async ({ request }) => {
  const { to, subject, text, html } = await request.json();
  
  const msg = {
    to,
    from: 'noreply@yoursite.com',
    subject,
    text,
    html,
  };
  
  try {
    await sgMail.send(msg);
    return new Response(JSON.stringify({ success: true }), {
      status: 200,
    });
  } catch (error) {
    return new Response(JSON.stringify({ error: error.message }), {
      status: 500,
    });
  }
};
```

### Resend
```typescript
// Using Resend with React Email templates
import { Resend } from 'resend';
const resend = new Resend(import.meta.env.RESEND_API_KEY);

await resend.emails.send({
  from: 'onboarding@resend.dev',
  to: 'user@example.com',
  subject: 'Welcome!',
  html: '<p>Welcome to our service!</p>',
});
```

## CMS Integration

### Contentful
```typescript
// src/lib/contentful.ts
import contentful from 'contentful';

export const client = contentful.createClient({
  space: import.meta.env.CONTENTFUL_SPACE_ID,
  accessToken: import.meta.env.CONTENTFUL_ACCESS_TOKEN,
});

// Usage in .astro file
const entries = await client.getEntries({
  content_type: 'blogPost',
  limit: 10,
});
```

### Strapi
```typescript
// Fetch from Strapi API
const response = await fetch('https://your-strapi.com/api/articles?populate=*');
const { data } = await response.json();
```

## Social Media

### Twitter/X Embed
```html
<blockquote class="twitter-tweet">
  <a href="https://twitter.com/user/status/TWEET_ID"></a>
</blockquote>
<script async src="https://platform.twitter.com/widgets.js"></script>
```

### Instagram Feed
Use Instagram Basic Display API or third-party services like Elfsight.

## Maps

### Mapbox GL JS
```astro
---
// Map.astro
const MAPBOX_TOKEN = import.meta.env.PUBLIC_MAPBOX_TOKEN;
---

<div id="map" style="height: 400px;"></div>

<link href='https://api.mapbox.com/mapbox-gl-js/v2.15.0/mapbox-gl.css' rel='stylesheet' />
<script src='https://api.mapbox.com/mapbox-gl-js/v2.15.0/mapbox-gl.js'></script>

<script define:vars={{ MAPBOX_TOKEN }}>
  mapboxgl.accessToken = MAPBOX_TOKEN;
  const map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v12',
    center: [-74.5, 40],
    zoom: 9
  });
</script>
```

### Google Maps
```html
<div id="map" style="height: 400px;"></div>
<script>
  function initMap() {
    const map = new google.maps.Map(document.getElementById("map"), {
      center: { lat: -34.397, lng: 150.644 },
      zoom: 8,
    });
  }
</script>
<script async defer 
  src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&callback=initMap">
</script>
```

## Comments

### Giscus (GitHub Discussions)
```astro
<script src="https://giscus.app/client.js"
        data-repo="YOUR_USERNAME/YOUR_REPO"
        data-repo-id="YOUR_REPO_ID"
        data-category="Announcements"
        data-category-id="YOUR_CATEGORY_ID"
        data-mapping="pathname"
        data-strict="0"
        data-reactions-enabled="1"
        data-emit-metadata="0"
        data-input-position="top"
        data-theme="light"
        data-lang="en"
        crossorigin="anonymous"
        async>
</script>
```

## Search

### Algolia DocSearch
```html
<div id="docsearch"></div>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@docsearch/css@3" />
<script src="https://cdn.jsdelivr.net/npm/@docsearch/js@3"></script>
<script>
  docsearch({
    container: '#docsearch',
    appId: 'YOUR_APP_ID',
    indexName: 'YOUR_INDEX_NAME',
    apiKey: 'YOUR_SEARCH_API_KEY',
  });
</script>
```

## Authentication

### Auth.js (NextAuth for Astro)
```bash
npm install @auth/core @auth/astro
```

```typescript
// auth.config.ts
import type { AuthConfig } from "@auth/core";
import GitHub from "@auth/core/providers/github";

export default {
  providers: [
    GitHub({
      clientId: import.meta.env.GITHUB_CLIENT_ID,
      clientSecret: import.meta.env.GITHUB_CLIENT_SECRET,
    }),
  ],
} satisfies AuthConfig;
```
