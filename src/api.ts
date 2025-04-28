const API_URL = import.meta.env.VITE_HTTP_URL;

const apiBase = async (url: string, body: object) => {
    const response = await fetch(`${API_URL}` + `${url}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(body)
    });
    if (!response.ok) {
        console.log(response);
        throw new Error("Error on response parsing");
    }

    return response.json();
};

export const loginUser = async (username: string, password: string) => {
    return await apiBase("/login", {username, password});
};

export const registerUser = async (username: string, password: string) => {
    return await apiBase("/register", {username, password});
};
