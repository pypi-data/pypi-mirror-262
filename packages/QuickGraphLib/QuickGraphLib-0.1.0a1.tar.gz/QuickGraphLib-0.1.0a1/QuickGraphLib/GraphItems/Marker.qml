// SPDX-FileCopyrightText: Copyright (c) 2024 Matthew Joyce and other QuickGraphLib contributors
// SPDX-License-Identifier: MIT

import QtQuick

/*!
    \qmltype Marker
    \inqmlmodule QuickGraphLib.GraphItems
    \inherits QtQuick::Rectangle
    \brief Displays a circular marker.
*/

Rectangle {
    id: root

    /*! TODO */
    required property matrix4x4 dataTransform
    readonly property point pixelPosition: root.dataTransform.map(position)
    /*! TODO */
    required property point position

    border.width: 0
    height: width
    radius: width / 2
    width: 5
    x: pixelPosition.x - width / 2
    y: pixelPosition.y - width / 2
}
