let user = undefined;

const user_card = document.getElementById('user-card');
const drawUserCard = (user) => {
    //debugger;
    const { displayName, email, phoneNumber, photoURL, uid } = user;
    user_card.innerHTML = `
                <img src="${photoURL}" class="card-img-top" alt="google profile photo">
                <div class="card-body m-2">
                    <h5 class="card-title">Asegurado: ${displayName}</h5>
                    <ul class="list-group">
                        <li class="list-group-item">
                            <code>email: </code>
                            <div class="card-text">${email}.</div>
                        </li>
                        <li class="list-group-item">
                            <code>phone: </code>
                            <div class="card-text">phoneNumber: ${phoneNumber}.</div>
                        </li>
                        <li class="list-group-item">
                            <code>Código de Asegurado: </code>
                            <div class="card-text">${uid}.</div>
                        </li>
                    </ul>
                </div>
                    `;
}


var dataRef = undefined;
const family_table = document.querySelector('#table-family-tbody');
const renderFamily = () => {
    dataRef.on('value', (snapshot) => {
        family_table.innerHTML = '';
        snapshot.forEach((child) => {

            console.log(child);
            const { name, email } = child.val();

            let row = family_table.insertRow();

            row.innerHTML += `
                <td class="align-middle text-capitalize">${name}</td>
                <td class="align-middle">${email}</td>
                <td class="align-middle">
                    <div style="display:flex" data-name="${name}">
                        <i class="fa fa-trash btn btn-outline-danger btn-sm" ></i>
                    </div>
                </td>
            `;

        });
    });
}

const add_family = document.querySelector("#add-family .btn");
add_family.onclick = (e) => {
    e.preventDefault();
    const person = {
        name: document.querySelector("#new-family-name").value,
        email: document.querySelector("#new-family-email").value,
    };
    add_person(person);
}

async function add_person(person) {
    // agrega la persona a los familiares del usuario registrado
    let valid = true;
    await fire_database.ref('family')
        .child(user.uid)
        .orderByChild('email')
        .equalTo(person.email)
        .once('value')
        .then(snap => {
            if (snap.exists())
                valid = false;
        });

    if (valid) {
        var listRef = firebase.database().ref('family/' + user.uid);
        var newItemRef = listRef.push();
        newItemRef.set({
            ...person,
        });
    } else {
        console.log("¡¡ El email ya fue registrado !!")
    }

}

const googleLogin = () => {

    var provider = new fire_auth.GoogleAuthProvider();

    console.log("Google login...")

    fire_auth()
        .signInWithPopup(provider)
        .then((result) => {
            var credential = result.credential;
            // This gives you a Google Access Token. You can use it to access the Google API.
            var token = credential.accessToken;
            // The signed-in user info.
            var _user = result.user;

            console.log(_user)
            console.log(token)

            user = _user;
            dataRef = firebase.database().ref('family/' + user.uid);

            let btn = document.querySelector('#google-login')
            btn.innerText = 'Cerrar Sesión'
            btn.onclick = () => {
                location.reload();
            }
            add_person({ name: user.displayName, email: user.email });
            drawUserCard(user)
            renderFamily(user)

        }).catch((error) => {
            var errorCode = error.code;
            var errorMessage = error.message;
            // The email of the user's account used.
            var email = error.email;
            // The firebase.auth.AuthCredential type that was used.
            var credential = error.credential;

            console.error(errorCode);
            console.error(errorMessage);
            console.error('email:', email);
            console.error('credential: ', error.credential);
        });
}

const google_login = document.querySelector('#google-login');
google_login.onclick = googleLogin;