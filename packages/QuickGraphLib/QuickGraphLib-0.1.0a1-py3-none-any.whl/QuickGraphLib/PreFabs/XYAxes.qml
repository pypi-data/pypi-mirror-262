// SPDX-FileCopyrightText: Copyright (c) 2024 Matthew Joyce and other QuickGraphLib contributors
// SPDX-License-Identifier: MIT

import QtQuick
import QtQuick.Layouts as QQL
import QuickGraphLib as QuickGraphLib
import QuickGraphLib.GraphItems as QGLGraphItems

/*!
    \qmltype Line
    \inqmlmodule QuickGraphLib.PreFabs
    \inherits QuickGraphLib::AntialiasingContainer
    \brief Displays an XY axis with a grid.
*/

QuickGraphLib.AntialiasingContainer {
    id: root

    /*! TODO */
    property alias axes: axes
    /*! TODO */
    property alias background: background
    /*! TODO */
    property alias dataTransform: grapharea.dataTransform
    /*! TODO */
    default property alias graphChildren: grapharea.data
    /*! TODO */
    property alias grapharea: grapharea
    /*! TODO */
    property alias grid: grid
    /*! TODO */
    property int numXTicks: 11
    /*! TODO */
    property int numYTicks: 11
    /*! TODO */
    property bool showXTickLabels: true
    /*! TODO */
    property bool showYTickLabels: true
    /*! TODO */
    property alias title: titleLabel.text
    /*! TODO */
    required property rect viewRect
    /*! TODO */
    property alias xAxis: xAxis
    /*! TODO */
    property alias xLabel: xAxis.label
    /*! TODO */
    property alias yAxis: yAxis
    /*! TODO */
    property alias yLabel: yAxis.label

    Rectangle {
        id: background

        anchors.fill: parent
    }
    QQL.GridLayout {
        id: axes

        anchors.fill: parent
        anchors.margins: 15
        columnSpacing: 0
        columns: 2
        rowSpacing: 0

        Text {
            id: titleLabel

            QQL.Layout.alignment: Qt.AlignCenter
            QQL.Layout.columnSpan: 2
            visible: text != ""
        }
        QuickGraphLib.Axis {
            id: yAxis

            QQL.Layout.fillHeight: true
            dataTransform: grapharea.dataTransform
            direction: QuickGraphLib.Axis.Direction.Left
            showTickLabels: root.showYTickLabels
            ticks: grid.yTicks
        }
        QuickGraphLib.GraphArea {
            id: grapharea

            QQL.Layout.fillHeight: true
            QQL.Layout.fillWidth: true
            viewRect: root.viewRect

            QGLGraphItems.Grid {
                id: grid

                dataTransform: grapharea.dataTransform
                parentHeight: grapharea.height
                parentWidth: grapharea.width
                strokeColor: "#11000000"
                strokeWidth: 1
                xTicks: QuickGraphLib.Helpers.tickLocator(grapharea.effectiveViewRect.x, grapharea.effectiveViewRect.x + grapharea.effectiveViewRect.width, root.numXTicks)
                yTicks: QuickGraphLib.Helpers.tickLocator(grapharea.effectiveViewRect.y, grapharea.effectiveViewRect.y + grapharea.effectiveViewRect.height, root.numYTicks)
            }
        }
        Item {
        }
        QuickGraphLib.Axis {
            id: xAxis

            QQL.Layout.fillWidth: true
            dataTransform: grapharea.dataTransform
            direction: QuickGraphLib.Axis.Direction.Bottom
            showTickLabels: root.showXTickLabels
            ticks: grid.xTicks
        }
    }
}
