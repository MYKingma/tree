/* checkupdate.js for createupdate.html

Maurice Kingma

Javascript for checking input when editing update
*/

// wait for page to load
document.addEventListener('DOMContentLoaded', () => {


    // show links already uploaded images
    var images = document.getElementById('images');
    var updateId = document.getElementById('updateId').value;
    var type = '/' + document.getElementById('type').value + '/'
    if (images.value.length > 0) {
        var uploadedImages = document.getElementById('images').value.split(',');
        label = document.createElement('LABEL');
        br = document.createElement('BR');
        label.innerHTML = 'Links naar afbeeldingen';
        div = document.querySelector('.imageLinks');
        div.className = "imageLinks smallbox"
        div.appendChild(br);
        div.appendChild(label);
        for (var i = 0; i < uploadedImages.length; ++i) {
            if (uploadedImages[i].length > 0) {
                var path = 'https://raw.githubusercontent.com/MYKingma/tree/master/static/img/uploads' + type + updateId + '/' + uploadedImages[i];
                pName = document.createElement('P');
                sPath = document.createElement('SPAN');
                sPath.id = "sPath"
                pName.innerHTML = uploadedImages[i];
                icon = document.createElement("I");
                icon.className = "fas fa-copy";
                text = document.createTextNode(" Kopieer link")
                sPath.appendChild(icon);
                sPath.appendChild(text);
                sPath.dataset.link = path
                sPath.className = 'floatright';
                sPath.style.cursor = "pointer";
                pName.appendChild(sPath);
                div.appendChild(pName);
            }
        }
        newLink()
    }
    // select file upload input
    document.getElementById('file').onchange = () => {
        var input = document.getElementById('file');
        if (images.value.length > 0) {
            var prevImages = images.value;
            images.value = ""
        }
        div = document.querySelector('.imageLinks');
        div.innerHTML = '';
        div.className = "imageLinks smallbox"
        label = document.createElement('LABEL');
        br = document.createElement('BR');
        label.innerHTML = 'Links naar afbeeldingen';
        div.appendChild(br);
        div.appendChild(label);
        if (uploadedImages) {
            for (var i = 0; i < uploadedImages.length; ++i) {
                var path = 'https://raw.githubusercontent.com/MYKingma/tree/master/static/img/uploads' + type + updateId + '/' + uploadedImages[i];
                pName = document.createElement('P');
                sPath = document.createElement('SPAN');
                sPath.id = "sPath"
                pName.innerHTML = uploadedImages[i];
                icon = document.createElement("I");
                icon.className = "fas fa-copy";
                text = document.createTextNode(" Kopieer link")
                sPath.appendChild(icon);
                sPath.appendChild(text);
                sPath.dataset.link = path
                sPath.className = 'floatright';
                sPath.style.cursor = "pointer";
                pName.appendChild(sPath);
                div.appendChild(pName);
            }
        }
        for (var i = 0; i < input.files.length; ++i) {
            var name = input.files.item(i).name;
            var path = 'https://raw.githubusercontent.com/MYKingma/tree/master/static/img/uploads' + type + updateId + '/' + name;
            pName = document.createElement('P');
            sPath = document.createElement('SPAN');





            sPath.id = "sPath"
            pName.innerHTML = name;
            icon = document.createElement("I");
            icon.className = "fas fa-copy";
            text = document.createTextNode(" Kopieer link")
            sPath.appendChild(icon);
            sPath.appendChild(text);
            sPath.dataset.link = path
            sPath.className = 'floatright';
            sPath.style.cursor = "pointer";


            pName.appendChild(sPath);
            div.appendChild(pName);
            if (images.value.length == 0) {
                images.value = name
            } else {
                images.value = images.value + ',' + name
            }
        }
        newLink()
        if (prevImages) {
            images.value = images.value + ',' + prevImages
        }
    }
});
