const uno = document.getElementById('primera')
const dos = document.getElementById('segunda')
const tres = document.getElementById('tercera')
const cuatro = document.getElementById('cuarta')
const cinco = document.getElementById('quinta')


const form = document.querySelector('.rate-form')
const confirmBox = document.getElementById('confirm-box')

const csrf = document.getElementsByName('csrfmiddlewaretoken')

const handleStarSelect = (size) => {
    const children = form.children
    for (let i=0; i < children.length; i++){
        if(i <= size){
            children[i].classList.add('checked')
        } else {
            children[i].classList.remove('checked')
        }
    }
}

const handleSelect = (selection) => {
    switch(selection){
        case 'primera':{
            // uno.classList.add('checked')
            // dos.classList.remove('checked')
            // tres.classList.remove('checked')
            // cuatro.classList.remove('checked')
            // cinco.classList.remove('checked')
            handleStarSelect(1)
            return
        }
        case 'segunda':{
            // uno.classList.add('checked')
            // dos.classList.add('checked')
            // tres.classList.remove('checked')
            // cuatro.classList.remove('checked')
            // cinco.classList.remove('checked')
            handleStarSelect(2)
            return
        }
        case 'tercera':{
            // uno.classList.add('checked')
            // dos.classList.add('checked')
            // tres.classList.add('checked')
            // cuatro.classList.remove('checked')
            // cinco.classList.remove('checked')
            handleStarSelect(3)
            return
        }
        case 'cuarta':{
            // uno.classList.add('checked')
            // dos.classList.add('checked')
            // tres.classList.add('checked')
            // cuatro.classList.add('checked')
            // cinco.classList.remove('checked')
            handleStarSelect(4)
            return
        }
        case 'quinta':{
            // uno.classList.add('checked')
            // dos.classList.add('checked')
            // tres.classList.add('checked')
            // cuatro.classList.add('checked')
            // cinco.classList.add('checked')
            handleStarSelect(5)
            return
        }
    }
        
}

const getNumericValue = (stringValue) => {
    let numericValue;
    if(stringValue === 'primera') {
        numericValue = 1
    } else if (stringValue === 'segunda'){
        numericValue = 2
    }  else if (stringValue === 'tercera'){
        numericValue = 3
    }  else if (stringValue === 'cuarta'){
        numericValue = 4
    }  else if (stringValue === 'quinta'){
        numericValue = 5
    } else {
        numericValue = 0
    }
    return numericValue
}

const obtieneEstrellasExistentes = (numericValue) => {
    switch(numericValue){
        case 1: return 'primera';
        case 2: return 'segunda';
        case 3: return 'tercera';
        case 4: return 'cuarta';
        case 5: return 'quinta';
        default: return null;
    }
}

if (uno){
    const arr = [uno, dos, tres, cuatro, cinco]

    const puntuacionInicial = form ? parseInt(form.getAttribute('data-initial-rating')) : 0;

    if (puntuacionInicial && puntuacionInicial > 0) {
        handleStarSelect(puntuacionInicial);
    }
    let seleccionActual = puntuacionInicial;

    arr.forEach(item =>item.addEventListener('mouseover',(event)=>{
        handleSelect(event.target.id)
    }))

    form.addEventListener('mouseout', () => {
        if (seleccionActual > 0) {
            handleStarSelect(seleccionActual);
        } else {
            handleStarSelect(0);
        }
    });

    arr.forEach(item => item.addEventListener('click', (event)=>{
        event.preventDefault()
        
        const estrellaClickeada = event.target.id 
        const val_num = getNumericValue(estrellaClickeada)
        const rateUrl = form ? form.getAttribute('data-rate-url') : null;
        
        seleccionActual = val_num;
        handleStarSelect(val_num);
        
        $.ajax({
            type: 'POST',
            url: rateUrl,
            data: {
                'csrfmiddlewaretoken': csrf[0].value,
                'val': val_num,
            },
            success: function(response) {
                if (response.success) {
                    console.log(`Puntuación de ${val_num} enviada. Nuevo promedio: ${response.promedio_estrellas}`);
                    
                    const promedioDisplay = document.querySelector('.ms-3 h4');
                    if (promedioDisplay) {
                        const nuevoPromedio = response.promedio_estrellas !== null 
                                            ? response.promedio_estrellas 
                                            : '-';
                                            
                        promedioDisplay.innerHTML = `${nuevoPromedio} <small class="text-muted">/ 5</small>`;
                    }
                } else {
                    console.error("Error del servidor:", response.error);
                }
            },
            error: function(xhr, status, error) {
                console.error("Error AJAX:", error);
            }
        })
    }))
}
