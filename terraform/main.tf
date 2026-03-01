resource "databricks_job" "medallion_pipeline_job" {
  name = "Automated_Medallion_Pipeline"

  task {
    task_key = "bronze_ingestion"
    spark_python_task {
      python_file = "/Workspace/Users/sulaipno97@gmail.com/Sulaiman/Zero-Cost Streaming DataOps Pipeline - Project 1/Zero_Cost_Streaming_DataOps_Pipeline/src/bronze.py"
    }
  }

  task {
    task_key = "silver_transformation"
    depends_on {
      task_key = "bronze_ingestion"
    }
    spark_python_task {
      python_file = "/Workspace/Users/sulaipno97@gmail.com/Sulaiman/Zero-Cost Streaming DataOps Pipeline - Project 1/Zero_Cost_Streaming_DataOps_Pipeline/src/silver.py"
    }
  }

  task {
    task_key = "gold_insights"
    depends_on {
      task_key = "silver_transformation"
    }
    spark_python_task {
      python_file = "/Workspace/Users/sulaipno97@gmail.com/Sulaiman/Zero-Cost Streaming DataOps Pipeline - Project 1/Zero_Cost_Streaming_DataOps_Pipeline/src/gold.py"
    }
  }
}