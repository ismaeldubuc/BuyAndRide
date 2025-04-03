# s3_handler.py
import boto3

s3 = boto3.client('s3')

def list_files_in_s3(bucket_name):
    """ Liste tous les fichiers d'un bucket S3. """
    objects = s3.list_objects_v2(Bucket=bucket_name)
    return [obj["Key"] for obj in objects.get("Contents", [])]

def download_file_from_s3(bucket_name, file_key, local_file_path):
    """ Télécharge un fichier depuis S3. """
    s3.download_file(bucket_name, file_key, local_file_path)
