# Используем официальный образ Ubuntu 20.04 как базовый
FROM ubuntu:20.04

# Устанавливаем рабочую директорию в контейнере
WORKDIR /work

# Устанавливаем переменные окружения для non-interactive режима установки пакетов
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

# Устанавливаем Python, pip, distutils и зависимости для LaTeX
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    python3-distutils \
    python3-venv \
    texlive-latex-extra \
    && rm -rf /var/lib/apt/lists/*

RUN python3.10 -m pip install --upgrade pip && \
    python3.10 -m pip install -r requirements.txt


# Копируем локальные файлы в рабочую директорию контейнера
COPY . /work

# Устанавливаем зависимости Python из файла requirements.txt
RUN python3 -m pip install -r requirements.txt

# Запускаем скрипт Python для генерации LaTeX файла, а затем компилируем его в PDF
CMD python3 main.py && pdflatex full_latex_document.tex