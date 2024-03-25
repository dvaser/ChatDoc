
function docButton(button, activeDocId, formId) {
    var buttons = document.getElementsByClassName("document");

    // Diğer butonlardaki aktif durumu ve "hidden" durumunu kaldır
    for (var i = 0; i < buttons.length; i++) {
        if (buttons[i] != button) {
            buttons[i].classList.remove("active");
            buttons[i].setAttribute("name", "");  // Document ID'sini sıfırla
        }
    }

    // Seçilen butona aktif durumu ekle ve Document ID'sini ayarla
    if (!button.classList.contains("active")) {
        button.classList.add("active");
        var documentId = button.value;
        button.setAttribute("name", "document_id");
        button.setAttribute("value", documentId);
        
        // Diğer formdaki butonun değerini güncelle
        var sendButton = document.querySelector("#" + formId + " .send");
        sendButton.setAttribute("value", activeDocId);
    }

    // HTML'i güncelle
    button.outerHTML = button.outerHTML;
    document.getElementById("sendButton").click();
}

function imgButton(image) {
    var buttons = document.getElementsByClassName("document");

    for (var i = 0; i < buttons.length; i++) {
        var button = buttons[i];
        var buttonShowImg = button.querySelector('#showImg');
        var buttonHiddenImg = button.querySelector('#hiddenImg');

        if (button.classList.contains('active')) {
            if (buttonShowImg.classList.contains("hidden")) {
                buttonShowImg.classList.remove("hidden");
                buttonHiddenImg.classList.add("hidden");
            } else {
                // Silme işlemi gelecek
                buttonShowImg.classList.add("hidden");
                buttonHiddenImg.classList.remove("hidden");
            }
        } else {
            buttonShowImg.classList.remove("hidden");
            buttonHiddenImg.classList.add("hidden");
        }
    }
}

function alertMessage() {
    var msg = "Dokuman secilmedi!";
    var activeDocId = "{{ activeDoc.id }}";

    if (activeDocId === '') {
        alert(msg);
    }
}

function clearAllButton() {
    var clearButton = document.getElementById("clearAllButton");
    var confirmButton = document.getElementById("confirmButton");

    if (confirmButton.classList.contains("hidden")) {
        clearButton.classList.add("hidden");
        confirmButton.classList.remove("hidden");
    } else {
        clearButton.classList.remove("hidden");
        confirmButton.classList.add("hidden");
    }
}