const add_button = document.querySelector('thead>tr>th:nth-child(6)')
add_button.addEventListener('click', addEntry)

const edit_buttons = document.querySelectorAll('tbody>tr>td:nth-child(6)')
edit_buttons.forEach(button => button.addEventListener('click', editEntry))

const delete_buttons = document.querySelectorAll('tbody>tr>td:nth-child(7)')
delete_buttons.forEach(button => button.addEventListener('click', deleteEntry))

const table_columns = Array.from(document.querySelectorAll('thead>tr>th')).slice(0, 5)
table_columns.forEach(button => button.addEventListener('click', orderBy))

async function addEntry(e){
    const steps = ['Titulo del libro', 'Estado del libro']
    const swalQueueStep = Swal.mixin({
        confirmButtonText: 'Siguiente',
        cancelButtonText: 'Volver',
        showDenyButton: true, 
        denyButtonText: 'Cancelar',
        progressSteps: ['1', '2'],
        input: 'select',
        reverseButtons: true,
    })
    
    const values = []
    let currentStep
    
    for (currentStep = 0; currentStep < steps.length;) {
        if(currentStep == 0){
            input_options = add_alert_options;
        }else if(currentStep == 1){
            input_options = state_options;
        }

        const result = await swalQueueStep.fire({
          title: `${steps[currentStep]}`,
          inputOptions: input_options,
          showCancelButton: currentStep > 0,
          currentProgressStep: currentStep
        })
      
        if (result.value) {
          values[currentStep] = result.value
          currentStep++
        } else if (result.dismiss === Swal.DismissReason.cancel) {
          currentStep--
        } else {
          break
        }
    }
    
    if (currentStep === steps.length) {
        const main = document.querySelector('main');
    
        const form = document.createElement('form');
        form.setAttribute('method','POST');
        form.setAttribute('action', document.location.href);
        main.appendChild(form);

        form.innerHTML = csrf_token;

        const entry = document.createElement('input');
        entry.setAttribute('type', 'hidden');
        entry.setAttribute('value',values[0]);
        entry.setAttribute('name', form_add_input_name);
        form.appendChild(entry);
        
        const state = document.createElement('input');
        state.setAttribute('type', 'hidden');
        state.setAttribute('value', values[1]);
        state.setAttribute('name', 'state');
        form.appendChild(state);
        
        form.submit();
    }
}

async function editEntry(e){
    const entry_id = e.currentTarget.id

     Swal.fire({
        title: edit_alert_title,
        input: 'select',
        inputOptions: state_options,
        allowOutsideClick: false,
        color: '#A777A6',
        confirmButtonText: 'Cambiar',
        confirmButtonColor: '#8368A7',
        showDenyButton: true,
        denyButtonText: 'Cancelar',
        inputPlaceholder: 'Selecciona un estado',
        inputValidator: (value) => {
            return new Promise((resolve) => {
                if (value === entry_state){
                    resolve(`¡¡${edit_alert_error} ${value.toLowerCase()}!!`)
                } else{
                    resolve()
                }
            })
        }
    }).then((result) => {
        if (result.isConfirmed) {
            const main = document.querySelector('main');
    
            const form = document.createElement('form');
            form.setAttribute('method','POST');
            form.setAttribute('action', document.location.href);
            form.innerHTML = csrf_token;
            main.appendChild(form);
    
            const entry = document.createElement('input');
            entry.setAttribute('type', 'hidden');
            entry.setAttribute('value', entry_id);
            entry.setAttribute('name', form_edit_input_name);
            form.appendChild(entry);
            
            const new_state = document.createElement('input');
            new_state.setAttribute('type', 'hidden');
            new_state.setAttribute('value', result.value);
            new_state.setAttribute('name', 'new_state');
            form.appendChild(new_state);
            
            form.submit();
        }
    })
    
}

async function deleteEntry(e){
    const entry_id = e.currentTarget.id
    const entry_title = e.currentTarget.dataset.title

    Swal.fire({
        icon: 'warning',
        title: `¿Estás seguro?`,
        text: `'${entry_title}' quedará eliminado de tu lista.`,
        allowOutsideClick: false,
        color: '#A777A6',
        confirmButtonText: 'Si, quiero eliminarlo',
        confirmButtonColor: '#8368A7',
        showDenyButton: true,
        denyButtonText: 'Cancelar',
    }).then((result) => {
        if (result.isConfirmed) {
            const main = document.querySelector('main');
    
            const form = document.createElement('form');
            form.setAttribute('method','POST');
            form.setAttribute('action',document.location.href);
            form.innerHTML = csrf_token;
            main.appendChild(form);
    
            const entry = document.createElement('input');
            entry.setAttribute('type', 'hidden');
            entry.setAttribute('value', entry_id);
            entry.setAttribute('name', 'delete_id');
            entry.setAttribute('id', 'delete_id');
            form.appendChild(entry);
            
            form.submit();
        }
    })

}

function orderBy(e){
    const main = document.querySelector('main');
    
    const form = document.createElement('form');
    form.setAttribute('method','POST');
    form.setAttribute('action', document.location.href);
    form.innerHTML = csrf_token;
    main.appendChild(form);

    const entry = document.createElement('input');
    entry.setAttribute('type', 'hidden');
    entry.setAttribute('value', e.target.id);
    entry.setAttribute('name', 'order_by');
    form.appendChild(entry);
    
    form.submit();
}