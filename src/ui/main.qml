import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    width: 550; height: 800
    visible: true
    title: qsTr("Yin & Yang")

    ColumnLayout {
        width: parent.width; height: parent.height

        TabBar {
                id: tabs
                width: parent.width
                Layout.alignment: Qt.AlignTop

                TabButton { text: qsTr("Settings") }
                TabButton { text: qsTr("Plugins") }
        }

        StackLayout {
            currentIndex: tabs.currentIndex

            ColumnLayout {
                id: settingsView

                CheckBox {
                    checked: true
                    text: qsTr("Enable automatic switching")
                }

                ColumnLayout {
                    RadioButton { text: qsTr("manual times") }

                    Row {
                        Text {text: "Light time:"}
                        TextInput { inputMask: "09:99"; inputMethodHints: Qt.ImhTime; text: "09:00" }
                    }

                    Row {
                        Text {text: "Dark time:"}
                        TextInput { inputMask: "09:99" }
                    }

                    RadioButton { text: qsTr("location based") }


                    ColumnLayout {
                        CheckBox {
                            text: qsTr("Automatically find location")
                        }

                        Row {
                            Text {text: "latitude:"}
                            TextInput { text: "text" }
                        }

                        Row {
                            Text {text: "longitude:"}
                            TextInput {}
                        }
                    }
                }

                CheckBox {
                    checked: true
                    text: qsTr("Enable notifications")
                }

                CheckBox {
                    checked: true
                    text: qsTr("Enable sound")
                }

                Text {
                    text: qsTr("Dark mode will be activate between x:xx and xx:xx")
                }
            }

            Component {
                id: pluginsView

                ColumnLayout {}
            }
        }

        DialogButtonBox {
            Layout.alignment: Qt.AlignBottom
            standardButtons:  DialogButtonBox.RestoreDefaults | DialogButtonBox.Apply | DialogButtonBox.Cancel
        }
    }

    footer: Text {
        text: qsTr("You are running Yin & Yang version x.x")
    }

}
