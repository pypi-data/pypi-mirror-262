from datetime import datetime

from airflow.decorators import dag, task
from airflow.models import Variable
from airflow.operators.empty import EmptyOperator
from airflow.utils.edgemodifier import Label
from airflow.utils.trigger_rule import TriggerRule


@dag(
    dag_id="workflow_pipeline",
    schedule="@daily",
    start_date=datetime(2023, 1, 1),
    catchup=True,
    tags=["feature-pipeline", "training-pipeline", "inference-pipeline"],
    max_active_runs=1,
)
def workflow_pipeline():
    """ """

    @task.virtualenv(
        task_id="run_feature_pipeline",
        requirements=[
            "--trusted-host 172.17.0.1:8000",
            "--index-url http://172.17.0.1:8000",
            "energy_consumption_forecasting",
        ],
        python_version="3.11.7",
        multiple_outputs=True,
        system_site_packages=True,
    )
    def run_feature_pipeline(
        start_date_time: str,
        end_date_time: str,
        rename_features: Dict[Any, Any],
        drop_features: Optional[List[Any]] = ["HourUTC"],
        check_features_duplicates: List[Any] = [
            "municipality_num",
            "branch",
            "datetime_dk",
        ],
    ):
        """ """
