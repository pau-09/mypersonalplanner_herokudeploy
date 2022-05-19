const edit_buttons = document.querySelectorAll('tbody>tr>td:nth-child(5)')
edit_buttons.forEach(button => button.addEventListener('click', editEntry))

const delete_buttons = document.querySelectorAll('tbody>tr>td:nth-child(6)')
delete_buttons.forEach(button => button.addEventListener('click', deleteEntry))

async function editEntry(e){
    const entry = e.currentTarget.id.split('-')
    const entry_id = entry[0]

    const { value: state } = await Swal.fire({
        title: alert_title,
        input: 'select',
        text: '', 
        inputOptions: alert_options,
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
                    resolve(`¡¡${alert_select_error} ${value.toLowerCase()}!!`)
                } else{
                    resolve()
                }
            })
        }
    })
    
    if (state) {
        const main = document.querySelector('main');

        const form = document.createElement('form');
        form.setAttribute('method','POST');
        form.setAttribute('action', document.location.href);
        main.appendChild(form);

        form.innerHTML = csrf_token;

        const book = document.createElement('input');
        book.setAttribute('type', 'hidden');
        book.setAttribute('value', entry_id);
        book.setAttribute('name', form_edit_input_name);
        form.appendChild(book);
        
        const new_state = document.createElement('input');
        new_state.setAttribute('type', 'hidden');
        new_state.setAttribute('value', state);
        new_state.setAttribute('name', 'new_state');
        form.appendChild(new_state);
        
        form.submit();
    }
}

async function deleteEntry(e){
    const entry = e.currentTarget.id.split('-')
    const entry_id = entry[0]
    const entry_title = entry[1]

    const { value: confirmed } = await Swal.fire({
        icon: 'warning',
        title: `¿Estás seguro?`,
        text: `'${entry_title}' quedará eliminado de tu lista.`,
        allowOutsideClick: false,
        color: '#A777A6',
        confirmButtonText: 'Si, quiero eliminarlo',
        confirmButtonColor: '#8368A7',
        showDenyButton: true,
        denyButtonText: 'Cancelar',
    })

    if (confirmed) {
        const main = document.querySelector('main');

        const form = document.createElement('form');
        form.setAttribute('method','POST');
        form.setAttribute('action',document.location.href);
        main.appendChild(form);

        form.innerHTML = csrf_token;

        const book = document.createElement('input');
        book.setAttribute('type', 'hidden');
        book.setAttribute('value', entry_id);
        book.setAttribute('name', 'delete_id');
        book.setAttribute('id', 'delete_id');
        form.appendChild(book);
        
        form.submit();
    }
}