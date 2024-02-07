# dvc-test

## Запуск пайплайна

1. Склонировать репозиторий локально, используя:

    ```bash
    git clone https://github.com/Lazarevasn/dvc-test.git 
    ```

2. В локальном каталоге создать и активировать виртуальное окружение:

    ```bash
    python -m venv venv
    ```

    Способ активации зависит от системы.

3. Установить необходимые зависимости:

    ```bash
    pip install -r requirements.txt
    ```

4. Выполнить пуллинг обучающих и тестовых данных из удаленного хранилища DVC:

    ```bash
    dvc pull -r trainremote data/train.zip
    ```

    ```bash
    dvc pull -r testremote data/test.zip
    ```

5. Запустить пайплайн:

    ```bash
    dvc repro
    ```
