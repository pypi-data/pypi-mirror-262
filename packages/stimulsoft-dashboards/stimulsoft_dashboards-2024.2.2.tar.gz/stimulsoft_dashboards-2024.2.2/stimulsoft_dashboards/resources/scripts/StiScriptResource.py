from importlib import resources

from stimulsoft_reports.classes.StiFileResult import StiFileResult
from stimulsoft_reports.enums.StiDataType import StiDataType


class StiScriptResource:

    def getResult(name: str) -> StiFileResult:
        try:
            data = resources.read_binary(__package__, name)
        except Exception as e:
            message = str(e)
            return StiFileResult.getError(message)
        
        return StiFileResult(data, StiDataType.JAVASCRIPT)