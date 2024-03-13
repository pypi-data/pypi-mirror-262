from typing import Optional

from qtpy.QtCore import QObject, Signal, Slot

from ert.storage import Ensemble, Storage


class ErtNotifier(QObject):
    ertChanged = Signal()
    storage_changed = Signal(object, name="storageChanged")
    current_case_changed = Signal(object, name="currentCaseChanged")

    def __init__(self, config_file: str):
        QObject.__init__(self)
        self._config_file = config_file
        self._storage: Optional[Storage] = None
        self._current_case = None
        self._is_simulation_running = False

    @property
    def is_storage_available(self) -> bool:
        return self._storage is not None

    @property
    def storage(self) -> Storage:
        assert self.is_storage_available
        return self._storage

    @property
    def config_file(self) -> str:
        return self._config_file

    @property
    def current_case(self) -> Optional[Ensemble]:
        if self._current_case is None and self._storage is not None:
            ensembles = list(self._storage.ensembles)
            if ensembles:
                self._current_case = ensembles[0]
        return self._current_case

    @property
    def current_case_name(self) -> str:
        if self._current_case is None:
            return "default"
        return self._current_case.name

    @property
    def is_simulation_running(self) -> bool:
        return self._is_simulation_running

    @Slot()
    def emitErtChange(self):
        self.ertChanged.emit()

    @Slot(object)
    def set_storage(self, storage: Storage) -> None:
        self._storage = storage
        self.storage_changed.emit(storage)

    @Slot(object)
    def set_current_case(self, case: Optional[Ensemble] = None) -> None:
        self._current_case = case
        self.current_case_changed.emit(case)

    @Slot(bool)
    def set_is_simulation_running(self, is_running: bool) -> None:
        self._is_simulation_running = is_running
