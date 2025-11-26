# Astro Integrations Reference

## Form Services

### Web3Forms (Recommended)
**Why this choice:** Free (250 submissions/month), no backend needed, works perfectly with static sites, built-in spam protection

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

## Analytics

### Plausible Analytics
**Why this choice:** Privacy-focused, GDPR compliant, simple script, no cookie consent needed

```html
<!-- In Layout.astro <head> -->
<script defer 
        data-domain="yoursite.com" 
        src="https://plausible.io/js/script.js">
</script>
```

### Google Analytics 4
**Why include:** Industry standard, most clients already have GA accounts, comprehensive features

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




