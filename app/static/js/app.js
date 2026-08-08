const searchForm = document.getElementById("customer-search-form");
const errorMessage = document.getElementById("error-message");
const customerResult = document.getElementById("customer-result");
console.log("APP.JS CARGADO");
// Loyal customers
const loadLoyalCustomersButton =
    document.getElementById("load-loyal-customers");

const loyalCustomersTableBody =
    document.getElementById("loyal-customers-table-body");

const loyalCustomersError =
    document.getElementById("loyal-customers-error");


// Search customer
searchForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const documentNumber = document
        .getElementById("document-number")
        .value
        .trim();
    
    console.log("Documento buscado:", documentNumber);

    hideError();
    customerResult.classList.add("d-none");

    let customer;

    // Get customer
    try {
        const response = await fetch(
            `/customers/${encodeURIComponent(documentNumber)}`
        );

        const data = await response.json();

        console.log("Respuesta API:", data);
        console.log("Status:", response.status);

        if (!response.ok) {
            throw new Error(
                data.message || "Customer not found"
            );
        }

        customer = data;
        console.log("Cliente antes de mostrar:", customer);
        displayCustomer(customer);
        console.log("displayCustomer ejecutado");
    } catch (error) {
        console.error("Error buscando cliente:", error);
        showError(error.message);
        return;
    }

    // Get customer purchases
    try {
        await loadPurchases(customer.id);

    } catch (error) {
        console.error("Error cargando compras:", error);
        showError(error.message);
    }
});


// Display customer information
function displayCustomer(customer) {
    document.getElementById("customer-document").textContent =
        `${customer.document_type} ${customer.document_number}`;

    document.getElementById("customer-name").textContent =
        `${customer.first_name} ${customer.last_name}`;

    document.getElementById("customer-email").textContent =
        customer.email;

    document.getElementById("customer-phone").textContent =
        customer.phone;

    customerResult.classList.remove("d-none");
}


// Load customer purchases
async function loadPurchases(customerId) {
    const response = await fetch(
        `/purchases/${customerId}/purchases`
    );

    const purchases = await response.json();

    if (!response.ok) {
        throw new Error(
            purchases.message || "Could not load purchases"
        );
    }

    displayPurchases(purchases);
}


// Display purchases
function displayPurchases(purchases) {
    const tableBody =
        document.getElementById("purchases-table-body");

    tableBody.innerHTML = "";

    if (purchases.length === 0) {
        tableBody.innerHTML = `
            <tr>
                <td colspan="3" class="text-center text-muted">
                    No purchases found
                </td>
            </tr>
        `;

        return;
    }

    purchases.forEach((purchase) => {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${purchase.purchase_date}</td>
            <td>${purchase.amount}</td>
            <td>${purchase.description || ""}</td>
        `;

        tableBody.appendChild(row);
    });
}


// Load loyal customers report
loadLoyalCustomersButton.addEventListener("click", async () => {
    hideLoyalCustomersError();

    try {
        const response = await fetch(
            "/reports/loyal-customers"
        );

        const report = await response.json();

        if (!response.ok) {
            throw new Error(
                report.message ||
                "Could not load loyal customers report"
            );
        }

        displayLoyalCustomers(report);

    } catch (error) {
        showLoyalCustomersError(error.message);
    }
});


// Display loyal customers report
function displayLoyalCustomers(report) {
    loyalCustomersTableBody.innerHTML = "";

    if (report.length === 0) {
        loyalCustomersTableBody.innerHTML = `
            <tr>
                <td colspan="6" class="text-center text-muted">
                    No loyal customers found
                </td>
            </tr>
        `;

        return;
    }

    report.forEach((customer) => {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${customer.document_type}</td>
            <td>${customer.document_number}</td>
            <td>
                ${customer.first_name} ${customer.last_name}
            </td>
            <td>${customer.email}</td>
            <td>${customer.phone}</td>
            <td>${formatCurrency(customer.total_amount)}</td>
        `;

        loyalCustomersTableBody.appendChild(row);
    });
}


// Format amounts as Colombian pesos
function formatCurrency(amount) {
    return new Intl.NumberFormat("es-CO", {
        style: "currency",
        currency: "COP",
        maximumFractionDigits: 0
    }).format(Number(amount));
}


// Customer search error
function showError(message) {
    errorMessage.textContent = message;
    errorMessage.classList.remove("d-none");
}


function hideError() {
    errorMessage.textContent = "";
    errorMessage.classList.add("d-none");
}


// Loyal customers report error
function showLoyalCustomersError(message) {
    loyalCustomersError.textContent = message;
    loyalCustomersError.classList.remove("d-none");
}


function hideLoyalCustomersError() {
    loyalCustomersError.textContent = "";
    loyalCustomersError.classList.add("d-none");
}