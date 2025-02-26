import subprocess
import os

import esptool

from pack_fatfs_image import OUTPUT_DIR, PARTITION_NAME, PARTITION_NAME, get_partition_info

# 配置
ESPTOOL_PATH = "/path/to/esptool.py"  # esptool.py 的路径
SERIAL_PORT = "COM95"  # 串口（如 COM95）
BAUD_RATE = "2000000"  # 波特率
FLASH_MODE = "dio"  # Flash 模式
FLASH_FREQ = "80m"  # Flash 频率
FLASH_SIZE = "16MB"  # Flash 大小
IMAGE_FILE = r"E:\JetBrains\Clion\Clion_project\esp32s3_idf532_flash\build_fatfs_bin\storage.bin"  # 镜像文件路径
# IMAGE_FILE = r"E:\JetBrains\Clion\Clion_project\esp32s3_idf532_flash\build\storage.bin"  # 镜像文件路径
# IMAGE_FILE = OUTPUT_DIR + "/" + PARTITION_NAME + ".bin"  # 镜像文件路径
IMAGE_OFFSET = "0x110000"  # 镜像文件的烧录地址


def flash_fatfs_image():
    size, offset = get_partition_info(PARTITION_NAME)
    IMAGE_OFFSET = offset

    print("size: ", size, "offset: ", offset)

    # 设置命令行参数
    command = [
        # "python", ESPTOOL_PATH,
        "python", "-m", "esptool",
        "--chip", "esp32s3",
        "-p", SERIAL_PORT,
        "-b", BAUD_RATE,
        "--before", "default_reset",
        "--after", "hard_reset",
        "write_flash", "--flash_mode",
        FLASH_MODE,
        "--flash_freq", FLASH_FREQ,
        "--flash_size", FLASH_SIZE,
        IMAGE_OFFSET, IMAGE_FILE,
    ]

    # 执行烧录命令
    try:
        print(f"Executing: {' '.join(command)}")
        # esptool.main(command)
        subprocess.run(command, check=True)
        print(f"FATFS image '{IMAGE_FILE}' flashed successfully to {SERIAL_PORT} at offset {IMAGE_OFFSET}.")
    except subprocess.CalledProcessError as e:
        print(f"Command failed with error code {e.returncode}")
        exit(-1)


if __name__ == "__main__":
    flash_fatfs_image()
