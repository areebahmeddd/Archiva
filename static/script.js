document.addEventListener("DOMContentLoaded", () => {
    const fileInput = document.getElementById("fileInput");
    const selectedFileContainer = document.getElementById("selectedFileContainer");
    let uploadedFiles = [];

    fileInput.addEventListener("change", updateFileInput);

    const updateFileInput = () => {
        const newFiles = fileInput.files;

        for (const file of newFiles) {
            if (!isFileAlreadyUploaded(file)) {
                uploadedFiles.push(file);
                const fileInputContainer = createFileInputContainer(file);
                selectedFileContainer.appendChild(fileInputContainer);
            }
        }
    };

    const isFileAlreadyUploaded = (newFile) => {
        return uploadedFiles.some((file) => file.name === newFile.name);
    };

    const createFileInputContainer = (file) => {
        const fileInputContainer = document.createElement("div");
        fileInputContainer.classList.add("d-flex", "justify-content-between", "align-items-center", "mb-2");
        fileInputContainer.innerHTML = `
            <div class="input-group">
                <span class="input-group-text"><i class="material-icons">description</i></span>
                <input type="text" class="form-control" value="${file.name}" readonly>
                <button type="button" class="btn btn-outline-danger btn-sm" data-file-name="${file.name}">X</button>
            </div>
        `;
        return fileInputContainer;
    };

    document.addEventListener("click", handleDocumentClick);

    const handleDocumentClick = (event) => {
        if (event.target.matches("[data-file-name]")) {
            handleFileRemoval(event.target);
        }
    };

    const handleFileRemoval = (target) => {
        const fileName = target.getAttribute("data-file-name");
        const fileContainer = target.closest(".d-flex");
        fileContainer.remove();

        uploadedFiles = uploadedFiles.filter((file) => file.name !== fileName);
    };
});