# DORA Metrics Dashboard - Project Setup

This project implements a complete CI/CD pipeline with DORA metrics tracking for a Spring Boot + React application.

## Project Structure

```
Test/
├── backend/                    # Spring Boot application
│   ├── Dockerfile             # Backend container image
│   ├── pom.xml               # Maven configuration
│   └── src/                  # Java source code (add your code here)
│
├── frontend/                  # React application
│   ├── Dockerfile            # Frontend container image
│   ├── package.json          # NPM configuration
│   ├── nginx.conf           # Nginx configuration
│   └── src/                 # React source code (add your code here)
│
├── .github/workflows/        # GitHub Actions CI/CD
│   ├── backend-ci-cd.yml    # Backend pipeline with DORA tracking
│   ├── frontend-ci-cd.yml   # Frontend pipeline with DORA tracking
│   └── aggregate-dora-metrics.yml  # Daily metrics aggregation
│
├── scripts/                  # Python scripts for metrics
│   ├── download_metrics.py  # Download artifacts from GitHub
│   └── aggregate_dora_metrics.py  # Process and aggregate metrics
│
├── metrics/                  # Generated metrics data
│   ├── raw/                 # Raw metrics from workflows
│   ├── aggregated/          # Processed metrics
│   ├── powerbi/            # CSV exports for Power BI
│   └── historical/         # Committed historical data
│
└── docs/
    ├── POWERBI_INTEGRATION.md  # Power BI setup guide
    └── README.md               # This file
```

## Quick Start

### 1. Prerequisites

- GitHub account with repository access
- Docker installed locally (for testing)
- GitHub Actions enabled
- Power BI Desktop (for dashboards)

### 2. Initial Setup

#### Push to GitHub

```bash
cd Test
git init
git add .
git commit -m "Initial setup with DORA metrics"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

#### Enable GitHub Actions

1. Go to your repository on GitHub
2. Navigate to **Settings** → **Actions** → **General**
3. Under "Workflow permissions", select:
   - ✅ Read and write permissions
   - ✅ Allow GitHub Actions to create and approve pull requests

#### Enable GitHub Container Registry

1. Go to your repository **Settings** → **Secrets and variables** → **Actions**
2. GitHub token is automatically available as `GITHUB_TOKEN`
3. No additional setup needed for GHCR

### 3. Add Your Application Code

#### Backend (Spring Boot)

Add your Spring Boot application code to `backend/src/`:

```
backend/src/
└── main/
    └── java/
        └── com/
            └── example/
                └── Application.java
```

#### Frontend (React)

Add your React application code to `frontend/src/`:

```
frontend/src/
├── App.js
├── index.js
└── components/
```

Or create a new React app:
```bash
cd frontend
npx create-react-app .
```

### 4. Build Docker Images Locally (Optional)

Test your Dockerfiles before pushing:

```bash
# Backend
cd backend
docker build -t backend:test .

# Frontend
cd ../frontend
docker build -t frontend:test .
```

### 5. Trigger CI/CD Pipelines

Push changes to trigger the workflows:

```bash
git add .
git commit -m "Add application code"
git push
```

The workflows will automatically:
- Run tests
- Build Docker images
- Push to GitHub Container Registry
- Collect DORA metrics

### 6. View DORA Metrics

#### Daily Aggregation

The metrics aggregation workflow runs daily at midnight (UTC). To trigger manually:

1. Go to **Actions** tab
2. Select "Aggregate DORA Metrics"
3. Click "Run workflow"

#### Download Metrics

1. Go to **Actions** → "Aggregate DORA Metrics"
2. Click on latest run
3. Download the `dora-metrics-aggregated` artifact

#### View in Repository

After the first aggregation, metrics are committed to:
```
metrics/historical/*.csv
```

## DORA Metrics Collected

### 1. Deployment Frequency
- **What**: How often deployments occur
- **Tracked by**: Counting successful deployments per day/week/month
- **Files**: `deployment_frequency_*.csv`

### 2. Lead Time for Changes
- **What**: Time from commit to deployment
- **Tracked by**: Comparing commit timestamp with deployment timestamp
- **Files**: `lead_time_*.csv`

### 3. Change Failure Rate
- **What**: Percentage of deployments that fail
- **Tracked by**: Comparing successful vs failed workflow runs
- **Files**: `change_failure_rate_*.csv`

### 4. Mean Time to Recovery (MTTR)
- **What**: Time to recover from failures
- **Tracked by**: Manual incident tracking (requires additional setup)
- **Note**: Use GitHub Issues with labels for incident tracking

## Setting Up Power BI Dashboard

See [POWERBI_INTEGRATION.md](POWERBI_INTEGRATION.md) for detailed instructions.

**Quick steps:**
1. Download metrics CSV files from `metrics/historical/`
2. Open Power BI Desktop
3. Import CSV files using **Get Data** → **Text/CSV**
4. Create visualizations using the sample queries in the guide
5. Publish to Power BI Service for sharing

## Docker Compose (Optional)

Create `docker-compose.yml` for local testing:

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8080:8080"
    environment:
      - SPRING_PROFILES_ACTIVE=dev
  
  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    depends_on:
      - backend
```

Run locally:
```bash
docker-compose up --build
```

## Monitoring CI/CD

### View Workflow Status

- **Actions Tab**: See all workflow runs
- **Badge**: Add to README:
```markdown
![Backend CI/CD](https://github.com/USERNAME/REPO/workflows/Backend%20CI/CD/badge.svg)
![Frontend CI/CD](https://github.com/USERNAME/REPO/workflows/Frontend%20CI/CD/badge.svg)
```

### Check Docker Images

View published images:
1. Go to repository main page
2. Click **Packages** in right sidebar
3. See `backend` and `frontend` images

## Customization

### Adjust Metrics Collection

Edit workflow files in `.github/workflows/`:
- Add custom metrics
- Change retention period
- Modify aggregation schedule

### Modify Python Scripts

Edit `scripts/*.py`:
- Customize metric calculations
- Add new visualizations
- Change export format

### Power BI Customization

- Create custom DAX measures
- Add new visualizations
- Set up alerts for thresholds

## Troubleshooting

### Workflows Failing

**Check logs:**
1. Go to **Actions** tab
2. Click on failed workflow
3. View job logs

**Common issues:**
- Missing dependencies in Dockerfile
- Test failures
- Docker build context issues

### No Metrics Data

**Verify:**
- Workflows have run successfully
- Artifacts are being created
- Aggregation workflow has run
- CSV files exist in `metrics/historical/`

### Docker Build Issues

**Test locally:**
```bash
cd backend  # or frontend
docker build --no-cache -t test:latest .
docker run -p 8080:8080 test:latest
```

## Best Practices

1. **Branch Strategy**
   - Use `main` for production
   - Use `develop` for development
   - Create feature branches for changes

2. **Commit Messages**
   - Use conventional commits
   - Include JIRA/issue numbers

3. **DORA Improvements**
   - Monitor trends weekly
   - Set team goals based on benchmarks
   - Review failures in retrospectives

4. **Security**
   - Scan Docker images
   - Update dependencies regularly
   - Use secrets for sensitive data

## Additional Resources

- [DORA Metrics Guide](https://cloud.google.com/blog/products/devops-sre/using-the-four-keys-to-measure-your-devops-performance)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Power BI Documentation](https://docs.microsoft.com/en-us/power-bi/)

## Support & Contributing

- Create GitHub Issues for bugs
- Submit Pull Requests for improvements
- Update documentation when adding features

## License

[Your License Here]
