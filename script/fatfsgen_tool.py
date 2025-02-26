import subprocess
import os

def generate_fatfs_file(fatfs_script_path, output_file, partition_size, sector_size, long_name_support, use_default_datetime, input_directory):
    """
    调用 fatfsgen.py 脚本生成 FATFS 镜像文件

    参数:
        fatfs_script_path (str): fatfsgen.py 脚本的路径
        output_file (str): 输出镜像文件的路径
        partition_size (int): 分区大小（字节）
        sector_size (int): 扇区大小（支持的值：4096）
        long_name_support (bool): 是否支持长文件名
        use_default_datetime (bool): 是否使用默认时间戳
        input_directory (str): 输入目录路径
    """
    # 构造命令行参数
    command = [
        'python',
        fatfs_script_path,
        '--output_file', output_file,
        '--partition_size', str(partition_size),
        '--sector_size', str(sector_size)
    ]

    # 添加可选参数
    if long_name_support:
        command.append('--long_name_support')
    if use_default_datetime:
        command.append('--use_default_datetime')

    # 添加必需的输入目录参数
    command.append(input_directory)

    # 打印命令
    print("正在执行命令:", ' '.join(command))

    # 执行命令
    try:
        subprocess.run(command, check=True)
        print(f"FATFS 镜像文件已生成：{output_file}")
    except subprocess.CalledProcessError:
        print("命令执行失败，请检查参数和路径是否正确。")

def main():
    fatfs_script_path = r"E:\JetBrains\Clion\Clion_project\esp32s3_idf532_flash\script\build_img\fatfs\fatfsgen.py"
    output_file = r"E:\JetBrains\Clion\Clion_project\esp32s3_idf532_flash\build_fatfs_bin\fatfs.bin"
    partition_size = 1048576  # 分区大小（字节）
    sector_size = 4096        # 扇区大小
    long_name_support = True  # 是否支持长文件名
    use_default_datetime = True  # 是否使用默认时间戳
    input_directory = r"E:\JetBrains\Clion\Clion_project\esp32s3_idf532_flash\data"  # 输入目录

    # 调用函数
    generate_fatfs_file(
        fatfs_script_path,
        output_file,
        partition_size,
        sector_size,
        long_name_support,
        use_default_datetime,
        input_directory
    )

if __name__ == "__main__":
    main()