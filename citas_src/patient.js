import MedicalApi from "./api.js"
import { filterBooksByName, getNameFromDNI } from './utils.js'

async function Patient() {

    const api = new MedicalApi();
    const dni = document.querySelector('#dni');
    const dni_error = document.querySelector("#dni-error")
    const content = document.querySelector('#content');
    // api.auth();

    dni.onchange = async (e) => {
        
        dni_error.innerText = "";
        
        const dni = e.target.value;
        const name = await getNameFromDNI(dni);

        if (!name){
            dni_error.innerText = "Ingrese un DNI valido, por favor.";
            return;
        }

        const data = await api.getBookings(name);

        const books = await Promise.all(data.map(
            async ({
                id,
                start_datetime, 
                end_datetime, 
                provider, 
                client, 
                service, 
                status, 
            }) => {
            
            const links = await api.getBookLink(id);
            
            return {
                id,
                start_datetime, 
                end_datetime, 
                provider: provider.name, 
                email: client.email, 
                service: service.name, 
                status,
                links,
            };
        }));
        
        console.log("Books");
        console.log(books);

        render(books);
    }
    

    const render = (books) => {

        content.innerHTML = books.map(book => `

            <li> Inicia: ${book.start_datetime} </li>
            <li> Finaliza: ${book.end_datetime} </li>
            <li> Area: ${book.provider} </li>
            <li> Email: ${book.email} </li>
            <li> Servicio: ${book.service} </li>
            <li> Estado: ${book.status} </li>
            <li> 
                <a class="btn btn-success" href=${book.links.booking_link}> Detalles </a> 
                <a class="btn btn-danger" href=${book.links.cancel_link}> Cancelar cita </a> 
                <a class="btn btn-warning" href=${book.links.reschedule_link}> Reprogramar </a> 
            </li>
        `
        );

    }
    

    
    // console.log({start_datetime, end_datetime, provider: provider.name, client: client.email, service: service.name, status, id});

    // const {booking_link} = await api.getBookLink(id);

    // console.log(booking_link);
}

Patient()