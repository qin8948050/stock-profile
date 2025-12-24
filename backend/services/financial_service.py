from sqlalchemy.orm import Session
from typing import Dict, Any, List, Type
from fastapi import Depends

from schemas.chart import ChartData
from repositories.financial_repo import BalanceStatementRepository, IncomeStatementRepository, CashStatementRepository, FinancialStatementRepository
from .metrics import get_metric_config
from core.database import get_db

class FinancialMetricService:
    def __init__(self, db: Session = Depends(get_db)):
        """
        Initializes the service with a database session dependency.
        Initializes all relevant financial statement repositories.
        """
        self.db = db
        self.income_repo = IncomeStatementRepository()
        self.balance_repo = BalanceStatementRepository()
        self.cash_repo = CashStatementRepository()
        # Store all repositories in a list for easy iteration
        self.all_repos: List[FinancialStatementRepository] = [
            self.income_repo,
            self.balance_repo,
            self.cash_repo
        ]

    def get_metric_chart_data(self, company_id: int, metric_name: str) -> ChartData:
        """
        Generates chart data for a given financial metric. It supports both single-metric
        charts and calculated metrics derived from multiple data series.
        """
        # 1. Get the specific metric configuration class
        metric_config_class = get_metric_config(metric_name)
        if not metric_config_class:
            raise ValueError(f"No chart configuration found for metric: '{metric_name}'")
        
        metric_config_instance = metric_config_class()
        
        # 2. Determine the required metrics (either the metric itself or its dependencies)
        metric_dependencies = metric_config_instance.dependencies or [metric_name]
        
        # 3. Fetch time series data for all required metrics
        time_series_data_map: Dict[str, List[Dict[str, Any]]] = {}
        for dep_metric_name in metric_dependencies:
            found_data = False
            for repository in self.all_repos:
                time_series_data = repository.get_metric_time_series(self.db, company_id, dep_metric_name)
                if time_series_data:
                    time_series_data_map[dep_metric_name] = time_series_data
                    found_data = True
                    break # Data found for this dependency, move to the next one
            
            if not found_data:
                raise LookupError(f"Data not found for dependency '{dep_metric_name}' of metric '{metric_name}' in any repository.")

        # 4. Generate the chart data using the fetched data
        # For single metrics, the map will have one entry. For calculated metrics, it will have multiple.
        chart_data = metric_config_instance.get_chart_data(time_series_data_map)
        
        return chart_data
