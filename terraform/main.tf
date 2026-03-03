resource "databricks_job" "medallion_pipeline_job" {
  name = "Automated_Medallion_Pipeline"

  # We tell it to build a simple, standard cluster just for this run.
  # This avoids ALL Serverless rules.
  job_cluster {
    job_cluster_key = "auto_cluster"
    new_cluster {
      spark_version = "13.3.x-scala2.12" # A standard, stable Spark version
      node_type_id  = "r3.xlarge"        # A common, widely available node type
      num_workers   = 1
    }
  }

  task {
    task_key = "bronze_ingestion"
    job_cluster_key = "auto_cluster"
    spark_python_task {
      python_file = "/Workspace/Users/sulaipno97@gmail.com/Sulaiman/Zero-Cost Streaming DataOps Pipeline - Project 1/Zero_Cost_Streaming_DataOps_Pipeline/src/bronze.py"
    }
  }

  task {
    task_key = "silver_transformation"
    depends_on {
      task_key = "bronze_ingestion"
    }
    job_cluster_key = "auto_cluster"
    spark_python_task {
      python_file = "/Workspace/Users/sulaipno97@gmail.com/Sulaiman/Zero-Cost Streaming DataOps Pipeline - Project 1/Zero_Cost_Streaming_DataOps_Pipeline/src/silver.py"
    }
  }

  task {
    task_key = "gold_insights"
    depends_on {
      task_key = "silver_transformation"
    }
    job_cluster_key = "auto_cluster"
    spark_python_task {
      python_file = "/Workspace/Users/sulaipno97@gmail.com/Sulaiman/Zero-Cost Streaming DataOps Pipeline - Project 1/Zero_Cost_Streaming_DataOps_Pipeline/src/gold.py"
    }
  }
}