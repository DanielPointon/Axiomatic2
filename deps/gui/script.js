hideAll = () => {
    ids = ["input-box", "result-box", "variable-select-box", "alternatives-box", "terminal-container"];
    ids.forEach(id => {
        if (document.getElementById(id)) {
            document.getElementById(id).style.display = "none";
        }
    });
}

renderResult = (result, id) => {
    generateImage("Result:", "result", result);
    //Old event listeners need to be cleared every time we change button text
    //To avoid multiple PDFs/Videos being rendered when the user has requested one
    replaceWithClickListener = (elementId, listener) => {
        element = document.getElementById(elementId);
        newElement = element.cloneNode(true);
        newElement.addEventListener("click", listener);
        element.parentNode.replaceChild(newElement, element);
    }
    replaceWithClickListener("video-maker", async () => {
        await getVideo(id);
    });
    replaceWithClickListener("pdf-maker", async () => {
        await getPDF(id);
    });
}



generateImage = (title, prefix, latex) => {
    renderLatex(prefix + "-image", latex);
    document.getElementById(prefix + "-box").style.display = "";
    document.getElementById(prefix + "-caption").innerText = title;
    document.getElementById(prefix + "-image-box").style.display = "";
}

displayInput = (parsedAndReTexed) => {
    document.getElementById("result-box").style.display = "none";
    generateImage("You entered:", "input", parsedAndReTexed);
}



getVideo = async (identifier) => {
    await sendPacket({ 'task': 'video', 'updateType': 'firstUpdate', 'solutionSessionID': identifier })
}

getPDF = async (identifier) => {
    await sendPacket({ 'task': 'pdf', 'updateType': 'firstUpdate', 'solutionSessionID': identifier })
}

//Applies default input attributes to the input
configureInput = (inputElement, inputId, needsFormControl) => {
    if (needsFormControl) {
        inputElement.className = "form-control";
    }
    inputElement.setAttribute('id', inputId);
}

addInputElement = (inputData, mainDiv, nextButton) => {
    switch (inputData['type']) {
        case 'select':
            id = inputData['id'];
            options = inputData['options'];
            inputElement = document.createElement("select");
            options.forEach(optionString => {
                option = document.createElement("option");
                option.text = optionString;
                inputElement.add(option);
            });
            break;
        case 'text':
            inputElement = document.createElement("input");
            inputElement.type = "text";
            break;
        case 'textarea':
            inputElement = document.createElement("textarea");
            break;
        case 'selectcorrectlatex':
            inputElement = document.createElement("div");
            inputData['options'].forEach(optionData => {
                [optionIndex, optionString] = optionData;
                optionTex = document.createElement("button");
                optionTex.className = "btn btn-outline-info";
                optionTex.addEventListener("click", (event) => {
                    inputElement.setAttribute("value", optionData[0]);
                    nextButton.click();
                });
                optionTex.style.marginBottom = "2px";
                katex.render(optionString, optionTex);
                inputElement.appendChild(optionTex);
                inputElement.appendChild(document.createElement("br"));

            });
            break;
    }
    configureInput(inputElement, inputData['id'], inputData['needsFormControl']);
    label = document.createElement("p");
    label.innerText = inputData['label'];
    mainDiv.appendChild(label);
    mainDiv.appendChild(inputElement);
    mainDiv.appendChild(document.createElement("br"));
    return inputElement;
}



handleInputs = (response, packet) => {
    [card, cardBody] = getCardAndBody();
    if (response['reparsed_input']) {
        displayInput(response['reparsed_input']);
    }
    nextButton = getNextButton(async () => {
        outputKeys = {};
        inputElements.forEach(inputElement => {
            outputKeys[inputElement.id] = inputElement.getAttribute("value") || inputElement.value;
        });
        card.remove();
        await sendPacket({ 'updateType': 'inputs', 'inputs': outputKeys, 'sessionID': response['sessionID'], 'task': packet['task'], 'phase': response['phase'] });
    });

    inputElements = response['inputs'].map(input => addInputElement(input, cardBody, nextButton));

    cardBody.appendChild(nextButton);
    document.getElementById("requested-input-container").appendChild(card);
}

handleNewCodeSession = (response, packet) => {
    document.getElementById("terminal-container").style.display = "contents";
    document.getElementById("newlinebutton").addEventListener("click", async () => {
        await sendPacket({ 'updateType': 'inputs', 'inputs': { 'code': document.getElementById("codeInput").value }, 'sessionID': response['sessionID'], 'phase': response['phase'] });
    });
}

generateParagraph = (text, isResponse) => {
    resultElement = document.createElement("p");
    if (isResponse) {
        resultElement.style.color = "red";
        resultElement.innerHTML = ">" + katex.renderToString(text);
    }
    else {
        resultElement.innerHTML = ">" + text;
    }
    return resultElement;
}

handleNewCodeResult = (response, packet) => {
    document.getElementById("code-holder").append(generateParagraph(response['payload']['input'], false));
    document.getElementById("code-holder").append(generateParagraph(response['payload']['output'], true));
}

//This function is used to communicate with the "server", it takes a packet of data
//Sends it to the server and performs actions conditional on the response
sendPacket = async (packet) => {
    response = await eel.getInputs(packet)();
    if (response['action'] == 'resultReady') {
        if (response['reparsed_input']) {
            displayInput(response['reparsed_input'])
        }
        renderResult(response['resultTex'], response['sessionID']);
    }
    if (response['action'] == 'inputNeeded') {
        handleInputs(response, packet);
    }

    if (response['action'] == 'newCodeSession') {
        handleNewCodeSession(response, packet);
    }

    if (response['action'] == 'newCodeResult') {
        handleNewCodeResult(response, packet);
    }
    if (response['action'] == 'Error') {
        generateAlert(response['payload']['description']);
    }
}

taskClickHandler = async (task) => {
    hideAll();
    sendPacket({ 'task': task, 'latex': document.getElementById("latex").value, 'updateType': 'firstUpdate' });
}

