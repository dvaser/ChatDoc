function changeIcon(){
    var icon = document.getElementById('changeIcon')
    if (icon.className == "photo") {
        document.getElementById('exhibitionUser').classList.remove('d-none');
        document.getElementById('photoUser').classList.add('d-none');
        document.getElementById('changeIcon').classList.remove('photo');
        document.getElementById('changeIcon').classList.add('exhibition');
    } 
    else if(icon.className == "exhibition") {
        document.getElementById('exhibitionUser').classList.add('d-none');
        document.getElementById('photoUser').classList.remove('d-none');
        document.getElementById('changeIcon').classList.remove('exhibition');
        document.getElementById('changeIcon').classList.add('photo');
    }
} 