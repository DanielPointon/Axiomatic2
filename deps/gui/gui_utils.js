removeEventListeners = (node) => {
    //The "true" argument passed into cloneNode ensures child nodes are preserved
    newElement = node.cloneNode(true);
    node.parentNode.replaceChild(newElement, node);
}

renderLatex = (id, latex) => {
    katex.render(latex, document.getElementById(id), {
        throwOnError: false
    });
}


getCardAndBody = () => {
    card = document.createElement("div");
    card.className = "card";
    cardBody = document.createElement("div");
    cardBody.className = "card-body";
    card.appendChild(cardBody);
    return [card, cardBody]
}


getNextButton = (onClick) => {
    nextButton = document.createElement("button");
    nextButton.className = "btn btn-outline-success";
    nextButton.addEventListener("click", onClick);
    nextButton.innerText = "Next";
    return nextButton;
}

generateAlert = (message) => {
    const timeOut=1000
    document.getElementById("warning-alert").innerHTML = message;
    //Unhide the alert container
    document.getElementById("warning-alert-container").style.display = "";
    setTimeout(() => {
        //Hide the alert container
        document.getElementById("warning-alert-container").style.display = "none";
    }, timeOut); 
}
