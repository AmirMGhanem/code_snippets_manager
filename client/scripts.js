const API_URL = "https://codesnippetsmanager-production.up.railway.app/snippets";
let codeEditor;

// Initialize CodeMirror when the page loads
document.addEventListener("DOMContentLoaded", function () {
    codeEditor = CodeMirror.fromTextArea(document.getElementById("snippetCode"), {
        mode: "javascript",
        lineNumbers: true,
        theme: "xq-dark",
        autoCloseBrackets: true
    });
});

// Fetch and display snippets
async function fetchSnippets() {
    const searchKeyword = document.getElementById("searchKeyword").value;
    const filterLanguage = document.getElementById("filterLanguage").value;
    const filterCreatedBy = document.getElementById("filterCreatedBy").value;

    let url = `${API_URL}?`;
    if (searchKeyword) url += `tag=${searchKeyword}&`;
    if (filterLanguage) url += `language=${filterLanguage}&`;
    if (filterCreatedBy) url += `created_by=${filterCreatedBy}`;

    const response = await fetch(url);
    const snippets = await response.json();
    displaySnippets(snippets);
}


async function deleteSnippet(id) {
    if (confirm("Are you sure you want to delete this snippet?")) {
        await fetch(`${API_URL}/${id}`, { method: "DELETE" });
        fetchSnippets();
    }
}



function displaySnippets(snippets) {
    const table = document.getElementById("snippetTable");
    table.innerHTML = "";

    snippets.forEach(snippet => {
        const decodedCode = decodeURIComponent(snippet.code); // Decode code before displaying
        table.innerHTML += `
            <tr>
                <td>${encodeHTML(snippet.title)}</td>
                <td>${encodeHTML(snippet.language)}</td>
                <td>${encodeHTML(snippet.tags)}</td>
                <td>${encodeHTML(snippet.created_by)}</td>
                <td>
                    <pre><code class="language-${encodeHTML(snippet.language.toLowerCase())}">${encodeHTML(decodedCode)}</code></pre>
                </td>
                <td>
                    <button class="btn btn-warning btn-sm" onclick="editSnippet(${snippet.id}, '${encodeHTML(snippet.title)}', '${encodeHTML(decodedCode)}', '${encodeHTML(snippet.language)}', '${encodeHTML(snippet.tags)}', '${encodeHTML(snippet.created_by)}')">
                        <i class="material-icons">edit</i>
                    </button>
                    <button class="btn btn-danger btn-sm" onclick="deleteSnippet(${snippet.id})">
                        <i class="material-icons">delete</i>
                    </button>
                </td>
            </tr>
        `;
    });

    Prism.highlightAll();  // Apply syntax highlighting
}

// Open and close modal
function openSnippetModal() {
    document.getElementById("snippetModal").style.display = "flex";
}
function closeSnippetModal() {
    document.getElementById("snippetModal").style.display = "none";
}


async function saveSnippet() {
    const id = document.getElementById("snippetId").value;
    const title = document.getElementById("snippetTitle").value;
    const code = encodeURIComponent(codeEditor.getValue());
    const language = document.getElementById("snippetLanguage").value;
    const tags = document.getElementById("snippetTags").value;
    const created_by = document.getElementById("snippetCreatedBy").value;

    const params = new URLSearchParams({ title, code, language, tags, created_by }).toString();
    let url = `${API_URL}?${params}`;

    if (id) {
        url = `${API_URL}/${id}?${params}`;
        await fetch(url, { method: "PUT" });
    } else {
        await fetch(url, { method: "POST" });
    }

    closeSnippetModal();
    fetchSnippets();
}


function updateCodeMirrorMode() {
    let language = document.getElementById("snippetLanguage").value;
    codeEditor.setOption("mode", language);
}


function formatCode() {
    let code = codeEditor.getValue();
    codeEditor.setValue(code);
}
// Function to encode HTML special characters to prevent injection
function encodeHTML(str) {
    return str.replace(/</g, "&lt;")
              .replace(/>/g, "&gt;")
              .replace(/"/g, "&quot;")
              .replace(/'/g, "&#39;")
              .replace(/&/g, "&amp;");
}


function editSnippet(id, title, code, language, tags, created_by) {
    document.getElementById("snippetId").value = id;
    document.getElementById("snippetTitle").value = title;
    codeEditor.setValue(code);
    document.getElementById("snippetLanguage").value = language;
    document.getElementById("snippetTags").value = tags;
    document.getElementById("snippetCreatedBy").value = created_by;

    openSnippetModal();
}
// Initial fetch
fetchSnippets();
