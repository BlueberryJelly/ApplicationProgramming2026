"""Приложение для просмотра датасета обложек.

Интерфейс описан в main_window.ui, логика - main_window.py.
"""

from collections.abc import Iterator
from pathlib import Path

from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QResizeEvent
from PyQt6.QtWidgets import QFileDialog, QMainWindow, QMenu

from lab_2.src.path_iterator import CoverPathIterator

UI_FILE = Path(__file__).with_name("main_window.ui")
SOURCE_ERRORS = (OSError, ValueError)


class MainWindow(QMainWindow):
    """Главное окно: выбор источника и просмотр изображений."""

    def __init__(self) -> None:
        """Загрузить интерфейс и подключить обработчики."""
        super().__init__()
        uic.loadUi(UI_FILE, self)

        self._paths: Iterator[Path] = iter(())
        self._history: list[Path] = []
        self._position = -1
        self._pixmap: QPixmap | None = None

        menu = QMenu(self.sourceButton)
        menu.addAction("Папка с изображениями...", self.choose_folder)
        menu.addAction("Файл аннотации (*.csv)...", self.choose_annotation)
        self.sourceButton.setMenu(menu)
        self.leftArrow.clicked.connect(self.show_previous)
        self.rightArrow.clicked.connect(self.show_next)

    def choose_folder(self) -> None:
        """Выбрать папку датасета и открыть её."""
        folder = QFileDialog.getExistingDirectory(self, "Выберите папку с датасетом")
        if folder:
            self.set_source(Path(folder))

    def choose_annotation(self) -> None:
        """Выбрать CSV-аннотацию и открыть её."""
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Выберите файл аннотации", "", "CSV (*.csv)"
        )
        if file_name:
            self.set_source(Path(file_name))

    def set_source(self, source: Path) -> None:
        """Открыть новый источник и показать первое изображение.

        Если источник не удалось открыть, текущее состояние не меняется.

        :param source: папка с изображениями или CSV-аннотация
        """
        try:
            paths = CoverPathIterator(source)
        except SOURCE_ERRORS as error:
            self.status_bar.showMessage(f"Не удалось открыть источник: {error}")
            return

        self._paths = paths
        self._history.clear()
        self._position = -1
        self._pixmap = None
        self.image.clear()
        self.show_next()

    def show_next(self) -> None:
        """Показать следующее изображение датасета."""
        if self._position + 1 < len(self._history):
            self._show(self._position + 1)
            return
        while (path := self._next_path()) is not None:
            self._history.append(path)
            if self._show(len(self._history) - 1):
                return
            self._history.pop()

    def show_previous(self) -> None:
        """Вернуться к ранее показанному изображению."""
        if self._position > 0:
            self._show(self._position - 1)

    def _next_path(self) -> Path | None:
        """Получить следующий путь от итератора.

        :return: путь или None, если датасет закончился или источник
            не удалось прочитать, причина выводится в строку состояния
        """
        try:
            return next(self._paths)
        except StopIteration:
            self._stop("Достигнут конец датасета")
        except SOURCE_ERRORS as error:
            self._stop(f"Ошибка чтения источника: {error}")
        return None

    def _stop(self, message: str) -> None:
        """Запретить переход вперёд и вывести сообщение.

        :param message: текст для статус-бара
        """
        self.rightArrow.setEnabled(False)
        self.status_bar.showMessage(message)

    def _show(self, position: int) -> bool:
        """Показать изображение из истории по индексу.

        :param position: индекс в истории показанных путей
        :return: True, если файл удалось открыть как изображение
        """
        path = self._history[position]
        pixmap = QPixmap(str(path))
        if pixmap.isNull():
            return False
        self._position = position
        self._pixmap = pixmap
        self._update_pixmap()
        self.leftArrow.setEnabled(position > 0)
        self.rightArrow.setEnabled(True)
        self.status_bar.showMessage(f"{position + 1}: {path}")
        return True

    def _update_pixmap(self) -> None:
        """Вписать изображение в метку без деформации и увеличения.

        Если изображение помещается - показывается в исходном размере,
        иначе уменьшается с сохранением пропорций.
        """
        if self._pixmap is None:
            return
        shown = self._pixmap
        size = self.image.size()
        if shown.width() > size.width() or shown.height() > size.height():
            shown = shown.scaled(
                size,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        self.image.setPixmap(shown)

    def resizeEvent(self, event: QResizeEvent) -> None:
        """Пересчитать масштаб изображения при изменении размера окна.

        :param event: событие изменения размера
        """
        super().resizeEvent(event)
        self._update_pixmap()
