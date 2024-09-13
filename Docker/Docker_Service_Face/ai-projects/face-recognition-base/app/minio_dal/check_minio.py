from minio import Minio
# from minio.error import ResponseError
import os

# Initialize Minio client and define bucket_name as in your example
minio_endpoint = 's3.oryza.vn'
minio_access_key = 'hoang'
minio_secret_key = '12345678'

minio_client = Minio(
    endpoint=minio_endpoint,
    access_key=minio_access_key,
    secret_key=minio_secret_key,
    secure=False
)

bucket_name = 'face'


# Function to upload image file to Minio and get URL
def upload_image_file_to_minio(minio_client, bucket_name, file_path, object_name):
    with open(file_path, 'rb') as file_data:
        # Uploading image file to Minio bucket
        minio_client.put_object(
            bucket_name,
            object_name,
            file_data,
            os.path.getsize(file_path),  # Getting file size
            content_type='image/jpg'  # Adjust content type based on your image type
        )
    # Generating URL for the uploaded image
    image_url = minio_client.presigned_get_object(bucket_name, object_name)

    return image_url


def upload_array_image_to_minio(array_image, object_name):
    array_image = 0
    with open(file_path, 'rb') as file_data:
        # Uploading image file to Minio bucket
        minio_client.put_object(
            bucket_name,
            object_name,
            file_data,
            os.path.getsize(file_path),  # Getting file size
            content_type='image/jpg'  # Adjust content type based on your image type
        )
    # Generating URL for the uploaded image
    image_url = minio_client.presigned_get_object(bucket_name, object_name)

    return image_url



if __name__ == '__main__':
    # Path to the image file on your computer
    image_file_path = '/home/oryza/Pictures/Face/Truc.jpg'
    image_object_name = 'Truc.jpg'  # Object name in Minio bucket, you can customize this

    # Uploading the image file to Minio
    image_url = upload_image_file_to_minio(minio_client, bucket_name, image_file_path, image_object_name)

    if image_url:
        print(f"Image uploaded successfully. URL: {image_url}")
    else:
        print("Failed to upload image.")