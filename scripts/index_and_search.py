import boto3
import pickle
import re

client = boto3.client('rekognition')

def index_images(folder_name, collection_name='ci-faces', bucket_name='ci-magicmirror'):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    objects = [x for x in bucket.objects.all() if x.key.startswith(folder_name)]
    for i, object in enumerate(objects):
        try:
            response = client.index_faces(
                CollectionId=collection_name,
                Image={
                    'S3Object': {
                        'Bucket': bucket_name,
                        'Name': object.key
                    }
                },
                ExternalImageId = folder_name + str(i),
                DetectionAttributes=[
                    'ALL'
                ]
            )
        except Exception as e:
            print(e)


def index_collection(names, collection_name='ci-faces', bucket='ci-magicmirror', create=False):
    if create:
        try:
            response = client.create_collection(CollectionId=collection_name)
        except Exception as e:
            print(e)
    for name in names:
        index_images(folder_name=name, collection_name=collection_name, bucket_name=bucket)


def search_image(image, collection_name='ci-faces', bucket_name='ci-magicmirror', max_faces=3, method='S3'):
    try:
        if method == 'S3':
            response = client.search_faces_by_image(
                CollectionId=collection_name,
                Image={
                        'S3Object': {
                            'Bucket': bucket_name,
                            'Name': image
                        }
                },
                MaxFaces=max_faces
            )
            return response
        elif method.lower() == 'byte':
            response = client.search_faces_by_image(
                CollectionId=collection_name,
                Image={
                    'Bytes': image
                },
                MaxFaces=max_faces
            )
            return response
        else:
            raise ValueError("method must be in ['S3', 'byte']")
    except Exception as e:
        print(e)


def get_name(response):
    names = {'beng': 'Ben Glick', 'alexf': 'Alex Foster', 'rohank': 'Rohan Kumar', 'logany': 'Logan Young', 'monical': 'Monica Lewis', 'helenaa':'Helena Abney-McPeek'}

    matches = response['FaceMatches']
    face_id = None
    if matches:
        image_id = matches[0]['Face']['ExternalImageId']
        pattern = re.compile('([a-zA-Z]+)\d+')
        result = re.search(pattern=pattern, string=image_id)
        face_id = result.groups()[0].lower() if result else None
    return names.get(face_id, 'Average Human')


if __name__ == '__main__':
    bucket_name = 'ci-magicmirror'
    collection_name = 'ci-faces'

    names = ['rohank', 'logany', 'monical', 'helenaa', 'beng', 'alexf']

    # Building the index (just to train)
    # client.delete_collection(CollectionId='ci-faces')
    # index_collection(names, 'ci-faces', 'ci-magicmirror', create=True)

    # Searching with byte image
    # uglybytes = pickle.load(open('../byteimage'))
    # response = search_image(uglybytes, collection_name=collection_name, bucket_name=bucket_name, method='byte')

    # Searching with S3 object
    key = 'beng/ben0.jpg'
    response = search_image(key, method='S3')
    print(get_name(response))
