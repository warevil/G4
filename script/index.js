

getFormDataAppointment = () => {
    const formData = {
        name: document.querySelector(".modal-body #appointment_name").value,
        email: document.querySelector(".modal-body #appointment_email").value,
        code: document.querySelector(".modal-body #appointment_code").value,
        date: document.querySelector(".modal-body #appointment_date").value,
        time: document.querySelector(".modal-body #appointment_time").value,
        message: document.querySelector(".modal-body #appointment_symptoms").value,
    }
    return formData;
}

validateFormData = async (data) => {
    let valid = false;

    await fire_database.ref('family')
        .child(data.code)
        .orderByChild('email')
        .equalTo(data.email)
        .once('value')
        .then(snap => {
            valid = snap.exists()
        });

    return valid;
}

const send = document.querySelector("#appointment_send");
send.onclick = async (e) => {
    e.preventDefault();
    const new_appointment = getFormDataAppointment()
    console.log(new_appointment);
    if (await validateFormData(new_appointment)) {
        console.log("Validate Success!")
        firePushAppointment(new_appointment);
        sendEmail(new_appointment);
    } else {
        console.log("Validate Fail!")
    }
}

function firePushAppointment(appointment) {
    // Create a new data reference with an auto-generated id
    var listRef = firebase.database().ref('appointments');
    var newItemRef = listRef.push();
    newItemRef.set({
        ...appointment,
    });
}

function sendEmail({ email, date, time, code }) {
    Email.send({
        Host: "smtp.gmail.com",
        Username: "appfisi21@gmail.com",
        Password: "fisi2021",
        To: email,
        From: "appfisi21@gmail.com",
        Subject: `Cita Médica - Asegurado ${code}`,
        Body: `
        Su cita está registrada para el ${date} a las ${time}.
        En el siguiente enlace: https://www.meet.com/SAdwQdas2
        Atte. Medical FISI.
        `,
    })
        .then(function (message) {
            alert("El enlace a su cita médica ha sido enviada a su correo.")
        });
}