import os
import shutil
import click


@click.group()
def cli():
    pass


@cli.command()
@click.argument('project_name')
def create_project(project_name):
    src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
    dest_path = os.path.join(os.getcwd(), project_name)

    # Создаем новую папку для проекта
    if not os.path.exists(dest_path):
        os.makedirs(dest_path)
    else:
        click.echo(f"Проект с именем '{project_name}' уже существует.")
        return

    # Копируем файлы из папки src в новый проект
    try:
        for root, dirs, files in os.walk(src_path):
            for file in files:
                src_file = os.path.join(root, file)
                dest_file = os.path.join(dest_path, os.path.relpath(src_file, src_path))
                dest_dir = os.path.dirname(dest_file)
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)
                shutil.copy2(src_file, dest_file)
        click.echo(f"Проект '{project_name}' успешно создан.")
    except Exception as e:
        click.echo(f"Возникла ошибка при создании проекта: {e}")


if __name__ == '__main__':
    cli()
