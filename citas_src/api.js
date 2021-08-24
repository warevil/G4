/* Create file pwd.js and set your password in variable named PWD */

import { COMPANY_LOGIN, API_KEY, PWD } from "./config.js";

export default class MecicalApi{

    constructor() {

    }
    
    async auth() {

        await fetch("https://user-api-v2.simplybook.me/admin/auth", {
            method: 'POST',
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                "company": COMPANY_LOGIN,
                "login": "admin",
                "password": PWD,
            })
        })
        .then(r => r.json())
        .then(d => this.token = d.token);

    }

    async auth() {

        await fetch("https://user-api-v2.simplybook.me/admin/auth", {
            method: 'POST',
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                "company": COMPANY_LOGIN,
                "login": "admin",
                "password": PWD,
            })
        })
        .then(r => r.json())
        .then(d => this.token = d.token);
        
    }
    
    async getBookings(name){
        
        await this.auth(); // TODO mejorar control

        let books;

        await fetch(`https://user-api-v2.simplybook.me/admin/bookings?filter[status]=confirmed&filter[search]=${name}`, {
            method: 'GET',
            headers: {
                "Content-Type": "application/json",
                "X-Company-Login": COMPANY_LOGIN,
                "X-Token": this.token,
            },
        })
        .then(r => r.json())
        .then(d => books = d);

        return books.data;
    }

    async getBookLink(id){

        let links;

        await fetch(`https://user-api-v2.simplybook.me/admin/bookings/${id}/links`, {
            method: 'GET',
            headers: {
                "Content-Type": "application/json",
                "X-Company-Login": COMPANY_LOGIN,
                "X-Token": this.token,
            },
        })
        .then(r => r.json())
        .then(d => links = d);

        return links
    }
}



