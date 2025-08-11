# 📚 Gitignore Patterns Guide

This document explains the comprehensive `.gitignore` patterns used in the Perplexity Clone project, following industry standards for modern full-stack applications.

## 🎯 Overview

Our `.gitignore` configuration follows industry best practices and covers:

- **Python Backend** - FastAPI, virtual environments, testing
- **Next.js Frontend** - React, TypeScript, build tools
- **Docker & Infrastructure** - Containers, monitoring, Terraform
- **Development Tools** - IDEs, package managers, testing frameworks
- **Operating Systems** - macOS, Windows, Linux
- **Security** - Environment files, secrets, sensitive data

## 🏗️ Architecture-Specific Patterns

### **Python Backend**
```gitignore
# Python bytecode
__pycache__/
*.py[cod]
*$py.class

# Virtual environments
.env
.venv
env/
venv/

# Testing & coverage
.coverage
.pytest_cache/
htmlcov/
.tox/
```

### **Next.js Frontend**
```gitignore
# Next.js build output
.next/
out/
build/

# Next.js cache
.next/cache/
.next/standalone/

# TypeScript
*.tsbuildinfo
next-env.d.ts

# Dependencies
node_modules/
```

### **Docker & Infrastructure**
```gitignore
# Docker
.dockerignore
docker-compose.override.yml

# Terraform
*.tfstate
*.tfstate.*
.terraform/
.terraform.lock.hcl

# Monitoring data
prometheus_data/
grafana_data/
```

## 🔧 Development Tools

### **Package Managers**
```gitignore
# npm
package-lock.json
.npmrc
.npm

# Yarn
yarn.lock
.yarn/*
!.yarn/patches
!.yarn/plugins

# pnpm
pnpm-lock.yaml
.pnpm-store/
```

### **Testing Frameworks**
```gitignore
# Jest
coverage/
.jest/

# Playwright
test-results/
playwright-report/

# Cypress
cypress/videos/
cypress/screenshots/
```

### **Build Tools**
```gitignore
# Vite
dist/
dist-ssr/

# Rollup
.rollup.cache/

# Webpack
.webpack/

# Turbo
.turbo/
```

## 🖥️ IDE & Editor Support

### **VS Code**
```gitignore
.vscode/
*.code-workspace
```

### **JetBrains IDEs**
```gitignore
.idea/
*.iml
*.ipr
*.iws
```

### **Vim/Emacs**
```gitignore
*.swp
*.swo
*~
\#*\#
```

## 💻 Operating System Files

### **macOS**
```gitignore
.DS_Store
.AppleDouble
.LSOverride
Icon
._*
.Spotlight-V100
.Trashes
```

### **Windows**
```gitignore
Thumbs.db
ehthumbs.db
Desktop.ini
$RECYCLE.BIN/
*.tmp
*.temp
```

### **Linux**
```gitignore
*~
.fuse_hidden*
.directory
.Trash-*
.nfs*
```

## 🔒 Security & Environment

### **Environment Files**
```gitignore
# All environment files
.env*

# Except examples
!.env.example
```

### **Secrets & Sensitive Data**
```gitignore
.secrets
secrets/
*.key
*.pem
*.p12
*.pfx
```

## 📁 Project Structure

```
perplexity-clone/
├── .gitignore              # Root gitignore (this file)
├── src/
│   ├── frontend/
│   │   ├── .gitignore     # Frontend-specific patterns
│   │   └── ...
│   ├── api/               # Backend
│   └── middleware/        # Middleware system
├── docker-compose.yml     # Docker services
└── terraform/             # Infrastructure
```

## 🚀 Best Practices

### **1. Layered Approach**
- **Root `.gitignore`**: Project-wide patterns
- **Frontend `.gitignore`**: Next.js-specific patterns
- **Backend patterns**: Python-specific in root

### **2. Security First**
- Always ignore `.env*` files
- Exclude secrets and sensitive data
- Ignore build artifacts and caches

### **3. Performance**
- Ignore large directories (`node_modules/`, `__pycache__/`)
- Exclude build outputs (`.next/`, `dist/`)
- Ignore temporary files and caches

### **4. Team Collaboration**
- Ignore IDE-specific files
- Exclude OS-generated files
- Ignore local development files

## 🔍 Common Patterns Explained

### **Why Ignore `package-lock.json`?**
```gitignore
# npm
package-lock.json
```
**Reason**: In monorepos, lock files can cause conflicts. Use `npm ci` for consistent installs.

### **Why Ignore `.next/`?**
```gitignore
# Next.js build output
.next/
```
**Reason**: Build artifacts are generated and should be rebuilt on each deployment.

### **Why Ignore `__pycache__/`?**
```gitignore
# Python bytecode
__pycache__/
```
**Reason**: Compiled Python files are machine-specific and should be regenerated.

## 📋 Maintenance

### **Regular Updates**
- Review patterns quarterly
- Add new tools as they're adopted
- Remove obsolete patterns

### **Team Onboarding**
- Share this guide with new developers
- Explain why specific patterns exist
- Document any project-specific exclusions

### **Troubleshooting**
If files are still being tracked:
```bash
# Check what's being ignored
git status --ignored

# Force remove from tracking
git rm --cached <file>

# Update gitignore and commit
git add .gitignore
git commit -m "Update gitignore patterns"
```

## 🌟 Industry Standards

Our `.gitignore` follows standards from:

- **GitHub** - Official templates
- **Next.js** - Framework recommendations
- **Python** - PEP standards
- **Docker** - Container best practices
- **Enterprise** - Security and collaboration patterns

## 📚 Resources

- [GitHub Gitignore Templates](https://github.com/github/gitignore)
- [Next.js Documentation](https://nextjs.org/docs)
- [Python Packaging Guide](https://packaging.python.org/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

---

**This configuration ensures your repository stays clean, secure, and follows industry best practices for modern full-stack applications.** 🚀
