# This 'sniffs' the correct Spark version for your specific account
data "databricks_spark_version" "latest" {
  long_term_support = true
}

# This 'sniffs' the cheapest possible machine type allowed on your account
data "databricks_node_type" "cheapest" {
  local_disk = true
}

resource "databricks_job" "medallion_pipeline_job" {
  name = "Automated_Medallion_Pipeline"

  # This creates a TEMPORARY cluster specifically for this run
  job_cluster {
    job_cluster_key = "auto_cluster"
    new_cluster {
      num_workers   = 1
      spark_version = data.databricks_spark_version.latest.id
      node_type_id  = data.databricks_node_type.cheapest.id
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