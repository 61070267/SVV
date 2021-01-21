let sbutt = document.getElementById("Sellbutt");
sbutt.addEventListener("click", FormSwitch);

let bbutt = document.getElementById("Buybutt");
bbutt.addEventListener("click", FormSwitch);

let ifield = document.getElementById("Info-field");
let submit = document.getElementById("submit");
let usertype = document.getElementById("usertype");

function FormSwitch(event) {
    if (event.target == sbutt) {
        sbutt.classList.add('active')
        bbutt.classList.remove('active')
        usertype.value = 'Seller'
    } else {
        bbutt.classList.add('active')
        sbutt.classList.remove('active')
        usertype.value = 'Buyer'
    }

    axios.get('/api/register/', {
            params: {
                usertype: usertype.value
            }
        })
        .then(function(response) {
            ifield.innerHTML = response.data;
        })
        .catch(function(error) {
            console.log(error)
        })
        .then(function() {
            submit.removeAttribute('hidden')
        });
}

function showImg(input, width = 400, height = 400) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function(e) {
            if (input.nextSibling) {
                let img = input.nextSibling
                img.setAttribute('src', e.target.result);
                img.setAttribute("height", height);
                img.setAttribute("width", width);
            } else {
                let img = document.createElement("img");
                img.setAttribute('src', e.target.result);
                img.setAttribute("height", height);
                img.setAttribute("width", width);
                input.parentNode.insertBefore(img, input.nextSibling)
            }
        };

        reader.readAsDataURL(input.files[0]);
    }
}