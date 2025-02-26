import subprocess
import logging
from concurrent.futures import ThreadPoolExecutor

import esptool


class ESPFlasher:
    def __init__(self):
        self.thread_pool = ThreadPoolExecutor(max_workers=20)

    def flash_esptool(self,
                      chip,
                      port,
                      baud=115200,
                      before_reset="default_reset",
                      after_reset="hard_reset",
                      flash_mode="dout",
                      flash_freq="80m",
                      flash_size="2MB",
                      flash_files=None,
                      verify=False,
                      **kwargs):
        if flash_files is None:
            flash_files = {}
        if not isinstance(flash_files, dict) or not flash_files:
            raise ValueError("flash_files must be a non-empty dictionary of the form {'address': 'file_path'}")

        command = [
            # "python", "-m", "esptool",
            "--chip", chip,
            "--port", port,
            "--baud", str(baud),
            "--before", before_reset,
            "--after", after_reset,
            "write_flash",
            "-z",
            "--flash_mode", flash_mode,
            "--flash_freq", flash_freq,
            "--flash_size", flash_size
        ]

        if verify:
            command.append("--verify")

        for address, file_path in flash_files.items():
            command.extend([address, file_path])

        print(f"Starting flash process with command:python -m esptool {' '.join(command)}")

        re = self.thread_pool.submit(self._run_flash_command, command)
        return re

    def _run_flash_command(self, command):
        try:
            esptool.main(command)
            return True, f" Flash successful!"
        except subprocess.CalledProcessError as e:
            logging.error(f" Flash failed.")
            return False, f" Error occurred: {e}"
        except Exception as e:
            logging.error(" Flash failed.")
            return False, f"  An unexpected error occurred: {e}"

    def erase_flash(self, port, chip):
        def erase_thread():
            try:
                # Construct erase command
                erase_command = [
                    "--chip", chip,  # Modify this if using a different ESP chip
                    "--port", port,
                    "erase_flash"
                ]
                # Execute erase command
                esptool.main(erase_command)
                return True, "flash success"
            except subprocess.CalledProcessError as e:
                logging.error("Erase Flash failed.", e)
                return False, "flash failed"

            except FileNotFoundError:
                logging.error("Erase Flash failed.")
                return False, "flash failed"

        re = self.thread_pool.submit(erase_thread)
        return re

    def shutdown(self):
        self.thread_pool.shutdown(wait=False, cancel_futures=True)


# 示例调用
def flash_esptool(chip, port, baud, flash_size, flash_files, verify):
    flasher = ESPFlasher()
    result = flasher.flash_esptool(
        chip=chip,
        port=port,
        baud=baud,
        flash_size=flash_size,
        flash_files=flash_files,
        verify=verify
    )
    pass


if __name__ == "__main__":
    flash_esptool(
        chip="esp32s3",
        port="COM95",
        baud=1152000,
        flash_size="16MB",
        flash_files={
            # "0x0": "E:\\work_space\\Cyber_Immortal\\code\\cyber-legends---idf\\SBCSV2.0_IDF_5.3.2\\build\\bootloader\\bootloader.bin",
            # "0x10000": "E:\\work_space\\Cyber_Immortal\\code\\cyber-legends---idf\\SBCSV2.0_IDF_5.3.2\\build\\SBCSV2.0_IDF_5.1.4.bin",
            # "0x5F0000": "E:\JetBrains\Clion\Clion_project\esp32s3_idf532\littlefs\spifs.bin",
            "0x110000": r"E:\JetBrains\Clion\Clion_project\esp32s3_idf532_flash\build_fatfs_bin\fatfs.bin",
            # "0x8000": "E:\\work_space\\Cyber_Immortal\\code\\cyber-legends---idf\\SBCSV2.0_IDF_5.3.2\\build\\partition_table\\partition-table.bin"
        },
        verify=True
    )
