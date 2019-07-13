document.addEventListener('DOMContentLoaded', () => {

    // Configure pizza-confirmation-section
    document.querySelectorAll('.add-pizza').forEach(button => {
        button.onclick = () => {
            document.querySelector(`#pizza-type-${button.dataset.type}`).checked = true;
            document.querySelector(`#pizza-size-${button.dataset.size}`).checked = true;

            var sections = document.querySelectorAll('.menu-section');
            for (var section of sections) {
                section.style.display = 'none';
            }
            document.querySelector('#pizza-confirmation-section').style.display = 'block';
        };
    });

    document.querySelector('#pizza-confirmation-box-cancel').onclick = () => {
        var toppings = document.querySelectorAll('.pizza-topping');
        for (var topping of toppings) {
            topping.checked = false;
        }

        var sections = document.querySelectorAll('.menu-section');
        for (var section of sections) {
            section.style.display = 'block';
        }
        document.querySelector('#pizza-confirmation-section').style.display = 'none';
    };

    // Configure sub-confirmation-area
    document.querySelectorAll('.add-sub').forEach(button => {
        button.onclick = () => {
            let sizes = {
                'sm': 'Small',
                'lg': 'Large'
            }

            var sections = document.querySelectorAll('.menu-section');
            for (var section of sections) {
                section.style.display = 'none';
            }
            document.querySelector('#sub-confirmation-section').style.display = 'block';

            document.querySelector('#sub-size-text').innerHTML = `Size: ${sizes[button.dataset.size]}`;
            document.querySelector('#sub-type-text').innerHTML = `Type: ${button.dataset.name}`;

            // create invisible inputs to be read by server
            let subSize = document.createElement('input');
            subSize.name = 'sub-size';
            subSize.value = button.dataset.size;
            subSize.style.display = 'none';
            document.querySelector('#sub-details').append(subSize);
            let subType = document.createElement('input');
            subType.name = 'sub-type';
            subType.value = button.dataset.type;
            subType.style.display = 'none';
            document.querySelector('#sub-details').append(subType);


            document.querySelector(`#sub-topping-list-${button.dataset.size}`).style.display = 'block'
        };
    });

    document.querySelector('#sub-confirmation-box-cancel').onclick = () => {

        var addons = document.querySelectorAll('.sub-topping');
        for (var addon of addons) {
            addon.checked = false;
        }

        var addonAreas = document.querySelectorAll('.sub-topping-list');
        for (var addonArea of addonAreas) {
            addonArea.style.display = 'none';
        }

        var sections = document.querySelectorAll('.menu-section');
        for (var section of sections) {
            section.style.display = 'block';
        }
        document.querySelector('#sub-section').style.display = 'block';
        document.querySelector('#sub-confirmation-section').style.display = 'none';

    };
})
