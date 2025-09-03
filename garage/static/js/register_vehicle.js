document.addEventListener("DOMContentLoaded", () => {
    const twoWheelersInput = document.getElementById("two_wheelers");
    const fourWheelersInput = document.getElementById("four_wheelers");
    const twoWheelerDiv = document.getElementById("two-wheeler-details");
    const fourWheelerDiv = document.getElementById("four-wheeler-details");

    function generateVehicleFields(count, container, type) {
        container.innerHTML = ""; // Clear previous fields
        for (let i = 1; i <= count; i++) {
            const fieldset = document.createElement("fieldset");
            const legend = document.createElement("legend");
            legend.textContent = `${type} ${i} Details`;
            fieldset.appendChild(legend);

            // Vehicle Brand
            const labelBrand = document.createElement("label");
            labelBrand.setAttribute("for", `${type.toLowerCase()}_brand_${i}`);
            labelBrand.textContent = "Brand";
            const inputBrand = document.createElement("input");
            inputBrand.type = "text";
            inputBrand.name = `${type.toLowerCase()}_brand_${i}`;
            inputBrand.id = `${type.toLowerCase()}_brand_${i}`;
            fieldset.appendChild(labelBrand);
            fieldset.appendChild(inputBrand);

            // Vehicle Model
            const labelModel = document.createElement("label");
            labelModel.setAttribute("for", `${type.toLowerCase()}_model_${i}`);
            labelModel.textContent = "Model";
            const inputModel = document.createElement("input");
            inputModel.type = "text";
            inputModel.name = `${type.toLowerCase()}_model_${i}`;
            inputModel.id = `${type.toLowerCase()}_model_${i}`;
            fieldset.appendChild(labelModel);
            fieldset.appendChild(inputModel);

            // Vehicle Year of Manufacture
            const labelYear = document.createElement("label");
            labelYear.setAttribute("for", `${type.toLowerCase()}_year_${i}`);
            labelYear.textContent = "Year of Manufacture";
            const inputYear = document.createElement("input");
            inputYear.type = "number";
            inputYear.name = `${type.toLowerCase()}_year_${i}`;
            inputYear.id = `${type.toLowerCase()}_year_${i}`;
            inputYear.min = 1900;
            inputYear.max = new Date().getFullYear();
            fieldset.appendChild(labelYear);
            fieldset.appendChild(inputYear);

            // Vehicle Registration Number
            const labelReg = document.createElement("label");
            labelReg.setAttribute("for", `${type.toLowerCase()}_reg_${i}`);
            labelReg.textContent = "Registration Number";
            const inputReg = document.createElement("input");
            inputReg.type = "text";
            inputReg.name = `${type.toLowerCase()}_reg_${i}`;
            inputReg.id = `${type.toLowerCase()}_reg_${i}`;
            fieldset.appendChild(labelReg);
            fieldset.appendChild(inputReg);

            container.appendChild(fieldset);
        }
    }

    twoWheelersInput.addEventListener("input", () => {
        generateVehicleFields(parseInt(twoWheelersInput.value) || 0, twoWheelerDiv, "Two-Wheeler");
    });

    fourWheelersInput.addEventListener("input", () => {
        generateVehicleFields(parseInt(fourWheelersInput.value) || 0, fourWheelerDiv, "Four-Wheeler");
    });

    // Initialize fields if page reloads with POST data
    if (twoWheelersInput.value) generateVehicleFields(parseInt(twoWheelersInput.value), twoWheelerDiv, "Two-Wheeler");
    if (fourWheelersInput.value) generateVehicleFields(parseInt(fourWheelersInput.value), fourWheelerDiv, "Four-Wheeler");
});
