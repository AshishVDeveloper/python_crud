async function apiFetch(url, options = {}) {
    const accessToken = localStorage.getItem("access_token");

    options.headers = {
        ...options.headers,
        "Content-Type": "application/json"
    };

    if (accessToken) {
        options.headers["Authorization"] = `Bearer ${accessToken}`;
    }

    let response = await fetch(url, options);

    if (response.status === 401) {
        const refreshed = await refreshAccessToken();

        if (refreshed) {
            options.headers["Authorization"] =
                `Bearer ${localStorage.getItem("access_token")}`;

            response = await fetch(url, options);
        } else {
            logout();
        }
    }

    return response;
}

async function refreshAccessToken() {
    const refreshToken = localStorage.getItem("refresh_token");

    if (!refreshToken) {
        return false;
    }

    try {
        const response = await fetch("/api/token/refresh/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                refresh: refreshToken
            })
        });

        if (!response.ok) {
            return false;
        }

        const data = await response.json();

        localStorage.setItem(
            "access_token",
            data.access
        );

        return true;

    } catch (error) {
        return false;
    }
}

function logout() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");

    window.location.href = "/login/";
}