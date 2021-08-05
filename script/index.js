
getFormDataAppointment = () => {
    const formData = {
        name: document.querySelector(".modal-body #appointment_name").value,
        email: document.querySelector(".modal-body #appointment_email").value,
        code: document.querySelector(".modal-body #appointment_code").value,
        modality: document.querySelector(".modal-body #appointment_modality").value,
        attentionArea: document.querySelector(".modal-body #appointment_attentionArea").value,
        doctor: document.querySelector(".modal-body #appointment_doctor").value,
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
    // var listRef = firebase.database().ref('appointments');
    // var newItemRef = listRef.push();
    // newItemRef.set({
    //     ...appointment,
    // });
    console.log(appointment);
}

const enlaces_meet = [
    "meet.google.com/ykh-kpzn-ojq",
    "meet.google.com/iqo-jrgn-amq",
    "meet.google.com/odj-wycf-fhh",
    "meet.google.com/ufm-bigv-fei",
    "meet.google.com/hcw-ezmm-bph",
    "meet.google.com/jkc-bvsy-cdi",
    "meet.google.com/ddz-atbj-nzd",
    "meet.google.com/fxz-jksp-czd",
    "meet.google.com/cxe-cedf-fkd",
    "meet.google.com/pji-wvqa-bzt",
]

function sendEmail({ 
    attentionArea,
    code,
    date,
    doctor,
    email,
    message,
    modality,
    name,
    time,
}) {

    const mail = {
        Host: "smtp.gmail.com",
        Username: "appfisi21@gmail.com",
        Password: "fisi2021",
        To: email,
        From: "appfisi21@gmail.com",
        Subject: `Cita Médica - Asegurado ${code}`,
        Body: `
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"
        integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">

    <h1>Cita Médica</h1>
    <hr>
    <p>
        Hola, ${name}.
        <br>
        Reciba un cordial saludo de parte de la clínica lider en salud SALUD G1.
        Este correo tiene el objetivo de agradecerle por su preferencia y comunicarle los detalles de su cita médica.
        <br>
        <strong>
            ::: Su cita está registrada para el ${date} a las ${time} :::
        </strong>
        <br>
        Detalles:
        <li> Modalidad: ${modality==2? "VIRTUAL":"PRESENCIAL"}</li>
        <li> Area de Atención: ${attentionArea}</li>
        <li> Doctor: ${doctor}</li>
        <li> Código de Asegurado: ${code}</li>
        <li> Fecha: ${date}</li>
        <li> Hora: ${time}</li>
        <li> Duración: 40 minutos.</li>
    </p>

    ${
    modality==2?
    `
    <li> Enlace: ${enlaces_meet[Math.floor(Math.random()*enlaces_meet.length)]}</li>
    `
    :
    `
    <li> Dirección: Av. Inca Garcilaso de la Vega 1420, Cercado de Lima 15001</li>
    <li> Piso: 2</li>
    <li> Google Maps:
        https://www.google.com/search?q=clinica%20lima&ei=MsALYdP2McfS1sQPouSwsAo&oq=clinica+lima&gs_lcp=Cgdnd3Mtd2l6EAMyEQguEIAEELEDEMcBEK8BEJMCMgoILhDHARCvARBDMgoILhDHARCvARBDMgQIABBDMgoILhDHARCvARBDMgsILhCABBDHARCvATIFCAAQgAQyCgguEMcBEK8BEEMyBQgAEIAEMgQIABBDOgcIABBHELADOg0ILhDHARCvARBDEJMCOhEILhCABBCxAxCDARDHARCvAToOCC4QgAQQsQMQxwEQrwFKBAhBGABQ4whYlAxgohBoAHAEeACAAZYDiAHdBpIBBzAuNC40LTGYAQCgAQHIAQjAAQE&sclient=gws-wiz&ved=2ahUKEwi8-rDt2JnyAhX2q5UCHUoICE4QvS4wAHoECB0QKg&uact=5&tbs=lf:1,lf_ui:2&tbm=lcl&rflfq=1&num=10&rldimm=9039619900020598529&lqi=CgxjbGluaWNhIGxpbWFI1NPB5eWAgIAIWhoQABgAGAEiDGNsaW5pY2EgbGltYSoECAMQAJIBDm1lZGljYWxfY2xpbmljmgEkQ2hkRFNVaE5NRzluUzBWSlEwRm5TVVJSTlhaTWNEWjNSUkFCqgEPEAEqCyIHY2xpbmljYSgO&rlst=f#rlfi=hd:;si:9039619900020598529,l,CgxjbGluaWNhIGxpbWFI1NPB5eWAgIAIWhoQABgAGAEiDGNsaW5pY2EgbGltYSoECAMQAJIBDm1lZGljYWxfY2xpbmljmgEkQ2hkRFNVaE5NRzluUzBWSlEwRm5TVVJSTlhaTWNEWjNSUkFCqgEPEAEqCyIHY2xpbmljYSgO;mv:[[-11.98801146848289,-76.92182392504883],[-12.217288893263106,-77.36333698657225]]
    </li>
    `
    }
    <p>
        Los sintomas especificados ya fueron enviados a su médico:
        <br>
        ${message}
    </p>
    <p>
        ¡Tenga un buen día!

    </p>

    Atte. SALUD G1.
        `,
    }

    console.log(mail);

    Email.send({
        ...mail
    })
        .then(function (message) {
            alert("El enlace a su cita médica ha sido enviada a su correo.")
        });
}