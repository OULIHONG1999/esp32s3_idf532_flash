import os
from argparse import ArgumentParser

from components.spiffs.spiffsgen import SpiffsBuildConfig, SpiffsFS


# from spiffs_build import SpiffsBuildConfig, SpiffsFS  # 假设这些类和方法已存在

def main():
    # 定义固定参数
    image_size = "0x9c0000"  # 替换为具体数值或字符串
    base_dir = f"E:\JetBrains\Clion\Clion_project\esp32s3_idf532\data"  # 替换为实际目录路径
    output_file = "E:\\JetBrains\\Clion\\Clion_project\\esp32s3_idf532\\littlefs\\data_file.bin"  # 替换为输出文件路径

    page_size = 256
    block_size = 4096
    obj_name_len = 32
    meta_len = 4
    use_magic = True
    use_magic_len = True
    follow_symlinks = False
    big_endian = False
    aligned_obj_ix_tables = True

    # 检查 base_dir 是否存在
    if not os.path.exists(base_dir):
        raise RuntimeError(f'given base directory {base_dir} does not exist')

    # 创建输出文件
    with open(output_file, 'wb') as image_file:
        image_size_bytes = int(image_size, 0)
        spiffs_build_default = SpiffsBuildConfig(
            page_size, SPIFFS_PAGE_IX_LEN,
            block_size, SPIFFS_BLOCK_IX_LEN,
            meta_len, obj_name_len,
            SPIFFS_OBJ_ID_LEN, SPIFFS_SPAN_IX_LEN,
            True, True,
            'big' if big_endian else 'little',
            use_magic, use_magic_len,
            aligned_obj_ix_tables
        )

        spiffs = SpiffsFS(image_size_bytes, spiffs_build_default)

        for root, dirs, files in os.walk(base_dir, followlinks=follow_symlinks):
            for f in files:
                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path, base_dir).replace('\\', '/')
                spiffs.create_file(f'/{rel_path}', full_path)

        image = spiffs.to_binary()
        image_file.write(image)

# 关于 SPIFFS 相关的常量，需要根据上下文定义
# 假设 SPIFFS_PAGE_IX_LEN 等常量由其他模块或配置提供
# 如果需要，可以在这里定义：

SPIFFS_OBJ_ID_LEN = 2  # spiffs_obj_id
SPIFFS_SPAN_IX_LEN = 2  # spiffs_span_ix
SPIFFS_PAGE_IX_LEN = 2  # spiffs_page_ix
SPIFFS_BLOCK_IX_LEN = 2  # spiffs_block_ix

if __name__ == "__main__":
    main()