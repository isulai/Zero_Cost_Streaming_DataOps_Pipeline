resource "databricks_job" "medallion_pipeline_job" {
  name = "Automated_Medallion_Pipeline"

  task {
    task_key = "bronze_ingestion"
    notebook_task {
      # Use the 'Repos' path instead of 'Workspace/Users'
      notebook_path = "/Repos/sulaipno97@gmail.com/Zero_Cost_Streaming_DataOps_Pipeline/src/bronze"
    }
  }

  task {
    task_key = "silver_transformation"
    depends_on {
      task_key = "bronze_ingestion"
    }
    notebook_task {
      notebook_path = "/Repos/sulaipno97@gmail.com/Zero_Cost_Streaming_DataOps_Pipeline/src/silver"
    }
  }

  task {
    task_key = "gold_insights"
    depends_on {
      task_key = "silver_transformation"
    }
    notebook_task {
      notebook_path = "/Repos/sulaipno97@gmail.com/Zero_Cost_Streaming_DataOps_Pipeline/src/gold"
    }
  }
}