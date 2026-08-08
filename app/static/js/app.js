const searchForm = document.getElementById("customer-search-form");
const errorMessage = document.getElementById("error-message");
const customerResult = document.getElementById("customer-result");


searchForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const documentNumber = document
        .getElementById("document-number")
        .value
        .trim();

    hideError();
    customerResult.classList.add("d-none");

    try {
        const response = await fetch(
            `/customers/${encodeURIComponent(documentNumber)}`
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.message || "Customer not found"
            );
        }

        displayCustomer(data);

        await loadPurchases(data.id);

    } catch (error) {
        showError(error.message);
    }
});


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


function showError(message) {
    errorMessage.textContent = message;
    errorMessage.classList.remove("d-none");
}


function hideError() {
    errorMessage.textContent = "";
    errorMessage.classList.add("d-none");
}