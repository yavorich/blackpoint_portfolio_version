document.addEventListener("DOMContentLoaded", function () {
    const filterType = document.querySelector("#filter-type");
    const customPeriod = document.querySelector("#custom-period");

    if (filterType && customPeriod) {
        filterType.addEventListener("change", function () {
            if (filterType.value === "custom") {
                customPeriod.style.display = "block";
            } else {
                customPeriod.style.display = "none";
            }
        });

        // Показывать поля, если пользователь уже выбрал "Свой период"
        if (filterType.value === "custom") {
            customPeriod.style.display = "block";
        }
    }
});
