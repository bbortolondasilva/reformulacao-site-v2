const form = document.getElementById("formContato");
const feedback = document.getElementById("feedback");

form.addEventListener("submit", function (event) {
    event.preventDefault();

    emailjs.sendForm(
        "service_5rt5j8w",
        "template_6u3y92j",
        form
    )
    .then(() => {

        feedback.classList.remove("d-none");
        feedback.className = "alert alert-success mt-3";
        feedback.innerHTML = "<strong>✓ Sucesso!</strong> Sua mensagem foi enviada com sucesso.";

        form.reset();

    })
    .catch((error) => {

        console.error(error);

        feedback.classList.remove("d-none");
        feedback.className = "alert alert-danger mt-3";
        feedback.innerHTML = "<strong>✕ Erro!</strong> Não foi possível enviar a mensagem.";

    });
});
