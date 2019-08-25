import os
from time import strftime

from minio import Minio
from minio.error import ResponseError, NoSuchKey, NoSuchBucket, BucketNotEmpty
from werkzeug.datastructures import FileStorage

from api.exceptions import FileOperationException


class StorageService:
    minio_client: Minio = None

    def __new__(cls, host, access_key, secret_key, secure=False):
        cls.minio_client = Minio(host, access_key=access_key, secret_key=secret_key, secure=secure)

    @classmethod
    def make_bucket(cls, bucket):
        try:
            if not cls.minio_client.bucket_exists(bucket):
                cls.minio_client.make_bucket(bucket, location="us-east-1")

        except ResponseError as err:
            raise FileOperationException(err.message, detail={
                "method": err.method,
                "request_id": err.request_id,
                "code": err.code
            })

    @classmethod
    def remove_bucket(cls, bucket):
        try:
            cls.minio_client.remove_bucket(bucket)

        except ResponseError as err:
            raise FileOperationException(err.message, detail={
                "method": err.method,
                "request_id": err.request_id,
                "code": err.code
            })
        except NoSuchBucket as err:
            raise FileOperationException(err.message)
        except BucketNotEmpty as err:
            raise FileOperationException(err.message)

    @classmethod
    def list_buckets(cls):
        buckets = cls.minio_client.list_buckets()
        return [{"name": bucket.name, "creation_date": bucket.creation_date} for bucket in buckets]

    @classmethod
    def upload_file(cls, bucket, file_path, file_name):
        try:
            if not cls.minio_client.bucket_exists(bucket):
                cls.make_bucket(bucket)

            if not os.path.exists(file_path):
                raise FileOperationException('File not exist', detail={
                    "file_path": file_path
                })

            cls.minio_client.fput_object(bucket, file_name, file_path)

            return file_name

        except ResponseError as err:
            raise FileOperationException(err.message, detail={
                "method": err.method,
                "request_id": err.request_id,
                "code": err.code
            })

    @classmethod
    def save_file(cls, bucket, file: FileStorage, file_name, content_type):
        if not cls.minio_client.bucket_exists(bucket):
            cls.make_bucket(bucket)

        content_size = 0
        while file.stream.read():
            content_size = file.stream.tell()

        file.stream.seek(0)
        cls.minio_client.put_object(bucket, file_name, file.stream, content_size, content_type=content_type)

    @classmethod
    def delete_file(cls, bucket, file_name):
        try:
            cls.minio_client.remove_object(bucket, file_name)

        except ResponseError as err:
            raise FileOperationException(err.message, detail={
                "method": err.method,
                "request_id": err.request_id,
                "code": err.code
            })

    @classmethod
    def get_file_info(cls, bucket, file_name):
        try:
            file_meta_data = cls.minio_client.stat_object(bucket, file_name)
            return {
                "name": file_meta_data.object_name,
                "last_modified": strftime('%Y-%m-%dT%H:%M:%SZ', file_meta_data.last_modified),
                "size": file_meta_data.size,
                "content_type": file_meta_data.content_type
            }

        except NoSuchBucket as err:
            raise FileOperationException(err.message)
        except NoSuchKey as err:
            raise FileOperationException(err.message)

    @classmethod
    def list_files(cls, bucket):
        try:
            file_objects = cls.minio_client.list_objects(bucket, recursive=True)
            return [{
                "name": file_object.object_name,
                "last_modified": strftime('%Y-%m-%dT%H:%M:%SZ', file_object.last_modified),
                "size": file_object.size,
                "content_type": file_object.content_type
            } for file_object in file_objects]

        except NoSuchBucket as err:
            raise FileOperationException(err.message)

    @classmethod
    def get_file_data(cls, bucket, file_name):
        try:
            file_meta_data = cls.minio_client.stat_object(bucket, file_name)
            data = cls.minio_client.get_object(bucket, file_name)
            file_content = b""
            for content in data.stream():
                file_content = file_content + content

            return {
                "meta_data": file_meta_data,
                "data": file_content
            }

        except ResponseError as err:
            raise FileOperationException(err.message, detail={
                "method": err.method,
                "request_id": err.request_id,
                "code": err.code
            })
        except NoSuchBucket as err:
            raise FileOperationException(err.message)
        except NoSuchKey as err:
            raise FileOperationException(err.message)

    @classmethod
    def download_save_file(cls, bucket, file_name, save_path):
        try:
            if not os.path.exists(save_path):
                raise FileOperationException('Save directory not exist', detail={
                    "save_path": save_path
                })

            cls.minio_client.fget_object(bucket, file_name, os.path.join(save_path, file_name))

        except ResponseError as err:
            raise FileOperationException(err.message, detail={
                "method": err.method,
                "request_id": err.request_id,
                "code": err.code
            })
        except PermissionError as err:
            raise FileOperationException("Write permission denied", detail={
                "file_name": file_name,
                "save_path": save_path
            })
