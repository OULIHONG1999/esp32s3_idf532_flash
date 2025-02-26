#include <cstring>
#include <cstdio>
#include <sys/stat.h>
#include <dirent.h>

#include "esp_vfs_fat.h"
#include "driver/sdmmc_host.h"


#define TAG "FAT"
#define BASE_PATH "/spiflash"

void list_directory(const char *dir_path) {
    DIR *dir = opendir(dir_path);
    if (!dir) {
        ESP_LOGE(TAG, "无法打开目录 %s", dir_path);
        return;
    }

    struct dirent *entry;
    while ((entry = readdir(dir)) != nullptr) {
        ESP_LOGI(TAG, "file name: %s", entry->d_name);
        if (strcmp(entry->d_name, ".") == 0 || strcmp(entry->d_name, "..") == 0) {
            continue;
        }

        char full_path[1024];
        snprintf(full_path, sizeof(full_path), "%s/%s", dir_path, entry->d_name);

        struct stat stat_info{};
        if (stat(full_path, &stat_info) != 0) {
            ESP_LOGE(TAG, "无法获取文件信息 %s", full_path);
            continue;
        }

        if (S_ISDIR(stat_info.st_mode)) {
            ESP_LOGI(TAG, "dir: %s", entry->d_name);
        } else {
            ESP_LOGI(TAG, "file: %s size: %lu bts", entry->d_name, stat_info.st_size);
        }
    }

    closedir(dir);
}

void display_file_content(const char *file_path) {
    FILE *file = fopen(file_path, "r");
    if (file == nullptr) {
        ESP_LOGE(TAG, "无法打开文件 %s", file_path);
        return;
    }

    char line[256];
    while (fgets(line, sizeof(line), file)) {
        ESP_LOGI(TAG, "行: %s", line);
    }

    fclose(file);
}

void mount_flash_partition() {
    const esp_vfs_fat_mount_config_t mount_config = {
        .format_if_mount_failed = false,
        .max_files = 4,
        .allocation_unit_size = CONFIG_WL_SECTOR_SIZE,
        .disk_status_check_enable = false,
        .use_one_fat = false,
    };

    wl_handle_t wlHandle = -1;

    esp_err_t err = esp_vfs_fat_spiflash_mount_rw_wl(BASE_PATH, "storage", &mount_config, &wlHandle);
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "挂载FatFS失败，错误名称：%s", esp_err_to_name(err));
        return;
    }
    ESP_LOGI(TAG, "挂载成功");

    list_directory(BASE_PATH);
    display_file_content("/spiflash/note.txt");
}

extern "C" void app_main(void)
{
    mount_flash_partition();
}
