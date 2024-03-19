# SPDX-FileCopyrightText: Copyright (c) 2024 Matthew Joyce and other QuickGraphLib contributors
# SPDX-License-Identifier: MIT

import pathlib
import re
import sys

from PySide6 import QtCore, QtGui, QtQml, QtQuickControls2

EXAMPLES_DIR = pathlib.Path(__file__).parent

sys.path.append(str(EXAMPLES_DIR.parent))

import quickgraphlib_helpers  # pylint: disable=unused-import

if __name__ == "__main__":
    QtQuickControls2.QQuickStyle.setStyle("Basic")
    app = QtGui.QGuiApplication(sys.argv)
    engine = QtQml.QQmlApplicationEngine()
    engine.addImportPath(EXAMPLES_DIR.parent)

    examples = []
    for f in EXAMPLES_DIR.glob("*.qdoc"):
        text = f.read_text()
        title_match = re.search(r"\\title (.*)", text)
        image_match = re.search(r"\\image (.*)", text)
        qf_match = re.search(r"\\quotefile (.*)", text)

        assert title_match is not None
        assert image_match is not None
        assert qf_match is not None

        title = title_match.group(1)
        image = QtCore.QUrl.fromLocalFile(EXAMPLES_DIR.parent / image_match.group(1))
        qml_file = QtCore.QUrl.fromLocalFile(EXAMPLES_DIR.parent / qf_match.group(1))

        examples.append([title, image, qml_file])

    engine.setInitialProperties({"examples": examples})
    engine.load(EXAMPLES_DIR / "ExampleGallery.qml")

    if engine.rootObjects():
        app.exec()
