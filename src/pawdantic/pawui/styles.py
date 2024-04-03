from fastui import class_name as _class_name
from loguru import logger

from pawdantic.pawui import pawui_types

ROW_STYLE: _class_name.ClassName = 'row'
COL_STYLE: _class_name.ClassName = 'col'
CONTAINER_STYLE: _class_name.ClassName = 'row w-90 mx-auto mt-5'
PAGE_STYLE: _class_name.ClassName = 'container'
ALERT_STYLE: _class_name.ClassName = 'alert alert-warning'
SHIP_BUTTON: _class_name.ClassName = 'row align-items-center'


def get_alert_style(alert_type: pawui_types.AlertType) -> _class_name.ClassName:
    base_style = 'alert mx-auto w-75'
    match alert_type:
        case 'ERROR':
            return f'{base_style} alert-danger'
        case 'WARNING':
            return f'{base_style} alert-warning'
        case 'NOTIFICATION':
            return f'{base_style} alert-info'
        case 'INFO':
            return f'{base_style} alert-info'
        case _:
            logger.info('alert type not recognized')
            return 'alert alert-info'
