## columndb
from daaskit.sdk import util
from minio import Minio
from duckdb import connect
import pandas as pd
import pyarrow.parquet as pq
import pyarrow as pa
import io

_globalMinoEndpoint = util.get_env('ENV_MINIO_ENDPOINT', "minio:9000")
_globalMinoAccessKey = util.get_env('ENV_MINIO_ACCESS_KEY', "accesskey_cvxa3663")
_globalMinoSecretKey = util.get_env('ENV_MINIO_SECRET_KEY', "secretkey_cvxa3663")
_globalMinoBucket = util.get_env('ENV_MINIO_BUCKET', "cvxa3663")

class CDB:
    # 初始化
    # minoEndpoint：minoendpoint
    # minoAccessKey：accesskey
    # minoSecretKey：secretkey
    # minoBucket：bucket
    def __init__(self, minoEndpoint=None, minoAccessKey=None, minoSecretKey=None, minoBucket=None):
        if minoEndpoint == None:
            minoEndpoint = _globalMinoEndpoint
        if minoAccessKey == None:
            minoAccessKey = _globalMinoAccessKey
        if minoSecretKey == None:
            minoSecretKey = _globalMinoSecretKey
        if minoBucket == None:
            minoBucket = _globalMinoBucket
        self.minoBucket = minoBucket
        self.minioAccessKey = minoAccessKey
        self.minioSecretKey = minoSecretKey
        self.minioEndpoint = minoEndpoint
        # 创建 MinIO 客户端
        self.minioClient = Minio(minoEndpoint,
                            access_key=minoAccessKey,
                            secret_key=minoSecretKey,
                            secure=False)
    
    def __del__(self):
        self.minoBucket = ''    
    
    def query(self, tableNames, sql, params=[]):
        create_table_statements = [
            f"CREATE TABLE {table_name} AS SELECT * FROM read_parquet('s3://{self.minoBucket}/{table_name}.parquet');"
            for table_name in tableNames
        ]
        createTableSQL = "\n".join(create_table_statements)
        conn = connect(config={"allow_unsigned_extensions": True})
        initSQL = f"""
            LOAD '/Users/hrf/Downloads/httpfs.duckdb_extension';
            SET s3_region='us-west-2';
            SET s3_access_key_id='{self.minioAccessKey}';
            SET s3_secret_access_key='{self.minioSecretKey}';
            SET s3_url_style='path';
            SET s3_use_ssl=false;
            SET s3_endpoint='{self.minioEndpoint}';
            {createTableSQL}
        """
        conn.execute(initSQL)
        result = conn.execute(sql, params)
        return result.fetchall()