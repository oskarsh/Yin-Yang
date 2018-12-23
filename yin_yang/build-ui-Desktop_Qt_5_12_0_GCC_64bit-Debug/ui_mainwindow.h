/********************************************************************************
** Form generated from reading UI file 'mainwindow.ui'
**
** Created by: Qt User Interface Compiler version 5.12.0
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_MAINWINDOW_H
#define UI_MAINWINDOW_H

#include <QtCore/QVariant>
#include <QtGui/QIcon>
#include <QtWidgets/QApplication>
#include <QtWidgets/QFormLayout>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QLabel>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QRadioButton>
#include <QtWidgets/QTimeEdit>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QWidget *centralWidget;
    QWidget *verticalLayoutWidget;
    QVBoxLayout *verticalLayout;
    QLabel *yinyangimg;
    QHBoxLayout *horizontalLayout;
    QPushButton *light_push;
    QPushButton *dark_push;
    QRadioButton *schedule_radio;
    QFormLayout *formLayout;
    QLabel *label;
    QLabel *label_2;
    QTimeEdit *light_time;
    QTimeEdit *dark_time;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName(QString::fromUtf8("MainWindow"));
        MainWindow->setEnabled(true);
        MainWindow->resize(260, 270);
        QSizePolicy sizePolicy(QSizePolicy::Fixed, QSizePolicy::Fixed);
        sizePolicy.setHorizontalStretch(0);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(MainWindow->sizePolicy().hasHeightForWidth());
        MainWindow->setSizePolicy(sizePolicy);
        MainWindow->setMinimumSize(QSize(260, 270));
        MainWindow->setMaximumSize(QSize(260, 270));
        MainWindow->setBaseSize(QSize(260, 270));
        QIcon icon;
        icon.addFile(QString::fromUtf8(":/icons/assets/yin-yang.png"), QSize(), QIcon::Normal, QIcon::Off);
        MainWindow->setWindowIcon(icon);
        centralWidget = new QWidget(MainWindow);
        centralWidget->setObjectName(QString::fromUtf8("centralWidget"));
        verticalLayoutWidget = new QWidget(centralWidget);
        verticalLayoutWidget->setObjectName(QString::fromUtf8("verticalLayoutWidget"));
        verticalLayoutWidget->setGeometry(QRect(19, 20, 221, 231));
        verticalLayout = new QVBoxLayout(verticalLayoutWidget);
        verticalLayout->setSpacing(6);
        verticalLayout->setContentsMargins(11, 11, 11, 11);
        verticalLayout->setObjectName(QString::fromUtf8("verticalLayout"));
        verticalLayout->setContentsMargins(0, 0, 0, 0);
        yinyangimg = new QLabel(verticalLayoutWidget);
        yinyangimg->setObjectName(QString::fromUtf8("yinyangimg"));
        yinyangimg->setTextFormat(Qt::RichText);
        yinyangimg->setPixmap(QPixmap(QString::fromUtf8(":/icons/assets/yin-yang.png")));
        yinyangimg->setAlignment(Qt::AlignCenter);

        verticalLayout->addWidget(yinyangimg);

        horizontalLayout = new QHBoxLayout();
        horizontalLayout->setSpacing(6);
        horizontalLayout->setObjectName(QString::fromUtf8("horizontalLayout"));
        light_push = new QPushButton(verticalLayoutWidget);
        light_push->setObjectName(QString::fromUtf8("light_push"));

        horizontalLayout->addWidget(light_push);

        dark_push = new QPushButton(verticalLayoutWidget);
        dark_push->setObjectName(QString::fromUtf8("dark_push"));
        dark_push->setEnabled(false);

        horizontalLayout->addWidget(dark_push);


        verticalLayout->addLayout(horizontalLayout);

        schedule_radio = new QRadioButton(verticalLayoutWidget);
        schedule_radio->setObjectName(QString::fromUtf8("schedule_radio"));

        verticalLayout->addWidget(schedule_radio);

        formLayout = new QFormLayout();
        formLayout->setSpacing(6);
        formLayout->setObjectName(QString::fromUtf8("formLayout"));
        formLayout->setHorizontalSpacing(40);
        label = new QLabel(verticalLayoutWidget);
        label->setObjectName(QString::fromUtf8("label"));
        label->setAlignment(Qt::AlignCenter);

        formLayout->setWidget(0, QFormLayout::LabelRole, label);

        label_2 = new QLabel(verticalLayoutWidget);
        label_2->setObjectName(QString::fromUtf8("label_2"));

        formLayout->setWidget(1, QFormLayout::LabelRole, label_2);

        light_time = new QTimeEdit(verticalLayoutWidget);
        light_time->setObjectName(QString::fromUtf8("light_time"));
        light_time->setEnabled(false);
        light_time->setTime(QTime(8, 0, 0));

        formLayout->setWidget(0, QFormLayout::FieldRole, light_time);

        dark_time = new QTimeEdit(verticalLayoutWidget);
        dark_time->setObjectName(QString::fromUtf8("dark_time"));
        dark_time->setEnabled(false);
        dark_time->setTime(QTime(20, 0, 0));

        formLayout->setWidget(1, QFormLayout::FieldRole, dark_time);


        verticalLayout->addLayout(formLayout);

        MainWindow->setCentralWidget(centralWidget);

        retranslateUi(MainWindow);

        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QApplication::translate("MainWindow", "Yin & Yang", nullptr));
        yinyangimg->setText(QString());
        light_push->setText(QApplication::translate("MainWindow", "Light", nullptr));
        dark_push->setText(QApplication::translate("MainWindow", "Dark", nullptr));
        schedule_radio->setText(QApplication::translate("MainWindow", "scheduled", nullptr));
        label->setText(QApplication::translate("MainWindow", "Light:", nullptr));
        label_2->setText(QApplication::translate("MainWindow", "Dark:", nullptr));
        light_time->setDisplayFormat(QApplication::translate("MainWindow", "HH:mm", nullptr));
        dark_time->setDisplayFormat(QApplication::translate("MainWindow", "HH:mm", nullptr));
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MAINWINDOW_H
