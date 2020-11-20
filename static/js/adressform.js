/* adressform.js for confirm.html

Maurice Kingma

Javascript for showing adress form
*/

// wait for page to load
document.addEventListener('DOMContentLoaded', () => {
    var clicked = false;
    var orderbutton = document.querySelector('#orderbutton')
    document.querySelectorAll('#adressButton').forEach(button => {
        button.onclick = () => {
            orderbutton.disabled = false;
            buttons = document.querySelectorAll('#adressButton')
            for (var i = 0; i < buttons.length; i++) {
                buttons[i].style.display = "none"
            }
            if (button.dataset.button === "deliver") {
                infobutton = document.createElement('DIV')
                infobutton.className = "btn btn-dark btn-block btn-blue"
                infobutton.id = "infobutton"
                infobutton.innerHTML = "Maak andere bezorgkeuze"
                document.querySelector('.adressform').appendChild(infobutton)
                formrow1 = document.createElement('DIV')
                formrow2 = document.createElement('DIV')
                formrow1.className = "form-row";
                formrow2.className = "form-row";
                formgroupcol41 = document.createElement('DIV');
                formgroupcol42 = document.createElement('DIV');
                formgroupcol81 = document.createElement('DIV');
                formgroupcol82 = document.createElement('DIV');
                formgroupcol41.className = "form-group col-sm-4";
                formgroupcol42.className = "form-group col-sm-4";
                formgroupcol81.className = "form-group col-sm-8";
                formgroupcol82.className = "form-group col-sm-8";
                streetlabel = document.createElement('LABEL');
                streetlabel.innerHTML = "Straat"
                numberlabel = document.createElement('LABEL');
                numberlabel.innerHTML = "Huisnummer"
                zipcodelabel = document.createElement('LABEL');
                zipcodelabel.innerHTML = "Postcode"
                locationlabel = document.createElement('LABEL');
                locationlabel.innerHTML = "Plaats"
                inputstreet = document.createElement('INPUT');
                inputnumber = document.createElement('INPUT');
                inputzipcode = document.createElement('INPUT');
                inputlocation = document.createElement('INPUT');
                inputstreet.type = "text";
                inputstreet.className = "form-control"
                inputhelpstreet = document.createElement('P');
                inputhelpstreet.className = "inputhelp"
                inputhelpstreet.id = "streetHelp";
                inputstreet.name = "street"
                inputstreet.id = "street"
                inputstreet.required = true
                inputnumber.type = "text";
                inputnumber.className = "form-control"
                inputhelpnumber = document.createElement('P');
                inputhelpnumber.className = "inputhelp"
                inputhelpnumber.id = "numberHelp";
                inputnumber.name = "number"
                inputnumber.id = "number"
                inputnumber.required = true
                inputzipcode.type = "text";
                inputzipcode.className = "form-control"
                inputhelpzipcode = document.createElement('P');
                inputhelpzipcode.className = "inputhelp"
                inputhelpzipcode.id = "zipcodeHelp";
                inputzipcode.name = "zipcode"
                inputzipcode.id = "zipcode"
                inputzipcode.required = true
                inputlocation.type = "text";
                inputlocation.className = "form-control"
                inputhelplocation = document.createElement('P');
                inputhelplocation.className = "inputhelp"
                inputhelplocation.id = "locationHelp";
                inputlocation.name = "location"
                inputlocation.id = "location"
                inputlocation.required = true
                formgroupcol81.appendChild(streetlabel)
                formgroupcol81.appendChild(inputstreet)
                formgroupcol81.appendChild(inputhelpstreet)
                formrow1.appendChild(formgroupcol81)
                formgroupcol41.appendChild(numberlabel)
                formgroupcol41.appendChild(inputnumber)
                formgroupcol41.appendChild(inputhelpnumber)
                formrow1.appendChild(formgroupcol41)
                formgroupcol42.appendChild(zipcodelabel)
                formgroupcol42.appendChild(inputzipcode)
                formgroupcol42.appendChild(inputhelpzipcode)
                formrow2.appendChild(formgroupcol42)
                formgroupcol82.appendChild(locationlabel)
                formgroupcol82.appendChild(inputlocation)
                formgroupcol82.appendChild(inputhelplocation)
                formrow2.appendChild(formgroupcol82)
                br = document.createElement('BR')
                document.querySelector('.adressform').appendChild(br)
                document.querySelector('.adressform').appendChild(formrow1)
                document.querySelector('.adressform').appendChild(formrow2)
                document.querySelector('#infobutton').onclick = () => {
                    document.querySelector('.adressform').innerHTML = "";
                    for (var i = 0; i < buttons.length; i++) {
                        buttons[i].style.display = ""
                        orderbutton.disabled = true;
                    }
                }
            } else {
                infobutton = document.createElement('DIV')
                infobutton.className = "btn btn-dark btn-block btn-blue"
                infobutton.id = "infobutton"
                infobutton.innerHTML = "Maak andere bezorgkeuze"
                document.querySelector('.adressform').appendChild(infobutton)
                br = document.createElement('BR')
                document.querySelector('.adressform').appendChild(br)
                infotext = document.createElement('P')
                infotext.className = "info"
                infotext.innerHTML = "U heeft gekozen voor afhalen in Bussum, na de betaling van de bestelling wordt er contact met u opgenomen om een afspraak te maken"
                document.querySelector('.adressform').appendChild(infotext)
                document.querySelector('#infobutton').onclick = () => {
                    document.querySelector('.adressform').innerHTML = "";
                    for (var i = 0; i < buttons.length; i++) {
                        buttons[i].style.display = ""
                        orderbutton.disabled = true;
                    }
                }
            }
        };
    });
});
