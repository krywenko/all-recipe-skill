import QtQuick 2.4
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.4
import org.kde.kirigami 2.4 as Kirigami
import Mycroft 1.0 as Mycroft
//import Process 1.0

Mycroft.Delegate {
id: root
  
    ColumnLayout {

       RowLayout{ 
           
      Button {

        text: "STOP READING RECIPE"
        onClicked:{
            triggerGuiEvent("pause", {})
        }
      }
      Button{
         text: "SEARCH RESULTS"
        onClicked: {
            triggerGuiEvent("cont", {})
        }
    }
          Button{
         text: "SCREENSHOT"
        onClicked: {
            triggerGuiEvent("scrot", {})
        }
    }
    }      
    }      

         Mycroft.PaginatedText {
         anchors.fill: parent
         anchors.topMargin: 55
         text: sessionData.title
         currentIndex: 0
         horizontalAlignment: Text.AlignHLeft

         font.pixelSize: 20

         font.pointSize: Kirigami.Units.smallSpacing * 3
     }
     
     
     Mycroft.PaginatedText {
         anchors.fill: parent
         anchors.topMargin: 100
         text: sessionData.reclist
         currentIndex: 0
         horizontalAlignment: Text.AlignHLeft

         font.pixelSize: 20

         font.pointSize: Kirigami.Units.smallSpacing * 3
     }
    
    Mycroft.PaginatedText {
         anchors.fill: parent
         anchors.topMargin: 100
         //text: sessionData.title
         text: sessionData.summary
         currentIndex: 0
         horizontalAlignment: Text.AlignHLeft

         font.pixelSize: 13
         //font.pointSize: Kirigami.Units.gridUnit
         // HACK TO SET BETTER SIZE ON RESPEAKER IMAGE
         font.pointSize: Kirigami.Units.smallSpacing * 3
    }
}
