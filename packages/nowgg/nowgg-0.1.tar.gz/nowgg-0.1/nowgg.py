import requests
import os
import traceback
import concurrent.futures
from urllib.parse import urlparse
from urllib.parse import parse_qs
import argparse
import shelve


UPLOAD_CHUNK_SIZE = 10 * 1024 * 1024  # 10MB
# Initialize the file where the result of cached methods will be stored.
cache_file = 'cache.nowgg'
cache = shelve.open(cache_file, writeback=True)


def get_host():
    return cache.get("host", "test.")


def upload_part(file_path, start_byte, end_byte, presigned_url):
    try:
        with open(file_path, 'rb') as file:
            file.seek(start_byte)
            chunk = file.read(end_byte - start_byte)

        response = requests.put(presigned_url, data=chunk)
        response.raise_for_status()
        return response
    except Exception as e:
        print(f"Error uploading part: {e}")
        traceback.print_exc()
        return None


def upload_async(file_path, part_id_url_list, chunks_count):
    promises_array = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for current_part in range(1, chunks_count + 1):
            current_chunk_start_byte = (current_part - 1) * UPLOAD_CHUNK_SIZE
            current_chunk_end_byte = current_part * UPLOAD_CHUNK_SIZE
            presigned_url = part_id_url_list[current_part - 1]
            future = executor.submit(
                upload_part, file_path, current_chunk_start_byte, current_chunk_end_byte, presigned_url)
            futures.append(future)
        for completed_future in concurrent.futures.as_completed(futures):
            progress = (
                len([f for f in futures if f.done()]) / chunks_count) * 100
            print(f"Uploading... {progress:.2f}%")

            response = completed_future.result()
            if response:
                promises_array.append(response)
            else:
                print("Error occurred during part upload.")

    return promises_array


def upload_file(file_path, game_id, token, app_version, app_version_code):
    try:
        file_name = os.path.basename(file_path)
        upload_type = "upload_file_zip" if file_name.endswith(".zip") or file_name.endswith(
            ".rar") or file_name.endswith(".7z") else "upload_file"
        headers = {"publisher_token": token}
        with open(file_path, 'rb') as file:
            file_size = os.path.getsize(file_path)
            chunks_count = int((file_size // UPLOAD_CHUNK_SIZE) + 1)

            # Initialize multipart upload
            response = requests.post(f"{get_host()}/v2/publisher/asset/mutipart_upload/start",
                                     params={"file_name": file_name, "game_id": game_id,
                                             "parts_count": chunks_count},
                                     headers=headers)
            data = response.json().get('data', {})
            upload_id = data.get('upload_id', "")
            part_id_url_list = data.get('presigned_url_data')
            s3_file_path = data.get('s3_file_path')

            promises_array = upload_async(
                file_path, part_id_url_list, chunks_count)

            upload_parts_array = []
            for i, resp in enumerate(promises_array):
                parsed_url = urlparse(resp.url)
                part_num = parse_qs(parsed_url.query)['partNumber'][0]
                upload_parts_array.append(
                    {"ETag": resp.headers['ETag'].replace('"', ''), "PartNumber": int(part_num)})

            sorted_upload_parts_array = sorted(
                upload_parts_array, key=lambda x: x['PartNumber'])
            response = requests.post(f"{get_host()}/v2/publisher/asset/mutipart_upload/end", json={
                                     "upload_id": upload_id, "parts_info": sorted_upload_parts_array,
                                     "s3_file_path": s3_file_path}, headers=headers)
            if response.status_code in [200, 201]:
                print("Upload completed.")
                file_url = f"https://cdn.now.gg/{s3_file_path}"
                response = requests.post(
                    f"{get_host()}/v2/publisher/apk-library",
                    json={"upload_url": file_url,
                          "app_version": app_version,
                          "app_version_code": app_version_code,
                          "game_id": game_id,
                          "upload_type": upload_type}, headers=headers)
                if response.status_code in [200, 201]:
                    print("Successfully uploaded to your Apk Library!")
                else:
                    print(response)
                    print(response.reason)
            else:
                print(response.reason)

    except Exception as e:
        print(f"Error: {e}")


class Nowgg:

    def config(self, hostname):
        
        if hostname:
            old_host = cache.get("host")
            cache["host"] = hostname
            print(f"changed host from {old_host} to {hostname}")
        else:
            print(cache.get("host"))    

    def init(self, token):
        """Init
        Args:
            token (str): required parameter token
        """

        cache['token'] = token
        print("init successful!")

    def upload(self, app_id, app_file_path, app_version, app_version_code):
        """Upload utility

        Args:
            app_id (str): required parameter app_id
            app_file_path (str): required parameter app_file_path
            app_version (str): required parameter app_version
            app_version_code (int): required parameter app_version_code

        """
        token = cache.get('token')
        if token:
            return upload_file(app_file_path, app_id, token, app_version, app_version_code)
        else:
            print("Please init first with token. nowgg init <your-token>")


def main():

    nowgg = Nowgg()
    parser = argparse.ArgumentParser(description="nowgg: Nowgg CLI")

    subparsers = parser.add_subparsers(
        title='subcommands', dest='command', description='Choose one of the following operations')

    # Subparser for the init command
    init_parser = subparsers.add_parser('init', help='Init')
    init_parser.add_argument(
        '-token', type=str, help='Publisher Token', required=True)

    # Subparser for the upload command
    upload_parser = subparsers.add_parser('upload', help='Upload utility')
    upload_parser.add_argument(
        '-app_id', type=str, help='App Id', required=True)
    upload_parser.add_argument(
        '-file_path', type=str, help='File Path', required=True)
    upload_parser.add_argument(
        '-apk_version', type=str, help='apk version name', required=True)
    upload_parser.add_argument(
        '-version_code', type=int, help='apk version code', required=True)

    config_parser = subparsers.add_parser('config', help=argparse.SUPPRESS)
    config_parser.add_argument('-host', help=argparse.SUPPRESS)

    args = parser.parse_args()

    if args.command == 'init':
        nowgg.init(args.token)
    elif args.command == 'upload':
        nowgg.upload(args.app_id, args.file_path,
                     args.apk_version, args.version_code)
    elif args.command == 'config':
        nowgg.config(args.host)
    else:    
        parser.print_help()


if __name__ == "__main__":
    main()
