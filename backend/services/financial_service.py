from sqlalchemy.orm import Session
from typing import Dict, Any, List
from fastapi import HTTPException, status

from schemas.chart import ChartData
from repositories.financial_repo import BalanceStatementRepository, IncomeStatementRepository
from models import IncomeSheetStatementCore, BalanceSheetStatementCore, IncomeSheetStatementEAV, BalanceSheetStatementEAV
from .metrics import get_metric_config

# A mapping to determine which repository and tables to use for a given metric.
# This can be expanded or moved to a more dynamic discovery mechanism later.
METRIC_MAPPING = {
    "total_revenue": (IncomeStatementRepository, IncomeSheetStatementCore, None),
    "net_income": (IncomeStatementRepository, IncomeSheetStatementCore, None),
    "total_assets": (BalanceStatementRepository, BalanceSheetStatementCore, None),
    "total_liabilities": (BalanceStatementRepository, BalanceSheetStatementCore, None),
    "other_comprehensive_income_loss": (IncomeStatementRepository, IncomeSheetStatementCore, IncomeSheetStatementEAV),
}

def get_metric_time_series(db: Session, company_id: int, metric_name: str) -> List[Dict[str, Any]]:
    """
    Fetches time series data for a given financial metric.
    """
    if metric_name not in METRIC_MAPPING:
        # Fallback for metrics not in the mapping, assuming they might be in an EAV table
        # A more robust implementation would be needed for a production system
        repo, core_model, eav_model = (BalanceStatementRepository, BalanceSheetStatementCore, BalanceSheetStatementEAV)
    else:
        repo, core_model, eav_model = METRIC_MAPPING[metric_name]

    query_results = []

    # Check if the metric is a column in the core model
    if hasattr(core_model, metric_name):
        results = db.query(
            core_model.fiscal_year.label("year"),
            getattr(core_model, metric_name).label("value")
        ).filter(core_model.company_id == company_id).order_by(core_model.fiscal_year).all()
        query_results.extend([{"year": r.year, "value": r.value} for r in results])

    # Check if the metric is in the EAV table
    elif eav_model:
        fk_name = repo().eav_fk_name
        results = db.query(
            core_model.fiscal_year.label("year"),
            eav_model.value_numeric.label("value")
        ).join(eav_model, core_model.id == getattr(eav_model, fk_name)) \
        .filter(
            core_model.company_id == company_id,
            eav_model.attribute_name == metric_name
        ).order_by(core_model.fiscal_year).all()
        query_results.extend([{"year": r.year, "value": r.value} for r in results])

    if not query_results and metric_name not in METRIC_MAPPING:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Metric '{metric_name}' not found or not configured.")

    # Deduplicate and sort
    final_results = list({(r['year']): r for r in query_results}.values())
    final_results.sort(key=lambda x: x['year'])
    
    return final_results


class FinancialMetricService:
    def get_metric_chart_data(self, db: Session, company_id: int, metric_name: str) -> ChartData:
        """
        Generates chart data for a given financial metric by dynamically loading its configuration.
        """
        # 1. Get the specific metric configuration class from the registry
        metric_config_class = get_metric_config(metric_name)
        
        if not metric_config_class:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No chart configuration found for metric: '{metric_name}'"
            )
            
        # 2. Fetch the raw time series data
        time_series_data = get_metric_time_series(db, company_id, metric_name)
        
        # 3. Instantiate the metric configuration and generate the chart data
        metric_config_instance = metric_config_class()
        chart_data = metric_config_instance.get_chart_data(time_series_data)
        
        return chart_data
