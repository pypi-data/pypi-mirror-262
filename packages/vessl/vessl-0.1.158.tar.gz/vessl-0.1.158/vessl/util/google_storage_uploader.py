import os

import google.cloud.storage
from concurrent.futures import Future

from requests_futures.sessions import FuturesSession

from vessl.util.file_transmission import FileTransmissionTracker, FileTransmissionHandler


class GoogleStorageUploader:
    @classmethod
    def upload(
        cls,
        client: google.cloud.storage.Client,
        source_directory: str,
        bucket_name: str,
        prefix: str = "",
    ):
        if prefix.startswith("/"):
            prefix = prefix.removeprefix("/")
        handler = FileTransmissionHandler(cls._upload_future, action="upload")
        bucket = google.cloud.storage.Bucket(client, bucket_name)
        for root, dirs, files in os.walk(source_directory):
            for file in files:
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, source_directory)
                bucket_path = os.path.join(prefix, relative_path)
                blob = google.cloud.storage.Blob(bucket_path, bucket, chunk_size=262144)
                signed_url = blob.create_resumable_upload_session(size=os.stat(full_path).st_size)
                handler.add_file(full_path, signed_url, os.stat(full_path).st_size)

        handler.run()

    @classmethod
    def _upload_future(
        cls,
        session: FuturesSession,
        full_path: str,
        url: str,
        tracker: FileTransmissionTracker,
    ) -> Future:
        return session.put(
            url, data=open(full_path, 'rb'), stream=True, hooks={"response": cls._upload_hook(full_path, tracker)}
        )

    @staticmethod
    def _upload_hook(full_path, tracker=None):
        def fn(resp, **kwargs):
            if not resp.ok:
                return

            if tracker:
                stat = os.stat(full_path)
                tracker.increase_done_size(stat.st_size)
                tracker.increase_done_count()
                tracker.print_progress()
        return fn