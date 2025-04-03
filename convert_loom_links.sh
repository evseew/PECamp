#!/bin/bash

# Этот скрипт заменяет ссылки на Loom на встроенные iframe-плееры во всех HTML-файлах

# Функция для замены ссылок Loom в одном файле
process_file() {
  file="$1"
  echo "Обрабатываю файл: $file"
  
  # Найти все ссылки на Loom в файле
  # Ищем строки вида <a href="https://www.loom.com/share/XXXXX">...</a>
  grep -o '<a href="https://www.loom.com/share/[^"]*"[^>]*>[^<]*</a>' "$file" | while read -r loom_link; do
    # Извлекаем URL из ссылки
    url=$(echo "$loom_link" | grep -o 'https://www.loom.com/share/[^"]*')
    
    # Создаем iframe-код для этой ссылки
    embed_url="${url/share/embed}"
    iframe_code="<div style=\"position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; margin-top: 10px; margin-bottom: 10px;\"><iframe src=\"$embed_url\" frameborder=\"0\" allowfullscreen style=\"position: absolute; top: 0; left: 0; width: 100%; height: 100%;\"></iframe></div>"
    
    # Заменяем ссылку на iframe в файле
    # Используем разделитель '#' для sed, чтобы избежать проблем с '/' в URL
    # Экранируем специальные символы в строке замены
    loom_link_escaped=$(echo "$loom_link" | sed 's/[\/&]/\\&/g')
    iframe_code_escaped=$(echo "$iframe_code" | sed 's/[\/&]/\\&/g')
    
    sed -i.bak "s#$loom_link_escaped#$iframe_code_escaped#g" "$file"
  done
  
  # Удаляем резервные копии
  rm -f "$file.bak"
}

# Обрабатываем файл index.html
process_file "index.html"

# Обрабатываем все файлы HTML в подпапках
find "Campleaders 2024 6be322c49792408689edb590a134746b" -type f -name "*.html" | while read -r file; do
  process_file "$file"
done

echo "Все файлы обработаны!" 