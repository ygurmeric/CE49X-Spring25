# src/visualization.py

"""
Visualization module for LCA tool.
Handles creation of plots and charts for impact analysis.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Optional, Dict
import numpy as np

class LCAVisualizer:
    def __init__(self):
        # HATA DÜZELTİLDİ: 'seaborn' stili, matplotlib 3.6+ versiyonlarında
        # 'seaborn-v0_8-darkgrid' gibi yeni isimlerle değiştirildi.
        try:
            plt.style.use('seaborn-v0_8-darkgrid')
        except OSError:
            # Çok eski bir matplotlib sürümü için yedek plan
            plt.style.use('seaborn')
            
        self.colors = sns.color_palette("husl", 8)
        self.impact_labels = {
            'carbon_impact': 'Carbon Impact (kg CO2e)',
            'energy_impact': 'Energy Impact (kWh)',
            'water_impact': 'Water Impact (L)',
            'waste_generated_kg': 'Waste Generated (kg)'
        }
    
    def plot_impact_breakdown(self, data: pd.DataFrame, impact_type: str, 
                            group_by: str = 'material_type',
                            title: Optional[str] = None) -> plt.Figure:
        """
        Create a pie chart showing impact breakdown by specified grouping.
        
        Args:
            data: DataFrame with impact data
            impact_type: Type of impact to plot (e.g., 'carbon_impact')
            group_by: Column to group by ('material_type' or 'life_cycle_stage')
            title: Optional title for the plot
            
        Returns:
            matplotlib Figure object
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        impact_data = data.groupby(group_by)[impact_type].sum()
        ax.pie(impact_data, labels=impact_data.index, autopct='%1.1f%%',
               colors=self.colors[:len(impact_data)])
        
        if title:
            ax.set_title(title)
        else:
            ax.set_title(f'{self.impact_labels.get(impact_type, impact_type)} by {group_by.replace("_", " ").title()}')
            
        return fig
    
    def plot_life_cycle_impacts(self, data: pd.DataFrame, 
                              product_id: str) -> plt.Figure:
        """
        Create a stacked bar chart showing impacts across life cycle stages.
        
        Args:
            data: DataFrame with impact data
            product_id: Product ID to analyze
            
        Returns:
            matplotlib Figure object
        """
        product_data = data[data['product_id'] == product_id]
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        axes = axes.flatten()
        
        impact_types = ['carbon_impact', 'energy_impact', 'water_impact', 'waste_generated_kg']
        
        for idx, impact_type in enumerate(impact_types):
            if impact_type in product_data.columns:
                stage_data = product_data.pivot_table(
                    index='life_cycle_stage',
                    values=impact_type,
                    aggfunc='sum'
                )
                
                stage_data.plot(kind='bar', ax=axes[idx], color=self.colors[idx], legend=False)
                axes[idx].set_title(self.impact_labels.get(impact_type, impact_type))
                axes[idx].set_xlabel('Life Cycle Stage')
                axes[idx].tick_params(axis='x', rotation=45)
        
        # Kullanılmayan eksenleri gizle
        for i in range(len(impact_types), len(axes)):
            axes[i].set_visible(False)
            
        plt.tight_layout()
        fig.suptitle(f'Life Cycle Impacts for Product {product_id}', fontsize=16, y=1.02)
        return fig
    
    def plot_product_comparison(self, data: pd.DataFrame, 
                              product_ids: List[str]) -> plt.Figure:
        """
        Create a radar chart comparing multiple products across impact categories.
        
        Args:
            data: DataFrame with impact data
            product_ids: List of product IDs to compare
            
        Returns:
            matplotlib Figure object
        """
        # Calculate total impacts for each product
        total_impacts = data[data['product_id'].isin(product_ids)].groupby('product_id').agg({
            'carbon_impact': 'sum',
            'energy_impact': 'sum',
            'water_impact': 'sum',
            'waste_generated_kg': 'sum'
        })
        
        # Normalize the data for fair comparison on the radar chart
        normalized = total_impacts.copy()
        for col in total_impacts.columns:
            max_val = total_impacts[col].max()
            if max_val > 0:
                normalized[col] = total_impacts[col] / max_val
        
        # Create radar chart
        categories = [label.split(' (')[0] for label in self.impact_labels.values()] # Use shorter labels
        num_vars = len(categories)
        
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
        angles += angles[:1] # Close the circle
        
        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
        
        for idx, product_id in enumerate(product_ids):
            values = normalized.loc[product_id].values.flatten().tolist()
            values += values[:1] # Close the circle
            ax.plot(angles, values, linewidth=2, linestyle='solid', label=data.loc[data['product_id'] == product_id, 'product_name'].iloc[0])
            ax.fill(angles, values, alpha=0.25)
        
        ax.set_yticklabels([])
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, size=12)
        ax.set_title('Product Comparison Across Impact Categories', size=16, y=1.1)
        plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
        
        return fig
    
    def plot_end_of_life_breakdown(self, data: pd.DataFrame, 
                                 product_id: str) -> plt.Figure:
        """
        Create a stacked bar chart showing end-of-life management breakdown.
        
        Args:
            data: DataFrame with impact data
            product_id: Product ID to analyze
            
        Returns:
            matplotlib Figure object
        """
        # Sadece End-of-Life aşamasını filtrele
        eol_data = data[(data['product_id'] == product_id) & (data['life_cycle_stage'].str.lower() == 'end-of-life')]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Eğer veri yoksa boş grafik göster
        if eol_data.empty:
            ax.text(0.5, 0.5, f'No End-of-Life data for Product {product_id}', ha='center', va='center')
            return fig

        product_name = eol_data['product_name'].iloc[0]
        eol_rates = eol_data[['recycling_rate', 'landfill_rate', 'incineration_rate']].iloc[0] # Sadece ilk satırı al
        
        eol_rates.plot(kind='pie', autopct='%1.1f%%', ax=ax,
                       labels=['Recycling', 'Landfill', 'Incineration'],
                       colors=['green', 'brown', 'orange'])
        
        ax.set_title(f'End-of-Life Management for {product_name} ({product_id})')
        ax.set_ylabel('') # "Rate" etiketini kaldır
        
        return fig
    
    def plot_impact_correlation(self, data: pd.DataFrame) -> plt.Figure:
        """
        Create a correlation heatmap of different impact categories.
        
        Args:
            data: DataFrame with impact data
            
        Returns:
            matplotlib Figure object
        """
        impact_columns = ['carbon_impact', 'energy_impact', 'water_impact', 'waste_generated_kg']
        correlation = data[impact_columns].corr()
        
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(correlation, annot=True, cmap='coolwarm', fmt=".2f", center=0, ax=ax)
        
        ax.set_title('Impact Category Correlations')
        
        return fig