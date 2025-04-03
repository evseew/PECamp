#!/usr/bin/env python3
import os
import re
import glob

def convert_loom_links_to_iframes(html_content):
    """
    Заменяет ссылки на Loom на встроенные iframe-плееры
    """
    # Регулярное выражение для поиска ссылок на Loom
    # Ищем строки вида <a href="https://www.loom.com/share/XXXXX">...</a>
    pattern = r'<a href="(https://www\.loom\.com/share/[^"]*)"[^>]*>(.*?)</a>'
    
    def replace_link(match):
        url = match.group(1)  # URL-ссылка на Loom
        text = match.group(2)  # Текст ссылки
        
        # Создаем URL для встраивания
        embed_url = url.replace('share', 'embed')
        
        # Создаем iframe-код
        iframe_code = (
            f'<div style="position: relative; padding-bottom: 56.25%; height: 0; '
            f'overflow: hidden; max-width: 100%; margin-top: 10px; margin-bottom: 10px;">'
            f'<iframe src="{embed_url}" frameborder="0" allowfullscreen '
            f'style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>'
            f'</div>'
        )
        
        return iframe_code
    
    # Заменяем все найденные ссылки на iframe
    modified_content = re.sub(pattern, replace_link, html_content)
    
    return modified_content

def process_file(file_path):
    """
    Обрабатывает один HTML-файл
    """
    print(f"Обрабатываю файл: {file_path}")
    
    try:
        # Читаем содержимое файла
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Заменяем ссылки на iframe
        modified_content = convert_loom_links_to_iframes(content)
        
        # Если были сделаны изменения, сохраняем файл
        if content != modified_content:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(modified_content)
            print(f"  Файл обновлен!")
        else:
            print(f"  Нет ссылок Loom для замены.")
    except Exception as e:
        print(f"  Ошибка при обработке файла {file_path}: {str(e)}")

def main():
    """
    Основная функция для обработки всех HTML-файлов
    """
    # Обрабатываем главную страницу
    process_file("index.html")
    
    # Получаем список всех HTML-файлов в папке проекта
    html_files = glob.glob("Campleaders 2024 6be322c49792408689edb590a134746b/**/*.html", recursive=True)
    
    # Обрабатываем каждый файл
    for file_path in html_files:
        process_file(file_path)
    
    print("\nВсе файлы обработаны!")

if __name__ == "__main__":
    main() 