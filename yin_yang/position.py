import logging
from time import sleep

import requests
from PySide6.QtCore import QObject
from PySide6.QtPositioning import QGeoPositionInfoSource, QGeoCoordinate, QGeoPositionInfo

logger = logging.getLogger(__name__)


def get_current_location() -> QGeoCoordinate:
    try:
        return get_qt_position()
    except TypeError as e:
        logger.warning(e)

    try:
        return get_ipinfo_position()
    except TypeError as e:
        logger.warning(e)

    raise TypeError('Unable to get current location')


parent = QObject()
location_source = QGeoPositionInfoSource.createDefaultSource(parent)


def get_qt_position() -> QGeoCoordinate:
    if location_source is None:
        raise TypeError('Location source is none')

    pos: QGeoPositionInfo = location_source.lastKnownPosition()
    if pos is None:
        location_source.requestUpdate(10)
    tries = 0
    while pos is None and tries < 10:
        pos = location_source.lastKnownPosition()
        tries += 1
        sleep(1)
    coordinate = pos.coordinate()

    if not coordinate.isValid():
        raise TypeError('Coordinates are not valid')

    return coordinate

# there is a freedesktop portal for getting the location,
# but it's not implemented by KDE, so I have no use for it


def get_ipinfo_position() -> QGeoCoordinate:
    # use the old method as a fallback
    try:
        response = requests.get('https://www.ipinfo.io/loc')
    except Exception as e:
        logger.error(e)
        raise TypeError('Error while sending a request to get location')

    if not response.ok:
        raise TypeError('Failed to get location from ipinfo.io')

    loc_response = response.text.removesuffix('\n').split(',')
    loc: [float] = [float(coordinate) for coordinate in loc_response]
    assert len(loc) == 2, 'The returned location should have exactly 2 values.'
    coordinate = QGeoCoordinate(loc[0], loc[1])

    if not coordinate.isValid():
        raise TypeError('Coordinates are not valid')

    return coordinate
