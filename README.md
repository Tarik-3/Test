# Spring Boot + React with DORA Metrics

A complete CI/CD setup for Spring Boot backend and React frontend with comprehensive DORA metrics tracking and Power BI integration.

## Features

- ✅ Spring Boot backend with Docker
- ✅ React frontend with Nginx
- ✅ GitHub Actions CI/CD pipelines
- ✅ DORA metrics collection (Deployment Frequency, Lead Time, Change Failure Rate)
- ✅ Automated metrics aggregation
- ✅ Power BI ready CSV exports
- ✅ Container registry integration (GHCR)

## Getting Started

See [docs/README.md](docs/README.md) for complete setup instructions.

### Quick Start

```bash
# 1. Clone and setup
git init
git add .
git commit -m "Initial setup"

# 2. Push to GitHub
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main

# 3. Workflows run automatically on push
```

## Project Structure

```
├── backend/          # Spring Boot application + Dockerfile
├── frontend/         # React application + Dockerfile
├── .github/workflows/  # CI/CD pipelines with DORA tracking
├── scripts/          # Metrics aggregation scripts
├── docs/            # Documentation
└── metrics/         # Generated DORA metrics data
```

## DORA Metrics Dashboard

Import the generated CSV files into Power BI to visualize:
- 📊 Deployment frequency trends
- ⏱️ Lead time for changes
- 🔴 Change failure rates
- 📈 DORA performance classification

See [docs/POWERBI_INTEGRATION.md](docs/POWERBI_INTEGRATION.md) for Power BI setup.

## Documentation

- [Complete Setup Guide](docs/README.md)
- [Power BI Integration](docs/POWERBI_INTEGRATION.md)

## Workflows

- **Backend CI/CD**: Builds, tests, and deploys Spring Boot app
- **Frontend CI/CD**: Builds, tests, and deploys React app
- **Aggregate Metrics**: Daily aggregation of DORA metrics

## License

[Your License]
