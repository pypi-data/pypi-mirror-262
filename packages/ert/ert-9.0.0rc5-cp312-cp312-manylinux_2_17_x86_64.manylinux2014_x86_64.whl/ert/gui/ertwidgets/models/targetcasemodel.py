from ert.config import AnalysisConfig
from ert.gui.ertnotifier import ErtNotifier
from ert.gui.ertwidgets.models.valuemodel import ValueModel


class TargetCaseModel(ValueModel):
    def __init__(
        self,
        analysis_config: AnalysisConfig,
        notifier: ErtNotifier,
    ):
        self.analysis_config = analysis_config
        self.notifier = notifier
        self._custom = False
        super().__init__(self.getDefaultValue())
        notifier.ertChanged.connect(self.on_current_case_changed)
        notifier.current_case_changed.connect(self.on_current_case_changed)

    def setValue(self, value: str):
        """Set a new target case"""
        if value is None or value.strip() == "" or value == self.getDefaultValue():
            self._custom = False
            ValueModel.setValue(self, self.getDefaultValue())
        else:
            self._custom = True
            ValueModel.setValue(self, value)

    def getDefaultValue(self) -> str:
        analysis_config = self.analysis_config
        if analysis_config.case_format_is_set():
            return analysis_config.case_format
        else:
            case_name = self.notifier.current_case_name
            return f"{case_name}_%d"

    def on_current_case_changed(self, *args) -> None:
        if not self._custom:
            super().setValue(self.getDefaultValue())
