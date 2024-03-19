import os
from setuptools import setup, find_packages

# Read the contents of your README file
with open(os.path.join(os.getcwd(), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
setup(
    name='latexgen-renzo-fu',  # Название вашей библиотеки
    version='0.1.2',  # Версия библиотеки
    packages=find_packages(),  # Автоматически находит пакеты в вашем проекте
    install_requires=[],  # Зависимости, необходимые для работы вашей библиотеки
    python_requires='>=3.6',  # Минимальная версия Python
    author='Renzo',  # Ваше имя
    author_email='renz_alexander@example.com',  # Ваш email
    description='A simple LaTeX table and image generator',
    long_description=long_description,
    # This is important for markdown files
    long_description_content_type='text/markdown',
    keywords='LaTeX, table, image',
    url='https://github.com/Renzo-Fu/Python_course',  # Ссылка на репозиторий проекта
)
