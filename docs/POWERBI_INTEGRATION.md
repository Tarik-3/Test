# Power BI Integration Guide for DORA Metrics

This guide explains how to import and visualize DORA metrics in Power BI.

## Overview

The DORA metrics are automatically collected from GitHub Actions and aggregated daily. The metrics are stored as CSV files that can be imported into Power BI.

## DORA Metrics Included

### 1. **Deployment Frequency**
- How often code is deployed to production
- Files: `deployment_frequency_daily_*.csv`, `deployment_frequency_weekly_*.csv`, `deployment_frequency_monthly_*.csv`

### 2. **Lead Time for Changes**
- Time from code commit to production deployment
- Files: `lead_time_daily_*.csv`, `lead_time_raw_*.csv`

### 3. **Change Failure Rate**
- Percentage of deployments that fail
- Files: `change_failure_rate_daily_*.csv`, `change_failure_rate_weekly_*.csv`

### 4. **Mean Time to Recovery (MTTR)**
- Time to recover from a failure
- Tracked through GitHub Issues with labels (requires manual tracking)

## Getting the Data

### Option 1: From GitHub Actions Artifacts

1. Go to your repository's **Actions** tab
2. Find the "Aggregate DORA Metrics" workflow
3. Click on the latest successful run
4. Download the `dora-metrics-aggregated` artifact
5. Extract the ZIP file to get the CSV files from the `powerbi` folder

### Option 2: From Repository (Recommended)

The aggregation workflow automatically commits metrics to the repository:
```
metrics/historical/
  ├── deployment_frequency_daily_YYYYMMDD.csv
  ├── deployment_frequency_weekly_YYYYMMDD.csv
  ├── deployment_frequency_monthly_YYYYMMDD.csv
  ├── lead_time_daily_YYYYMMDD.csv
  ├── lead_time_raw_YYYYMMDD.csv
  ├── change_failure_rate_daily_YYYYMMDD.csv
  └── change_failure_rate_weekly_YYYYMMDD.csv
```

## Importing Data into Power BI

### Step 1: Import CSV Files

1. Open Power BI Desktop
2. Click **Get Data** → **Text/CSV**
3. Navigate to the `metrics/historical` folder
4. Select all CSV files you want to import
5. Click **Load**

### Step 2: Set Up Data Relationships

Power BI should automatically detect relationships based on common columns:
- `date` column links daily metrics
- `service` column identifies backend/frontend

### Step 3: Create Visualizations

## Sample Power BI Visualizations

### Dashboard 1: Deployment Frequency

**Card Visual - Total Deployments (Last 30 Days)**
```
Measure: Total Deployments = SUM('deployment_frequency_daily'[deployment_count])
Filter: Date is in the last 30 days
```

**Line Chart - Deployments Over Time**
- X-axis: `date`
- Y-axis: `deployment_count`
- Legend: `service`

**Bar Chart - Deployments by Service**
- Axis: `service`
- Values: `SUM(deployment_count)`

### Dashboard 2: Lead Time for Changes

**Card Visual - Average Lead Time (Hours)**
```
Measure: Avg Lead Time = AVERAGE('lead_time_daily'[avg_lead_time_hours])
```

**Line Chart - Lead Time Trend**
- X-axis: `date`
- Y-axis: `avg_lead_time_hours`
- Legend: `service`

**Scatter Chart - Lead Time Distribution**
- X-axis: `commit_timestamp`
- Y-axis: `lead_time_hours`
- Legend: `service`

### Dashboard 3: Change Failure Rate

**Gauge Visual - Current Failure Rate**
```
Measure: Failure Rate = AVERAGE('change_failure_rate_weekly'[failure_rate])
Target: 15% (adjust based on your goals)
```

**Stacked Bar Chart - Success vs Failure**
- Axis: `date`
- Values: `success`, `failure`
- Legend: `service`

**KPI Visual - Failure Rate Trend**
- Indicator: Current week failure rate
- Trend axis: `week`
- Goal: Previous month average

### Dashboard 4: DORA Performance Classification

