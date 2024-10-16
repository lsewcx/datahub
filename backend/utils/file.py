import shutil

class FileUtils:
    @staticmethod
    def unzip_file(upload_path: str, output_path: str):
        shutil.unpack_archive(upload_path, output_path)
        return output_path