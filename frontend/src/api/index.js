export function callApi(endpoint, query, body) {
    const baseUrl = "http://127.0.0.1:8000/api";
    const headers = new Headers();
    headers.append("accept", "application/json");
    headers.append("Content-Type", "application/json");
    let queryString = "";
    if (typeof query === "object" && Object.keys(query).length > 0) {
        queryString+="?";
        let queries = [];
        Object.keys(query).forEach(key => {
            queries.push(`${key}=${JSON.stringify(query[key])}`);
        });
        queryString+=queries.join('&');
    }
    console.log(baseUrl, endpoint, queryString, `${baseUrl}/${endpoint}${queryString}`);
    return fetch(`${baseUrl}/${endpoint}${queryString}`, {
        method: 'POST',
        body: JSON.stringify(body),
        headers,
        redirect: "follow"
    });
}