Create a calculated column to classify performance:

```DAX
DORA Level = 
VAR DeployFreq = [Deployments Per Day]
VAR LeadTimeHours = [Avg Lead Time Hours]
VAR FailureRate = [Failure Rate %]
RETURN
    SWITCH(TRUE(),
        DeployFreq >= 1 && LeadTimeHours <= 24 && FailureRate <= 15, "Elite",
        DeployFreq >= 0.14 && LeadTimeHours <= 168 && FailureRate <= 30, "High",
        DeployFreq >= 0.03 && LeadTimeHours <= 720 && FailureRate <= 45, "Medium",
        "Low"
    )
```

## Refreshing Data

### Manual Refresh
1. Click **Refresh** in Power BI Desktop
2. Re-import the latest CSV files

### Automatic Refresh (Power BI Service)

1. Publish your report to Power BI Service
2. Go to **Settings** → **Datasets**
3. Configure **Scheduled Refresh**:
   - Set data source credentials
   - Schedule: Daily at 1:00 AM
   - Time zone: Your timezone

### Using OneDrive/SharePoint for Auto-Sync

1. Store CSV files in OneDrive or SharePoint
2. In Power BI, connect to **OneDrive** or **SharePoint folder**
3. Select the metrics folder
4. Power BI will automatically detect new files

## Sample DAX Measures

```DAX
// Deployments per day (last 30 days)
Deployments Per Day = 
    DIVIDE(
        SUM('deployment_frequency_daily'[deployment_count]),
        DISTINCTCOUNT('deployment_frequency_daily'[date])
    )

// Average Lead Time in Hours
Avg Lead Time Hours = 
    AVERAGE('lead_time_daily'[avg_lead_time_hours])

// Change Failure Rate Percentage
Failure Rate = 
    AVERAGE('change_failure_rate_daily'[failure_rate])

// Success Rate
Success Rate = 
    AVERAGE('change_failure_rate_daily'[success_rate])

// Total Changes
Total Changes = 
    SUM('change_failure_rate_daily'[total_changes])

// Week over Week Change
WoW Change = 
VAR CurrentWeek = [Deployments Per Day]
VAR PreviousWeek = 
    CALCULATE(
        [Deployments Per Day],
        DATEADD('Calendar'[Date], -7, DAY)
    )
RETURN
    DIVIDE(CurrentWeek - PreviousWeek, PreviousWeek, 0)
```

## DORA Benchmarks

Use these benchmarks to set goals in your visualizations:

| Metric | Elite | High | Medium | Low |
|--------|-------|------|--------|-----|
| Deployment Frequency | Multiple per day | Weekly to monthly | Monthly to semi-annually | Less than semi-annually |
| Lead Time for Changes | < 1 day | 1 week to 1 month | 1 month to 6 months | > 6 months |
| Change Failure Rate | 0-15% | 16-30% | 31-45% | > 45% |
| MTTR | < 1 hour | < 1 day | 1 day to 1 week | > 1 week |

## Troubleshooting

### No Data Showing
- Verify CSV files are in the correct location
- Check that workflows have run successfully
- Ensure date columns are formatted correctly (YYYY-MM-DD)

### Duplicate Data
- Remove old CSV files before importing new ones
- Use the "Remove Duplicates" feature in Power Query
- Filter by date range to show only recent data

### Performance Issues
- Import only necessary columns in Power Query
- Use aggregated data (daily/weekly) instead of raw data
- Create an aggregation table for large datasets

## Additional Resources

- [DORA Metrics Documentation](https://cloud.google.com/blog/products/devops-sre/using-the-four-keys-to-measure-your-devops-performance)
- [Power BI Documentation](https://docs.microsoft.com/en-us/power-bi/)
- [GitHub Actions Artifacts](https://docs.github.com/en/actions/using-workflows/storing-workflow-data-as-artifacts)

## Support

For issues with:
- **Metrics collection**: Check GitHub Actions workflow logs
- **Data accuracy**: Review the aggregation script logs
- **Power BI**: Refer to Power BI documentation or community forums
