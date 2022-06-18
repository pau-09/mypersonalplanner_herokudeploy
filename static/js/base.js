document.addEventListener('DOMContentLoaded', setup)

function setup(e){
    document.querySelector('#menu_label').addEventListener('click', toggleMenu)
    try{
        const el = document.querySelectorAll('li > a');
        const url = document.location.href;
        el.forEach((a)=>{
            if (url==a.href){
                a.className = 'act';
            }
        })
    }catch(e){
        console.error(e)
    }
}

function toggleMenu(e){
    const menu = document.querySelector('nav');
    const checkbox = document.querySelector('#menu_checkbox');
    
    if(checkbox.checked){
        menu.style.display = 'none'
    }else{
        menu.style.display = 'initial'
    }
}