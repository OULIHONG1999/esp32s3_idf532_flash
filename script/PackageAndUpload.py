import subprocess

def call_fatfsparse(image_file, wl_layer=None, verbose=False):
    command = ["./fatfsparse.py", image_file]

    if wl_layer:
        command.append(f"--wl-layer={wl_layer}")

    if verbose:
        command.append("--verbose")

    # 调用 fatfsparse.py 并捕获输出
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
        print("Successfully parsed FATFS image.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)


image_file = "E:\JetBrains\Clion\Clion_project\esp32s3_idf532\littlefs\image_file.bin"


# 示例用法
call_fatfsparse(image_file, wl_layer="detect", verbose=True)