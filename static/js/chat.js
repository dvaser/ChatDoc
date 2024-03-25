
function animateTitle() {
    var titleElement = document.getElementById("animatedTitle");
    var text = titleElement.innerText;
    var length = text.length;
    var index = 0;

    var interval = setInterval(function() {
        titleElement.innerText = text.substring(0, index++);
        if (index > length) {
            clearInterval(interval);
            titleElement.innerText = text; // İşlem tamamlandığında orijinal yazıyı göster
            setTimeout(animateTitle, 15000); // 1 dakika sonra yeniden başlat
        }
    }, 100); // Yeni harf ekleme hızı (ms)
}

animateTitle(); // Animasyonu başlatmak için çağır
