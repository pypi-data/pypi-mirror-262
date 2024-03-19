from setuptools import setup, find_packages

setup(
    name='latexgen-renzo-fu',  # Название вашей библиотеки
    version='0.1.1',  # Версия библиотеки
    packages=find_packages(),  # Автоматически находит пакеты в вашем проекте
    install_requires=[],  # Зависимости, необходимые для работы вашей библиотеки
    python_requires='>=3.6',  # Минимальная версия Python
    author='Renzo',  # Ваше имя
    author_email='renz_alexander@example.com',  # Ваш email
    description='A simple LaTeX table and image generator',  # Описание проекта
    keywords='LaTeX, table, image',  # Ключевые слова, описывающие проект
    url='https://github.com/Renzo-Fu/Python_course',  # Ссылка на репозиторий проекта
)
