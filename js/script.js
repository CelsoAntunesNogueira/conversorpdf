document.getElementById("uploadForm").addEventListener("submit", async function(event) {
    event.preventDefault();

    let formData = new FormData();
    let fileInput = document.getElementById("file");  // Corrigido!

    if (fileInput.files.length === 0) {
        alert("Selecione um arquivo DOCX!");
        return;
    }

    formData.append("file", fileInput.files[0]);

    try {
        let response = await fetch("/upload", {
            method: "POST",
            body: formData
        });

        if (!response.ok) throw new Error("Erro na conversão!");

        let blob = await response.blob();
        let url = window.URL.createObjectURL(blob);
        let a = document.createElement("a");
        a.href = url;
        a.download = "documento_convertido.pdf";
        document.body.appendChild(a);
        a.click();
        a.remove();
    } catch (error) {
        console.error(error);
        alert("Erro ao converter o arquivo");
    }
});
