document.addEventListener("DOMContentLoaded", function() {
    const container = document.getElementById('new_vehicles_container');
    let newVehicleCount = parseInt(container.dataset.existing) || 0;

    const addBtn = document.getElementById('addVehicleBtn');
    const hiddenCountInput = document.getElementById('new_vehicle_count');

    addBtn.addEventListener('click', function () {
        newVehicleCount++;
        hiddenCountInput.value = newVehicleCount;

        const div = document.createElement('div');
        div.classList.add('vehicle-block');

        div.innerHTML = `
            <h4>New Vehicle #${newVehicleCount}</h4>
            <div class="inp">
                <label>Vehicle Type</label>
                <select name="new_vehicle_type_${newVehicleCount}" required>
                    <option value="bike">Bike</option>
                    <option value="scooter">Scooter</option>
                    <option value="car">Car</option>
                    <option value="other">Other</option>
                </select>
            </div>
            <div class="inp"><label>Brand</label>
                <input type="text" name="new_vehicle_brand_${newVehicleCount}" required></div>
            <div class="inp"><label>Model</label>
                <input type="text" name="new_vehicle_model_${newVehicleCount}" required></div>
            <div class="inp"><label>Year</label>
                <input type="number" name="new_vehicle_year_${newVehicleCount}" min="1900" max="2100"></div>
            <div class="inp"><label>Reg No.</label>
                <input type="text" name="new_vehicle_reg_${newVehicleCount}"></div>
        `;

        container.appendChild(div);
        div.scrollIntoView({ behavior: 'smooth' });
    });
});
