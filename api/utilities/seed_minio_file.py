import os

from api.services import StorageService
from mock_seed.confmock import script_path, minio_host, minio_access_key, minion_secret_key

StorageService(minio_host, minio_access_key, minion_secret_key)


class SeedMinioFiles:
    file_path = script_path + "/minio_files"

    @classmethod
    def load_files(cls):
        buckets = [x for x in os.listdir(cls.file_path)]
        for bucket in buckets:
            bucket_path = os.path.join(cls.file_path, bucket)
            files = [x for x in os.listdir(bucket_path)]
            for file_name in files:
                StorageService.upload_file(bucket, os.path.join(bucket_path, file_name), file_name)
