from sqlalchemy.orm import Session
from typing import Dict, Any, List, Type
from fastapi import HTTPException, status, Depends

from schemas.chart import ChartData
from repositories.financial_repo import BalanceStatementRepository, IncomeStatementRepository, CashStatementRepository, FinancialStatementRepository
from .metrics import get_metric_config
from core.database import get_db

# A mapping to determine which repository to use for a given metric.
# We map the metric to the repository *class* for more flexible instantiation.
METRIC_REPOSITORY_MAPPING: Dict[str, Type[FinancialStatementRepository]] = {
    "total_assets": BalanceStatementRepository,
    "total_liabilities": BalanceStatementRepository,
    "cash_at_end_of_period": CashStatementRepository,
    "asset_liability_ratio": BalanceStatementRepository,
    # Add other metric-to-repository mappings here
}

class FinancialMetricService:
    def __init__(self, db: Session = Depends(get_db)):
        """
        Initializes the service with a database session dependency.
        """
        self.db = db

    def get_metric_chart_data(self, company_id: int, metric_name: str) -> ChartData:
        """
        Generates chart data for a given financial metric. It supports both single-metric
        charts and calculated metrics derived from multiple data series.
        """
        # 1. Get the specific metric configuration class
        metric_config_class = get_metric_config(metric_name)
        if not metric_config_class:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No chart configuration found for metric: '{metric_name}'"
            )
        
        metric_config_instance = metric_config_class()
        
        # 2. Determine the required metrics (either the metric itself or its dependencies)
        metric_dependencies = metric_config_instance.dependencies or [metric_name]
        
        # 3. Fetch time series data for all required metrics
        time_series_data_map: Dict[str, List[Dict[str, Any]]] = {}
        for dep_metric_name in metric_dependencies:
            repo_class = METRIC_REPOSITORY_MAPPING.get(dep_metric_name, IncomeStatementRepository)
            repository = repo_class()
            
            time_series_data = repository.get_metric_time_series(self.db, company_id, dep_metric_name)
            
            if not time_series_data:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Data not found for dependency '{dep_metric_name}' of metric '{metric_name}'"
                )
            time_series_data_map[dep_metric_name] = time_series_data

        # 4. Generate the chart data using the fetched data
        # For single metrics, the map will have one entry. For calculated metrics, it will have multiple.
        chart_data = metric_config_instance.get_chart_data(time_series_data_map)
        
        return chart_data
