"""
Aggregate DORA metrics and prepare for Power BI export
Calculates the 4 key DORA metrics:
1. Deployment Frequency
2. Lead Time for Changes
3. Change Failure Rate
4. Time to Restore Service (MTTR)
"""
import os
import json
import pandas as pd
from datetime import datetime, timedelta
from dateutil import parser

def load_metrics():
    """Load all metrics JSON files"""
    metrics = []
    
    raw_dir = 'metrics/raw'
    if not os.path.exists(raw_dir):
        print("No metrics directory found")
        return []
    
    for root, dirs, files in os.walk(raw_dir):
        for file in files:
            if file.endswith('.json'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r') as f:
                        data = json.load(f)
                        metrics.append(data)
                except Exception as e:
                    print(f"Error loading {filepath}: {e}")
    
    return metrics

def calculate_deployment_frequency(metrics):
    """Calculate deployment frequency per service"""
    
    deployments = []
    
    for metric in metrics:
        if 'deployment_frequency' in metric:
            deployments.append({
                'timestamp': metric['timestamp'],
                'service': metric['service'],
                'deployment_id': metric['deployment_frequency']['deployment_id'],
                'branch': metric['deployment_frequency'].get('branch', 'unknown'),
                'commit_sha': metric['deployment_frequency'].get('commit_sha', '')
            })
    
    df = pd.DataFrame(deployments)
    
    if df.empty:
        return pd.DataFrame()
    
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['date'] = df['timestamp'].dt.date
    
    # Daily deployment frequency per service
    daily_freq = df.groupby(['date', 'service']).size().reset_index(name='deployment_count')
    
    # Weekly deployment frequency
    df['week'] = df['timestamp'].dt.to_period('W')
    weekly_freq = df.groupby(['week', 'service']).size().reset_index(name='deployment_count')
    weekly_freq['week'] = weekly_freq['week'].astype(str)
    
    # Monthly deployment frequency
    df['month'] = df['timestamp'].dt.to_period('M')
    monthly_freq = df.groupby(['month', 'service']).size().reset_index(name='deployment_count')
    monthly_freq['month'] = monthly_freq['month'].astype(str)
    
    return {
        'daily': daily_freq,
        'weekly': weekly_freq,
        'monthly': monthly_freq,
        'raw': df
    }

def calculate_lead_time(metrics):
    """Calculate lead time for changes"""
    
    lead_times = []
    
    for metric in metrics:
        if 'lead_time_for_changes' in metric:
            lt = metric['lead_time_for_changes']
            
            commit_time = parser.parse(lt['commit_timestamp'])
            deploy_time = parser.parse(lt['deploy_timestamp'])
            
            lead_time_seconds = (deploy_time - commit_time).total_seconds()
            lead_time_hours = lead_time_seconds / 3600
            lead_time_minutes = lead_time_seconds / 60
            
            lead_times.append({
                'timestamp': metric['timestamp'],
                'service': metric['service'],
                'commit_sha': lt.get('commit_sha', ''),
                'commit_timestamp': commit_time,
                'deploy_timestamp': deploy_time,
                'lead_time_seconds': lead_time_seconds,
                'lead_time_minutes': lead_time_minutes,
                'lead_time_hours': lead_time_hours
            })
    
    df = pd.DataFrame(lead_times)
    
    if df.empty:
        return pd.DataFrame()
    
    df['date'] = pd.to_datetime(df['timestamp']).dt.date
    
    # Average lead time per service per day
    daily_avg = df.groupby(['date', 'service']).agg({
        'lead_time_hours': ['mean', 'median', 'min', 'max']
    }).reset_index()
    
    daily_avg.columns = ['date', 'service', 'avg_lead_time_hours', 
                          'median_lead_time_hours', 'min_lead_time_hours', 
                          'max_lead_time_hours']
    
    return {
        'daily_average': daily_avg,
        'raw': df
    }

def calculate_change_failure_rate(metrics):
    """Calculate change failure rate"""
    
    changes = []
    
    for metric in metrics:
        if 'change_failure_rate' in metric:
            cfr = metric['change_failure_rate']
            
            changes.append({
                'timestamp': metric['timestamp'],
                'service': metric['service'],
                'status': cfr['status'],
                'workflow_run_id': cfr.get('workflow_run_id', ''),
                'commit_sha': cfr.get('commit_sha', '')
            })
    
    df = pd.DataFrame(changes)
    
    if df.empty:
        return pd.DataFrame()
    
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['date'] = df['timestamp'].dt.date
    
    # Calculate failure rate per service per day
    daily_cfr = df.groupby(['date', 'service', 'status']).size().unstack(fill_value=0)
    
    if 'success' not in daily_cfr.columns:
        daily_cfr['success'] = 0
    if 'failure' not in daily_cfr.columns:
        daily_cfr['failure'] = 0
    
    daily_cfr['total_changes'] = daily_cfr['success'] + daily_cfr['failure']
    daily_cfr['failure_rate'] = (daily_cfr['failure'] / daily_cfr['total_changes'] * 100).round(2)
    daily_cfr['success_rate'] = (daily_cfr['success'] / daily_cfr['total_changes'] * 100).round(2)
    
    daily_cfr = daily_cfr.reset_index()
    
    # Weekly failure rate
    df['week'] = df['timestamp'].dt.to_period('W')
    weekly_cfr = df.groupby(['week', 'service', 'status']).size().unstack(fill_value=0)
    
    if 'success' not in weekly_cfr.columns:
        weekly_cfr['success'] = 0
    if 'failure' not in weekly_cfr.columns:
        weekly_cfr['failure'] = 0
    
    weekly_cfr['total_changes'] = weekly_cfr['success'] + weekly_cfr['failure']
    weekly_cfr['failure_rate'] = (weekly_cfr['failure'] / weekly_cfr['total_changes'] * 100).round(2)
    weekly_cfr = weekly_cfr.reset_index()
    weekly_cfr['week'] = weekly_cfr['week'].astype(str)
    
    return {
        'daily': daily_cfr,
        'weekly': weekly_cfr,
        'raw': df
    }

def generate_powerbi_export():
    """Generate CSV files for Power BI import"""
    
    print("Loading metrics...")
    metrics = load_metrics()
    
    if not metrics:
        print("No metrics found")
        return
    
    print(f"Loaded {len(metrics)} metric records")
    
    # Create output directories
    os.makedirs('metrics/aggregated', exist_ok=True)
    os.makedirs('metrics/powerbi', exist_ok=True)
    
    # Calculate metrics
    print("Calculating deployment frequency...")
    deployment_freq = calculate_deployment_frequency(metrics)
    
    print("Calculating lead time...")
    lead_time = calculate_lead_time(metrics)
    
    print("Calculating change failure rate...")
    change_failure_rate = calculate_change_failure_rate(metrics)
    
    # Export to CSV for Power BI
    timestamp = datetime.now().strftime('%Y%m%d')
    
    if deployment_freq and not deployment_freq['daily'].empty:
        deployment_freq['daily'].to_csv(
            f'metrics/powerbi/deployment_frequency_daily_{timestamp}.csv', 
            index=False
        )
        deployment_freq['weekly'].to_csv(
            f'metrics/powerbi/deployment_frequency_weekly_{timestamp}.csv', 
            index=False
        )
        deployment_freq['monthly'].to_csv(
            f'metrics/powerbi/deployment_frequency_monthly_{timestamp}.csv', 
            index=False
        )
    
    if lead_time and not lead_time['daily_average'].empty:
        lead_time['daily_average'].to_csv(
            f'metrics/powerbi/lead_time_daily_{timestamp}.csv', 
            index=False
        )
        lead_time['raw'].to_csv(
            f'metrics/powerbi/lead_time_raw_{timestamp}.csv', 
            index=False
        )
    
    if change_failure_rate and not change_failure_rate['daily'].empty:
        change_failure_rate['daily'].to_csv(
            f'metrics/powerbi/change_failure_rate_daily_{timestamp}.csv', 
            index=False
        )
        change_failure_rate['weekly'].to_csv(
            f'metrics/powerbi/change_failure_rate_weekly_{timestamp}.csv', 
            index=False
        )
    
    # Generate summary report
    summary = {
        'generated_at': datetime.now().isoformat(),
        'total_metrics': len(metrics),
        'date_range': {
            'start': min([m['timestamp'] for m in metrics]),
            'end': max([m['timestamp'] for m in metrics])
        }
    }
    
    with open(f'metrics/aggregated/summary_{timestamp}.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"Metrics aggregation complete. Files saved to metrics/powerbi/")
    print(f"Summary: {summary}")

if __name__ == '__main__':
    generate_powerbi_export()
