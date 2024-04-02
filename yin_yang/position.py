import logging

import requests
from PySide6.QtCore import QObject, Slot
from PySide6.QtPositioning import (
    QGeoPositionInfoSource,
    QGeoCoordinate,
    QGeoPositionInfo,
)

logger = logging.getLogger(__name__)


class QTPositionReceiver(QObject):
    """Small handler for QT positioning service."""

    def __init__(self):
        super().__init__()

        # Create the position service and hook it to us
        self._positionSource = QGeoPositionInfoSource.createSource(
            "geoclue2", {"desktopId": "Yin-Yang"}, self
        )
        self._positionSource.positionUpdated.connect(self.handlePosition)

        # Start the position service.
        # This will only work after the app calls `exec()`.
        self._positionSource.startUpdates()

        # Get the initial last position.
        self._lastPosition = self._positionSource.lastKnownPosition()

    @Slot(QGeoPositionInfo)
    def handlePosition(self, position: QGeoPositionInfo):
        """Track the position provided by the service."""
        self._lastPosition = position

        # TODO: Here trigger a refresh.
        # I tried the following but it seem to not work:
        ## Trigger a refresh. Ugly but does the job
        # from yin_yang.config import config
        # _ = config.location
        # del config

    def lastKnownPosition(self):
        """Return the last known position, if valid."""
        return self._lastPosition


position_handler = QTPositionReceiver()


def get_current_location() -> QGeoCoordinate:
    try:
        return get_qt_position()
    except TypeError as e:
        logger.warning(e)

    try:
        return get_ipinfo_position()
    except TypeError as e:
        logger.warning(e)

    raise TypeError("Unable to get current location")


def get_qt_position() -> QGeoCoordinate:
    """Get the position via QT service"""
    # Fetch the last known position
    global position_handler
    pos: QGeoPositionInfo = position_handler.lastKnownPosition()

    coordinate = pos.coordinate()

    if not coordinate.isValid():
        raise TypeError("Coordinates are not valid")

    return coordinate


# there is a freedesktop portal for getting the location,
# but it's not implemented by KDE, so I have no use for it


def get_ipinfo_position() -> QGeoCoordinate:
    # use the old method as a fallback
    try:
        response = requests.get("https://www.ipinfo.io/loc")
    except Exception as e:
        logger.error(e)
        raise TypeError("Error while sending a request to get location")

    if not response.ok:
        raise TypeError("Failed to get location from ipinfo.io")

    loc_response = response.text.removesuffix("\n").split(",")
    loc: [float] = [float(coordinate) for coordinate in loc_response]
    assert len(loc) == 2, "The returned location should have exactly 2 values."
    coordinate = QGeoCoordinate(loc[0], loc[1])

    if not coordinate.isValid():
        raise TypeError("Coordinates are not valid")

    return coordinate
