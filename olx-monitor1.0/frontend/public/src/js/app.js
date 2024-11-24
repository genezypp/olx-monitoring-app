document.getElementById("login-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    try {
        const response = await fetch("/token", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ username, password }),
        });

        const result = await response.json();

        if (response.ok) {
            document.getElementById("login-section").style.display = "none";
            document.getElementById("dashboard-section").style.display = "block";
            document.getElementById("response-message").innerHTML = "";
            fetchProfiles();
        } else {
            document.getElementById("response-message").innerHTML =
                `<div class="alert alert-danger">Error: ${result.detail}</div>`;
        }
    } catch (error) {
        document.getElementById("response-message").innerHTML =
            `<div class="alert alert-danger">Connection error: ${error.message}</div>`;
    }
});

async function fetchProfiles() {
    const response = await fetch("/profiles");
    const profiles = await response.json();
    const profilesList = document.getElementById("profiles-list");
    profilesList.innerHTML = "";
    profiles.forEach(profile => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${profile.id}</td>
            <td>${profile.name}</td>
            <td>${profile.keyword || "-"}</td>
            <td>${profile.min_price || "-"}</td>
            <td>${profile.max_price || "-"}</td>
            <td>${profile.location || "-"}</td>
            <td>${profile.category || "-"}</td>
            <td>
                <button class="btn btn-danger" onclick="deleteProfile(${profile.id})">Delete</button>
            </td>
        `;
        profilesList.appendChild(row);
    });
}

async function addProfile(e) {
    e.preventDefault();
    const name = document.getElementById("profile-name").value;
    const keyword = document.getElementById("profile-keyword").value;
    const minPrice = document.getElementById("profile-min-price").value;
    const maxPrice = document.getElementById("profile-max-price").value;
    const location = document.getElementById("profile-location").value;
    const category = document.getElementById("profile-category").value;

    const response = await fetch("/profiles", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            id: Date.now(),
            name,
            keyword,
            min_price: minPrice ? parseFloat(minPrice) : null,
            max_price: maxPrice ? parseFloat(maxPrice) : null,
            location,
            category,
        }),
    });

    if (response.ok) {
        document.getElementById("add-profile-form").reset();
        fetchProfiles();
    }
}

async function deleteProfile(profileId) {
    const response = await fetch(`/profiles/${profileId}`, {
        method: "DELETE",
    });
    if (response.ok) {
        fetchProfiles();
    }
}

document.getElementById("add-profile-form").addEventListener("submit", addProfile);
