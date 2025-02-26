# 添加文件夹内所有文件
file(GLOB_RECURSE SOURCES "*.cpp" "*.c" "*.h")
set(EXTRA_COMPONENT_DIRS /esp/esp-idf-lib/components)
set(EXTRA_COMPONENT_DIRS /components)

# 注册组件
idf_component_register(SRCS "main.cpp"
        SRCS ${SOURCES}
        INCLUDE_DIRS ".")

# 生成bin文件
set(image ../data)

#fatfs_create_rawflash_image(storage ${image} FLASH_IN_PROJECT)
fatfs_create_spiflash_image(storage ${image} FLASH_IN_PROJECT PRESERVE_TIME)