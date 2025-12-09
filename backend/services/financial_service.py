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
        Generates chart data for a given financial metric by dynamically loading its configuration
        and fetching data via the appropriate repository.
        """
        # 1. Get the specific metric configuration class (for chart styling and logic)
        metric_config_class = get_metric_config(metric_name)
        if not metric_config_class:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No chart configuration found for metric: '{metric_name}'"
            )

        # 2. Determine the correct repository to use for fetching data
        # We default to IncomeStatementRepository if not specified, as it's a common source.
        repo_class = METRIC_REPOSITORY_MAPPING.get(metric_name, IncomeStatementRepository)
        repository = repo_class()

        # 3. Fetch the raw time series data using the repository
        time_series_data = repository.get_metric_time_series(self.db, company_id, metric_name)

        # Handle case where no data is found for the metric
        if not time_series_data:
             raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Metric '{metric_name}' not found or no data available for the given company."
            )

        # 4. Instantiate the metric configuration and generate the chart data
        metric_config_instance = metric_config_class()
        chart_data = metric_config_instance.get_chart_data(time_series_data)
        
        return chart_data
