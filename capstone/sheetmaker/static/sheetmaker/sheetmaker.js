const utils = (() => {
    let _iframe = null
    let _url = ''
    const _sheetTypeMapOperator = {
        'Multiplication': 'x',
        'multiplication': 'x',
        'Division': '÷',
        'division': '÷',
        'Arithmetic': '',
        'arithmetic': ''
    }
    // Function to print the sheet
    const _printSheet = () => {
        let printFrame = _iframe.get(0)

        try {
            printFrame.contentWindow.print()
        } catch(e) {
            let printWindow = window.open(_url, "Print Sheet Window", "width=900,height=800");
            printWindow.focus();
            printWindow.print();
        }
    }

    // Function to make the printing process on the same window
    const _print = (url) => {
        _url = url

        if (_iframe) _iframe.remove()

        _iframe = $('<iframe>', {
            class: 'print',
            id: 'iframePrint',
            src: url,
            onload: "utils.printSheet()"
        })
        $("body").prepend(_iframe)
    }

    // Parsing to an integer to apply mathematical operations
    const _toNumber = (val) => {
        if (!val) return 0
        return parseInt(val)
    }

    // Checking if the edits to the division sheet are valid
    // Does not let the user submit if:
    //  The second number and first number can't be zero
    //  Marked the problems that produce a zero or an undefined number 
    const _validateDivisionForm = (frm) => {
        // Getting all the answers
        const answers = frm.elements['answer']
        let formValid = true
        answers.forEach((item) => {
            const expContainer = item.closest('.d_expression')
            if (['0', 'Infinity'].indexOf(item.value) !== -1 ) {
                formValid = false
                $(expContainer).addClass('bg-danger')
            } else {
                $(expContainer).removeClass('bg-danger')
            }
        })
        if (formValid) {
            _alertMessage('alertContainerForDivisionEl', '', '')    
        } else {
            _alertMessage('alertContainerForDivisionEl', 'Invalid entries!', 'danger')    
        } 
        return formValid        
    }

    // Checking if the edits to the arithmetic form are valid
    // Does not let the user submit if:
    //  The answer is negative
    const _validateArithmeticForm = (frm) => {
        let formValid = true

        let subtype = frm.getAttribute("data-subtype")
        let levels = 0
        if (subtype === "Mitori" || subtype === "Mitori Addition") {
            levels = 6
        }
        else if (subtype === "Challenged" || subtype === "Challenged Addition") {
            levels = 3
        }

        for (let idx=0; idx<levels; idx++) {
            const answers = frm.elements[`Level ${idx+1}_answer`]
            answers.forEach((item) => {
                const expContainer = item.closest('.a_expression')
                if (['-Infinity'].indexOf(item.value) !== -1) {
                    formValid = false
                    $(expContainer).addClass('bg-danger')
                } else {
                    $(expContainer).removeClass('bg-danger')
                }
            })
        } 
        if (formValid) {
            _alertMessage('alertContainerForArithmeticEl', '', '')
        } else {
            _alertMessage('alertContainerForArithmeticEl', 'Invalid entries!', 'danger')
        }
        return formValid
    }

    // Function to append an an alert message to the top of the edit page to signal if there are any invalid expressions
    const _alertMessage = (alertContainerId, message, type) => {
        const alertContainer = document.querySelector('#' + alertContainerId)
        if (!message) {
            alertContainer.innerHTML = ''
        } else {
            alertContainer.innerHTML = ''
            const wrapper = document.createElement('div')
            wrapper.innerHTML = [
                `<div class="alert alert-${type} alert-dismissible" role="alert">`,
                `   <div>${message}</div>`,
                '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
                '</div>'
            ].join('')
            alertContainer.append(wrapper)
        }
    }
    
    const _generateNewNumberSetByLevelHTML = (data, sheetType) => {
        const operator = _sheetTypeMapOperator[sheetType]
        const { numberSet, levelName } = data
        const html = numberSet.map(d => {
            const { number, numbers, first, second, answer } = d
            const isEditMode = window.location.pathname.endsWith('edit') ? true : false
            let tmpHtml = ''
            if (operator) {
                // Multiplication / Division
                tmpHtml = isEditMode 
                    ? `<tr>
                            <td>
                                ${ number }
                            </td>
                            <td class="m_expression">
                                <span>
                                    <input type="number" name="first" value="${first}" min="0" max="99999" />
                                    ${operator}
                                    <input type="number" name="second" value="${second}" min="0" max="99999" />
                                </span>
                                <span>=</span>
                                <span class="answer">${answer}</span>
                                <input type="hidden" name="answer" value="${answer}" />
                            </td>
                        </tr>`
                    : `<tr>
                        <td>
                            ${ number }
                        </td>
                        <td>
                            <span>
                                ${first} ${operator} ${second }
                            </span>
                            <span>=</span>
                            <span>${answer}</span>
                        </td>
                    </tr>
                    `
            } else {
                // Arithmetic
                tmpHtml = isEditMode 
                ? `<tr>
                        <td>${number}</td>
                        <td class="a_expression">
                            <table>
                                <tr>
                                    ${numbers.map(num => {
                                        return `
                                            <td class="px-2">
                                                <input type="number" name="${levelName}_numbers" value="${num}" min="-99999" max="99999" />
                                            </td>
                                        `    
                                    }).join('')}
                                    <td class="equal">=</td>
                                    <td class="answer">${answer}</td>
                                    <input type="hidden" name="${levelName}_answer" value="${answer}" />
                                </tr>
                            </table>
                        </td>
                    </tr>`
                : `<tr>
                        <td>${number}</td>
                        <td>
                            <table>
                                <tr>
                                    ${numbers.map(num => {
                                        return `
                                            <td class="px-2">${num}</td>
                                        `    
                                    }).join('')}
                                    <td class="equal">=</td>
                                    <td class="answer">${answer}</td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                `
            }
            return tmpHtml
        }).join('')
        return html
    }

    return {
        print: _print,
        printSheet: _printSheet,
        toNumber: _toNumber,
        validateDivisionForm: _validateDivisionForm,
        validateArithmeticForm: _validateArithmeticForm,
        alertMessage: _alertMessage,
        generateNewNumberSetByLevelHTML: _generateNewNumberSetByLevelHTML
    }
})()


