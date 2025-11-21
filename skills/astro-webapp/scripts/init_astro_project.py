#!/usr/bin/env python3
"""
Initialize a new Astro project with TypeScript and common configurations.

Usage:
    python init_astro_project.py <project-name> [options]

Options:
    --features    Comma-separated features: tailwind,react,vue,forms,seo
    --template    Astro template: minimal,blog,portfolio (default: minimal)

Example:
    python init_astro_project.py my-site --features tailwind,react,forms
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path


def run_command(cmd, cwd=None):
    """Execute shell command and return output."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd, check=False)
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"Command failed: {e}")
        return False


def create_astro_project(project_name, template="minimal", features=None):
    """Initialize Astro project with specified features."""

    if features is None:
        features = []

    print(f"🚀 Creating Astro project: {project_name}")

    # Create project with Astro CLI
    cmd = f"npm create astro@latest {project_name} -- --template {template} --typescript strict --git --install"
    if not run_command(cmd):
        return False

    project_path = Path(project_name)

    # Add integrations based on features
    if "tailwind" in features:
        print("📦 Adding Tailwind CSS...")
        run_command("npx astro add tailwind -y", cwd=project_path)

    if "react" in features:
        print("📦 Adding React...")
        run_command("npx astro add react -y", cwd=project_path)

    if "vue" in features:
        print("📦 Adding Vue...")
        run_command("npx astro add vue -y", cwd=project_path)

    # Create directory structure
    dirs = ["src/components", "src/layouts", "src/styles", "src/assets", "src/utils"]

    for dir_path in dirs:
        (project_path / dir_path).mkdir(parents=True, exist_ok=True)

    # Add Web3Forms contact form if requested
    if "forms" in features or "contact-form" in features:
        print("📝 Adding contact form component...")
        create_contact_form(project_path)

    # Add SEO component if requested
    if "seo" in features:
        print("🔍 Adding SEO component...")
        create_seo_component(project_path)

    # Create environment file
    env_content = """# Web3Forms Key (get yours at https://web3forms.com)
PUBLIC_WEB3FORMS_KEY=YOUR_ACCESS_KEY_HERE

# Site URL
PUBLIC_SITE_URL=http://localhost:4321

# Production URL (update for deployment)
# PUBLIC_SITE_URL=https://yoursite.com
"""
    (project_path / ".env").write_text(env_content)
    (project_path / ".env.example").write_text(env_content)

    # Add useful scripts to package.json
    package_json_path = project_path / "package.json"
    if package_json_path.exists():
        with open(package_json_path, "r") as f:
            package_data = json.load(f)

        package_data["scripts"].update(
            {
                "preview": "astro preview",
                "check": "astro check && tsc --noEmit",
                "format": "prettier --write .",
            }
        )

        with open(package_json_path, "w") as f:
            json.dump(package_data, f, indent=2)

    print(f"""
✅ Project "{project_name}" created successfully!

📁 Project structure:
   {project_name}/
   ├── src/
   │   ├── components/
   │   ├── layouts/
   │   ├── pages/
   │   ├── styles/
   │   └── assets/
   ├── public/
   ├── .env
   └── package.json

🚀 Get started:
   cd {project_name}
   npm run dev

📚 Next steps:
   - Update .env with your Web3Forms key
   - Customize src/layouts/Layout.astro
   - Add pages in src/pages/
   - Deploy to Netlify or Vercel
""")

    return True


def create_contact_form(project_path):
    """Create a contact form component using Web3Forms."""

    form_component = """---
export interface Props {
  redirectUrl?: string;
  className?: string;
}

const { redirectUrl = "/thank-you", className = "" } = Astro.props;
const WEB3FORMS_KEY = import.meta.env.PUBLIC_WEB3FORMS_KEY;
---

<form 
  action="https://api.web3forms.com/submit" 
  method="POST"
  class={`max-w-lg mx-auto ${className}`}
>
  <input type="hidden" name="access_key" value={WEB3FORMS_KEY}>
  <input type="hidden" name="redirect" value={redirectUrl}>
  
  <div class="space-y-4">
    <div>
      <label for="name" class="block text-sm font-medium mb-2">
        Name
      </label>
      <input 
        type="text" 
        id="name"
        name="name" 
        required
        class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        placeholder="John Doe"
      >
    </div>
    
    <div>
      <label for="email" class="block text-sm font-medium mb-2">
        Email
      </label>
      <input 
        type="email" 
        id="email"
        name="email" 
        required
        class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        placeholder="john@example.com"
      >
    </div>
    
    <div>
      <label for="message" class="block text-sm font-medium mb-2">
        Message
      </label>
      <textarea 
        id="message"
        name="message" 
        required
        rows="5"
        class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        placeholder="Your message here..."
      ></textarea>
    </div>
    
    <button 
      type="submit" 
      class="w-full bg-blue-600 text-white font-semibold py-2 px-4 rounded-md hover:bg-blue-700 transition duration-200"
    >
      Send Message
    </button>
  </div>
</form>
"""

    component_path = project_path / "src/components/ContactForm.astro"
    component_path.write_text(form_component)

    # Create thank you page
    thank_you_page = """---
import Layout from '../layouts/Layout.astro';
---

<Layout title="Thank You">
  <main class="min-h-screen flex items-center justify-center">
    <div class="text-center">
      <h1 class="text-4xl font-bold mb-4">Thank You!</h1>
      <p class="text-lg text-gray-600 mb-8">
        Your message has been sent successfully. We'll get back to you soon.
      </p>
      <a 
        href="/" 
        class="inline-block bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700 transition"
      >
        Back to Home
      </a>
    </div>
  </main>
</Layout>
"""

    thank_you_path = project_path / "src/pages/thank-you.astro"
    thank_you_path.write_text(thank_you_page)


def create_seo_component(project_path):
    """Create an SEO component for meta tags."""

    seo_component = """---
export interface Props {
  title: string;
  description: string;
  image?: string;
  canonical?: string;
}

const { 
  title, 
  description, 
  image = '/og-image.jpg',
  canonical 
} = Astro.props;

const siteUrl = import.meta.env.PUBLIC_SITE_URL || 'http://localhost:4321';
const canonicalUrl = canonical || new URL(Astro.url.pathname, siteUrl).href;
const imageUrl = new URL(image, siteUrl).href;
---

<!-- Primary Meta Tags -->
<title>{title}</title>
<meta name="title" content={title} />
<meta name="description" content={description} />
<link rel="canonical" href={canonicalUrl} />

<!-- Open Graph / Facebook -->
<meta property="og:type" content="website" />
<meta property="og:url" content={canonicalUrl} />
<meta property="og:title" content={title} />
<meta property="og:description" content={description} />
<meta property="og:image" content={imageUrl} />

<!-- Twitter -->
<meta property="twitter:card" content="summary_large_image" />
<meta property="twitter:url" content={canonicalUrl} />
<meta property="twitter:title" content={title} />
<meta property="twitter:description" content={description} />
<meta property="twitter:image" content={imageUrl} />
"""

    component_path = project_path / "src/components/SEO.astro"
    component_path.write_text(seo_component)


def main():
    parser = argparse.ArgumentParser(description="Initialize an Astro project")
    parser.add_argument("project_name", help="Name of the project")
    parser.add_argument("--template", default="minimal", help="Astro template to use")
    parser.add_argument("--features", help="Comma-separated list of features")

    args = parser.parse_args()

    features = []
    if args.features:
        features = [f.strip() for f in args.features.split(",")]

    success = create_astro_project(args.project_name, template=args.template, features=features)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
