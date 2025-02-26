import subprocess
import os

def parse_fatfs_file(fatfsparse_script_path, input_image, wl_layer=None):
    """
    调用 fatfsparse.py 脚本解析 FATFS 镜像文件

    参数:
        fatfsparse_script_path (str): fatfsparse.py 脚本的路径
        input_image (str): 输入的 FATFS 镜像文件路径
        wl_layer (str, optional): 磨损均衡层选项（可选值：detect, enabled, disabled）
    """
    # 构造命令行参数
    command = [
        'python',
        fatfsparse_script_path,
        input_image
    ]

    # 添加可选参数
    if wl_layer is not None:
        command.extend(['--wl-layer', wl_layer])

    # 打印命令
    print("正在执行命令:", ' '.join(command))

    # 执行命令
    try:
        subprocess.run(command, check=True)
        print(f"FATFS 镜像文件解析完成：{input_image}")
    except subprocess.CalledProcessError:
        print("命令执行失败，请检查参数和路径是否正确。")

def main():
    # 示例参数
    fatfsparse_script_path = r"E:\JetBrains\Clion\Clion_project\esp32s3_idf532\script\build_img\fatfs\fatfsparse.py"
    input_image = r"E:\JetBrains\Clion\Clion_project\esp32s3_idf532\littlefs\fatfs.bin"
    wl_layer = "detect"  # 可选：detect, enabled, disabled

    # 调用函数
    parse_fatfs_file(
        fatfsparse_script_path,
        input_image,
        wl_layer
    )

if __name__ == "__main__":
    main()