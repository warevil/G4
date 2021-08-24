// UTILS

export function isNumeric(str) {
    if (typeof str != "string") return false // we only process strings!  
    return !isNaN(str) && // use type coercion to parse the _entirety_ of the string (`parseFloat` alone does not do this)...
           !isNaN(parseFloat(str)) // ...and ensure strings of whitespace fail
}

export async function getNameFromDNI(dni) {
    
    if (!isNumeric(dni)){
        return false;
    }

    const URL =`https://dniruc.apisperu.com/api/v1/dni/${dni}?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6InlpaHNpY0BnbWFpbC5jb20ifQ.JtcQWJs0oWX1bFMoxtfIDwooMXcbqeRBKTJADq7-p5Y`
    
    let data;
    let error = false;
    
    await fetch(URL)
        .then(r => r.json())
        .then(d => data = d)
        .catch(err => error = true);
    
    if (error || !data.nombres){
        console.log("DNI API Fail")
        return false;
    }

    const DNIName = `${data.nombres}, ${data.apellidoPaterno} ${data.apellidoMaterno}`;
    
    console.log({DNIName});
    
    return DNIName;
}

export function filterBooksByName(books, name){
    console.log(books);
    return books.filter(({client}) => client.name==name);
}