# Databricks notebook source
# MAGIC %md
# MAGIC
# MAGIC # Mount s3 to Databricks

# COMMAND ----------

# MAGIC %md
# MAGIC  Following way is not reccommended as we have hard coded the credential values. As we are using Databricks community edition we dont have access to secret scopes here. this is why we have done hard coding to mount s3 bucket with databricks.
# MAGIC
# MAGIC best practice to mount s3 bucket - 1. create IAM roles and instance profiles 
# MAGIC
# MAGIC 2. save credentials in secret scope in Databricks 
# MAGIC
# MAGIC and then use dbutils

# COMMAND ----------



ACCESS_KEY = 'hidden'
SECRET_KEY = 'hidden'

AWS_BUCKET_NAME = 'tenetic-s3-databricks'

MOUNT_NAME = 'mybucket'
# we are using s3a:// protocol instead of standard s3://  as this is optimized for spark and big data
dbutils.fs.mount(
    source=f"s3a://{AWS_BUCKET_NAME}",
    mount_point=f"/mnt/{MOUNT_NAME}",
    extra_configs = {
        "fs.s3a.access.key":ACCESS_KEY,
        "fs.s3a.secret.key":SECRET_KEY
    }
)

# COMMAND ----------

display(dbutils.fs.mounts())

# COMMAND ----------

df=spark.read.csv('/mnt/mybucket/sample.csv',header=True)
display(df)

# COMMAND ----------

# MAGIC %md
# MAGIC created s3 bucket in aws and added sample.csv file in it.
# MAGIC created aws user - gave access to AMAZONS3FULLACCESS
# MAGIC created secret key and access key
# MAGIC
# MAGIC go to databricks - saved(hardcoded) secret and access key
# MAGIC then by using dbutils.fs.mount create a mount point for the s3 bucket
# MAGIC
# MAGIC (in databricks community edition we dont have secret scope api access)
# MAGIC recommended way is to store secrets in secret scope and 
# MAGIC then by using dbutils.secrets.get(scope='' , key='')
# MAGIC
# MAGIC best practice = 1. use IAM roles and instance profiles instead of access key
# MAGIC create instance profile (available in standard or premium workspaces in databricks)
# MAGIC
# MAGIC 2. store access key in secret scope of databricks
# MAGIC
