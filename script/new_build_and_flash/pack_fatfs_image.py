import subprocess
import os
import csv

# 配置
IDF_PATH = r"E:\ESP\IDF532\Espressif\frameworks\esp-idf-v5.3.2"  # ESP-IDF 的路径
PYTHON_PATH = r"..\..\.venv\Scripts"  # Python 解释器路径
FATFS_DIR = r"..\..\data"  # 要打包的文件目录路径
OUTPUT_DIR = r"..\..\build_fatfs_bin"  # 生成的镜像文件输出路径
PARTITION_CSV = r"..\..\partitions.csv"  # 分区表 CSV 文件路径

PARTITION_NAME = "storage"  # 分区名称

USE_DEFAULT_DATETIME = False  # 是否使用默认时间戳
ONE_FAT = False  # 是否只创建一个 FAT 分区
WL_INIT = True  # 是否启用 Wear Levelling
CONFIG_FATFS_SECTOR_512 = False  # 假设扇区大小为 512
CONFIG_FATFS_LFN_NONE = False  # 假设不支持长文件名


# 取得相对地址的绝对地址
def get_absolute_path(relative_path):
    return os.path.abspath(relative_path)


# 取得相对地址的绝对地址
PYTHON_PATH = get_absolute_path(PYTHON_PATH)
FATFS_DIR = get_absolute_path(FATFS_DIR)
OUTPUT_DIR = get_absolute_path(OUTPUT_DIR)
PARTITION_CSV = get_absolute_path(PARTITION_CSV)

def get_partition_info(partition_name):
    """
    从分区表 CSV 文件中读取指定分区的大小和偏移量
    """
    size = None
    offset = None
    with open(PARTITION_CSV, 'r') as csvfile:
        # 读取第一行作为原始表头
        raw_header = csvfile.readline().strip()
        # 清理表头，去除多余的空格和逗号
        header = [col.strip() for col in raw_header.replace('#', '').split(',') if col.strip()]
        reader = csv.DictReader(csvfile, fieldnames=header)
        for row in reader:
            if row.get('Name') == partition_name:
                size = row.get('Size')
                offset = row.get('Offset')
                break
    return size, offset

def pack_fatfs_image():
    # 获取分区信息
    size, offset = get_partition_info(PARTITION_NAME)
    if not size or not offset:
        print(f"Failed to get partition info for '{PARTITION_NAME}'. Check the partition table file.")
        exit(-1)

    # 去除size前后的空格
    size = size.strip()
    print(size)

    # 转换大小为十六进制
    if 'M' in size:
        print(size)
        size = hex(int(size.replace('M', '')) * 1024 * 1024)
    elif 'K' in size:
        size = hex(int(size.replace('K', '')) * 1024)
    elif size.startswith('0x') or size.startswith('0X'):
        print(f"size is hex {size}")
        size = hex(int(size, 16))  # 修改这里，添加进制参数
    else:
        size = hex(int(size))

    # 设置命令行参数
    if WL_INIT:
        fatfsgen_tool = os.path.join(IDF_PATH, "components", "fatfs", "wl_fatfsgen.py")
    else:
        fatfsgen_tool = os.path.join(IDF_PATH, "components", "fatfs", "fatfsgen.py")

    image_file = os.path.join(OUTPUT_DIR, f"{PARTITION_NAME}.bin")
    base_dir = FATFS_DIR

    # 确定扇区大小
    if CONFIG_FATFS_SECTOR_512:
        fatfs_sector_size = "512"
    # 可以根据需要添加其他扇区大小的判断
    else:
        fatfs_sector_size = "4096"

    # 确定长文件名支持
    if CONFIG_FATFS_LFN_NONE:
        fatfs_long_names_option = []
    # 可以根据需要添加其他长文件名支持的判断
    else:
        fatfs_long_names_option = ["--long_name_support"]

    command = [
        "python",
        fatfsgen_tool,
        base_dir,
        *fatfs_long_names_option,
        "--partition_size",
        size,
        "--sector_size",
        fatfs_sector_size,
        "--output_file",
        image_file,
    ]

    if not USE_DEFAULT_DATETIME:
        command.append("--use_default_datetime")

    if ONE_FAT:
        command.extend(["--fat_count", "1"])

    # 执行打包命令
    try:
        # 打印完整的命令行
        print(f"Executing: {' '.join(command)}")
        subprocess.run(command, check=True)
        print(f"FATFS image '{image_file}' generated successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Command failed with error code {e.returncode}")
        exit(-1)

if __name__ == "__main__":
    pack_fatfs_image()