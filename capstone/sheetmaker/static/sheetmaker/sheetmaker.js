

const utils = (() => {
    let _iframe = null
    let _url = ''
    const _printSheet = () => {
        //
        console.log('printSheet function', _iframe)
        let printFrame = _iframe.get(0)

        try {
            printFrame.contentWindow.print()
        } catch(e) {
            let printWindow = window.open(_url, "Print Sheet Window", "width=900,height=800");
            printWindow.focus();
            printWindow.print();
        }
    }
    const _print = (url) => {
        _url = url
        console.log('print', url);

        if (_iframe) _iframe.remove()

        _iframe = $('<iframe>', {
            class: 'print',
            id: 'iframePrint',
            src: url,
            onload: "utils.printSheet()"
        })
        $("body").prepend(_iframe)
    }
    const _downloadSheet = () => {
        let downloadFrame = _iframe.get(0)
        try {
            downloadFrame.contentWindow.downloadPDF()
        } catch(e) {
            console.log('unable to download ...')
        }
    }
    const _download = (url) => {
        _url = url
        console.log('download', url);

        if (_iframe) _iframe.remove()

        _iframe = $('<iframe>', {
            class: 'print',
            id: 'iframeDownload',
            src: url,
            onload: "utils.downloadSheet()"
        })
        $("body").prepend(_iframe)
    }
    const _toNumber = (val) => {
        if (!val) return 0
        return parseInt(val)
    }
    const _validateDivisionForm = (frm) => {
        console.log(frm)
        // get all the answers..
        const answers = frm.elements['answer']
        let formValid = true
        // for(let idx=0; idx<answers.length;idx++) {
        //     const item = answers[idx]
        //     if (['0', 'Infinity'].indexOf(item.value) !== -1 ) {
        //         formValid = false
        //         break
        //     }
        // }
        answers.forEach((item) => {
            const expContainer = item.closest('.d_expression')
            if (['0', 'Infinity'].indexOf(item.value) !== -1 ) {
                formValid = false
                // expContainer.classList.add('bg-danger')
                $(expContainer).addClass('bg-danger')
            } else {
                // expContainer.classList.remove('bg-danger')
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
    return {
        print: _print,
        printSheet: _printSheet,
        download: _download,
        downloadSheet: _downloadSheet,
        toNumber: _toNumber,
        validateDivisionForm: _validateDivisionForm,
        alertMessage: _alertMessage
    }
})()


$().ready(() => {
    // browser's forward and back button is pressed
    if (window.performance.navigation.type === 2) {
        window.location.reload()
    }

    $('.problem-sheet form.form-editing').bind("keypress", function (e) {
        if (e.keyCode == 13) {
            e.preventDefault();
            return false;
        }
    });

    $('.grid.editing td.m_expression input').keyup((e) => {
        console.log(e)
        // get the current target's name
        let input1 = e.currentTarget
        let parentEl = input1.closest('.m_expression')
        let inputName1 = input1.attributes['name'].value
        let inputName2 = (inputName1 === 'first') ? 'second' : 'first'
        let input2 = parentEl.querySelector(`input[name=${inputName2}]`)
        let spanAnswer = parentEl.querySelector('span.answer')
        let hiddenAnswer = parentEl.querySelector('input[type="hidden"]')

        const input1Value = utils.toNumber(input1.value)
        if (input1Value < 0) {
            input1.value = 0
            return
        }
        const input2Value = utils.toNumber(input2.value)
        const answerValue = input1Value * input2Value

        spanAnswer.innerText = answerValue
        hiddenAnswer.value = answerValue
    })

    $('.grid.editing td.d_expression input').keyup((e) => {
        console.log(e)
        // get the current target's name
        let input1 = e.currentTarget
        let parentEl = input1.closest('.d_expression')
        let inputName1 = input1.attributes['name'].value
        let inputName2 = (inputName1 === 'first') ? 'second' : 'first'
        let input2 = parentEl.querySelector(`input[name=${inputName2}]`)
        let spanAnswer = parentEl.querySelector('span.answer')
        let hiddenAnswer = parentEl.querySelector('input[type="hidden"]')

        const input1Value = utils.toNumber(input1.value)
        if (input1Value < 0) {
            input1.value = 0
            return
        }
        const input2Value = utils.toNumber(input2.value)

        let answerValue = 0
        if (inputName2 === "first") {
            answerValue = Math.floor(input2Value / input1Value)
        }
        else {
            answerValue = Math.floor(input1Value / input2Value)
        }

        if (answerValue === 0 || answerValue === Infinity) {
            $(parentEl).addClass('bg-danger')
        } else {
            $(parentEl).removeClass('bg-danger')
        }

        spanAnswer.innerText = answerValue
        hiddenAnswer.value = answerValue
    })

    $('.grid.editing td.a_expression input').keyup((e) => {
        let currentInput = e.currentTarget
        let parentEl = currentInput.closest('.a_expression')
        let tdAnswer = parentEl.querySelector('td.answer')
        let hiddenAnswer = parentEl.querySelector('input[type="hidden"]')
        let numberInputs = parentEl.querySelectorAll('input[type="number"]')

        let total = 0
        numberInputs.forEach(item => {
            total += utils.toNumber(item.value)
        })
        hiddenAnswer.value = total
        tdAnswer.innerText = total

        if (total < 0) {
            $(parentEl).addClass('bg-danger')
        } else {
            $(parentEl).removeClass('bg-danger')
        }
    })

    $('#M_printSheetEl').click((e) => {
        console.log(e)
        let url = `/multiplication/${e.currentTarget.dataset.sheet_id}/print`
        utils.print(url);
    })

    $('#D_printSheetEl').click((e) => {
        console.log(e)
        let url = `/division/${e.currentTarget.dataset.sheet_id}/print`
        utils.print(url);
    })

    $('.btn-download-pdf').click((e) => {
        const {sheet_id, sheet_type} = e.currentTarget.dataset
        let url = `/${sheet_type}/${sheet_id}/print`
        utils.download(url);
    })

})


// Vanilla javascript
// window.addEventListener('popstate',  () => {
//     // var state = e.state;
//     // if (state !== null) {
//     //     //load content with ajax
//     // }
//     console.log('kyle popstate')
// });

