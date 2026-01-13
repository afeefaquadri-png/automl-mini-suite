"""
Visualization Module
Creates charts and reports for model comparison
"""

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Any
import pandas as pd
import numpy as np
from pathlib import Path


class ModelVisualizer:
    """Creates visualizations for model comparison and reports"""
    
    def __init__(self, output_dir: str = "reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        sns.set_style("whitegrid")
    
    def plot_model_comparison(self, results: Dict[str, Any], problem_type: str, save_path: str = None):
        """Create comparison chart for models"""
        model_names = list(results.keys())
        
        if problem_type == 'regression':
            metrics = ['test_r2', 'test_rmse', 'test_mae']
            metric_labels = ['R² Score', 'RMSE', 'MAE']
        else:
            metrics = ['test_accuracy', 'test_precision', 'test_recall', 'test_f1']
            metric_labels = ['Accuracy', 'Precision', 'Recall', 'F1 Score']
        
        # Prepare data
        data = []
        for name, result in results.items():
            for metric, label in zip(metrics, metric_labels):
                value = result['metrics'].get(metric, 0)
                data.append({
                    'Model': name,
                    'Metric': label,
                    'Value': value
                })
        
        df = pd.DataFrame(data)
        
        # Create plotly figure
        fig = px.bar(
            df,
            x='Model',
            y='Value',
            color='Metric',
            barmode='group',
            title='Model Comparison',
            labels={'Value': 'Score', 'Model': 'Model Name'}
        )
        
        if save_path:
            fig.write_html(save_path)
        
        return fig
    
    def plot_prediction_vs_actual(self, y_true: np.ndarray, y_pred: np.ndarray, 
                                  model_name: str, save_path: str = None):
        """Plot predictions vs actual values"""
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=y_true,
            y=y_pred,
            mode='markers',
            name='Predictions',
            marker=dict(color='blue', size=8)
        ))
        
        # Add diagonal line (perfect predictions)
        min_val = min(min(y_true), min(y_pred))
        max_val = max(max(y_true), max(y_pred))
        fig.add_trace(go.Scatter(
            x=[min_val, max_val],
            y=[min_val, max_val],
            mode='lines',
            name='Perfect Prediction',
            line=dict(color='red', dash='dash')
        ))
        
        fig.update_layout(
            title=f'{model_name} - Predictions vs Actual',
            xaxis_title='Actual Values',
            yaxis_title='Predicted Values',
            showlegend=True
        )
        
        if save_path:
            fig.write_html(save_path)
        
        return fig
    
    def create_model_report(self, model_name: str, results: Dict[str, Any], 
                           problem_type: str, save_path: str = None):
        """Create comprehensive model report"""
        report_path = save_path or self.output_dir / f"{model_name}_report.html"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{model_name} - Model Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ color: #0ea5e9; }}
                .metric {{ margin: 10px 0; padding: 10px; background: #f0f9ff; border-radius: 5px; }}
                table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #0ea5e9; color: white; }}
            </style>
        </head>
        <body>
            <h1>{model_name} - Model Report</h1>
            <h2>Problem Type: {problem_type}</h2>
            
            <h3>Metrics</h3>
            <div class="metric">
        """
        
        metrics = results.get('metrics', {})
        for key, value in metrics.items():
            html_content += f"<p><strong>{key.replace('_', ' ').title()}:</strong> {value:.4f if isinstance(value, float) else value}</p>"
        
        html_content += """
            </div>
            
            <h3>Hyperparameters</h3>
            <table>
                <tr><th>Parameter</th><th>Value</th></tr>
        """
        
        params = results.get('params', {})
        for key, value in params.items():
            html_content += f"<tr><td>{key}</td><td>{value}</td></tr>"
        
        html_content += """
            </table>
            
            <h3>Cross-Validation</h3>
            <p><strong>Mean CV Score:</strong> """ + f"{results.get('cv_mean', 0):.4f}" + """</p>
            <p><strong>Std CV Score:</strong> """ + f"{results.get('cv_std', 0):.4f}" + """</p>
        </body>
        </html>
        """
        
        with open(report_path, 'w') as f:
            f.write(html_content)
        
        return report_path
