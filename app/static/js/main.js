document.addEventListener("DOMContentLoaded", () => {
const form = document.getElementById("quoteForm");

if(form){
form.addEventListener("submit", async (e) => {
e.preventDefault();

const data = {
fullName: document.getElementById("fullName").value,
phone: document.getElementById("phone").value,
email: document.getElementById("email").value
};

console.log(data);

document.getElementById("formMessage").innerText = "Submitted!";
});
}
});
