from pathlib import Path
import zipfile


class ZipService:

    def _add_directory(
        self,
        zip_file,
        directory: Path,
        archive_name: str | None = None
    ):

        for file in directory.rglob("*"):

            if not file.is_file():
                continue

            if archive_name is None:
                arcname = file.relative_to(directory)
            else:
                arcname = Path(archive_name) / file.relative_to(directory)

            zip_file.write(
                file,
                arcname=arcname
            )

    def create_zip(
        self,
        output_dir: str,
        zip_path: str,
        include_debug: bool = False,
        debug_dir: str | None = None,
        include_logs: bool = False,
        log_dir: str | None = None
    ) -> str:

        output_dir = Path(output_dir)
        zip_path = Path(zip_path)

        with zipfile.ZipFile(
            zip_path,
            "w",
            compression=zipfile.ZIP_DEFLATED
        ) as zip_file:

            # --------------------------
            # Output Images
            # --------------------------

            self._add_directory(
                zip_file,
                output_dir
            )

            # --------------------------
            # Debug Images
            # --------------------------

            if include_debug and debug_dir:

                self._add_directory(
                    zip_file,
                    Path(debug_dir),
                    "debug"
                )

            # --------------------------
            # Logs
            # --------------------------

            if include_logs and log_dir:

                self._add_directory(
                    zip_file,
                    Path(log_dir),
                    "logs"
                )

        return str(zip_path)