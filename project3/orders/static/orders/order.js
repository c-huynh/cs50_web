document.addEventListener('DOMContentLoaded', () => {

    // Configure pizza-confirmation-box
    document.querySelectorAll('.add-pizza').forEach(button => {
        button.onclick = () => {
            document.querySelector(`#pizza-type-${button.dataset.type}`).checked = true;
            document.querySelector(`#pizza-size-${button.dataset.size}`).checked = true;
            document.querySelector('#pizza-confirmation-box').style.display = 'flex';
        };
    });

    document.querySelector('#pizza-confirmation-box-cancel').onclick = () => {
        let toppings = document.querySelectorAll('.pizza-topping');
        for (var i = 0; i < toppings.length; i++) {
            toppings[i].checked = false;
        }
        document.querySelector('#pizza-confirmation-box').style.display = 'none';
    };

    // document.querySelector('#pizza-confirmation-box-confirm').onclick = () => {
    //     let selectedToppings = [];
    //     let toppings = document.querySelectorAll('.pizza-topping');
    //     for (var i = 0; i < toppings.length; i++) {
    //         if (toppings[i].checked === true) {
    //             selectedToppings.push(toppings[i].value)
    //         }
    //     }
    //     console.log(selectedToppings);
    // };
})
