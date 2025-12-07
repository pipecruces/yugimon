const mazoSelect1 = document.getElementById('mazo-select-1'); 
const mazoSelect2 = document.getElementById('mazo-select-2'); 
const cardBody1 = document.getElementById('card-body-1'); 
const cardBody2 = document.getElementById('card-body-2'); 
const comparacionStatsBody = document.getElementById('comparacion-stats-body'); 
const deck1Name = document.getElementById('deck-1-name'); 
const deck2Name = document.getElementById('deck-2-name'); 
const cardModalDetails = document.getElementById('cardModalDetails');
const cardModalImage = document.getElementById('cardModalImage');

let deck1Data = null; 
let deck2Data = null; 

const cardModalElement = document.getElementById('cardModal');
if (cardModalElement) {
    cardModalElement.addEventListener('show.bs.modal', function (event) {
        const triggerElement = event.relatedTarget; 
        
        const imageUrl = triggerElement.getAttribute('data-image-url');
        const cardName = triggerElement.getAttribute('data-card-name');

        const habilidad = triggerElement.getAttribute('data-habilidad');
        const fuerza = triggerElement.getAttribute('data-fuerza');
        const coste = triggerElement.getAttribute('data-coste');
        const raza = triggerElement.getAttribute('data-raza');
        const edicion = triggerElement.getAttribute('data-edicion');
        const tipo = triggerElement.getAttribute('data-tipo');
        
        if (cardModalImage && imageUrl) {
            cardModalImage.src = imageUrl;
            cardModalImage.alt = cardName || 'Ilustración de Carta';
        }
        
        const modalTitle = document.getElementById('cardModalLabel');
        if (modalTitle) {
             modalTitle.textContent = cardName || 'Ilustración de Carta';
        }

        if (cardModalDetails) {
            cardModalDetails.innerHTML = `
                <p><strong>Habilidad:</strong> ${habilidad}</p>
                <p><strong>Fuerza:</strong> ${fuerza}</p>
                <p><strong>Coste:</strong> ${coste}</p>
                <p><strong>Raza:</strong> ${raza}</p>
                <p><strong>Tipo:</strong> ${tipo}</p>
                <p><strong>Edición:</strong> ${edicion}</p>

            `;
        }

    });
}

async function fetchDeckData(mazoId) { 
    if (!mazoId) return null; 
    try { 
        const url = `/comparador/datos_mazo/${mazoId}/`;
        const response = await fetch(url); 
        if (!response.ok) { 
            throw new Error('Error al cargar los datos del mazo.'); 
        } 
        return await response.json(); 
    } catch (error) { 
        console.error("Error al obtener datos:", error); 
        return null; 
    } 
} 

function renderCardList(data, container) { 
    if (!data || data.cartas.length === 0) { 
        container.innerHTML = '<p class="text-danger">Mazo sin cartas o no seleccionado.</p>'; 
        return; 
    } 
 
    let html = `<div class="row">`;
    data.cartas.forEach(carta => {
        html += 
        `<div class="col-6 mb-3 text-center">
            <div>
            <a href="#" class="card-modal-trigger" 
               data-bs-toggle="modal" 
               data-bs-target="#cardModal" 
               data-image-url="${carta.ilustracion}" 
               data-card-name="${carta.nombre}"
               data-habilidad="${carta.habilidad}"
               data-fuerza="${carta.fuerza}"
               data-coste="${carta.coste}"
               data-raza="${carta.raza}"
               data-edicion="${carta.edicion}"
               data-tipo="${carta.tipo}">
                <img src="${carta.ilustracion}" alt="${carta.nombre}" style="width: 100px">
            </a>
            </div>
            <b>${carta.nombre}</b>
            </div>`;
    }); 
    html += `</div>`; 
    container.innerHTML = html; 
} 

function renderComparisonTable() { 
    if (!deck1Data || !deck2Data) { 
        comparacionStatsBody.innerHTML = '<tr><td colspan="3" class="text-center">Selecciona ambos mazos para comparar.</td></tr>'; 
        deck1Name.textContent = 'Mazo 1'; 
        deck2Name.textContent = 'Mazo 2'; 
        return; 
    } 

    deck1Name.textContent = deck1Data.stats.Nombre; 
    deck2Name.textContent = deck2Data.stats.Nombre; 

    const stats1 = deck1Data.stats; 
    const stats2 = deck2Data.stats; 
    let html = ''; 

    const statKeys = [ 
        'Total de Cartas',  
        'Coste Total',  
        'Fuerza Total',  
        'Coste Promedio',  
        'Fuerza Promedio',
        'Puntuación Promedio'
    ]; 

    statKeys.forEach(key => { 
        const val1 = stats1[key]; 
        const val2 = stats2[key]; 
        
        let class1 = ''; 
        let class2 = ''; 
        
        const isCostStat = key.includes('Coste');
        const isScoreStat = key.includes('Puntuación');

        // Resalta la mejor estadistica
        if (isCostStat) {
            if (val1 < val2) {
                class1 = 'bg-success text-white fw-bold';
            } else if (val2 < val1) {
                class2 = 'bg-success text-white fw-bold';
            }
        } else if (isScoreStat) {
            if (val1 > val2) {
                class1 = 'bg-success text-white fw-bold';
            } else if (val2 > val1) {
                class2 = 'bg-success text-white fw-bold';
            }
        } else {
            if (val1 > val2) {
                class1 = 'bg-success text-white fw-bold';
            } else if (val2 > val1) {
                class2 = 'bg-success text-white fw-bold';
            }
        }

        html += ` 
            <tr> 
                <td class="${class1}">${val1}</td> 
                <td>${key}</td> 
                <td class="${class2}">${val2}</td> 
            </tr> 
        `; 
    }); 

    comparacionStatsBody.innerHTML = html; 
} 

mazoSelect1.addEventListener('change', async (e) => { 
    const mazoId = e.target.value; 

    cardBody1.innerHTML = '<div class="text-center"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">Cargando...</span></div></div>';
 
    if (mazoId) { 
        deck1Data = await fetchDeckData(mazoId); 
        renderCardList(deck1Data, cardBody1); 
    } else { 
        deck1Data = null; 
        cardBody1.innerHTML = '<p>Selecciona un mazo para ver las cartas.</p>'; 
    } 
     
    renderComparisonTable(); 
}); 

mazoSelect2.addEventListener('change', async (e) => { 
    const mazoId = e.target.value; 

    cardBody2.innerHTML = '<div class="text-center"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">Cargando...</span></div></div>';
 
    if (mazoId) { 
        deck2Data = await fetchDeckData(mazoId); 
        renderCardList(deck2Data, cardBody2); 
    } else { 
        deck2Data = null; 
        cardBody2.innerHTML = '<p>Selecciona un mazo para ver las cartas.</p>'; 
    } 

    renderComparisonTable(); 
});