$().ready(() => {
    // When the forward or backward button is pressed, the window reloads to show the new data
    if (window.performance.navigation.type === 2) {
        window.location.reload()
        return
    }

    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))

    // To get the user's timezone
    $('#localTimezoneName').val(Intl.DateTimeFormat().resolvedOptions().timeZone)

    // Preventing pressing the enter key from submitting the edited form
    // Pressing enter is used to update the number box when the user has entered a new number
    $('.problem-sheet form.form-editing').bind("keypress", function (e) {
        if (e.keyCode == 13) {
            e.preventDefault();
            return false;
        }
    });

    // When the user inputs a number in the multiplicaion edit screen
    // Prevents all numbers less than zero from being entered
    // Dynamically updates the answer to the expression
    $('.grid.editing td.m_expression input').keyup((e) => {
        let input1 = e.currentTarget // Can either be the first or second number
        let parentEl = input1.closest('.m_expression') // Container of the expression
        let inputName1 = input1.attributes['name'].value
        let inputName2 = (inputName1 === 'first') ? 'second' : 'first'
        let input2 = parentEl.querySelector(`input[name=${inputName2}]`)
        let spanAnswer = parentEl.querySelector('span.answer')
        let hiddenAnswer = parentEl.querySelector('input[type="hidden"]')

        // Getting integer values of the first and second operands
        const input1Value = utils.toNumber(input1.value)
        if (input1Value < 0) {
            input1.value = 0
            return
        }
        const input2Value = utils.toNumber(input2.value)
        const answerValue = input1Value * input2Value // Obtaining the answer

        // Changing the answer that is being shown and the answer that is being accessed when the form is submitted
        spanAnswer.innerText = answerValue
        hiddenAnswer.value = answerValue
    })

    // When the user inputs a number in the division edit screen
    // Prevents both first and second numbers from becoming 0
    // Dynamically updates the answer to the expression
    $('.grid.editing td.d_expression input').keyup((e) => {
        let input1 = e.currentTarget
        let parentEl = input1.closest('.d_expression')
        let inputName1 = input1.attributes['name'].value
        let inputName2 = (inputName1 === 'first') ? 'second' : 'first'
        let input2 = parentEl.querySelector(`input[name=${inputName2}]`)
        let spanAnswer = parentEl.querySelector('span.answer')
        let hiddenAnswer = parentEl.querySelector('input[type="hidden"]')

        // Not letting either number be equal to 0; changing it to 1
        const input1Value = utils.toNumber(input1.value)
        if (input1Value <= 0) {
            input1.value = 1
            return
        }

        const input2Value = utils.toNumber(input2.value)

        // Integer answers only; non integers are flagged by setting the answer to zero
        let answerValue = 0
        if (inputName2 === "first") {
            if ((input2Value % input1Value) !== 0) {
                answerValue = 0
            }
            else {
                answerValue = (input2Value / input1Value)
            }
        }
        else {
            if ((input1Value % input2Value) !== 0) {
                answerValue = 0
            }
            else {
                answerValue = Math.floor(input1Value / input2Value)
            }
        }

        // Adding styling as a visual flag that the problem is invalid
        if (answerValue === 0) {
            $(parentEl).addClass('bg-danger')
        } else {
            $(parentEl).removeClass('bg-danger')

            // Form validation (calling the validation form function)
            const frm = input1.closest('form')
            utils.validateDivisionForm(frm)
        }

        // Changing the displayed and hidden answer
        spanAnswer.innerText = answerValue
        hiddenAnswer.value = answerValue
    })

    // When the user inputs a number in the arithmetic edit screen
    // Prevents the answer from being less than 0
    // Dynamically updates the answer to the expression
    $('.grid.editing td.a_expression input').keyup((e) => {
        let currentInput = e.currentTarget
        let parentEl = currentInput.closest('.a_expression')
        let tdAnswer = parentEl.querySelector('td.answer')
        let hiddenAnswer = parentEl.querySelector('input[type="hidden"]')
        let numberInputs = parentEl.querySelectorAll('input[type="number"]') // Because there is not just a first or second number

        // Gettting the total number
        let total = 0
        numberInputs.forEach(item => {
            total += utils.toNumber(item.value)
        })

        // Answer cannot be negative; answer is changed to negative infinity to flag it if it is
        if (total < 0) {
            total = -Infinity
        }

        // Adding styling as a visual flag that the problem is invalid
        if (total < 0) {
            $(parentEl).addClass('bg-danger')
        } else {
            $(parentEl).removeClass('bg-danger')

            // Validating form
            const frm = currentInput.closest('form')
            utils.validateArithmeticForm(frm)
        }

        // Changing the displayed and hidden anwer
        hiddenAnswer.value = total
        tdAnswer.innerText = total
    })

    // On-click event listener for the print buttons for the sheets
    $('#printSheetEl').click((e) => {
        const {sheetType, sheet_id} = e.currentTarget.dataset
        let url  = `/${sheetType}/${sheet_id}/print`
        utils.print(url)
    })

    $('button.print-action').click((e) => {
        console.log('e.currentTarget.dataset', e.currentTarget.dataset)
        const {sheetType, sheetId} = e.currentTarget.dataset
        let url  = `/${sheetType}/${sheetId}/print`
        utils.print(url)
    })

    // For registering and logging in to force the users to input all fields of the form
    let forms = document.querySelectorAll('form.needs-validation')
    // Loop over them and prevent submission
    Array.prototype.slice.call(forms)
        .forEach(function (form) {
            form.addEventListener('submit', function (event) {
                if (!form.checkValidity()) {
                    event.preventDefault()
                    event.stopPropagation()
                }
                form.classList.add('was-validated')
            }, false)
        })

    // for listening to opening of the modal dialog
    const deleteConfirmModal = document.getElementById('deleteConfirmModal')
    if (deleteConfirmModal) {
        deleteConfirmModal.addEventListener('show.bs.modal', event => {
            // Button that triggered the modal
            const button = event.relatedTarget
            // Extract info from data-bs-* attributes
            const apiName = button.getAttribute('data-bs-api-name')
            const sheetId = button.getAttribute('data-bs-sheet-id')
    
            const confirmButton = deleteConfirmModal.querySelector('.btn.confirm')
            const form = document.querySelector(`#${apiName}Form_${sheetId}`)
            $(confirmButton).click(() => {
                form && form.submit()
            })
            // // If necessary, you could initiate an AJAX request here
            // // and then do the updating in a callback.
            // //
            // // Update the modal's content.
            // const modalTitle = deleteConfirmModal.querySelector('.modal-title')
            // const modalBodyInput = deleteConfirmModal.querySelector('.modal-body input')
            // modalTitle.textContent = `New message to ${recipient}`
            // modalBodyInput.value = recipient
        })
    }

    $('button.action-refresh').click((e) => {
        e.preventDefault()
        e.stopPropagation()
        if (!e.currentTarget) return

        let tokenEl = document.querySelector('input[name="csrfmiddlewaretoken"]')
        if (tokenEl && e.currentTarget.dataset) {
            const parentTable = e.currentTarget.closest('table')
            const tableBody = parentTable.querySelector('tbody')
            const { sheetId, sheetType, levelId } = e.currentTarget.dataset
            const autosave = window.location.pathname.endsWith('view') ? true : false
            const url = '/generateNewSet'
            fetch(url, {
                body: JSON.stringify({ sheetId: utils.toNumber(sheetId), level: utils.toNumber(levelId), autosave: autosave}),
                method: 'POST',
                headers: { "X-CSRFToken": tokenEl.value}
            })
            .then((response) => response.json())
            .then((data) => { 
                console.log(data)
                if (data?.numberSet) {
                    const newNumberSetHTML = utils.generateNewNumberSetByLevelHTML(data, sheetType)
                    $(tableBody).html(newNumberSetHTML)
                }
            })
        }
    })
})