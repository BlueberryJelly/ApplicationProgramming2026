"""Просмотр обложек с графическим интерфейсом.

Запуск:
    python -m lab_5.main
"""

import sys

from PyQt6.QtWidgets import QApplication

from lab_5.src.main_window import MainWindow


def main() -> int:
    """Запустить программу.

    :return: код завершения (0 - успех, 1 - ошибка)
    """
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
